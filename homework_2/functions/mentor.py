from functions.helpers import choose_label, format_history, get_answer
from functions.mentor_actions import answer_question, teach, test

MENTOR_ACTIONS = ["teach", "answer_question", "test"]


def default_action(state):
    if not state.get("lesson_started"):
        return "teach"

    latest = state["history"][-1] if state["history"] else {}
    if latest.get("speaker") == "Student" and latest.get("action") == "ask_question":
        return "answer_question"
    return "test"


def enforce_action(action, state):
    latest = state["history"][-1] if state["history"] else {}
    if not state.get("lesson_started"):
        return "teach"
    if latest.get("speaker") == "Student" and latest.get("action") == "ask_question":
        return "answer_question"
    if latest.get("speaker") == "Student" and latest.get("action") in ["learn", "take_test"]:
        return "test"
    return action


def decide_action(mentor_prompt, lesson, state, provider=None):
    latest = state["history"][-1] if state["history"] else {}
    prompt = f"""
{mentor_prompt}

Choose the next Mentor action.

Allowed actions:
- teach: introduce or continue teaching the current lesson.
- answer_question: answer the Student's latest question or confusion.
- test: check whether the Student can apply the skill and decide whether to advance.

Current lesson:
{lesson["title"]}

State:
- turn: {state["turn"]}
- lesson started: {state.get("lesson_started", False)}
- last mentor status: {state.get("last_mentor_status", "")}
- latest speaker: {latest.get("speaker", "None")}
- latest action: {latest.get("action", "None")}

Recent dialogue:
{format_history(state["history"])}

Rules:
- Return only one allowed action.
- If lesson started is False, choose teach.
- If the latest Student message asks a question, choose answer_question.
- If the latest Student message attempts the practice task, choose test.
"""
    raw = get_answer(prompt.strip(), provider=provider, temperature=0, max_tokens=80)
    action = choose_label(raw, MENTOR_ACTIONS, default_action(state))
    return enforce_action(action, state)


def reply(mentor_prompt, lesson, state, total_lessons=10, provider=None):
    action = decide_action(mentor_prompt, lesson, state, provider=provider)

    if action == "teach":
        text = teach(mentor_prompt, lesson, state["history"], provider=provider)
    elif action == "answer_question":
        text = answer_question(mentor_prompt, lesson, state["history"], provider=provider)
    else:
        text = test(mentor_prompt, lesson, state["history"], total_lessons=total_lessons, provider=provider)

    return {"speaker": "Mentor", "action": action, "text": text}
