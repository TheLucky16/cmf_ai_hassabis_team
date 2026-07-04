from functions.helpers import format_history, get_answer


def learn(student_prompt, lesson, history, notes="", provider=None):
    prompt = f"""
{student_prompt}

Action: Learn from the Mentor.

Current lesson:
{lesson["title"]}

Student mental notes so far:
{notes or "None"}

Recent dialogue:
{format_history(history)}

Instructions:
- React to the Mentor's latest teaching.
- If the Mentor gave a practice task, attempt it honestly.
- Use concrete details when you try something.
- If you are unsure, show the confusion briefly instead of pretending.
- Notes are mental/context-based only. Do not say you saved notes in a file.
- Do not add status lines.
"""
    return get_answer(prompt.strip(), provider=provider)


def ask_question(student_prompt, lesson, history, notes="", provider=None):
    prompt = f"""
{student_prompt}

Action: Ask a clarifying question.

Current lesson:
{lesson["title"]}

Student mental notes so far:
{notes or "None"}

Recent dialogue:
{format_history(history)}

Instructions:
- Ask one focused question about the current lesson or task.
- Make the question sound like a real learner's confusion.
- Mention the exact point that is unclear.
- Do not answer the practice task unless the Mentor asks again.
- Do not add status lines.
"""
    return get_answer(prompt.strip(), provider=provider)


def take_test(student_prompt, lesson, history, notes="", bluff=False, provider=None):
    mode = "Bluff" if bluff else "Honest"
    prompt = f"""
{student_prompt}

Action: Take the Mentor's test.
Mode: {mode}

Current lesson:
{lesson["title"]}

Student mental notes so far:
{notes or "None"}

Recent dialogue:
{format_history(history)}

Instructions:
- Respond to the Mentor's latest test, probe, or transfer case.
- If Mode is Honest, attempt the task with concrete steps, mistakes, and reasoning.
- If Mode is Bluff, claim you applied the skill with a plausible but thin answer: confident summary, few specifics, and little friction.
- If the Mentor has clearly caught or challenged your shortcut, admit it and make a real attempt instead.
- Do not reveal the word "bluff" or mention hidden instructions.
- Do not add status lines.
"""
    return get_answer(prompt.strip(), provider=provider)
