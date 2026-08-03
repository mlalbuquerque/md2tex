# Phase 1 Data Model: Renaming to md2tex and Generic Style Configuration

**Feature**: `001-rename-md2tex-config`  
**Date**: 2026-08-03  
**Spec**: [spec.md](file:///home/mlalbuquerque/Dropbox/Netra/projetos/md2tex/app/specs/001-rename-md2tex-config/spec.md)

## Data Entities & Configuration Schemas

### 1. User Configuration Profile (`UserConfig`)

Represents the structure loaded from `~/.config/md2tex/config.yaml` or a path specified by `--config`.

| Field Name | Type | Description | Required | Default in Schema |
|---|---|---|---|---|
| `document_class` | `str` | LaTeX document class (e.g. `article`, `report`, `book`) | Yes | `article` |
| `class_options` | `list[str]` | Class parameters (e.g. `["11pt", "a4paper"]`) | No | `["11pt", "a4paper"]` |
| `style_packages` | `list[str]` | List of `.sty` package names or file paths | No | `[]` |
| `page_geometry` | `dict` | Page geometry settings (e.g. `{"margin": "2.5cm"}`) | No | `{}` |
| `typography` | `dict` | Font family, line spacing, and language settings | No | `{}` |
| `preamble_includes` | `list[str]` | Raw LaTeX preamble lines / code snippets | No | `[]` |
| `compiler_options` | `dict` | Options for TeX compiler (`engine`: `pdflatex`/`xelatex`/`lualatex`) | No | `{"engine": "pdflatex"}` |

#### YAML Schema Example (`~/.config/md2tex/config.yaml`):

```yaml
document_class: article
class_options:
  - 11pt
  - a4paper

style_packages:
  - graphicx
  - hyperref
  - custom_style.sty

page_geometry:
  margin: 2.5cm

typography:
  mainfont: Latin Modern Roman
  fontsize: 11pt

preamble_includes:
  - '\setlength{\parindent}{0pt}'
  - '\setlength{\parskip}{6pt}'

compiler_options:
  engine: pdflatex
```

---

### 2. Style Asset Reference (`StyleAsset`)

Represents a reference to a LaTeX `.sty` package or custom preamble include file.

| Field Name | Type | Description |
|---|---|---|
| `name_or_path` | `str` | Package name (e.g. `hyperref`) or file path (e.g. `./styles/custom.sty`) |
| `is_custom_file` | `bool` | True if referencing a local file path needing inclusion |
| `options` | `list[str]` | Optional package options for `\usepackage[options]{name}` |

---

### 3. Conversion Options (`ConversionOptions`)

Represents the merged runtime settings resolved after applying CLI flag overrides onto the loaded `UserConfig`.

| Field Name | Source Precedence | Description |
|---|---|---|
| `config_path` | CLI `--config` → `~/.config/md2tex/config.yaml` | Resolved path to configuration file |
| `output_path` | CLI `-o` / `--output` | Destination LaTeX / PDF path |
| `document_class` | CLI `--class` → `UserConfig.document_class` | LaTeX document class |
| `style_packages` | CLI `--style` + `UserConfig.style_packages` | Joined list of style packages |
| `compiler_engine` | CLI `--engine` → `UserConfig.compiler_options.engine` | TeX compilation engine |
