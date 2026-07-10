from functions.helpers import choose_label, format_history, get_answer
from functions.student_actions import ask_question, learn, take_test

STUDENT_ACTIONS = ["learn", "ask_question", "take_test"]


def default_action(state):
    latest = state["history"][-1] if state["history"] else {}
    if latest.get("speaker") == "Mentor" and latest.get("action") == "test":
        return "take_test"
    return "learn"


def enforce_action(action, state):
    latest = state["history"][-1] if state["history"] else {}
    if latest.get("speaker") == "Mentor" and latest.get("action") == "answer_question":
        return "learn"
    if latest.get("speaker") == "Mentor" and latest.get("action") == "test":
        return "take_test"
    return action


def decide_action(student_prompt, lesson, state, provider=None):
    latest = state["history"][-1] if state["history"] else {}
    prompt = f"""
{student_prompt}

Choose the next Student action.

Allowed actions:
- learn: respond to teaching and attempt a normal practice task.
- ask_question: ask one clarifying question.
- take_test: answer a Mentor probe, test, or transfer challenge.

Current lesson:
{lesson["title"]}

State:
- turn: {state["turn"]}
- student notes: {state.get("student_notes", "") or "None"}
- latest speaker: {latest.get("speaker", "None")}
- latest action: {latest.get("action", "None")}

Recent dialogue:
{format_history(state["history"])}

Rules:
- Return only one allowed action.
- If the Mentor just taught and gave a practice task, choose learn.
- If something is unclear, choose ask_question.
- If the Mentor is checking application, choose take_test.
"""
    raw = get_answer(prompt.strip(), provider=provider, temperature=0, max_tokens=80)
    action = choose_label(raw, STUDENT_ACTIONS, default_action(state))
    return enforce_action(action, state)


def reply(student_prompt, lesson, state, provider=None):
    action = decide_action(student_prompt, lesson, state, provider=provider)
    notes = state.get("student_notes", "")
    bluff = False

    if action == "ask_question":
        text = ask_question(student_prompt, lesson, state["history"], notes=notes, provider=provider)
    elif action == "take_test":
        used_bluffs = set(state.get("used_bluff_lessons", []))
        bluff = lesson["number"] in state.get("bluff_lessons", []) and lesson["number"] not in used_bluffs
        text = take_test(student_prompt, lesson, state["history"], notes=notes, bluff=bluff, provider=provider)
    else:
        text = learn(student_prompt, lesson, state["history"], notes=notes, provider=provider)

    return {"speaker": "Student", "action": action, "text": text, "bluff": bluff}
