"""main.py — run the 3-agent pipeline end to end.

Each agent is a standalone script that reads the previous agent's output file
and writes its own. main.py runs them in order and validates the handoff file
after every step, so a bad stage stops the pipeline instead of silently
cascading into the next one.

    python main.py

Agents 1 and 2 choose their own input (URL / prompt files) internally — see
their source. Final result lands in outputs/agent_3_output.json.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (script, output it must produce, how to validate that output)
STEPS = [
    ("agent_1.py", "outputs/agent_1_output.md", "nonempty"),
    ("agent_2.py", "outputs/agent_2_output.json", "json_list"),
    ("agent_3.py", "outputs/agent_3_output.json", "json_list"),
]


def validate(path: Path, kind: str):
    """Return an error string if `path` is a bad handoff file, else None."""
    if not path.exists() or path.stat().st_size == 0:
        return "missing or empty"
    if kind == "json_list":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return f"not valid JSON ({exc})"
        if not isinstance(data, list) or not data:
            return "not a non-empty JSON list"
    return None


def run():
    for script, output, kind in STEPS:
        print(f"\n=== {script} ===")
        if subprocess.run([sys.executable, script], cwd=ROOT).returncode != 0:
            sys.exit(f"{script} failed. Pipeline stopped.")
        problem = validate(ROOT / output, kind)
        if problem:
            sys.exit(f"Validation failed after {script}: {output} {problem}")
        print(f"OK  {script} -> {output}")
    print("\nDone. Final output: outputs/agent_3_output.json")


if __name__ == "__main__":
    run()
