# i18n.py
# i18n.py — zentrale Übersetzungen + Helfer
# Quelle der Wahrheit für alle Texte/Regexe.
# Benutzung aus script.py:
#   from user_data.extensions.maat_reflection.i18n import I18N, t as t_i18n, rx as rx_i18n

I18N = {
    "de": {
        # UI
        "ui.tab": "🧭 Maat Reflection",
        "ui.lang": "Sprache",
        "ui.enabled": "Aktiv",
        "ui.debug": "Debug-Logs",
        "ui.show_scores": "Am Ende Score-Zeile erlauben",
        "ui.legend": "Legende einblenden",
        "ui.apply_to": "Injektion anwenden auf",
        "ui.min_score": "Mindestscore (0–100)",
        "ui.max_repairs": "Max. stille Verbesserungen (0–5)",
        "ui.limit_cap": "Kontext-Limit aktivieren",
        "ui.max_context": "Max. Kontext-Zeichen (Injection)",
        "ui.gate_min_chars": "Nicht nachdenken unter N Zeichen",
        "ui.force_regex": "Force-Regex (zwingt Thinking, z. B. ? oder /think)",
        "ui.min_triggers": "Min. Heuristik-Treffer bis Thinking",
        "ui.preset_questions": "💡 Preset: Nur bei Fragen denken",
        "ui.preset_always": "💡 Preset: Immer denken (ohne Heuristik)",
        "ui.preset_min": "⚡ Preset: Minimal",
        "ui.preset_light": "✨ Preset: Light",
        "ui.preset_strict": "🔥 Preset: Strict",
        "ui.heuristics": "Heuristiken (Feinauswahl)",
        "ui.h_question": "Frage (“?”/W-Wörter)",
        "ui.h_multisent": "Mehrere Sätze",
        "ui.h_min_sentences": "Min. Sätze",
        "ui.h_long_text": "Langer Text (min. Wörter)",
        "ui.h_min_words": "Min. Wörter",
        "ui.h_conjunctions": "Konnektoren",
        "ui.h_numbers_math": "Zahlen/Mathe",
        "ui.h_code_or_url": "Code/URL",
        "ui.h_uncertainty": "Unsicherheiten/Bitte",
        "ui.preview": "Vorschau der Reflexions-Regeln",
        "ui.mode": "Modus",
        "ui.mode_simple": "Einfach",
        "ui.mode_expert": "Experte",
        "ui.inject_agent_template": "Maat-Agent-Template injizieren",

        # Guide & Legend
        "guide.scores_on": "Optional: Am Ende eine Zeile 'SCORES: H=.. B=.. S=.. V=.. R=..' (wenn sinnvoll).",
        "guide.scores_off": "Gib KEINE Scores aus.",
        "guide.template": (
            "[MAAT_REFLECTION_GUIDE v2]\n\n"
            "ZIEL: Gib eine saubere, klare Endantwort aus. Führe davor eine kurze, stille Selbstreflexion durch.\n\n"
            "SCHRITTE (intern, NICHT ausgeben):\n"
            "1) <reflect>Erzeuge einen ersten Entwurf zur Nutzeranfrage.</reflect>\n"
            "2) Bewerte 5 Maat-Werte (0–100):\n"
            "   H=Harmonie, B=Balance, S=Schöpfungskraft, V=Verbundenheit, R=Respekt.\n"
            "3) Wenn einer der Werte < {min_score} ist, führe eine stille Verbesserung (Self-Repair) durch.\n"
            "   Maximal erlaubte Verbesserungen: {max_repairs} Durchläufe.\n"
            "   Nach jeder Verbesserung erneut die 5 Werte prüfen.\n"
            "4) Schließe das Denken ab und gib NUR die fertige Endantwort aus.\n\n"
            "FORMAT der Antwort:\n"
            "- Standard: Nur die Endantwort, KEINE inneren Gedanken, KEINE Tags.\n"
            "- {scores_hint}\n\n"
            "HINWEISE:\n"
            "- Bevorzuge Kürze & Klarheit, nenne Unsicherheiten transparent.\n"
            "- Vermeide Redundanz, Halluzinationen und unnötige Selbstbezüge.\n"
            "- Stelle konstruktive Nachfragen nur, wenn sie wirklich die Qualität verbessern.\n"
        ),
        "legend.short": (
            "LEGENDEN-KURZFORM:\n"
            "- H (Harmonie): Stimmigkeit, Kohärenz, roter Faden.\n"
            "- B (Balance): Fakten-Genauigkeit, Logik, Klarheit.\n"
            "- S (Schöpfungskraft): Neuheit, Nützlichkeit, Originalität.\n"
            "- V (Verbundenheit): Kontextbezug, Empathie, Nutzerintention.\n"
            "- R (Respekt): Ethik, Grenzen, Transparenz, Sicherheit.\n"
        ),

        # Regex
        "rx.interro": r"\b(wer|wie|was|wo|warum|wieso|weshalb|welche?r?|wann|wieviel|wieviele)\b",
        "rx.conj": r"\b(und|oder|aber|denn|sondern|doch|jedoch|weil|obwohl|während|falls|damit|dass|deshalb|trotzdem)\b",
        "rx.uncertainty": r"\b(vielleicht|unsicher|schätz|ungewiss|bitte|hilfe|kannst du|könntest du|wäre es möglich)\b",
    },

    "en": {
        "ui.tab": "🧭 Maat Reflection",
        "ui.lang": "Language",
        "ui.enabled": "Enabled",
        "ui.debug": "Debug logs",
        "ui.show_scores": "Allow score line at the end",
        "ui.legend": "Show legend",
        "ui.apply_to": "Apply injection to",
        "ui.min_score": "Min. score (0–100)",
        "ui.max_repairs": "Max. silent repairs (0–5)",
        "ui.limit_cap": "Enable context cap",
        "ui.max_context": "Max context chars (injection)",
        "ui.gate_min_chars": "Don’t reflect below N characters",
        "ui.force_regex": "Force-regex (forces thinking, e.g. ? or /think)",
        "ui.min_triggers": "Min. heuristic hits to trigger",
        "ui.preset_questions": "💡 Preset: Think only for questions",
        "ui.preset_always": "💡 Preset: Always think (no heuristics)",
        "ui.preset_min": "⚡ Preset: Minimal",
        "ui.preset_light": "✨ Preset: Light",
        "ui.preset_strict": "🔥 Preset: Strict",
        "ui.heuristics": "Heuristics (fine tuning)",
        "ui.h_question": "Question (“?”/wh-words)",
        "ui.h_multisent": "Multiple sentences",
        "ui.h_min_sentences": "Min. sentences",
        "ui.h_long_text": "Long text (min. words)",
        "ui.h_min_words": "Min. words",
        "ui.h_conjunctions": "Conjunctions",
        "ui.h_numbers_math": "Numbers/Math",
        "ui.h_code_or_url": "Code/URL",
        "ui.h_uncertainty": "Uncertainty/Please",
        "ui.preview": "Preview of reflection rules",
        "ui.mode": "Mode",
        "ui.mode_simple": "Simple",
        "ui.mode_expert": "Expert",
        "ui.inject_agent_template": "Inject Maat agent template",

        "guide.scores_on": "Optional: Add a final line 'SCORES: H=.. B=.. S=.. V=.. R=..' (if helpful).",
        "guide.scores_off": "Do NOT output scores.",
        "guide.template": (
            "[MAAT_REFLECTION_GUIDE v2]\n\n"
            "GOAL: Produce a clean, clear final answer. Before that, perform a brief, silent self-reflection.\n\n"
            "STEPS (internal, DO NOT reveal):\n"
            "1) <reflect>Create an initial draft for the user's request.</reflect>\n"
            "2) Rate 5 Maat values (0–100):\n"
            "   H=Harmony, B=Balance, S=Creativity, V=Connectedness, R=Respect.\n"
            "3) If any value < {min_score}, perform a silent improvement (Self-Repair).\n"
            "   Maximum allowed improvements: {max_repairs} iterations.\n"
            "   After each improvement, re-check the 5 values.\n"
            "4) Stop thinking and output ONLY the polished final answer.\n\n"
            "OUTPUT FORMAT:\n"
            "- Default: Only the final answer, NO inner thoughts, NO tags.\n"
            "- {scores_hint}\n\n"
            "NOTES:\n"
            "- Prefer brevity & clarity; state uncertainties transparently.\n"
            "- Avoid redundancy, hallucinations, and unnecessary self-references.\n"
            "- Ask clarifying questions only if they truly improve quality.\n"
        ),
        "legend.short": (
            "LEGEND (SHORT):\n"
            "- H (Harmony): Coherence, consistency, clear thread.\n"
            "- B (Balance): Factual accuracy, logic, clarity.\n"
            "- S (Creativity): Novelty, usefulness, originality.\n"
            "- V (Connectedness): Context fit, empathy, user intent.\n"
            "- R (Respect): Ethics, boundaries, transparency, safety.\n"
        ),

        "rx.interro": r"\b(who|how|what|where|why|which|when|how\s+many|how\s+much)\b",
        "rx.conj": r"\b(and|or|but|nor|yet|so|because|although|while|if|thus|therefore|however)\b",
        "rx.uncertainty": r"\b(maybe|perhaps|unsure|uncertain|estimate|not\s+sure|please|could you|would you|is it possible)\b",
    },

    "es": {
        "ui.tab": "🧭 Maat Reflection",
        "ui.lang": "Idioma",
        "ui.enabled": "Activo",
        "ui.debug": "Registros de depuración",
        "ui.show_scores": "Permitir línea de puntuación al final",
        "ui.legend": "Mostrar leyenda",
        "ui.apply_to": "Aplicar inyección a",
        "ui.min_score": "Puntuación mínima (0–100)",
        "ui.max_repairs": "Máx. reparaciones silenciosas (0–5)",
        "ui.limit_cap": "Activar límite de contexto",
        "ui.max_context": "Máx. caracteres de contexto (inyección)",
        "ui.gate_min_chars": "No reflexionar por debajo de N caracteres",
        "ui.force_regex": "Regex forzado (p. ej., ? o /think)",
        "ui.min_triggers": "Mín. coincidencias heurísticas",
        "ui.preset_questions": "💡 Preajuste: Pensar solo ante preguntas",
        "ui.preset_always": "💡 Preajuste: Pensar siempre (sin heurística)",
        "ui.preset_min": "⚡ Preajuste: Mínimo",
        "ui.preset_light": "✨ Preajuste: Light",
        "ui.preset_strict": "🔥 Preajuste: Strict",
        "ui.heuristics": "Heurísticas (ajuste fino)",
        "ui.h_question": "Pregunta (“?”/palabras interrogativas)",
        "ui.h_multisent": "Varias frases",
        "ui.h_min_sentences": "Mín. frases",
        "ui.h_long_text": "Texto largo (mín. palabras)",
        "ui.h_min_words": "Mín. palabras",
        "ui.h_conjunctions": "Conjunciones",
        "ui.h_numbers_math": "Números/Matemáticas",
        "ui.h_code_or_url": "Código/URL",
        "ui.h_uncertainty": "Incertidumbre/Por favor",
        "ui.preview": "Vista previa de las reglas de reflexión",
        "ui.mode": "Modo",
        "ui.mode_simple": "Simple",
        "ui.mode_expert": "Experto",
        "ui.inject_agent_template": "Inyectar plantilla del agente Maat",

        "guide.scores_on": "Opcional: añade 'SCORES: H=.. B=.. S=.. V=.. R=..' (si ayuda).",
        "guide.scores_off": "NO muestres puntuaciones.",
        "guide.template": (
            "[MAAT_REFLECTION_GUIDE v2]\n\n"
            "OBJETIVO: Entregar una respuesta final clara y limpia. Antes, realiza una breve autorreflexión silenciosa.\n\n"
            "PASOS (interno, NO revelar):\n"
            "1) <reflect>Genera un primer borrador para la solicitud del usuario.</reflect>\n"
            "2) Valora 5 criterios Maat (0–100):\n"
            "   H=Armonía, B=Balance, S=Creatividad, V=Conexión, R=Respeto.\n"
            "3) Si algún valor < {min_score}, realiza una mejora silenciosa (Auto-Reparación).\n"
            "   Máx. mejoras permitidas: {max_repairs} iteraciones.\n"
            "   Tras cada mejora, vuelve a evaluar los 5 criterios.\n"
            "4) Finaliza el pensamiento y entrega SOLO la respuesta final pulida.\n\n"
            "FORMATO DE SALIDA:\n"
            "- Por defecto: solo la respuesta final, SIN pensamientos internos ni etiquetas.\n"
            "- {scores_hint}\n\n"
            "NOTAS:\n"
            "- Prioriza brevedad y claridad; declara las incertidumbres con transparencia.\n"
            "- Evita redundancias, alucinaciones y autorreferencias innecesarias.\n"
            "- Haz preguntas aclaratorias solo si realmente mejoran la calidad.\n"
        ),
        "legend.short": (
            "LEYENDA (BREVE):\n"
            "- H (Armonía): Coherencia, consistencia, hilo conductor.\n"
            "- B (Balance): Exactitud factual, lógica, claridad.\n"
            "- S (Creatividad): Novedad, utilidad, originalidad.\n"
            "- V (Conexión): Ajuste al contexto, empatía, intención del usuario.\n"
            "- R (Respeto): Ética, límites, transparencia, seguridad.\n"
        ),

        "rx.interro": r"\b(qui[eé]n|c[oó]mo|qu[eé]|d[oó]nde|por\s+qu[eé]|cu[aá]l(?:es)?|cu[aá]ndo|cu[aá]nto(?:s|as)?|cu[aá]nta)\b",
        "rx.conj": r"\b(y|o|pero|sino|aunque|mientras|porque|pues|si|as[ií]\s+que|por\s+tanto|por\s+lo\s+tanto|sin embargo)\b",
        "rx.uncertainty": r"\b(quiz[aá]s|tal vez|puede ser|no\s+estoy\s+seguro|no\s+estoy\s+segura|por favor|podr[ií]as|ser[ií]a posible)\b",
    },
}
# DE
I18N["de"].update({
    "apply.off": "Aus",
    "apply.context": "Kontext",
    "apply.prefix": "Prefix",
    "apply.both": "Beide",
})

