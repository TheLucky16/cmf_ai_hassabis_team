# cmf_ai_hw_1

Multi-agent pipeline that turns an online course webpage into personalized,
per-learner study plans.

- **Agent 1** (`agent_1.py`): scrape a course URL → clean course layout (Markdown).
- **Agent 2** (`agent_2.py`): course layout → self-contained micro-lessons (`outputs/agent_2_output.json`).
- **Agent 3** (`agent_3.py`): micro-lessons + learner profiles (`inputs/users.md`) → personalized
  learning paths (`outputs/agent_3_output.json`).

All agents call the LLM through `get_answer()` in `chatbot.py` (Google Gemini, free tier).

## Dev To Do:
1) ~~write prompts and users.md in inputs/~~ done
2) ~~connect chatbot api~~ done (Gemini in `chatbot.py`)
3) ~~agent 2~~ done
4) ~~agent 3~~ done

## To Run:
1) Create and activate a virtual environment:
   `python3 -m venv .venv && source .venv/bin/activate`
2) Install dependencies: `pip install -r requirements.txt`
3) Get a free Gemini API key (https://aistudio.google.com/apikey) and provide it
   via a local `.env` file (recommended, gitignored):
   `cp .env.example .env`  then edit `.env` and paste your key.
   (Alternatively: `export GEMINI_API_KEY="your-key"`.)
4) Run the whole pipeline: `python main.py`
   (runs the three agents in order and validates each handoff file).

   Or run the stages individually:
   - `python agent_1.py`   (scrape + clean a course page)
   - `python agent_2.py`   (split into micro-lessons)
   - `python agent_3.py`   (build personalized learning paths)
