from importlib.resources import files
from pathlib import Path

import pytest

from md2tex.config import (
    initialize_config,
    load_config,
    validate_style_paths,
)
from md2tex.errors import ConfigError


def write_valid_config(path: Path) -> Path:
    path.write_text(files("md2tex").joinpath("templates", "config.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return path


def test_load_config_missing_raises_config_error(tmp_path: Path):
    with pytest.raises(ConfigError, match="md2tex init"):
        load_config(tmp_path / "nonexistent.yaml")


def test_load_config_valid_yaml(tmp_path: Path):
    user_config = load_config(write_valid_config(tmp_path / "config.yaml"))
    assert user_config.document_class == "article"
    assert user_config.typography["fontsize"] == "11pt"
    assert user_config.compiler_options["engine"] == "xelatex"


@pytest.mark.parametrize("content, expected", [
    ("document_class: article\n", "chave(s) obrigatória(s) ausente(s)"),
    ("unknown: value\n", "chave(s) desconhecida(s)"),
])
def test_load_config_rejects_incomplete_or_unknown_schema(tmp_path: Path, content: str, expected: str):
    config_file = tmp_path / "bad.yaml"
    config_file.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigError) as exc_info:
        load_config(config_file)
    assert expected in str(exc_info.value)


def test_load_config_malformed_yaml_reports_line(tmp_path: Path):
    config_file = tmp_path / "bad.yaml"
    config_file.write_text("document_class: [unclosed list", encoding="utf-8")
    with pytest.raises(ConfigError) as exc_info:
        load_config(config_file)
    assert "linha" in str(exc_info.value)


def test_initialize_config_does_not_overwrite_without_force(tmp_path: Path):
    target = tmp_path / "nested" / "config.yaml"
    assert initialize_config(target) == target.resolve()
    with pytest.raises(ConfigError, match="já existe"):
        initialize_config(target)
    initialize_config(target, force=True)
    assert load_config(target).document_class == "article"


def test_validate_style_paths_missing_local_file(tmp_path: Path):
    warnings = validate_style_paths(["nonexistent_style.sty"], base_dir=tmp_path)
    assert len(warnings) == 1
    assert "nonexistent_style.sty" in warnings[0]


def test_local_style_that_owns_geometry_requires_empty_page_geometry(tmp_path: Path):
    config_path = write_valid_config(tmp_path / "config.yaml")
    style_path = tmp_path / "letterhead.sty"
    style_path.write_text(r"\RequirePackage[margin=2cm]{geometry}", encoding="utf-8")
    content = config_path.read_text(encoding="utf-8").replace("style_packages:\n", f"style_packages:\n  - {style_path}\n")
    config_path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigError, match=r"page_geometry: \{\}"):
        load_config(config_path)


def test_local_style_with_package_options_reports_duplicate_package(tmp_path: Path):
    config_path = write_valid_config(tmp_path / "config.yaml")
    style_path = tmp_path / "letterhead.sty"
    style_path.write_text(r"\RequirePackage[table]{xcolor}", encoding="utf-8")
    content = config_path.read_text(encoding="utf-8").replace("style_packages:\n", f"style_packages:\n  - {style_path}\n")
    config_path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigError, match="Remova xcolor"):
        load_config(config_path)


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        ("engine: xelatex", "engine: invalid", "compiler_options.engine"),
        ("zebra: false", "zebra: maybe", "tables.zebra"),
        ("font: small", "font: huge", "tables.font"),
        ("class_options:\n  - a4paper", "class_options: a4paper", "class_options"),
    ],
)
def test_load_config_rejects_invalid_value_types_and_choices(
    tmp_path: Path, old: str, new: str, expected: str
):
    config_file = write_valid_config(tmp_path / "invalid.yaml")
    content = config_file.read_text(encoding="utf-8").replace(old, new)
    config_file.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigError, match=expected):
        load_config(config_file)
