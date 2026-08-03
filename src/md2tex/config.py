from __future__ import annotations

from pathlib import Path
import sys
import yaml

from md2tex.errors import ConfigError
from md2tex.models import UserConfig

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "md2tex" / "config.yaml"


def load_config(config_path: Path | None = None) -> UserConfig:
    """Carrega o arquivo de configuração do usuário (~/.config/md2tex/config.yaml ou caminho customizado)."""
    resolved_path = config_path.expanduser().resolve() if config_path else DEFAULT_CONFIG_PATH

    if not resolved_path.exists():
        raise ConfigError(
            f"Arquivo de configuração não encontrado em: '{resolved_path}'.\n"
            "Crie o arquivo ~/.config/md2tex/config.yaml ou especifique um caminho com --config."
        )

    try:
        content = resolved_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"Erro de sintaxe no arquivo de configuração '{resolved_path}': {exc}") from exc
    except Exception as exc:
        raise ConfigError(f"Falha ao ler arquivo de configuração '{resolved_path}': {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigError(f"O conteúdo da configuração em '{resolved_path}' deve ser um dicionário YAML.")

    user_config = UserConfig(
        document_class=data.get("document_class", "article"),
        class_options=data.get("class_options", ["11pt", "a4paper"]),
        style_packages=data.get("style_packages", []),
        page_geometry=data.get("page_geometry", {}),
        typography=data.get("typography", {}),
        preamble_includes=data.get("preamble_includes", []),
        compiler_options=data.get("compiler_options", {"engine": "pdflatex"}),
    )

    validate_style_paths(user_config.style_packages, base_dir=resolved_path.parent)
    return user_config


def validate_style_paths(style_packages: list[str], base_dir: Path | None = None) -> list[str]:
    """Valida se pacotes .sty locais existem e emite avisos se não encontrados."""
    warnings: list[str] = []
    for pkg in style_packages:
        if pkg.endswith(".sty") or "/" in pkg or "\\" in pkg:
            p = Path(pkg)
            if not p.is_absolute() and base_dir:
                p = base_dir / p
            if not p.exists():
                msg = f"Aviso: Pacote de estilo local não encontrado: '{pkg}'"
                warnings.append(msg)
                print(msg, file=sys.stderr)
    return warnings