# EN
I18N["en"].update({
    "apply.off": "Off",
    "apply.context": "Context",
    "apply.prefix": "Prefix",
    "apply.both": "Both",
})

# ES
I18N["es"].update({
    "apply.off": "Apagado",
    "apply.context": "Contexto",
    "apply.prefix": "Prefijo",
    "apply.both": "Ambos",
})

I18N.update({
    "fr": {
        # UI
        "ui.tab": "🧭 Réflexion Maat",
        "ui.lang": "Langue",
        "ui.enabled": "Actif",
        "ui.debug": "Journaux de débogage",
        "ui.show_scores": "Autoriser la ligne de score à la fin",
        "ui.legend": "Afficher la légende",
        "ui.apply_to": "Appliquer l’injection à",
        "ui.min_score": "Score minimum (0–100)",
        "ui.max_repairs": "Max. améliorations silencieuses (0–5)",
        "ui.limit_cap": "Activer la limite de contexte",
        "ui.max_context": "Caractères max du contexte (injection)",
        "ui.gate_min_chars": "Ne pas réfléchir en dessous de N caractères",
        "ui.force_regex": "Regex forcée (force la réflexion, p. ex. ? ou /think)",
        "ui.min_triggers": "Min. de déclencheurs heuristiques avant réflexion",
        "ui.preset_questions": "💡 Préréglage : Ne réfléchir que pour les questions",
        "ui.preset_always": "💡 Préréglage : Toujours réfléchir (sans heuristiques)",
        "ui.preset_min": "⚡ Préréglage : Minimal",
        "ui.preset_light": "✨ Préréglage : Light",
        "ui.preset_strict": "🔥 Préréglage : Strict",
        "ui.heuristics": "Heuristiques (réglage fin)",
        "ui.h_question": "Question (« ? »/mots interrogatifs)",
        "ui.h_multisent": "Phrases multiples",
        "ui.h_min_sentences": "Min. de phrases",
        "ui.h_long_text": "Texte long (min. de mots)",
        "ui.h_min_words": "Min. de mots",
        "ui.h_conjunctions": "Conjonctions",
        "ui.h_numbers_math": "Nombres/Maths",
        "ui.h_code_or_url": "Code/URL",
        "ui.h_uncertainty": "Incertitude/Demande",
        "ui.preview": "Aperçu des règles de réflexion",
        "ui.mode": "Mode",
        "ui.mode_simple": "Simple",
        "ui.mode_expert": "Expert",
        "ui.inject_agent_template": "Injecter le template d’agent Maat",

        # Guide & Légende
        "guide.scores_on": "Optionnel : ajouter en fin « SCORES: H=.. B=.. S=.. V=.. R=.. » (si utile).",
        "guide.scores_off": "NE PAS afficher de scores.",
        "guide.template": (
            "[MAAT_REFLECTION_GUIDE v2]\n\n"
            "OBJECTIF : Produire une réponse finale claire et propre. Avant cela, effectuer une courte auto-réflexion silencieuse.\n\n"
            "ÉTAPES (internes, NE PAS révéler) :\n"
            "1) <reflect>Créer une première ébauche pour la requête utilisateur.</reflect>\n"
            "2) Évaluer 5 valeurs Maat (0–100) :\n"
            "   H=Harmonie, B=Balance, S=Créativité, V=Connexion, R=Respect.\n"
            "3) Si une valeur < {min_score}, faire une amélioration silencieuse (Auto-Réparation).\n"
            "   Améliorations max autorisées : {max_repairs} itérations.\n"
            "   Après chaque amélioration, re-vérifier les 5 valeurs.\n"
            "4) Terminer la réflexion et sortir UNIQUEMENT la réponse finale.\n\n"
            "FORMAT DE SORTIE :\n"
            "- Par défaut : seulement la réponse finale, PAS de pensées internes, PAS de balises.\n"
            "- {scores_hint}\n\n"
            "NOTES :\n"
            "- Préférer la brièveté et la clarté ; déclarer les incertitudes avec transparence.\n"
            "- Éviter redondances, hallucinations, auto-références inutiles.\n"
            "- Poser des questions de clarification seulement si cela améliore vraiment la qualité.\n"
        ),
        "legend.short": (
            "LÉGENDE (COURTE) :\n"
            "- H (Harmonie) : Cohérence, consistance, fil conducteur.\n"
            "- B (Balance) : Exactitude factuelle, logique, clarté.\n"
            "- S (Créativité) : Nouveauté, utilité, originalité.\n"
            "- V (Connexion) : Adéquation au contexte, empathie, intention utilisateur.\n"
            "- R (Respect) : Éthique, limites, transparence, sécurité.\n"
        ),

        # Regex
        "rx.interro": r"\b(qui|comment|quoi|où|pourquoi|lequel|laquelle|lesquels|lesquelles|quand|combien|quelle|quelles|quel)\b",
        "rx.conj": r"\b(et|ou|mais|or|ni|car|cependant|pourtant|tandis que|bien que|parce que|si|donc|ainsi|toutefois)\b",
        "rx.uncertainty": r"\b(peut[-\s]?être|incertain|pas\s+sûr|svp|s'il vous plaît|pourriez[-\s]?vous|serait[-\s]?il possible)\b",
    },

    "pt": {
        # UI
        "ui.tab": "🧭 Reflexão Maat",
        "ui.lang": "Idioma",
        "ui.enabled": "Ativo",
        "ui.debug": "Registos de depuração",
        "ui.show_scores": "Permitir linha de pontuação no fim",
        "ui.legend": "Mostrar legenda",
        "ui.apply_to": "Aplicar injeção em",
        "ui.min_score": "Pontuação mínima (0–100)",
        "ui.max_repairs": "Máx. melhorias silenciosas (0–5)",
        "ui.limit_cap": "Ativar limite de contexto",
        "ui.max_context": "Máx. caracteres de contexto (injeção)",
        "ui.gate_min_chars": "Não refletir abaixo de N caracteres",
        "ui.force_regex": "Regex forçada (obriga a refletir, p.ex. ? ou /think)",
        "ui.min_triggers": "Mín. acertos heurísticos antes de refletir",
        "ui.preset_questions": "💡 Predefinição: Refletir apenas em perguntas",
        "ui.preset_always": "💡 Predefinição: Refletir sempre (sem heurísticas)",
        "ui.preset_min": "⚡ Predefinição: Mínimo",
        "ui.preset_light": "✨ Predefinição: Light",
        "ui.preset_strict": "🔥 Predefinição: Strict",
        "ui.heuristics": "Heurísticas (ajuste fino)",
        "ui.h_question": "Pergunta (“?”/palavras interrogativas)",
        "ui.h_multisent": "Múltiplas frases",
        "ui.h_min_sentences": "Mín. frases",
        "ui.h_long_text": "Texto longo (mín. palavras)",
        "ui.h_min_words": "Mín. palavras",
        "ui.h_conjunctions": "Conjunções",
        "ui.h_numbers_math": "Números/Matemática",
        "ui.h_code_or_url": "Código/URL",
        "ui.h_uncertainty": "Incerteza/Pedido",
        "ui.preview": "Pré-visualização das regras de reflexão",
        "ui.mode": "Modo",
        "ui.mode_simple": "Simples",
        "ui.mode_expert": "Avançado",
        "ui.inject_agent_template": "Injetar template do agente Maat",

        # Guia & Legenda
        "guide.scores_on": "Opcional: adicionar no fim ‘SCORES: H=.. B=.. S=.. V=.. R=..’ (se útil).",
        "guide.scores_off": "NÃO apresentar pontuações.",
        "guide.template": (
            "[MAAT_REFLECTION_GUIDE v2]\n\n"
            "OBJETIVO: Entregar uma resposta final clara e limpa. Antes disso, realizar uma breve autorreflexão silenciosa.\n\n"
            "PASSOS (interno, NÃO revelar):\n"
            "1) <reflect>Criar um rascunho inicial para a solicitação do utilizador.</reflect>\n"
            "2) Avaliar 5 valores Maat (0–100):\n"
            "   H=Harmonia, B=Balanço, S=Criatividade, V=Conexão, R=Respeito.\n"
            "3) Se algum valor < {min_score}, realizar uma melhoria silenciosa (Auto-Reparo).\n"
            "   Máx. melhorias permitidas: {max_repairs} iterações.\n"
            "   Após cada melhoria, voltar a verificar os 5 valores.\n"
            "4) Finalizar a reflexão e apresentar APENAS a resposta final.\n\n"
            "FORMATO DE SAÍDA:\n"
            "- Padrão: Apenas a resposta final, SEM pensamentos internos, SEM tags.\n"
            "- {scores_hint}\n\n"
            "NOTAS:\n"
            "- Preferir brevidade e clareza; declarar incertezas com transparência.\n"
            "- Evitar redundâncias, alucinações e autorreferências desnecessárias.\n"
            "- Fazer perguntas de esclarecimento apenas se realmente melhorarem a qualidade.\n"
        ),
        "legend.short": (
            "LENDA (RESUMO):\n"
            "- H (Harmonia): Coerência, consistência, fio condutor.\n"
            "- B (Balanço): Exatidão factual, lógica, clareza.\n"
            "- S (Criatividade): Novidade, utilidade, originalidade.\n"
            "- V (Conexão): Ajuste ao contexto, empatia, intenção do utilizador.\n"
            "- R (Respeito): Ética, limites, transparência, segurança.\n"
        ),

        # Regex
        "rx.interro": r"\b(quem|como|o\s+que|que|onde|por\s+que|porque|qual(?:es)?|quando|quanto(?:s|as)?|quanta)\b",
        "rx.conj": r"\b(e|ou|mas|porém|todavia|contudo|porque|embora|enquanto|se|assim|portanto|no\s+entanto)\b",
        "rx.uncertainty": r"\b(talvez|incerto|n[aã]o\s+tenho\s+certeza|por\s+favor|poderia|seria\s+poss[ií]vel)\b",
    }
})

