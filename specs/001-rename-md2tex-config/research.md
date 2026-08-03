# Phase 0 Research: Renaming to md2tex and Generic Style Configuration

**Feature**: `001-rename-md2tex-config`  
**Date**: 2026-08-03  
**Spec**: [spec.md](file:///home/mlalbuquerque/Dropbox/Netra/projetos/md2tex/app/specs/001-rename-md2tex-config/spec.md)

## Research Findings & Architectural Decisions

### 1. Package Renaming Strategy (`netra_md2tex` → `md2tex`)

- **Decision**: Rename the Python package directory `src/netra_md2tex` to `src/md2tex` and update `pyproject.toml` entry points (`md2tex = "md2tex.cli:main"`).
- **Rationale**: Clean package structure matching the new project identity `md2tex`. Eliminates all `netra_` namespace prefixes.
- **Alternatives Considered**:
  - *Keeping module internal name `netra_md2tex` with alias `md2tex`*: Rejected because it leaves lingering Netra references in code and package metadata.

### 2. User-Only Configuration File Resolution (`~/.config/md2tex/config.yaml`)

- **Decision**: Load configuration from `~/.config/md2tex/config.yaml` using `PyYAML` (already a project dependency). Allow overriding the configuration path via the `--config <path>` CLI option.
- **Rationale**: As clarified in spec session 2026-08-03, configuration resides strictly in the user's config directory (or custom `--config` path) with no hardcoded fallback defaults inside the codebase. If `~/.config/md2tex/config.yaml` is missing and no `--config` flag is passed, `md2tex` halts with a clear user notice asking the user to create `~/.config/md2tex/config.yaml`.
- **Alternatives Considered**:
  - *Cascading local/user/system configs with hardcoded code defaults*: Rejected per explicit user decision in specification clarification phase.

### 3. Decoupling Templates and Styling Options

- **Decision**: Refactor Jinja2 templates and LaTeX preamble generation logic in `src/md2tex/templates.py` and `src/md2tex/converter.py` so that LaTeX preamble macros, `.sty` package imports, document classes, margins, and typography are dynamically populated from the loaded YAML configuration object.
- **Rationale**: Removes all Netra-specific template headers, logos, macro definitions, and styling constants from the repository, making the conversion engine 100% generic and user-configurable.
- **Alternatives Considered**:
  - *Conditional Netra flag in template*: Rejected because the goal is full domain-agnostic generic operation.

### 4. CLI Argument Precedence Over Config File

- **Decision**: Click CLI parameters in `src/md2tex/cli.py` take precedence over values provided in `~/.config/md2tex/config.yaml`.
- **Rationale**: Standard CLI behavior allowing per-invocation overrides while defaulting to the user's `config.yaml` settings.
- **Alternatives Considered**:
  - *Config file overriding CLI arguments*: Rejected as counter-intuitive.
