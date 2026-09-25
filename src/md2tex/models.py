from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class DocumentRequirement:
    """Regra declarativa e orientada para um campo ou seção documental."""

    target: str
    label: str
    required: bool
    instruction: str
    example: str


@dataclass(slots=True)
class ProfileRequirements:
    """Requisitos configuráveis de um perfil documental."""

    fields: list[DocumentRequirement] = field(default_factory=list)
    sections: list[DocumentRequirement] = field(default_factory=list)


@dataclass(slots=True)
class UserConfig:
    """Configuração explícita do usuário, sem valores de estilo implícitos."""

    document_class: str
    class_options: list[str]
    style_packages: list[str]
    page_geometry: dict[str, str]
    typography: dict[str, str]
    preamble_includes: list[str]
    compiler_options: dict[str, str]
    tables: dict[str, str | bool]
    document_requirements: dict[str, ProfileRequirements] = field(default_factory=dict)


@dataclass(slots=True)
class DocumentMetadata:
    title: str
    author: str = ""
    date: str = ""
    version: str = "1.0"
    client: str = ""
    document_type: str = "Documento"
    subtitle: str = ""
    status: str = ""
    system_name: str = ""
    revision_history: list[RevisionEntry] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)
    meeting_minutes: MeetingMinutesData | None = None


@dataclass(slots=True)
class RevisionEntry:
    date: str = ""
    version: str = ""
    description: str = ""
    author: str = ""


@dataclass(slots=True)
class Participant:
    """Participante normalizado de uma memória de reunião."""

    name: str
    role: str
    group: str


@dataclass(slots=True)
class MeetingMinutesData:
    """Dados estruturados exclusivos do perfil ``meeting-minutes``."""

    period_start: str = ""
    period_end: str = ""
    client_participants: list[Participant] = field(default_factory=list)
    netra_participants: list[Participant] = field(default_factory=list)
    has_no_pending_items: bool = False


@dataclass(slots=True)
class ConversionOptions:
    input_path: Path
    output_path: Path
    config_path: Path | None = None
    rules_path: Path | None = None
    user_config: UserConfig | None = None
    profile: str = "default"
    figures_dir: Path = Path("figures")
    template_path: Path | None = None
    generate_pdf: bool = False
    validate: bool = True
    strict: bool = False
    toc: bool = True
    engine: str = ""
    mermaid: bool = True
    mermaid_format: str = "png"
    landscape_tables: str = "auto"
    table_font: str = ""
    table_width: str = ""
    table_borders: str = ""
    table_zebra: bool | None = None
    keep_build: bool = False
    force: bool = False
    verbose: bool = False
    title: str | None = None
    subtitle: str | None = None
    author: str | None = None
    date: str | None = None
    document_version: str | None = None
    client: str | None = None
    system_name: str | None = None
    shell_escape: bool = False
    clean: bool = False
    clean_all: bool = False


@dataclass(slots=True)
class ValidationMessage:
    level: str
    message: str
    source: str = ""


@dataclass(slots=True)
class ConversionResult:
    tex_path: Path
    pdf_path: Path | None
    messages: list[ValidationMessage]
    build_dir: Path | None = None
