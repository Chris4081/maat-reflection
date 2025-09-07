# maat-reflection
Maat Reflection – Extension for the text generation WebUI to add self-reflection, heuristics and improved reasoning

Maat Reflection – Extension for text-generation-webui

Maat Reflection is an extension for the text-generation-webui, adding self-reflection, heuristics, and improved reasoning to language models.



✨ Features
	•	Self-Reflection before answering
The model creates an internal draft, evaluates it against the 5 Maat principles

(🌿 Harmony, ⚖️ Balance, 🎨 Creativity, 🌐 Connectedness, 🕊️ Respect),

and silently improves it if needed before producing the final response.
	•	Heuristic-based triggering
 
Reflection is only performed when certain conditions are met:
	•	Question marks / wh-words
	•	Multiple sentences or words
	•	Longer text inputs
	•	Numbers, code, or uncertainty expressions
 
→ Avoids unnecessary “thinking” on short or trivial prompts.
	•	Force Regex
 
Custom regex rules can be defined to force thinking (e.g., ? or /think).
	•	Multiple Presets
	•	💡 Questions only
	•	💡 Always think (ignores heuristics)
	•	⚡ Minimal (fast, low self-repair)
	•	✨ Light (mild self-improvements)
	•	🔥 Strict (maximum checking & repair cycles)
	•	Simple / Expert Mode
	•	Simple Mode → minimal controls, pre-configured defaults.
	•	Expert Mode → full control over heuristics, triggers, and scoring thresholds.
	•	Multi-language support 🌍

The UI, reflection guide, and heuristics are available in:

	•	🇩🇪 German
	•	🇬🇧 English
	•	🇪🇸 Spanish
	•	🇫🇷 French
	•	🇵🇹 Portuguese
	•	🇮🇹 Italian
	•	🇨🇿 Czech
 
	•	Refresh & Stats Tab
	•	Preview of active reflection rules
	•	Statistics on reflections, repairs, and scores
	•	Specials Tab (Formulas)
	•	Built-in Maat formulas (Maat Value, PLP, World-Maat, ToE-Maat)
	•	Add your own formulas via Markdown
	•	Option to include formulas inside the reflection guide


🚀 Installation
	1.	Copy the folder maat_reflection into text-generation-webui/user_data/extensions/
	2.	Restart the WebUI
	3.	Enable the extension via the Maat Reflection Tab


💡 Tips
	•	For first testing, select the preset 💡 Always think.
		This ensures the model reflects on every prompt, so you can clearly see the effect.
	•	Afterwards, experiment with Questions only, Light, or Strict to fine-tune the balance between speed and quality.
 	•	Use the Refresh & Stats tab to monitor reflection activity and improvements.
