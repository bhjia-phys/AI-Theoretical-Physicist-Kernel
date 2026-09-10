from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from aitp.notes import NOTE_MODES
from aitp.records import AUTHORITIES, ENTRY_KINDS

REPO = Path(__file__).parents[2]
PLUGIN_ROOT = REPO / "plugins" / "aitp-research-protocol"
CONTRACT_PATH = PLUGIN_ROOT / "aitp.contract.json"
VENDOR = PLUGIN_ROOT / "scripts" / "vendor"

EXPECTED_COMMANDS = {
    "enter",
    "list",
    "show",
    "check",
    "record prepare",
    "record save",
    "note prepare",
    "note save",
    "backfill workstreams",
}


def run_cli(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(VENDOR)
    return subprocess.run(
        [sys.executable, "-m", "aitp", *args],
        cwd=repo,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load_contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def contract() -> dict[str, object]:
    return load_contract()


def test_contract_identity_matches_plugin(contract: dict[str, object]):
    assert contract["schema"] == "aitp/adapter-contract-0.3"
    assert contract["plugin"] == {
        "name": "aitp-research-protocol",
        "version": "0.10.0",
    }
    kimi_manifest = json.loads(
        (PLUGIN_ROOT / "kimi.plugin.json").read_text(encoding="utf-8")
    )
    assert kimi_manifest["version"] == contract["plugin"]["version"]
    codex_manifest = json.loads(
        (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    assert codex_manifest["version"].startswith(
        f"{contract['plugin']['version']}+"
    )


def test_contract_commands_are_the_model_surface(contract: dict[str, object]):
    commands = contract["commands"]
    assert isinstance(commands, dict)
    assert set(commands) == EXPECTED_COMMANDS
    for command, spec in commands.items():
        assert spec["tool"].startswith("aitp_")
        assert isinstance(spec["argv"], list) and spec["argv"]
        assert isinstance(spec["parameters"], list)
        assert spec["parameters"], command
        for parameter in spec["parameters"]:
            assert parameter["name"]
            assert parameter["type"] in {"string", "integer", "boolean", "enum", "array"}
            if parameter["type"] == "enum":
                assert isinstance(parameter["values"], list) and parameter["values"]


def test_hakimi_skill_read_routing_uses_native_tools_or_exact_skill_directory():
    manifest = json.loads((PLUGIN_ROOT / "kimi.plugin.json").read_text(encoding="utf-8"))
    guidance = manifest["skillInstructions"]
    for tool in ("aitp_enter", "aitp_list", "aitp_show", "aitp_check"):
        assert tool in guidance
    assert "do not also run their CLI equivalents" in guidance
    assert "dir attribute" in guidance
    assert "../../scripts/aitp.py" in guidance
    assert "not permission to bypass" in guidance
    assert "/skill:aitp" not in guidance
    for name in ("aitp", "using-aitp", "distilling-methods"):
        skill_dir = PLUGIN_ROOT / "skills" / name
        assert (skill_dir / "../../scripts/aitp.py").resolve() == PLUGIN_ROOT / "scripts/aitp.py"


def test_contract_flags_exist_in_cli_help(contract: dict[str, object]):
    for command, spec in contract["commands"].items():
        result = run_cli(REPO, *spec["argv"], "--help")
        assert result.returncode == 0, result.stderr
        help_text = result.stdout
        for parameter in spec["parameters"]:
            if "flag" not in parameter:
                continue
            assert parameter["flag"] in help_text, (command, parameter["flag"])
            if parameter["type"] == "enum":
                runtime_values = {
                    "entry-kind": ENTRY_KINDS,
                    "authority": AUTHORITIES,
                    "note-mode": NOTE_MODES,
                }.get(parameter["name"], None)
                if runtime_values is not None:
                    assert set(parameter["values"]) == runtime_values


def test_record_save_compare_and_save_parameters_are_a_pair(contract: dict[str, object]):
    description = contract["commands"]["record save"]["description"]
    assert "does not require a Research Action or checkpoint" in description
    assert "including direct records and checkpoint-bound records" in description
    parameters = {
        parameter["name"]: parameter
        for parameter in contract["commands"]["record save"]["parameters"]
    }
    assert parameters["expected_topic"] == {
        "name": "expected_topic",
        "type": "string",
        "required": False,
        "description": "Expected current Topic slug. Must be passed together with exact_workstream.",
        "flag": "--expected-topic",
        "paired_with": "exact_workstream",
    }
    assert parameters["exact_workstream"]["paired_with"] == "expected_topic"


def test_contract_skills_and_policy_paths_exist(contract: dict[str, object]):
    for skill in contract["skills"]:
        assert (PLUGIN_ROOT / skill["path"]).is_file()
    for policy in contract["semantic_policy_files"]:
        assert (REPO / policy).is_file()
    launcher = PLUGIN_ROOT / contract["python"]["launcher"]
    assert launcher.is_file()


def test_read_guidance_is_proportional_without_weakening_validation(contract: dict[str, object]):
    enter = contract["commands"]["enter"]["description"]
    check = contract["commands"]["check"]["description"]
    assert "Ordinary follow-up questions are not new session boundaries" in enter
    assert "not proof of absence" in enter
    assert "unrelated findings do not block independent research" in check
    assert "Always check after save" in check
    assert "Exit 2 does not establish verified memory" in check


def test_memory_guidance_is_reachable_from_the_installable_skill(contract: dict[str, object]):
    skill = next(item for item in contract["skills"] if item["name"] == "using-aitp")
    entrypoint = PLUGIN_ROOT / skill["path"]
    relative = "references/research-memory.md"
    assert f"]({relative})" in entrypoint.read_text(encoding="utf-8")
    assert (entrypoint.parent / relative).is_file()
    for name in ("enter", "note save"):
        assert f"using-aitp/{relative}" in contract["commands"][name]["description"]


def test_on_demand_guidance_links_survive_installation_layout(contract: dict[str, object]):
    """A shorter entrypoint must still route to readable rules, not dead links."""
    skill = PLUGIN_ROOT / "skills/using-aitp/SKILL.md"
    refs = skill.parent / "references"
    for path in [skill, *refs.glob("*.md")]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            destination = (path.parent / target.split("#", 1)[0]).resolve()
            assert destination.is_file(), (path, target)
    for relative, command in (("references/cli-contracts.md", "check"),
                              ("references/recording.md", "note save")):
        assert f"]({relative})" in skill.read_text(encoding="utf-8")
        assert f"using-aitp/{relative}" in contract["commands"][command]["description"]


def test_contract_transport_schemas_match_live_cli(
    tmp_path: Path, contract: dict[str, object]
):
    init = run_cli(
        tmp_path,
        "init",
        "--cwd",
        ".",
        "--topic",
        "contract",
        "--title",
        "Contract Test",
        "--json",
    )
    assert init.returncode == 0, init.stderr

    live = {
        "enter": json.loads(run_cli(tmp_path, "enter", "--cwd", ".", "--json").stdout),
        "list": json.loads(run_cli(tmp_path, "list", "--cwd", ".", "--json").stdout),
        "check": json.loads(run_cli(tmp_path, "check", "--cwd", ".", "--json").stdout),
    }
    assert live["enter"]["schema"] == contract["commands"]["enter"]["json_schemas"][0]
    assert live["list"]["schema"] == contract["commands"]["list"]["json_schemas"][0]
    assert live["check"]["schema"] == contract["commands"]["check"]["json_schemas"][0]

    scoped_enter = json.loads(
        run_cli(
            tmp_path, "enter", "--cwd", ".", "--workstream", "demo", "--json"
        ).stdout
    )
    scoped_list = json.loads(
        run_cli(tmp_path, "list", "--cwd", ".", "--workstream", "demo", "--json").stdout
    )
    scoped_check = json.loads(
        run_cli(tmp_path, "check", "--cwd", ".", "--workstream", "demo", "--json").stdout
    )
    assert scoped_enter["schema"] == contract["commands"]["enter"]["json_schemas"][1]
    assert scoped_list["schema"] == contract["commands"]["list"]["json_schemas"][1]
    assert scoped_check["schema"] == contract["commands"]["check"]["json_schemas"][1]
