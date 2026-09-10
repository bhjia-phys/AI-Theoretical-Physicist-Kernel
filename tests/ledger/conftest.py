"""Installed Skill distribution coverage, not a claim of model conformance."""
from pathlib import Path
import re

import pytest


@pytest.fixture
def using_aitp_guidance() -> str:
    root = Path(__file__).resolve().parents[2] / "plugins/aitp-research-protocol/skills/using-aitp"
    main = (root / "SKILL.md").read_text(encoding="utf-8")
    linked = re.findall(r"\]\((references/[^)#]+\.md)\)", main)
    assert linked, "Detailed rules must be reachable from the shipped entrypoint"
    return main + "\n" + "\n".join(
        (root / name).read_text(encoding="utf-8") for name in dict.fromkeys(linked)
    )
