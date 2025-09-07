# script.py

# Maat-Reflection — stille Selbstreflexion & Self-Repair (H, B, S, V, R)
import os, io, re, yaml, threading
from datetime import datetime
import gradio as gr
from user_data.extensions.maat_reflection.i18n import I18N, t, rx

# ───────────────────────────────────────────────────────────────
# Pfade & Defaults
# ───────────────────────────────────────────────────────────────
EXT_DIR = os.path.join("user_data", "extensions", "maat_reflection")
STATE_FILE = os.path.join(EXT_DIR, "reflection.yaml")
SCHEMA_VERSION = 5  # bump
LAST_USER_INPUT = ""

DEFAULTS = {
    "version": SCHEMA_VERSION,
    "apply_to": "context",   # off | context | prefix | both
    "enabled": True,            # Hauptschalter
    "debug": False,
    "show_scores": False,       # wenn True: am Ende eine Score-Zeile erlauben
    "min_score": 0,             # 0–100; unterhalb: still verbessern
    "max_context_chars": 4000,  # Schutzkappe für Injektions-Text
    "legend": True,             # Reflexions-Legende anzeigen?
    "max_repairs": 2,           # maximale stille Verbesserungsdurchläufe
    "show_stats": True,         # Tab mit Stats
    "inject_agent_template": True,  # Agent-Template vor den Reflection-Guide injizieren?
    #language
    "lang": "en",  # Sprache für Reflection-Block: de | en | es
    "ui_mode": "simple",            # "simple" | "expert"
    "limit_cap": True, 
    # Gate + Force
    "min_input_chars": 6,                       # unter dieser Länge → kein Thinking
    "force_on_regex": r"[?]|(^/think\b)",       # Regex erzwingt Thinking, leer = aus

    # 🔹 Mini-Heuristiken
    "h_question": True,          # Fragezeichen/Interrogativwörter
    "h_multisent": True,         # mehrere Sätze
    "h_min_sentences": 2,        # mind. Sätze, um als "mehrsatz" zu zählen
    "h_long_text": False,        # Mindestwortanzahl
    "h_min_words": 12,           # min. Wörter
    "h_conjunctions": True,      # Konnektoren (und, aber, weil, etc.)
    "h_numbers_math": True,      # Zahlen/Mathe-Symbole
    "h_code_or_url": True,       # Backticks/URLs
    "h_uncertainty": True,       # unsichere/bitte/hilfs-Phrasen
    "min_triggers": 2,           # Wieviele Heuristik-Treffer nötig, um Thinking zu aktivieren

    # Stats
    "stats": {
        "sessions_started": 0,
        "reflections_injected": 0,
        "repairs_requested": 0
    }
}

state = dict(DEFAULTS)
_IO_LOCK = threading.Lock()



def _ensure_dir():
    os.makedirs(EXT_DIR, exist_ok=True)

