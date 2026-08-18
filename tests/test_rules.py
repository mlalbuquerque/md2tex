from pathlib import Path

import pytest

from md2tex.errors import ConfigError
from md2tex.rules import initialize_rules, load_rules


def test_load_rules_accepts_known_profiles_and_normalizes_display(tmp_path: Path):
    path = tmp_path / "rules.yaml"
    path.write_text("rules:\n  adr:\n    - ' Decisão '\n", encoding="utf-8")
    assert load_rules(path) == {"adr": ["Decisão"]}


@pytest.mark.parametrize(
    "content",
    [
        "rules:\n  unknown:\n    - Topic\n",
        "rules:\n  adr: Topic\n",
        "rules:\n  adr:\n    - Topic\n    - topic\n",
        "other: {}\n",
    ],
)
def test_load_rules_rejects_invalid_schema(tmp_path: Path, content: str):
    path = tmp_path / "rules.yaml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigError):
        load_rules(path)


def test_load_rules_silently_ignores_missing_default(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("md2tex.rules.DEFAULT_RULES_PATH", tmp_path / "missing.yaml")
    assert load_rules() == {}


def test_initialize_rules_does_not_overwrite_without_force(tmp_path: Path):
    target = tmp_path / "nested" / "rules.yaml"
    assert initialize_rules(target) == target.resolve()
    original = target.read_bytes()
    with pytest.raises(ConfigError, match="já existe"):
        initialize_rules(target)
    assert target.read_bytes() == original