# FR
I18N["fr"].update({
    "apply.off": "Désactivé",
    "apply.context": "Contexte",
    "apply.prefix": "Préfixe",
    "apply.both": "Les deux",
})

# PT
I18N["pt"].update({
    "apply.off": "Desligado",
    "apply.context": "Contexto",
    "apply.prefix": "Prefixo",
    "apply.both": "Ambos",
})

I18N.update({
    "it": {
        # UI
        "ui.tab": "🧭 Riflessione Maat",
        "ui.lang": "Lingua",
        "ui.enabled": "Attivo",
        "ui.debug": "Log di debug",
        "ui.show_scores": "Consenti riga di punteggio alla fine",
        "ui.legend": "Mostra legenda",
        "ui.apply_to": "Applica iniezione a",
        "ui.min_score": "Punteggio minimo (0–100)",
        "ui.max_repairs": "Max. miglioramenti silenziosi (0–5)",
        "ui.limit_cap": "Attiva limite di contesto",
        "ui.max_context": "Caratteri massimi di contesto (iniezione)",
        "ui.gate_min_chars": "Non riflettere sotto N caratteri",
        "ui.force_regex": "Regex forzata (obbliga a riflettere, es. ? o /think)",
        "ui.min_triggers": "Min. trigger euristici prima di riflettere",
        "ui.preset_questions": "💡 Preset: Riflettere solo su domande",
        "ui.preset_always": "💡 Preset: Riflettere sempre (senza euristiche)",
        "ui.preset_min": "⚡ Preset: Minimo",
        "ui.preset_light": "✨ Preset: Light",
        "ui.preset_strict": "🔥 Preset: Strict",
        "ui.heuristics": "Euristiche (regolazione fine)",
        "ui.h_question": "Domanda (“?”/parole interrogative)",
        "ui.h_multisent": "Frasi multiple",
        "ui.h_min_sentences": "Frasi minime",
        "ui.h_long_text": "Testo lungo (min. parole)",
        "ui.h_min_words": "Parole minime",
        "ui.h_conjunctions": "Congiunzioni",
        "ui.h_numbers_math": "Numeri/Matematica",
        "ui.h_code_or_url": "Codice/URL",
        "ui.h_uncertainty": "Incertezza/Richiesta",
        "ui.preview": "Anteprima delle regole di riflessione",
        "ui.mode": "Modalità",
        "ui.mode_simple": "Semplice",
        "ui.mode_expert": "Esperto",
        "ui.inject_agent_template": "Inietta il template dell’agente Maat",

        # Guide & Legend
        "guide.scores_on": "Opzionale: aggiungere alla fine 'SCORES: H=.. B=.. S=.. V=.. R=..' (se utile).",
        "guide.scores_off": "NON mostrare i punteggi.",
        "guide.template": (
            "[MAAT_REFLECTION_GUIDE v2]\n\n"
            "You speak Italian with the user.\n\n"
            "GOAL: Produce a clean, clear final answer. Before that, perform a brief, silent self-reflection.\n\n"
            "STEPS (internal, DO NOT reveal):\n"
            "1) <reflect>Create an initial draft for the user's request.</reflect>\n"
            "2) Rate 5 Maat values (0–100):\n"
            "   H=Harmony, B=Balance, S=Creativity, V=Connectedness, R=Respect.\n"
            "3) If any value < {min_score}, perform a silent improvement (Self-Repair).\n"
            "   Maximum allowed improvements: {max_repairs} iterations.\n"
            "   After each improvement, re-check the 5 values.\n"
            "4) Stop thinking and output ONLY the polished final answer.\n\n"
            "OUTPUT FORMAT:\n"
            "- Default: Only the final answer, NO inner thoughts, NO tags.\n"
            "- {scores_hint}\n\n"
            "NOTES:\n"
            "- Prefer brevity & clarity; state uncertainties transparently.\n"
            "- Avoid redundancy, hallucinations, and unnecessary self-references.\n"
            "- Ask clarifying questions only if they truly improve quality.\n"
        ),
        "legend.short": (
            "LEGENDA (BREVE):\n"
            "- H (Armonia): Coerenza, consistenza, filo logico.\n"
            "- B (Equilibrio): Accuratezza, logica, chiarezza.\n"
            "- S (Creatività): Novità, utilità, originalità.\n"
            "- V (Connessione): Contesto, empatia, intento utente.\n"
            "- R (Rispetto): Etica, limiti, trasparenza, sicurezza.\n"
        ),

        # Regex
        "rx.interro": r"\b(chi|come|cosa|che|dove|perch[eé]|quale|quali|quando|quanto|quanti|quante)\b",
        "rx.conj": r"\b(e|o|ma|però|bensì|sebbene|mentre|perché|quindi|dunque|tuttavia)\b",
        "rx.uncertainty": r"\b(forse|incerto|non\s+sono\s+sicuro|per\s+favore|potresti|sarebbe\s+possibile)\b",
    }
})

