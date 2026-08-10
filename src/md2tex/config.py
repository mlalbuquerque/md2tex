from __future__ import annotations

import re
import sys
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml

from md2tex.errors import ConfigError
from md2tex.models import UserConfig

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "md2tex" / "config.yaml"
REQUIRED_KEYS = {
    "document_class",
    "class_options",
    "style_packages",
    "page_geometry",
    "typography",
    "preamble_includes",
    "compiler_options",
    "tables",
}
TYPOGRAPHY_KEYS = {"language", "fontsize", "mainfont", "line_spacing"}
TABLE_KEYS = {"landscape", "font", "width", "borders", "zebra"}
TABLE_CHOICES = {
    "landscape": {"auto", "always", "never"},
    "font": {"normalsize", "small", "footnotesize", "scriptsize"},
    "width": {"auto", "equal", "natural"},
    "borders": {"none", "outer", "grid"},
}
ENGINES = {"pdflatex", "xelatex", "lualatex"}
PACKAGE_IMPORT_RE = re.compile(r"\\(?:RequirePackage|usepackage)(?:\[([^]]*)\])?\{([^}]+)\}")


def _config_error(path: Path, message: str) -> ConfigError:
    return ConfigError(f"Configuração inválida em '{path}': {message}")


def _require_string(path: Path, data: dict[str, Any], key: str) -> str:
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        raise _config_error(path, f"'{key}' deve ser uma string não vazia.")
    return value


def _require_string_list(path: Path, data: dict[str, Any], key: str) -> list[str]:
    value = data[key]
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise _config_error(path, f"'{key}' deve ser uma lista de strings não vazias.")
    return value


def _require_string_map(path: Path, data: dict[str, Any], key: str) -> dict[str, str]:
    value = data[key]
    if not isinstance(value, dict) or any(
        not isinstance(map_key, str) or not isinstance(map_value, str)
        for map_key, map_value in value.items()
    ):
        raise _config_error(path, f"'{key}' deve ser um mapa de strings.")
    return value


