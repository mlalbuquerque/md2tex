# Implementation Plan: Renaming to md2tex and Generic Style Configuration

**Branch**: `001-rename-md2tex-config` | **Date**: 2026-08-03 | **Spec**: [spec.md](file:///home/mlalbuquerque/Dropbox/Netra/projetos/md2tex/app/specs/001-rename-md2tex-config/spec.md)

**Input**: Feature specification from `specs/001-rename-md2tex-config/spec.md`

## Summary

Rename system entrypoints, package directories, and metadata from `netra-md2tex` / `netra_md2tex` to `md2tex`. Decouple all Netra-specific template headers, logos, and defaults. Implement user-level configuration loading from `~/.config/md2tex/config.yaml` using PyYAML for custom `.sty` package imports, document classes, page geometry, and typography without hardcoded code fallbacks.

## Technical Context

**Language/Version**: Python >= 3.10  
**Primary Dependencies**: `click>=8.1`, `Jinja2>=3.1`, `PyYAML>=6.0`  
**Storage**: User YAML Configuration file (`~/.config/md2tex/config.yaml`)  
**Testing**: `pytest>=8.0`, `pytest-cov>=5.0`  
**Target Platform**: Linux / macOS / Windows CLI  
**Project Type**: CLI tool & Python library  
**Performance Goals**: < 1s conversion execution time for standard Markdown documents  
**Constraints**: Zero hardcoded code defaults; require valid user configuration file or `--config` flag  
**Scale/Scope**: Single package rename, template refactoring, configuration module addition

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Library & CLI First**: `md2tex` exposes core conversion as a clean Python library and Click CLI command. *(PASS)*
- **Generic / Uncoupled Design**: Eliminates domain/company-specific branding and uses user configuration for all document defaults. *(PASS)*
- **Testable Architecture**: Isolated configuration loader, template engine, and CLI parameter resolver. *(PASS)*

## Project Structure

### Documentation (this feature)

```text
specs/001-rename-md2tex-config/
├── spec.md              # Feature specification
├── plan.md              # Implementation Plan (this file)
├── research.md          # Phase 0 Research findings
├── data-model.md        # Phase 1 Data Model & Schemas
├── quickstart.md        # Phase 1 Quickstart Validation Guide
├── contracts/           # Phase 1 Interface contracts
│   ├── cli.md
│   └── config-schema.md
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
src/
└── md2tex/              # Renamed from netra_md2tex
    ├── __init__.py
    ├── __main__.py
    ├── cli.py           # Updated click commands and CLI entrypoint
    ├── config.py        # New configuration loader (YAML parser & validator)
    ├── converter.py     # Core conversion logic using UserConfig
    ├── compiler.py      # LaTeX to PDF compilation
    ├── errors.py        # Application exceptions
    ├── frontmatter.py   # YAML frontmatter parser
    ├── mermaid.py       # Mermaid diagram filter
    ├── metadata.py      # Document metadata handler
    ├── models.py        # Data models
    ├── pandoc.py       # Pandoc wrapper
    ├── templates.py     # Jinja2 template loader
    ├── templates/       # Generic LaTeX Jinja2 templates (decoupled from Netra)
    ├── filters/         # Lua filters for Pandoc
    ├── utils.py         # Utility functions
    ├── setup.py         # Interactive dependency checker and installer (LaTeX, Mermaid)
    └── validator.py     # Document validator

.github/
└── workflows/
    └── ci.yml           # GitHub Actions CI/CD matrix (Linux, macOS, Windows) and PyInstaller release build

tests/
├── test_cli.py
├── test_config.py      # Tests for user config loading & error handling
├── test_compiler.py
├── test_converter.py
├── test_frontmatter.py
├── test_integration.py
├── test_utils.py
└── test_validator.py
```

**Structure Decision**: Single Python project structure with source code under `src/md2tex`, GitHub Actions workflow under `.github/workflows/`, and tests under `tests/`.

## Complexity Tracking

> No constitution violations. Architecture remains minimal, modular, and maintainable.