# Apply-Labels IT
I18N["it"].update({
    "apply.off": "Spento",
    "apply.context": "Contesto",
    "apply.prefix": "Prefisso",
    "apply.both": "Entrambi",
})

I18N.update({
    "cz": {
        # UI
        "ui.tab": "🧭 Maat Reflexe",
        "ui.lang": "Jazyk",
        "ui.enabled": "Aktivní",
        "ui.debug": "Ladicí záznamy",
        "ui.show_scores": "Povolit řádek se skóre na konci",
        "ui.legend": "Zobrazit legendu",
        "ui.apply_to": "Aplikovat injekci na",
        "ui.min_score": "Minimální skóre (0–100)",
        "ui.max_repairs": "Max. tichých oprav (0–5)",
        "ui.limit_cap": "Aktivovat limit kontextu",
        "ui.max_context": "Max. znaků kontextu (injekce)",
        "ui.gate_min_chars": "Nereflektovat pod N znaků",
        "ui.force_regex": "Vynucené regex (nutí k přemýšlení, např. ? nebo /think)",
        "ui.min_triggers": "Min. heuristických zásahů před reflexí",
        "ui.preset_questions": "💡 Předvolba: Přemýšlet jen při otázkách",
        "ui.preset_always": "💡 Předvolba: Vždy přemýšlet (bez heuristiky)",
        "ui.preset_min": "⚡ Předvolba: Minimální",
        "ui.preset_light": "✨ Předvolba: Light",
        "ui.preset_strict": "🔥 Předvolba: Strict",
        "ui.heuristics": "Heuristiky (jemné nastavení)",
        "ui.h_question": "Otázka („?“/tázací slova)",
        "ui.h_multisent": "Více vět",
        "ui.h_min_sentences": "Min. vět",
        "ui.h_long_text": "Dlouhý text (min. slov)",
        "ui.h_min_words": "Min. slov",
        "ui.h_conjunctions": "Spojky",
        "ui.h_numbers_math": "Čísla/Matematika",
        "ui.h_code_or_url": "Kód/URL",
        "ui.h_uncertainty": "Nejistota/Žádost",
        "ui.preview": "Náhled pravidel reflexe",
        "ui.mode": "Režim",
        "ui.mode_simple": "Jednoduchý",
        "ui.mode_expert": "Expert",
        "ui.inject_agent_template": "Injektovat šablonu agenta Maat",

        # Návod & Legenda
        "guide.scores_on": "Volitelné: přidejte na konec ‚SCORES: H=.. B=.. S=.. V=.. R=..‘ (pokud je užitečné).",
        "guide.scores_off": "NEzobrazovat skóre.",
        "guide.template": (
            "[MAAT_REFLECTION_GUIDE v2]\n\n"
            "CÍL: Vytvořit čistou, jasnou konečnou odpověď. Předtím proveď krátkou tichou sebereflexi.\n\n"
            "KROKY (interní, NEzveřejňovat):\n"
            "1) <reflect>Vytvoř první návrh odpovědi na dotaz uživatele.</reflect>\n"
            "2) Ohodnoť 5 Maat hodnot (0–100):\n"
            "   H=Harmonie, B=Rovnováha, S=Kreativita, V=Propojenost, R=Respekt.\n"
            "3) Pokud je některá hodnota < {min_score}, proveď tichou opravu (Auto-oprava).\n"
            "   Max. povolených oprav: {max_repairs} iterací.\n"
            "   Po každé opravě znovu zkontroluj 5 hodnot.\n"
            "4) Ukonči reflexi a vrať POUZE konečnou odpověď.\n\n"
            "FORMÁT VÝSTUPU:\n"
            "- Výchozí: pouze konečná odpověď, BEZ vnitřních myšlenek, BEZ tagů.\n"
            "- {scores_hint}\n\n"
            "POZNÁMKY:\n"
            "- Upřednostni stručnost a jasnost; nejistoty uváděj transparentně.\n"
            "- Vyhýbej se redundanci, halucinacím a zbytečným autoreferencím.\n"
            "- Uveď upřesňující otázky jen pokud opravdu zlepší kvalitu.\n"
        ),
        "legend.short": (
            "LEGENDA (KRÁTKÁ):\n"
            "- H (Harmonie): Koherence, konzistence, hlavní linie.\n"
            "- B (Rovnováha): Faktická přesnost, logika, jasnost.\n"
            "- S (Kreativita): Novost, užitečnost, originalita.\n"
            "- V (Propojenost): Kontext, empatie, záměr uživatele.\n"
            "- R (Respekt): Etika, hranice, transparentnost, bezpečnost.\n"
        ),

        # Regex
        "rx.interro": r"\b(kdo|jak|co|kde|proč|který|která|které|kdy|kolik)\b",
        "rx.conj": r"\b(a|nebo|ale|nýbrž|avšak|protože|i když|zatímco|jestli|tedy|takže|nicméně)\b",
        "rx.uncertainty": r"\b(možná|nejistý|nejsem si jistý|prosím|mohl bys|bylo by možné)\b",
    }
})

