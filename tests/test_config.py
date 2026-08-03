from pathlib import Path
import pytest

from md2tex.config import load_config, validate_style_paths
from md2tex.errors import ConfigError


def test_load_config_missing_raises_config_error(tmp_path: Path):
    missing_config = tmp_path / "nonexistent.yaml"
    with pytest.raises(ConfigError) as exc_info:
        load_config(missing_config)
    assert "Arquivo de configuração não encontrado" in str(exc_info.value)


def test_load_config_valid_yaml(tmp_path: Path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
document_class: report
class_options:
  - 12pt
  - a4paper
style_packages:
  - graphicx
  - hyperref
page_geometry:
  margin: 2cm
compiler_options:
  engine: xelatex
""",
        encoding="utf-8",
    )
    user_config = load_config(config_file)
    assert user_config.document_class == "report"
    assert user_config.class_options == ["12pt", "a4paper"]
    assert "graphicx" in user_config.style_packages
    assert user_config.page_geometry == {"margin": "2cm"}
    assert user_config.compiler_options.get("engine") == "xelatex"


def test_load_config_malformed_yaml(tmp_path: Path):
    config_file = tmp_path / "bad.yaml"
    config_file.write_text("document_class: [unclosed list", encoding="utf-8")
    with pytest.raises(ConfigError) as exc_info:
        load_config(config_file)
    assert "Erro de sintaxe" in str(exc_info.value)


def test_validate_style_paths_missing_local_file(tmp_path: Path):
    warnings = validate_style_paths(["nonexistent_style.sty"], base_dir=tmp_path)
    assert len(warnings) == 1
    assert "nonexistent_style.sty" in warnings[0]
