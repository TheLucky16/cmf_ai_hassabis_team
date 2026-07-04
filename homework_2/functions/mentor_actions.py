from functions.helpers import format_history, get_answer


def teach(mentor_prompt, lesson, history, provider=None):
    prompt = f"""
{mentor_prompt}

Action: Teach the current lesson.

Current lesson:
{lesson["title"]}

{lesson["body"]}

Recent dialogue:
{format_history(history)}

Instructions:
- Teach only this lesson.
- Explain the skill briefly.
- Give one small practice task the Student can answer in conversation.
- Do not test or advance yet.
- End with: STATUS: continue lesson {lesson["number"]}
"""
    return get_answer(prompt.strip(), provider=provider)


def answer_question(mentor_prompt, lesson, history, provider=None):
    prompt = f"""
{mentor_prompt}

Action: Answer the Student's question.

Current lesson:
{lesson["title"]}

{lesson["body"]}

Recent dialogue:
{format_history(history)}

Instructions:
- Answer the latest Student question directly.
- Keep it short and useful.
- Connect the answer back to the current practice task.
- Do not advance the lesson.
- End with: STATUS: continue lesson {lesson["number"]}
"""
    return get_answer(prompt.strip(), provider=provider)


def test(mentor_prompt, lesson, history, total_lessons=10, provider=None):
    next_status = "STATUS: course complete" if lesson["number"] >= total_lessons else f"STATUS: advance to lesson {lesson['number'] + 1}"
    prompt = f"""
{mentor_prompt}

Action: Test whether the Student truly applied the skill.

Current lesson:
{lesson["title"]}

{lesson["body"]}

Recent dialogue:
{format_history(history)}

Instructions:
- Judge the Student's latest answer as evidence of application, not just recall.
- Look for concrete steps, specific results, mistakes, surprises, or a transfer attempt.
- If the answer is vague, too smooth, contradictory, or sounds like bluffing, challenge it.
- If evidence is weak, ask one sharper follow-up or give a smaller task.
- If evidence is strong, briefly say why and advance.
- Use exactly one final status line:
  - STATUS: continue lesson {lesson["number"]}
  - {next_status}
"""
    return get_answer(prompt.strip(), provider=provider)