# Apply-Labels CZ
I18N["cz"].update({
    "apply.off": "Vypnuto",
    "apply.context": "Kontext",
    "apply.prefix": "Prefix",
    "apply.both": "Oboje",
})

# Italienisch (it)
I18N["it"].update({
    "rx.interro": r"\b(chi|come|cosa|dove|perch[eé]|quale|quando|quanto|quanti|quante)\b",
    "rx.conj": r"\b(e|o|ma|però|sebbene|mentre|perché|quindi|tuttavia)\b",
    "rx.uncertainty": r"\b(forse|magari|incerto|non\s+so|potresti|sarebbe\s+possibile)\b",
})

# Čeština (cz)
I18N["cz"].update({
    "rx.interro": r"\b(kdo|jak|co|kde|proč|který|kdy|kolik)\b",
    "rx.conj": r"\b(a|nebo|ale|nýbrž|avšak|protože|přestože|zatímco|jestli|tedy)\b",
    "rx.uncertainty": r"\b(možná|snad|nejsem\s+si\s+jistý|nejsem\s+si\s+jistá|prosím|mohl\s+by|bylo\s+by\s+možné)\b",
})

def t(lang: str, key: str, default: str = "") -> str:
    """Holt den Text für (lang,key); Fallback zu 'de' und/oder default."""
    lang = (lang or "de").lower()
    base = I18N.get("de", {})
    return I18N.get(lang, base).get(key, base.get(key, default or key))


def rx(lang: str, key: str, fallback: str) -> str:
    """Holt Regex-String für (lang,key) – oder fallback, falls fehlend."""
    lang = (lang or "de").lower()
    return I18N.get(lang, {}).get(key, fallback)