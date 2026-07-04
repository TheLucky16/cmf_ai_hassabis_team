import re, sys
from pathlib import Path
from functions import mentor, student
from functions.helpers import get_status, read_json, read_text, save_dialogue, save_state, split_lessons

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"
OUTPUTS = ROOT / "outputs"


def new_state():
    return {
        "turn": 0,
        "lesson_index": 0,
        "lesson_started": False,
        "next_speaker": "Mentor",
        "course_complete": False,
        "student_notes": "",
        "bluff_lessons": [3, 7],
        "used_bluff_lessons": [],
        "last_mentor_status": "",
        "history": [],
    }


def save_outputs(state):
    save_dialogue(state["history"], OUTPUTS / "dialogue.md")
    save_state(state, OUTPUTS / "state.json")


def add_turn(state, message):
    state["turn"] += 1
    message = {"turn": state["turn"], **message}
    state["history"].append(message)
    return message


def update_after_mentor(state, message, total_lessons):
    status = get_status(message["text"])
    state["last_mentor_status"] = status

    if "course complete" in status:
        state["course_complete"] = True
        state["next_speaker"] = "Mentor"
        return

    if "advance" in status:
        match = re.search(r"lesson\s+(\d+)", status)
        next_number = int(match.group(1)) if match else state["lesson_index"] + 2
        state["lesson_index"] = min(next_number - 1, total_lessons - 1)
        state["lesson_started"] = False
        state["next_speaker"] = "Mentor"
        return

    if message["action"] == "teach":
        state["lesson_started"] = True
    state["next_speaker"] = "Student"


def update_after_student(state, lesson, message):
    if message.get("bluff"):
        used = state.setdefault("used_bluff_lessons", [])
        if lesson["number"] not in used:
            used.append(lesson["number"])

    if message["action"] in ["learn", "take_test"]:
        text = re.sub(r"\s+", " ", message["text"]).strip()
        note = f"Lesson {lesson['number']} {message['action']}: {text[:240]}"
        notes = [line for line in state.get("student_notes", "").splitlines() if line.strip()]
        notes.append(note)
        state["student_notes"] = "\n".join(notes[-12:])

    state["next_speaker"] = "Mentor"


def load_state(resume):
    path = OUTPUTS / "state.json"
    if resume and path.exists():
        return read_json(path)
    return new_state()


def run(max_turns=80, resume=False):
    mentor_prompt = read_text(INPUTS / "mentor_prompt.txt")
    student_prompt = read_text(INPUTS / "student_prompt.txt")
    lessons = split_lessons(read_text(INPUTS / "lessons.md"))
    state = load_state(resume)
    save_outputs(state)

    while not state["course_complete"] and state["turn"] < max_turns:
        lesson = lessons[state["lesson_index"]]

        if state["next_speaker"] == "Mentor":
            message = mentor.reply(mentor_prompt, lesson, state, total_lessons=len(lessons))
            add_turn(state, message)
            update_after_mentor(state, message, len(lessons))
        else:
            message = student.reply(student_prompt, lesson, state)
            add_turn(state, message)
            update_after_student(state, lesson, message)

        save_outputs(state)
        print(f"Turn {state['turn']}: {message['speaker']} / {message['action']}")

    if not state["course_complete"]:
        print(f"Stopped after {max_turns} turns before course completion.")
    print(f"Dialogue: {OUTPUTS / 'dialogue.md'}")
    print(f"State: {OUTPUTS / 'state.json'}")
    return state


if __name__ == "__main__":
    run(resume="--resume" in sys.argv)
