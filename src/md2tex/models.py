from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class UserConfig:
    document_class: str = "article"
    class_options: list[str] = field(default_factory=lambda: ["11pt", "a4paper"])
    style_packages: list[str] = field(default_factory=list)
    page_geometry: dict[str, Any] = field(default_factory=dict)
    typography: dict[str, Any] = field(default_factory=dict)
    preamble_includes: list[str] = field(default_factory=list)
    compiler_options: dict[str, Any] = field(default_factory=lambda: {"engine": "pdflatex"})


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
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ConversionOptions:
    input_path: Path
    output_path: Path
    config_path: Path | None = None
    user_config: UserConfig | None = None
    profile: str = "default"
    style_path: str | None = None
    figures_dir: Path = Path("figures")
    template_path: Path | None = None
    generate_pdf: bool = False
    validate: bool = True
    strict: bool = False
    toc: bool = True
    engine: str = "pdflatex"
    mermaid: bool = True
    mermaid_format: str = "png"
    landscape_tables: str = "auto"
    table_font: str = "small"
    table_width: str = "auto"
    keep_build: bool = False
    force: bool = False
    verbose: bool = False
    title: str | None = None
    author: str | None = None
    date: str | None = None
    document_version: str | None = None
    client: str | None = None
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