def load_config(config_path: Path | None = None) -> UserConfig:
    """Carrega e valida a configuração explícita do usuário."""
    resolved_path = config_path.expanduser().resolve() if config_path else DEFAULT_CONFIG_PATH
    if not resolved_path.exists():
        raise ConfigError(
            f"Arquivo de configuração não encontrado em: '{resolved_path}'.\n"
            "Execute 'md2tex init' para criar o modelo ou especifique um caminho com --config."
        )
    try:
        data = yaml.safe_load(resolved_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = f" (linha {mark.line + 1})" if mark else ""
        raise ConfigError(f"Erro de sintaxe no arquivo de configuração '{resolved_path}'{line}: {exc}") from exc
    except OSError as exc:
        raise ConfigError(f"Falha ao ler arquivo de configuração '{resolved_path}': {exc}") from exc

    if not isinstance(data, dict):
        raise _config_error(resolved_path, "o conteúdo deve ser um mapa YAML.")
    unknown = set(data) - REQUIRED_KEYS
    missing = REQUIRED_KEYS - set(data)
    if unknown:
        raise _config_error(resolved_path, "chave(s) desconhecida(s): " + ", ".join(sorted(unknown)) + ".")
    if missing:
        raise _config_error(resolved_path, "chave(s) obrigatória(s) ausente(s): " + ", ".join(sorted(missing)) + ".")

    typography = _require_string_map(resolved_path, data, "typography")
    typography_unknown = set(typography) - TYPOGRAPHY_KEYS
    if typography_unknown:
        raise _config_error(resolved_path, "chave(s) de typography desconhecida(s): " + ", ".join(sorted(typography_unknown)) + ".")
    if "fontsize" not in typography:
        raise _config_error(resolved_path, "'typography.fontsize' é obrigatório.")

    compiler_options = _require_string_map(resolved_path, data, "compiler_options")
    if set(compiler_options) != {"engine"} or compiler_options["engine"] not in ENGINES:
        raise _config_error(resolved_path, "'compiler_options.engine' deve ser pdflatex, xelatex ou lualatex.")

    tables = data["tables"]
    if not isinstance(tables, dict) or set(tables) != TABLE_KEYS:
        raise _config_error(resolved_path, "'tables' deve conter landscape, font, width, borders e zebra.")
    for key, choices in TABLE_CHOICES.items():
        if tables.get(key) not in choices:
            raise _config_error(resolved_path, f"'tables.{key}' deve ser um de: " + ", ".join(sorted(choices)) + ".")
    if not isinstance(tables.get("zebra"), bool):
        raise _config_error(resolved_path, "'tables.zebra' deve ser true ou false.")

    user_config = UserConfig(
        document_class=_require_string(resolved_path, data, "document_class"),
        class_options=_require_string_list(resolved_path, data, "class_options"),
        style_packages=_require_string_list(resolved_path, data, "style_packages"),
        page_geometry=_require_string_map(resolved_path, data, "page_geometry"),
        typography=typography,
        preamble_includes=_require_string_list(resolved_path, data, "preamble_includes"),
        compiler_options=compiler_options,
        tables=tables,
    )
    validate_style_paths(user_config.style_packages, base_dir=resolved_path.parent)
    validate_style_configuration(user_config, base_dir=resolved_path.parent)
    return user_config


def initialize_config(config_path: Path | None = None, *, force: bool = False) -> Path:
    """Cria o arquivo de configuração inicial, sem sobrescrever por padrão."""
    target = config_path.expanduser().resolve() if config_path else DEFAULT_CONFIG_PATH
    if target.exists() and not force:
        raise ConfigError(f"A configuração já existe em '{target}'. Use 'md2tex init --force' para sobrescrevê-la.")
    target.parent.mkdir(parents=True, exist_ok=True)
    template = files("md2tex").joinpath("templates", "config.yaml").read_text(encoding="utf-8")
    target.write_text(template, encoding="utf-8")
    return target


def validate_style_paths(style_packages: list[str], base_dir: Path | None = None) -> list[str]:
    """Avisa quando um pacote de estilo local não puder ser localizado."""
    warnings: list[str] = []
    for pkg in style_packages:
        if pkg.endswith(".sty") or "/" in pkg or "\\" in pkg:
            candidate = Path(pkg)
            if not candidate.is_absolute() and base_dir:
                candidate = base_dir / candidate
            with_suffix = Path(str(candidate) + ".sty") if candidate.suffix != ".sty" else candidate
            if not (candidate.exists() or with_suffix.exists()):
                message = f"Aviso: Pacote de estilo local não encontrado: '{pkg}'"
                warnings.append(message)
                print(message, file=sys.stderr)
    return warnings


def _local_style_path(package: str, base_dir: Path | None) -> Path | None:
    """Resolve um pacote .sty local quando ele existe no sistema de arquivos."""
    if not (package.endswith(".sty") or "/" in package or "\\" in package):
        return None
    candidate = Path(package)
    if not candidate.is_absolute() and base_dir:
        candidate = base_dir / candidate
    if candidate.suffix != ".sty":
        candidate = Path(str(candidate) + ".sty")
    return candidate if candidate.is_file() else None


def available_style_packages(style_packages: list[str], base_dir: Path | None = None) -> set[str]:
    """Retorna pacotes declarados diretamente ou importados por .sty locais."""
    packages = {
        Path(package).stem if package.endswith(".sty") else package
        for package in style_packages
    }
    for package in style_packages:
        style_path = _local_style_path(package, base_dir)
        if style_path is None:
            continue
        packages.update(
            name.strip()
            for _, names in PACKAGE_IMPORT_RE.findall(style_path.read_text(encoding="utf-8", errors="replace"))
            for name in names.split(",")
        )
    return packages


def validate_style_configuration(user_config: UserConfig, base_dir: Path | None = None) -> None:
    """Detecta conflitos previsíveis entre um .sty local e o YAML do md2tex."""
    configured_packages = {
        Path(package).stem if package.endswith(".sty") else package
        for package in user_config.style_packages
    }
    for package in user_config.style_packages:
        style_path = _local_style_path(package, base_dir)
        if style_path is None:
            continue
        imports = [(options or "", name.strip()) for options, names in PACKAGE_IMPORT_RE.findall(style_path.read_text(encoding="utf-8", errors="replace")) for name in names.split(",")]
        imported_names = {name for _, name in imports}
        if "geometry" in imported_names and user_config.page_geometry:
            raise ConfigError(
                f"Conflito de configuração: '{style_path.name}' já carrega o pacote geometry. "
                "Defina 'page_geometry: {}' no config.yaml e deixe as margens sob responsabilidade do .sty, "
                "ou remova geometry do .sty para que o md2tex aplique page_geometry."
            )
        conflicting_options = sorted(
            name for options, name in imports
            if options and name in configured_packages and name != "geometry"
        )
        if conflicting_options:
            packages = ", ".join(conflicting_options)
            raise ConfigError(
                f"Conflito de configuração: '{style_path.name}' já carrega {packages} com opções próprias. "
                f"Remova {packages} de style_packages ou retire as opções do .sty."
            )
