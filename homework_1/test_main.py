"""Self-check for main.validate — the only non-trivial logic in the orchestrator."""

import json
import tempfile
from pathlib import Path

from main import validate


def test_validate():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)

        assert validate(d / "nope.txt", "nonempty")            # missing
        (d / "empty").write_text(""); assert validate(d / "empty", "nonempty")
        (d / "ok.md").write_text("x"); assert validate(d / "ok.md", "nonempty") is None

        (d / "bad.json").write_text("nope"); assert validate(d / "bad.json", "json_list")
        (d / "e.json").write_text("[]"); assert validate(d / "e.json", "json_list")
        (d / "obj.json").write_text("{}"); assert validate(d / "obj.json", "json_list")
        (d / "g.json").write_text(json.dumps([{"a": 1}]))
        assert validate(d / "g.json", "json_list") is None

    print("ok")


if __name__ == "__main__":
    test_validate()