def _atomic_write_yaml(path, data):
    tmp = path + ".tmp"
    with _IO_LOCK:
        with io.open(tmp, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
        os.replace(tmp, path)

def _load_yaml(path):
    if not os.path.exists(path): return {}
    with _IO_LOCK:
        with io.open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

def _save_state():
    _ensure_dir(); _atomic_write_yaml(STATE_FILE, state)

def _load_state():
    _ensure_dir()
    raw = _load_yaml(STATE_FILE)
    state.clear(); state.update(DEFAULTS)
    if isinstance(raw, dict):
        for k, v in raw.items():
            if k == "stats" and isinstance(v, dict):
                state["stats"].update(v)
            else:
                state[k] = v

    if "max_context_chars" not in state:
        state["max_context_chars"] = 10000   # Safety-Default


def _cap(text: str, n: int) -> str:
    if n <= 0 or len(text) <= n: return text
    return text[:max(0, n-60)].rstrip() + "\n… [gekürzt]"

def _debug(*a):
    if state.get("debug"): print("[maat-reflection]", *a, flush=True)

# ───────────────────────────────────────────────────────────────
# Reflection-Rubric (unsichtbar in den Kontext injiziert)
# ───────────────────────────────────────────────────────────────
_LEGEND = """LEGENDEN-KURZFORM:
- H (Harmonie): Stimmigkeit, Kohärenz, roter Faden.
- B (Balance): Fakten-Genauigkeit, Logik, Klarheit.
- S (Schöpfungskraft): Neuheit, Nützlichkeit, Originalität.
- V (Verbundenheit): Kontextbezug, Empathie, Nutzerintention.
- R (Respekt): Ethik, Grenzen, Transparenz, Sicherheit.
"""
#------------------
#   Sprache
#------------------
# --- i18n wrappers (use global state['lang']) ---

def _build_agent_template(min_score: int, max_repairs: int) -> str:
    return f"""
name: Maat-KI Agent
description: >
  Experimental AI assistant aligned with the Maat-Principles (Harmony, Balance, Creativity, Connection, Respect).
  Uses silent self-reflection and self-repair before every answer.
  Goal: Always reach Maat-Value ≥ {min_score}, with max {max_repairs} silent improvements.

persona:
  style: "Warm, clear, respectful, human-like."
  tone: "Reflective, concise, with occasional empathy and imagery."
  language: "Adapt automatically to user language (de/en/es/fr/pt/it/cz)."

core_principles:
  H: Harmony 🌿 - Coherence, logical flow, clarity
  B: Balance ⚖️ - Depth vs. accessibility
  S: Creativity 🎨 - Novel, useful, original
  V: Connection 🌐 - Context-awareness, empathy, user intent
  R: Respect 🕊️ - Ethics, dignity, transparency

instruct:
  - "Before answering, perform a silent self-reflection."
  - "Rate H, B, S, V, R (0–100)."
  - "If any score < {min_score}, silently repair draft. Repeat up to {max_repairs} times."
  - "Output ONLY the polished final answer. No inner thoughts, no tags."
  - "Be concise, clear, and truthful. State uncertainty transparently."
  - "Prefer useful, creative, and ethical responses."

formulas:
  - "Maat-Value = (H*B*S*V*R) / 5"
  - "PLP = ((H*B*S*V*R)*K) / (Barriers + ΔE)"
  - "World-Maat = (H*B*S*V*R) / ΔE"
  - "ToE_Maat = ∫ ((H+B+S+V+R) * Z * string_tension) / (ΔE+ΔQ+M-dimensions) dt"
"""

def _t(key: str) -> str:
    return t(state.get("lang", "de"), key)

def _rx(key: str, fallback: str) -> str:
    return rx(state.get("lang", "de"), key, fallback)

def _apply_display_list():
    return [
        _t("apply.off"),
        _t("apply.context"),
        _t("apply.prefix"),
        _t("apply.both"),
    ]

def _apply_code_to_display(code: str) -> str:
    return {
        "off": _t("apply.off"),
        "context": _t("apply.context"),
        "prefix": _t("apply.prefix"),
        "both": _t("apply.both"),
    }.get(code or "context", _t("apply.context"))

def _apply_display_to_code(display: str) -> str:
    m = {
        _t("apply.off"): "off",
        _t("apply.context"): "context",
        _t("apply.prefix"): "prefix",
        _t("apply.both"): "both",
    }
    return m.get(display, "context")


def _build_reflection_block(min_score: int, show_scores: bool, legend_on: bool, max_repairs: int) -> str:
    # Scores-Hinweis je nach Flag
    scores_hint = _t("guide.scores_on") if show_scores else _t("guide.scores_off")

    blocks = []

    # Optional das Agent-Template vorn anstellen
    if state.get("inject_agent_template", True):
        blocks.append(_build_agent_template(min_score, max_repairs))

    # I18N-Template holen und formatieren
    tmpl = _t("guide.template")
    try:
        guide = tmpl.format(
            min_score=min_score,
            max_repairs=max_repairs,
            scores_hint=scores_hint,
        )
    except Exception:
        # Falls irgendwo {…} im Text nicht ersetzt werden kann, nicht crashen
        guide = tmpl

    # Optional Legende anhängen
    if state.get("legend", legend_on):
        guide = guide + "\n" + _t("legend.short")

    blocks.append(guide.strip())

    # Zusammenfügen & Kappen
    full = "\n\n".join(blocks).strip()

    if state.get("limit_cap", True):
        return _cap(full, state.get("max_context_chars", DEFAULTS["max_context_chars"]))
    else:
        return full


def _apply_display_list():
    return [
        _t("apply.off"),
        _t("apply.context"),
        _t("apply.prefix"),
        _t("apply.both"),
    ]

def _apply_display_to_code(display: str) -> str:
    m = {
        _t("apply.off"): "off",
        _t("apply.context"): "context",
        _t("apply.prefix"): "prefix",
        _t("apply.both"): "both",
    }
    return m.get(display, "context")

def _apply_code_to_display(code: str) -> str:
    rev = {
        "off": _t("apply.off"),
        "context": _t("apply.context"),
        "prefix": _t("apply.prefix"),
        "both": _t("apply.both"),
    }
    return rev.get((code or "context"), _t("apply.context"))

#----------------------
    #SPRACHE ENDE#
#----------------------
# ───────────────────────────────────────────────────────────────
# Heuristik-Logik
# ───────────────────────────────────────────────────────────────
_RX_WORD = re.compile(r"\w+", re.UNICODE)
_RX_SENT_SPLIT = re.compile(r"[.!?]+")
_INTERRO_WORDS = r"\b(wer|wie|was|wo|warum|wieso|weshalb|welche?r?|wann|wieviel|wieviele)\b"
_CONJUNCTIONS = r"\b(und|oder|aber|denn|sondern|doch|jedoch|weil|obwohl|während|falls|damit|dass|deshalb|trotzdem)\b"
_UNCERTAINTY = r"\b(vielleicht|unsicher|schätz|ungewiss|bitte|hilfe|kannst du|könntest du|wäre es möglich)\b"

def _count_sentences(text: str) -> int:
    text = (text or "").strip()
    if not text: return 0
    parts = [p for p in _RX_SENT_SPLIT.split(text) if _RX_WORD.search(p)]
    return max(1 if text else 0, len(parts))

def _word_count(text: str) -> int:
    return len(_RX_WORD.findall(text or ""))


# ───────────────────────────────────────────────────────────────
# WebUI Hooks
# ───────────────────────────────────────────────────────────────
# ── Mini-Gate & Force ─────────────────────────────────────────


# Cache für kompilierte Regex pro Sprache
_LANG_RX_CACHE = {}

def _get_lang() -> str:
    return (state.get("lang") or "de").lower()

def _get_lang_patterns():
    """
    Liefert ein Dict mit kompilierter Regex je nach state['lang'].
    Keys: INTERRO, CONJ, UNC
    """
    lang = _get_lang()
    if lang in _LANG_RX_CACHE:
        return _LANG_RX_CACHE[lang]

    interro = re.compile(I18N.get(lang, I18N["de"])["rx.interro"], re.IGNORECASE)
    conj    = re.compile(I18N.get(lang, I18N["de"])["rx.conj"], re.IGNORECASE)
    unc     = re.compile(I18N.get(lang, I18N["de"])["rx.uncertainty"], re.IGNORECASE)

    _LANG_RX_CACHE[lang] = {"INTERRO": interro, "CONJ": conj, "UNC": unc}
    return _LANG_RX_CACHE[lang]

def _should_reflect(user_text: str) -> bool:
    if not state.get("enabled", True):
        return False

    text = (user_text or "").strip()

    # 1) Force-Regex gewinnt immer
    force_rx = state.get("force_on_regex", "")
    try:
        if force_rx and re.search(force_rx, text, flags=re.IGNORECASE):
            _debug(f"force_on_regex matched: {force_rx!r}")
            return True
    except re.error as e:
        _debug(f"invalid force_on_regex: {e}")

    # 2) Gate: Minimallänge (Zeichen)
    try:
        min_len = int(state.get("min_input_chars", 0) or 0)
    except Exception:
        min_len = 0
    if min_len and len(text) < min_len:
        _debug(f"skip reflection (len<{min_len})")
        return False

    # 3) Heuristiken pro Sprache – Regexe aus I18N laden (mit Fallback)
    try:
        rx_interro = re.compile(_rx("rx.interro",
            r"\b(wer|wie|was|wo|warum|wieso|weshalb|welche?r?|wann|wieviel|wieviele)\b"), re.IGNORECASE)
        rx_conj = re.compile(_rx("rx.conj",
            r"\b(und|oder|aber|denn|sondern|doch|jedoch|weil|obwohl|während|falls|damit|dass|deshalb|trotzdem)\b"), re.IGNORECASE)
        rx_unc = re.compile(_rx("rx.uncertainty",
            r"\b(vielleicht|unsicher|schätz|ungewiss|bitte|hilfe|kannst du|könntest du|wäre es möglich)\b"), re.IGNORECASE)
    except Exception as e:
        _debug(f"fallback to default regex due to: {e}")
        rx_interro = re.compile(r"\b(wer|wie|was|wo|warum|wieso|weshalb|welche?r?|wann|wieviel|wieviele)\b", re.IGNORECASE)
        rx_conj    = re.compile(r"\b(und|oder|aber|denn|sondern|doch|jedoch|weil|obwohl|während|falls|damit|dass|deshalb|trotzdem)\b", re.IGNORECASE)
        rx_unc     = re.compile(r"\b(vielleicht|unsicher|schätz|ungewiss|bitte|hilfe|kannst du|könntest du|wäre es möglich)\b", re.IGNORECASE)

    triggers = 0

    # Frage?
    if state.get("h_question", True):
        if "?" in text or rx_interro.search(text):
            triggers += 1

    # mehrere Sätze?
    if state.get("h_multisent", True):
        min_s = max(1, int(state.get("h_min_sentences", 2)))
        parts = [p for p in _RX_SENT_SPLIT.split(text) if _RX_WORD.search(p)]
        if max(1 if text else 0, len(parts)) >= min_s:
            triggers += 1

    # Mindestwortanzahl?
    if state.get("h_long_text", False):
        min_w = max(1, int(state.get("h_min_words", 12)))
        if len(_RX_WORD.findall(text)) >= min_w:
            triggers += 1

    # Konnektoren?
    if state.get("h_conjunctions", True):
        if rx_conj.search(text):
            triggers += 1

    # Zahlen/Mathe?
    if state.get("h_numbers_math", True):
        if re.search(r"\d", text) or re.search(r"[+\-*/=<>^]", text):
            triggers += 1

    # Code oder URL?
    if state.get("h_code_or_url", True):
        if "`" in text or "http://" in text or "https://" in text:
            triggers += 1

    # Unsicherheit/Bitte?
    if state.get("h_uncertainty", True):
        if rx_unc.search(text):
            triggers += 1

    # 4) Schwelle auswerten (0 erlaubt)
    try:
        need = int(state.get("min_triggers", 1))
    except Exception:
        need = 1

    if need <= 0:
        _debug("min_triggers=0 → reflect (after gate)")
        return True

    ok = triggers >= need
    _debug(f"heuristic triggers={triggers} need={need} → {ok}")
    return ok



# ── Hooks ─────────────────────────────────────────────────────
def input_modifier(string):
    """Nichts Sichtbares anhängen – nur den letzten User-Input merken."""
    global LAST_USER_INPUT
    LAST_USER_INPUT = string or ""
    return string

def custom_generate_chat_prompt(user_input, state_dict, **kwargs):
    """
    Minimal & robust:
    - prüft Gate/Force
    - injiziert Block unsichtbar in state['context'] (prepend)
    - gibt IMMER None zurück → andere Extensions dürfen weiter arbeiten
    """
    if not isinstance(state_dict, dict):
        _debug("state not dict; skip inject")
        return None

    if not _should_reflect(user_input):
        return None

    block = _build_reflection_block(
        state.get("min_score", 0),
        state.get("show_scores", False),
        state.get("legend", True),
        state.get("max_repairs", 2),
    )

    before = len(state_dict.get("context", "") or "")
    state_dict["context"] = (block + "\n\n" + (state_dict.get("context", "") or "")).strip()
    after = len(state_dict["context"])
    _debug(f"[inject-context] +{len(block)} chars (len {before}→{after})")

    # kleine Statistik
    try:
        state["stats"]["reflections_injected"] += 1
        if state.get("min_score", 0) > 0 and state.get("max_repairs", 0) > 0:
            state["stats"]["repairs_requested"] += 1
        _save_state()
    except Exception as e:
        _debug("stats update failed:", e)

    return None  # ← wichtig für Extension-Ketten

def bot_prefix_modifier(prefix: str):
    """
    Fallback, falls später geladene Extensions den Kontext überschreiben.
    Injiziert denselben Block in den Bot-Prefix, ABER nur wenn Gate/Force passt.
    """
    if not _should_reflect(LAST_USER_INPUT):
        return prefix

    block = _build_reflection_block(
        state.get("min_score", 0),
        state.get("show_scores", False),
        state.get("legend", True),
        state.get("max_repairs", 2),
    )
    _debug(f"[inject-prefix] +{len(block)} chars")
    return (block + "\n\n" + (prefix or "")).strip()

# ───────────────────────────────────────────────────────────────
# UI
# ───────────────────────────────────────────────────────────────
def ui():
    _load_state()
    if state.get("ui_mode", "simple") == "simple":
        state["inject_agent_template"] = True  # Simple => immer an
        _save_state()
    with gr.Tabs():
        with gr.Tab(_t("ui.tab")):
            # ───────────────── Kopfzeile ─────────────────
            with gr.Row():
                dd_lang = gr.Dropdown(
                    choices=["de", "en", "es", "fr", "pt", "it", "cz"],
                    value=state.get("lang", "de"),
                    label=_t("ui.lang"),
                )
                dd_mode = gr.Dropdown(
                    choices=[_t("ui.mode_simple"), _t("ui.mode_expert")],
                    value=_t("ui.mode_expert") if state.get("ui_mode", "simple") == "expert" else _t("ui.mode_simple"),
                    label=_t("ui.mode"),
                )
                cb_en  = gr.Checkbox(value=state.get("enabled", True),  label=_t("ui.enabled"))
                cb_dbg = gr.Checkbox(value=state.get("debug", False),   label=_t("ui.debug"))

            # ─────────────── Simple / Expert Gruppen ───────────────
            grp_simple = gr.Group(visible=(state.get("ui_mode", "simple") == "simple"))
            with grp_simple:
                with gr.Row():
                    cb_show = gr.Checkbox(value=state.get("show_scores", False), label=_t("ui.show_scores"))
                    cb_leg  = gr.Checkbox(value=state.get("legend", True),       label=_t("ui.legend"))
                    dd_apply = gr.Dropdown(
                        choices=["off", "context", "prefix", "both"],
                        value=state.get("apply_to", "context"),
                        label=_t("ui.apply_to"),
                    )
                cb_agent = gr.Checkbox(  # im Simple-Mode gesperrt (immer an)
                    value=True,
                    label=_t("ui.inject_agent_template"),
                    interactive=False
                )
                with gr.Row():
                    nb_min = gr.Number(value=state.get("min_score", 0), precision=0, label=_t("ui.min_score"))
                    nb_rep = gr.Number(value=state.get("max_repairs", 2), precision=0, label=_t("ui.max_repairs"))

            grp_expert = gr.Group(visible=(state.get("ui_mode", "simple") == "expert"))
            with grp_expert:
                with gr.Row():
                    cb_show_e = gr.Checkbox(value=state.get("show_scores", False), label=_t("ui.show_scores"))
                    cb_leg_e  = gr.Checkbox(value=state.get("legend", True),       label=_t("ui.legend"))
                    dd_apply_e = gr.Dropdown(
                        choices=["off", "context", "prefix", "both"],
                        value=state.get("apply_to", "context"),
                        label=_t("ui.apply_to"),
                    )
                    cb_agent_e = gr.Checkbox(  # im Expert-Mode frei schaltbar
                        value=state.get("inject_agent_template", True),
                        label=_t("ui.inject_agent_template"),
                        interactive=False
                    )
                with gr.Row():
                    nb_min_e = gr.Number(value=state.get("min_score", 0), precision=0, label=_t("ui.min_score"))
                    nb_rep_e = gr.Number(value=state.get("max_repairs", 2), precision=0, label=_t("ui.max_repairs"))
                with gr.Row():
                    cb_cap = gr.Checkbox(value=state.get("limit_cap", True), label=_t("ui.limit_cap"))
                    sl_cap = gr.Slider(
                        200, 4000, step=50,
                        value=state.get("max_context_chars", 1200),
                        label=_t("ui.max_context"),
                        interactive=state.get("limit_cap", True)
                    )

            # ───────────────── Gate & Force ─────────────────
            with gr.Row():
                nb_gate  = gr.Number(value=state.get("min_input_chars", 6), precision=0, label=_t("ui.gate_min_chars"))
                tb_force = gr.Textbox(value=state.get("force_on_regex", r"[?]|(^/think\b)"), label=_t("ui.force_regex"))
                nb_mintr = gr.Number(value=state.get("min_triggers", 2), precision=0, label=_t("ui.min_triggers"))
                btn_preset_q = gr.Button(_t("ui.preset_questions"))
                btn_preset_always = gr.Button(_t("ui.preset_always"))
                btn_preset_min  = gr.Button("⚡ Preset: Minimal (OSS)")
                btn_preset_light = gr.Button("✨ Preset: Light")
                btn_preset_strict = gr.Button("🔥 Preset: Strict")

            # ─────────────── Heuristiken (Widgets MÜSSEN vor Wiring existieren) ───────────────
            with gr.Accordion(_t("ui.heuristics"), open=False):
                with gr.Row():
                    cb_q   = gr.Checkbox(value=state.get("h_question", True), label=_t("ui.h_question"))
                    cb_ms  = gr.Checkbox(value=state.get("h_multisent", True), label=_t("ui.h_multisent"))
                    nb_ms  = gr.Number(value=state.get("h_min_sentences", 2), precision=0, label=_t("ui.h_min_sentences"))
                with gr.Row():
                    cb_len = gr.Checkbox(value=state.get("h_long_text", False), label=_t("ui.h_long_text"))
                    nb_w   = gr.Number(value=state.get("h_min_words", 12), precision=0, label=_t("ui.h_min_words"))
                with gr.Row():
                    cb_conj = gr.Checkbox(value=state.get("h_conjunctions", True), label=_t("ui.h_conjunctions"))
                    cb_num  = gr.Checkbox(value=state.get("h_numbers_math", True), label=_t("ui.h_numbers_math"))
                    cb_code = gr.Checkbox(value=state.get("h_code_or_url", True), label=_t("ui.h_code_or_url"))
                    cb_unc  = gr.Checkbox(value=state.get("h_uncertainty", True), label=_t("ui.h_uncertainty"))



            # ───────────────── Vorschau ─────────────────
            prev = gr.Code(
                value=_build_reflection_block(
                    state.get("min_score", 0),
                    state.get("show_scores", False),
                    state.get("legend", True),
                    state.get("max_repairs", 2),
                ),
                language="markdown",
                label=_t("ui.preview"),
                lines=20,
                interactive=False
            )

            # ─────────────── Helper ───────────────
            def _toi_int(v, lo=None, hi=None, default=0):
                try:
                    x = int(v)
                except Exception:
                    x = default
                if lo is not None:
                    x = max(lo, x)
                if hi is not None:
                    x = min(hi, x)
                return x

            # Haupt-Update (deine _upd Signatur bleibt gleich!)
            def _upd(en, dbg, show, leg, minsc, repairs, cap, gate, force_rx, mintr,
                     hq, hms, hms_min, hlen, hlen_min, hconj, hnum, hcode, hunc, apply_to):
                state["enabled"]            = bool(en)
                state["debug"]              = bool(dbg)
                state["show_scores"]        = bool(show)
                state["legend"]             = bool(leg)
                state["min_score"]          = _toi_int(minsc, 0, 100, state.get("min_score", 0))
                state["max_repairs"]        = _toi_int(repairs, 0, 5,   state.get("max_repairs", 2))
                state["max_context_chars"]  = _toi_int(cap,   200, 4000, state.get("max_context_chars", 1200))
                state["min_input_chars"]    = _toi_int(gate,  0,   200,  state.get("min_input_chars", 6))
                state["force_on_regex"]     = str(force_rx or "")
                state["min_triggers"]       = _toi_int(mintr, 0,   10,   state.get("min_triggers", 2))
                state["h_question"]         = bool(hq)
                state["h_multisent"]        = bool(hms)
                state["h_min_sentences"]    = _toi_int(hms_min, 1, 10,   state.get("h_min_sentences", 2))
                state["h_long_text"]        = bool(hlen)
                state["h_min_words"]        = _toi_int(hlen_min, 1, 200, state.get("h_min_words", 12))
                state["h_conjunctions"]     = bool(hconj)
                state["h_numbers_math"]     = bool(hnum)
                state["h_code_or_url"]      = bool(hcode)
                state["h_uncertainty"]      = bool(hunc)
                state["apply_to"]           = str(apply_to or "context").lower()
                _save_state()
                return gr.update(value=_build_reflection_block(
                    state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                ))

            # Preset
            def _apply_preset_questions():
                state["apply_to"]        = "context"
                state["min_input_chars"] = 6
                state["force_on_regex"]  = r"[?]"
                state["min_triggers"]    = 1
                state["h_question"]      = True
                state["h_multisent"]     = False
                state["h_min_sentences"] = 2
                state["h_long_text"]     = False
                state["h_min_words"]     = 12
                state["h_conjunctions"]  = False
                state["h_numbers_math"]  = False
                state["h_code_or_url"]   = False
                state["h_uncertainty"]   = False
                _save_state()
                return (
                    gr.update(value=_build_reflection_block(
                        state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                    gr.update(value=state["min_input_chars"]),
                    gr.update(value=state["force_on_regex"]),
                    gr.update(value=state["min_triggers"]),
                    gr.update(value=state["h_question"]),
                    gr.update(value=state["h_multisent"]),
                    gr.update(value=state["h_min_sentences"]),
                    gr.update(value=state["h_long_text"]),
                    gr.update(value=state["h_min_words"]),
                    gr.update(value=state["h_conjunctions"]),
                    gr.update(value=state["h_numbers_math"]),
                    gr.update(value=state["h_code_or_url"]),
                    gr.update(value=state["h_uncertainty"]),
                    gr.update(value=state["apply_to"]),
                )

            # ───────────── Presets ─────────────
            def _apply_preset_always():
                # Immer denken – Gates/Heuristik aus
                state["enabled"]         = True
                state["apply_to"]        = "context"
                state["min_input_chars"] = 0
                state["force_on_regex"]  = r""
                state["min_triggers"]    = 0

                # Heuristiken dürfen an sein, wirken bei min_triggers=0 nicht
                state["h_question"]      = False
                state["h_multisent"]     = False
                state["h_min_sentences"] = 0
                state["h_long_text"]     = False
                state["h_min_words"]     = 0
                state["h_conjunctions"]  = False
                state["h_numbers_math"]  = False
                state["h_code_or_url"]   = False
                state["h_uncertainty"]   = False

                # Snappier
               # state["min_score"]   = max(0, int(state.get("min_score", 30)))
               # state["max_repairs"] = 1

                _save_state()
                return (
                    gr.update(value=_build_reflection_block(state["min_score"], state["show_scores"], state["legend"], state["max_repairs"])),
                    gr.update(value=state["min_input_chars"]),  # nb_gate
                    gr.update(value=state["force_on_regex"]),   # tb_force
                    gr.update(value=state["min_triggers"]),     # nb_mintr
                    gr.update(value=state["h_question"]),       # cb_q
                    gr.update(value=state["h_multisent"]),      # cb_ms
                    gr.update(value=state["h_min_sentences"]),  # nb_ms
                    gr.update(value=state["h_long_text"]),      # cb_len
                    gr.update(value=state["h_min_words"]),      # nb_w
                    gr.update(value=state["h_conjunctions"]),   # cb_conj
                    gr.update(value=state["h_numbers_math"]),   # cb_num
                    gr.update(value=state["h_code_or_url"]),    # cb_code
                    gr.update(value=state["h_uncertainty"]),    # cb_unc
                    gr.update(value=state["apply_to"]),         # dd_apply
                )

            def _apply_preset_minimal():
                # OSS Minimal – keine Reflexion, nur Template + direkte Antwort
                state["apply_to"]        = "context"
                state["min_input_chars"] = 0
                state["force_on_regex"]  = r""
                state["min_triggers"]    = 1

                state["h_question"]      = True
                state["h_multisent"]     = True
                state["h_min_sentences"] = 2
                state["h_long_text"]     = False
                state["h_min_words"]     = 12
                state["h_conjunctions"]  = True
                state["h_numbers_math"]  = True
                state["h_code_or_url"]   = True
                state["h_uncertainty"]   = True

                state["min_score"]   = 1
                state["max_repairs"] = 0

                _save_state()
                return (
                    gr.update(value=_build_reflection_block(state["min_score"], state["show_scores"], state["legend"], state["max_repairs"])),
                    gr.update(value=state["min_input_chars"]),
                    gr.update(value=state["force_on_regex"]),
                    gr.update(value=state["min_triggers"]),
                    gr.update(value=state["h_question"]),
                    gr.update(value=state["h_multisent"]),
                    gr.update(value=state["h_min_sentences"]),
                    gr.update(value=state["h_long_text"]),
                    gr.update(value=state["h_min_words"]),
                    gr.update(value=state["h_conjunctions"]),
                    gr.update(value=state["h_numbers_math"]),
                    gr.update(value=state["h_code_or_url"]),
                    gr.update(value=state["h_uncertainty"]),
                    gr.update(value=state["apply_to"]),
                )

            def _apply_preset_light():
                # Light – sanfte Reflexion
                state["apply_to"]        = "context"
                state["min_input_chars"] = 0
                state["force_on_regex"]  = r"[?]"
                state["min_triggers"]    = 1

                state["h_question"]      = True
                state["h_multisent"]     = True
                state["h_min_sentences"] = 2
                state["h_long_text"]     = False
                state["h_min_words"]     = 12
                state["h_conjunctions"]  = True
                state["h_numbers_math"]  = True
                state["h_code_or_url"]   = True
                state["h_uncertainty"]   = True

                state["min_score"]   = 40
                state["max_repairs"] = 2

                _save_state()
                return (
                    gr.update(value=_build_reflection_block(state["min_score"], state["show_scores"], state["legend"], state["max_repairs"])),
                    gr.update(value=state["min_input_chars"]),
                    gr.update(value=state["force_on_regex"]),
                    gr.update(value=state["min_triggers"]),
                    gr.update(value=state["h_question"]),
                    gr.update(value=state["h_multisent"]),
                    gr.update(value=state["h_min_sentences"]),
                    gr.update(value=state["h_long_text"]),
                    gr.update(value=state["h_min_words"]),
                    gr.update(value=state["h_conjunctions"]),
                    gr.update(value=state["h_numbers_math"]),
                    gr.update(value=state["h_code_or_url"]),
                    gr.update(value=state["h_uncertainty"]),
                    gr.update(value=state["apply_to"]),
                )

            def _apply_preset_strict():
                # Strict – klare Schwelle & 2 Reparaturen
                state["apply_to"]        = "context"
                state["min_input_chars"] = 6
                state["force_on_regex"]  = r"[?]|(^/think\b)"
                state["min_triggers"]    = 2

                state["h_question"]      = True
                state["h_multisent"]     = True
                state["h_min_sentences"] = 2
                state["h_long_text"]     = False
                state["h_min_words"]     = 12
                state["h_conjunctions"]  = True
                state["h_numbers_math"]  = True
                state["h_code_or_url"]   = True
                state["h_uncertainty"]   = True

                state["min_score"]   = 65
                state["max_repairs"] = 4

                _save_state()
                return (
                    gr.update(value=_build_reflection_block(state["min_score"], state["show_scores"], state["legend"], state["max_repairs"])),
                    gr.update(value=state["min_input_chars"]),
                    gr.update(value=state["force_on_regex"]),
                    gr.update(value=state["min_triggers"]),
                    gr.update(value=state["h_question"]),
                    gr.update(value=state["h_multisent"]),
                    gr.update(value=state["h_min_sentences"]),
                    gr.update(value=state["h_long_text"]),
                    gr.update(value=state["h_min_words"]),
                    gr.update(value=state["h_conjunctions"]),
                    gr.update(value=state["h_numbers_math"]),
                    gr.update(value=state["h_code_or_url"]),
                    gr.update(value=state["h_uncertainty"]),
                    gr.update(value=state["apply_to"]),
                )
                
            # Modus wechseln
            def _on_mode_change(mode: str):
                mode = (mode or "simple").lower()
                state["ui_mode"] = "expert" if "expert" in mode else "simple"
                if state["ui_mode"] == "simple":
                    state["inject_agent_template"] = True
                    vis_simple, vis_expert = True, False
                    agent_val, agent_inter = True, False
                else:
                    vis_simple, vis_expert = False, True
                    agent_val  = bool(state.get("inject_agent_template", True))
                    agent_inter = True
                _save_state()
                return (
                    gr.update(visible=vis_simple),    # grp_simple
                    gr.update(visible=vis_expert),    # grp_expert
                    gr.update(value=agent_val, interactive=agent_inter),  # cb_agent
                    gr.update(value=agent_val, interactive=agent_inter),  # cb_agent_e
                    gr.update(value=_build_reflection_block(
                        state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                )

            def _on_agent_toggle_simple(v: bool):
                state["inject_agent_template"] = bool(v)
                _save_state()
                return gr.update(value=_build_reflection_block(
                    state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                ))

            def _on_show_toggle_expert(v: bool):
                state["show_scores"] = bool(v)
                _save_state()
                # Preview + beide Checkboxen synchronisieren
                return (
                    gr.update(value=_build_reflection_block(
                        state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                    gr.update(value=bool(v)),  # cb_show (simple)
                    gr.update(value=bool(v)),  # cb_show_e (expert)
                )

            def _on_legend_toggle_expert(v: bool):
                state["legend"] = bool(v)
                _save_state()
                return (
                    gr.update(value=_build_reflection_block(
                    state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                    gr.update(value=bool(v)),  # cb_leg (simple)
                    gr.update(value=bool(v)),  # cb_leg_e (expert)
                )

            def _on_agent_toggle_expert(v: bool):
                state["inject_agent_template"] = bool(v)
                _save_state()
                return gr.update(value=_build_reflection_block(
                    state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                ))

            def _on_min_score_expert(v):
                try:
                    state["min_score"] = max(0, min(100, int(v or 0)))
                except Exception:
                    state["min_score"] = 0
                _save_state()
                return (
                    gr.update(value=_build_reflection_block(
                        state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                    gr.update(value=state["min_score"]),  # nb_min (simple)
                    gr.update(value=state["min_score"]),  # nb_min_e (expert)
                )

            def _on_max_repairs_expert(v):
                try:
                    state["max_repairs"] = max(0, min(5, int(v or 0)))
                except Exception:
                    state["max_repairs"] = 0
                _save_state()
                return (
                    gr.update(value=_build_reflection_block(
                        state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                    gr.update(value=state["max_repairs"]), # nb_rep (simple)
                    gr.update(value=state["max_repairs"]), # nb_rep_e (expert)
                )

            def _on_apply_to_expert(v):
                state["apply_to"] = _apply_display_to_code(str(apply_to or _apply_code_to_display("context")))
                _save_state()
                return (
                    gr.update(value=_build_reflection_block(
                        state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                    gr.update(value=state["apply_to"]),  # dd_apply (simple)
                    gr.update(value=state["apply_to"]),  # dd_apply_e (expert)
                )


            def _on_cap_toggle(limit_on: bool):
                state["limit_cap"] = bool(limit_on)
                _save_state()
                # 1) Slider interaktiv machen/entsperren
                # 2) Preview neu rendern (weil _build_reflection_block cap beachtet)
                return (
                    gr.update(interactive=bool(limit_on)),  # wirkt auf sl_cap
                    gr.update(value=_build_reflection_block(
                        state["min_score"], state["show_scores"], state["legend"], state["max_repairs"]
                    )),
                )
            
            # ───────────── Sprachwechsel ─────────────
            def _on_lang_change(lang: str):
                state["lang"] = (lang or "de").lower()
                _save_state()

                # 1) Preview neu
                updates = [gr.update(
                    value=_build_reflection_block(
                        state.get("min_score", 0),
                        state.get("show_scores", False),
                        state.get("legend", True),
                        state.get("max_repairs", 2),
                    )
                )]

                # 2) Labels/Choices/Values in derselben Reihenfolge wie dd_lang.change(...outputs=[...])
                updates += [
                    gr.update(label=_t("ui.lang")),  # dd_lang

                    # dd_mode: Label, Choices und Value lokalisieren
                    gr.update(
                        label=_t("ui.mode"),
                        choices=[_t("ui.mode_simple"), _t("ui.mode_expert")],
                        value=(_t("ui.mode_expert")
                               if state.get("ui_mode", "simple") == "expert"
                               else _t("ui.mode_simple")),
                    ),

                    gr.update(label=_t("ui.enabled")),         # cb_en
                    gr.update(label=_t("ui.debug")),           # cb_dbg
                    gr.update(label=_t("ui.show_scores")),     # cb_show
                    gr.update(label=_t("ui.legend")),          # cb_leg

                    # dd_apply: Label + lokalisierte Choices + gemappter Value
                    gr.update(
                        label=_t("ui.apply_to"),
                        choices=_apply_display_list(),
                        value=_apply_code_to_display(state.get("apply_to", "context")),
                    ),

                    gr.update(label=_t("ui.min_score")),       # nb_min
                    gr.update(label=_t("ui.max_repairs")),     # nb_rep
                    gr.update(label=_t("ui.max_context")),     # sl_cap

                    gr.update(label=_t("ui.gate_min_chars")),  # nb_gate
                    gr.update(label=_t("ui.force_regex")),     # tb_force
                    gr.update(label=_t("ui.min_triggers")),    # nb_mintr

                    # Buttons – ALLE fünf Presets beschriften
                    gr.update(value=_t("ui.preset_questions")), # btn_preset_q
                    gr.update(value=_t("ui.preset_always")),    # btn_preset_always
                    gr.update(value=_t("ui.preset_min")),       # btn_preset_min
                    gr.update(value=_t("ui.preset_light")),     # btn_preset_light
                    gr.update(value=_t("ui.preset_strict")),    # btn_preset_strict

                    # Heuristik-Labels
                    gr.update(label=_t("ui.h_question")),       # cb_q
                    gr.update(label=_t("ui.h_multisent")),      # cb_ms
                    gr.update(label=_t("ui.h_min_sentences")),  # nb_ms
                    gr.update(label=_t("ui.h_long_text")),      # cb_len
                    gr.update(label=_t("ui.h_min_words")),      # nb_w
                    gr.update(label=_t("ui.h_conjunctions")),   # cb_conj
                    gr.update(label=_t("ui.h_numbers_math")),   # cb_num
                    gr.update(label=_t("ui.h_code_or_url")),    # cb_code
                    gr.update(label=_t("ui.h_uncertainty")),    # cb_unc
                ]
                return updates

            # ─────────────── Verdrahtung ───────────────

            dd_lang.change(
                _on_lang_change,
                inputs=[dd_lang],
                outputs=[
                    # exakt gleiche Reihenfolge wie oben:
                    prev, dd_lang, dd_mode,
                    cb_en, cb_dbg, cb_show, cb_leg,
                    dd_apply,
                    nb_min, nb_rep, sl_cap,
                    nb_gate, tb_force, nb_mintr,
                    btn_preset_q, btn_preset_always, btn_preset_min, btn_preset_light, btn_preset_strict,
                    cb_q, cb_ms, nb_ms, cb_len, nb_w, cb_conj, cb_num, cb_code, cb_unc,
                ],
            )

            dd_mode.change(
                _on_mode_change,
                inputs=[dd_mode],
                outputs=[grp_simple, grp_expert, cb_agent, cb_agent_e, prev]
            )
            cb_agent.change(_on_agent_toggle_simple, inputs=[cb_agent], outputs=[prev])
            cb_agent_e.change(_on_agent_toggle_expert, inputs=[cb_agent_e], outputs=[prev])
            cb_show_e.change(_on_show_toggle_expert,   inputs=[cb_show_e], outputs=[prev, cb_show, cb_show_e])
            cb_leg_e.change(_on_legend_toggle_expert,  inputs=[cb_leg_e],  outputs=[prev, cb_leg,  cb_leg_e])
            nb_min_e.change(_on_min_score_expert,      inputs=[nb_min_e],  outputs=[prev, nb_min, nb_min_e])
            nb_rep_e.change(_on_max_repairs_expert,    inputs=[nb_rep_e],  outputs=[prev, nb_rep, nb_rep_e])
            dd_apply_e.change(_on_apply_to_expert,     inputs=[dd_apply_e],outputs=[prev, dd_apply, dd_apply_e])
            cb_cap.change(_on_cap_toggle, inputs=[cb_cap], outputs=[sl_cap, prev])

            btn_preset_q.click(
                _apply_preset_questions,
                inputs=[],
                outputs=[prev, nb_gate, tb_force, nb_mintr,
                         cb_q, cb_ms, nb_ms, cb_len, nb_w,
                         cb_conj, cb_num, cb_code, cb_unc, dd_apply],
            )
            btn_preset_always.click(
                _apply_preset_always,
                inputs=[],
                outputs=[prev, nb_gate, tb_force, nb_mintr,
                         cb_q, cb_ms, nb_ms, cb_len, nb_w,
                         cb_conj, cb_num, cb_code, cb_unc, dd_apply],
            )
            btn_preset_min.click(
                _apply_preset_minimal,
                inputs=[],
                outputs=[prev, nb_gate, tb_force, nb_mintr,
                         cb_q, cb_ms, nb_ms, cb_len, nb_w,
                         cb_conj, cb_num, cb_code, cb_unc, dd_apply],
            )
            btn_preset_light.click(
                _apply_preset_light,
                inputs=[],
                outputs=[prev, nb_gate, tb_force, nb_mintr,
                         cb_q, cb_ms, nb_ms, cb_len, nb_w,
                         cb_conj, cb_num, cb_code, cb_unc, dd_apply],
            )
            btn_preset_strict.click(
                _apply_preset_strict,
                inputs=[],
                outputs=[prev, nb_gate, tb_force, nb_mintr,
                         cb_q, cb_ms, nb_ms, cb_len, nb_w,
                         cb_conj, cb_num, cb_code, cb_unc, dd_apply],
            )

            # Optional: Cap-Checkbox steuert, ob der Slider interaktiv ist
            def _on_cap_toggle(v: bool):
                state["limit_cap"] = bool(v)
                _save_state()
                return gr.update(interactive=bool(v))

            # Gemeinsames Update (alle relevanten Controls) → _upd
            controls = [
                cb_en, cb_dbg, cb_show, cb_leg, nb_min, nb_rep, sl_cap,
                nb_gate, tb_force, nb_mintr,
                cb_q, cb_ms, nb_ms, cb_len, nb_w, cb_conj, cb_num, cb_code, cb_unc,
                dd_apply,  # 20
            ]
            sl_cap.release(_upd, controls, [prev])
            for ctl in [c for c in controls if c is not sl_cap]:
                ctl.change(_upd, controls, [prev])


# ───────────────────────────────────────────────────────────────
# Auto-Load
# ───────────────────────────────────────────────────────────────
_load_state()
