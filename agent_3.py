"""Agent 3 — Personalized Learning Path.

Consumes the micro-lessons produced by Agent 2 (outputs/agent_2_output.json) and
the learner profiles in inputs/users.md, then asks the LLM to build a tailored,
ordered, scheduled study plan for each learner.

Run:
    export GEMINI_API_KEY="your-key"
    python agent_3.py

Output:
    outputs/agent_3_output.json  — a list with one personalized plan per learner.
"""

import json
import os
import re

from chatbot import get_answer

LESSONS_FILE = "outputs/agent_2_output.json"
USERS_FILE = "inputs/users.md"
PROMPT_FILE = "inputs/agent_3_prompt.txt"
OUTPUT_FILE = "outputs/agent_3_output.json"


def parse_llm_response(response: str) -> dict:
    """Parse a JSON object from the LLM response, tolerating markdown fences
    or surrounding prose."""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Strip ```json ... ``` fences if present.
    fenced = re.search(r"```(?:json)?\s*(.*?)```", response, re.DOTALL)
    candidate = fenced.group(1) if fenced else response

    # Fall back to the outermost {...} block.
    match = re.search(r"\{.*\}", candidate, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("Failed to parse JSON object from LLM response")


def load_lessons(path: str = LESSONS_FILE) -> list:
    """Load the Agent 2 micro-lessons."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_users(path: str = USERS_FILE) -> list:
    """Split users.md into individual profiles.

    Each profile starts with a level-2 heading (## Name). Returns a list of
    {"name": str, "profile": str} where profile is the full markdown block.
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    users = []
    # Split keeping the heading lines; each chunk after a "## " starts a profile.
    chunks = re.split(r"(?m)^##\s+", text)
    for chunk in chunks[1:]:  # chunks[0] is the preamble before the first "## "
        chunk = chunk.strip()
        if not chunk:
            continue
        name = chunk.splitlines()[0].strip()
        users.append({"name": name, "profile": "## " + chunk})
    return users


def build_prompt(template: str, lessons: list, user_profile: str) -> str:
    """Fill the Agent 3 prompt template with the lesson catalog and one profile."""
    lessons_json = json.dumps(lessons, ensure_ascii=False, indent=2)
    return (
        template
        .replace("[PASTE USER PROFILE HERE]", user_profile)
        .replace("[PASTE LESSONS HERE]", lessons_json)
    )


def personalize(user: dict, lessons: list, template: str, answer_fn=get_answer) -> dict:
    """Build one learner's personalized plan. `answer_fn` is injectable for testing."""
    prompt = build_prompt(template, lessons, user["profile"])
    raw = answer_fn(prompt)
    plan = parse_llm_response(raw)
    # Ensure the learner name is always present, even if the model omits it.
    plan.setdefault("user", user["name"])
    return plan


def run(answer_fn=get_answer) -> list:
    """Run Agent 3 over all learners and write outputs/agent_3_output.json."""
    if not os.path.exists(LESSONS_FILE):
        raise SystemExit(
            f"{LESSONS_FILE} not found. Run Agent 2 first to generate the micro-lessons."
        )

    lessons = load_lessons()
    users = parse_users()
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    plans = []
    for user in users:
        print(f"Building learning path for {user['name']} ...")
        plans.append(personalize(user, lessons, template, answer_fn=answer_fn))

    os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(plans)} personalized learning paths to {OUTPUT_FILE}")
    return plans


if __name__ == "__main__":
    run()
