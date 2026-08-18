"""Carregamento seguro de regras de tópicos por perfil documental."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import yaml

from .errors import ConfigError
from .profiles import PROFILES

DEFAULT_RULES_PATH = Path.home() / ".config" / "md2tex" / "rules.yaml"


def _error(path: Path, message: str) -> ConfigError:
    return ConfigError(f"Regras inválidas em '{path}': {message}")


def resolve_rules_path(rules_path: Path | None = None) -> Path:
    """Resolve o caminho explícito ou a localização padrão das regras."""
    return (rules_path or DEFAULT_RULES_PATH).expanduser().resolve()


def load_rules(rules_path: Path | None = None) -> dict[str, list[str]]:
    """Carrega regras estritas; a ausência do arquivo padrão não é um erro."""
    target = resolve_rules_path(rules_path)
    explicit = rules_path is not None
    if not target.exists():
        if explicit:
            raise ConfigError(f"Arquivo de regras não encontrado em: '{target}'.")
        return {}
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = f" (linha {mark.line + 1})" if mark else ""
        raise ConfigError(f"Erro de sintaxe no arquivo de regras '{target}'{line}: {exc}") from exc
    except OSError as exc:
        raise ConfigError(f"Falha ao ler arquivo de regras '{target}': {exc}") from exc

    if not isinstance(data, dict) or set(data) != {"rules"}:
        raise _error(target, "a única chave de topo permitida é 'rules'.")
    rules = data["rules"]
    if not isinstance(rules, dict):
        raise _error(target, "'rules' deve ser um mapa de perfis para listas de tópicos.")

    validated: dict[str, list[str]] = {}
    for profile, topics in rules.items():
        if not isinstance(profile, str) or profile not in PROFILES:
            raise _error(target, f"perfil desconhecido: {profile!r}.")
        if not isinstance(topics, list):
            raise _error(target, f"'rules.{profile}' deve ser uma lista de strings não vazias.")
        normalized: set[str] = set()
        validated_topics: list[str] = []
        for topic in topics:
            if not isinstance(topic, str) or not topic.strip():
                raise _error(target, f"'rules.{profile}' deve conter apenas strings não vazias.")
            display = topic.strip()
            key = display.casefold()
            if key in normalized:
                raise _error(target, f"'rules.{profile}' contém tópico duplicado: {display!r}.")
            normalized.add(key)
            validated_topics.append(display)
        validated[profile] = validated_topics
    return validated


def initialize_rules(rules_path: Path | None = None, *, force: bool = False) -> Path:
    """Cria o modelo comentado de regras sem sobrescrever por padrão."""
    target = resolve_rules_path(rules_path)
    if target.exists() and not force:
        raise ConfigError(
            f"O arquivo de regras já existe em '{target}'. Use 'md2tex rules init --force' para sobrescrevê-lo."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    template = files("md2tex").joinpath("templates", "rules.yaml").read_text(encoding="utf-8")
    target.write_text(template, encoding="utf-8")
    return target
