from __future__ import annotations

PROFILES = {
    "default": {
        "label": "Documento Padrão",
        "template": "base.tex.j2",
    },
    "report": {
        "label": "Relatório",
        "template": "report.tex.j2",
    },
    "meeting-minutes": {
        "label": "Memória de Reunião",
        "template": "meeting-minutes.tex.j2",
    },
    "adr": {
        "label": "Registro de Decisão Arquitetural (ADR)",
        "template": "adr.tex.j2",
    },
    "technical-plan": {
        "label": "Plano Técnico",
        "template": "technical-plan.tex.j2",
    },
}


def get_profile(name: str) -> dict[str, str]:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Perfil desconhecido: {name}") from exc
