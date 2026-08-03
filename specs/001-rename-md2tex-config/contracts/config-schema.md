# Interface Contract: md2tex Configuration YAML Schema

**Feature**: `001-rename-md2tex-config`  
**Date**: 2026-08-03  
**Spec**: [spec.md](file:///home/mlalbuquerque/Dropbox/Netra/projetos/md2tex/app/specs/001-rename-md2tex-config/spec.md)

## User Configuration File (`~/.config/md2tex/config.yaml`)

### Full Example Specification

```yaml
# md2tex Configuration File
# Location: ~/.config/md2tex/config.yaml

document_class: article
class_options:
  - 11pt
  - a4paper

# List of .sty style packages or local .sty file paths to include in the preamble
style_packages:
  - graphicx
  - hyperref
  - geometry

# Page geometry options passed to \geometry{}
page_geometry:
  margin: 2.5cm
  top: 3cm
  bottom: 3cm

# Typography and language options
typography:
  language: portuguese
  fontsize: 11pt

# Direct preamble code additions
preamble_includes:
  - '\setlength{\parindent}{0pt}'
  - '\setlength{\parskip}{6pt}'

# Compiler engine default
compiler_options:
  engine: pdflatex
```

### Schema Validation Rules

1. `document_class`: Must be a valid non-empty string.
2. `style_packages`: List of strings representing LaTeX package names or `.sty` relative/absolute paths.
3. `preamble_includes`: List of strings representing raw TeX statements.
4. `compiler_options.engine`: Must be one of `["pdflatex", "xelatex", "lualatex"]`.
