# Scriptoria — Generative AI–Powered Film Pre-Production

Minimal full-stack prototype (Flask) that generates screenplays, character profiles, and production plans from a short idea.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. (Optional) Set `OPENAI_API_KEY` to enable real AI outputs:

```powershell
$env:OPENAI_API_KEY = 'sk-...'
```

3. Run the app:

```bash
python app.py
```

Open http://127.0.0.1:5000

Notes

- If `OPENAI_API_KEY` is not set or `openai` isn't available, the app uses a simple deterministic fallback generator suitable for prototyping.
- Extend `scriptoria/generator.py` to customize prompts, models, or integrate other LLM providers.
