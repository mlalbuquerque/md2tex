# Quickstart Validation Guide: md2tex

**Feature**: `001-rename-md2tex-config`  
**Date**: 2026-08-03  
**Spec**: [spec.md](file:///home/mlalbuquerque/Dropbox/Netra/projetos/md2tex/app/specs/001-rename-md2tex-config/spec.md)

## Validation Scenarios

### Scenario 1: Verify System Renaming and Package Execution

1. Check installed CLI entrypoint:
   ```bash
   md2tex --help
   ```
2. **Expected Result**: CLI help identifies application as `md2tex`, displaying options for input, output, configuration, and style packages.

---

### Scenario 2: Create User Configuration and Convert Markdown to LaTeX

1. Ensure the user configuration directory exists:
   ```bash
   mkdir -p ~/.config/md2tex
   ```
2. Create `~/.config/md2tex/config.yaml` with custom style settings:
   ```yaml
   document_class: article
   class_options:
     - 12pt
     - a4paper
   style_packages:
     - hyperref
     - graphicx
   preamble_includes:
     - '\setlength{\parindent}{0pt}'
   ```
3. Create a test Markdown file `sample.md`:
   ```markdown
   # Hello md2tex

   This is a generic document converted using **md2tex**.
   ```
4. Execute conversion:
   ```bash
   md2tex sample.md -o sample.tex
   ```
5. **Expected Result**: `sample.tex` is generated containing `\documentclass[12pt,a4paper]{article}`, `\usepackage{hyperref}`, `\usepackage{graphicx}`, and `\setlength{\parindent}{0pt}` without any Netra-specific macros or headers.

---

### Scenario 3: Verify Missing Configuration File Warning

1. Temporarily move or point to a non-existent configuration path:
   ```bash
   md2tex sample.md -c /tmp/nonexistent.yaml
   ```
2. **Expected Result**: Execution halts with exit code 1 and outputs a descriptive message: `Error: Configuration file not found at /tmp/nonexistent.yaml. Please create a valid md2tex configuration file.`

---

### Scenario 4: CLI Flag Override

1. Execute conversion with explicit CLI engine/style flags:
   ```bash
   md2tex sample.md -s extra_custom.sty -o sample_override.tex
   ```
2. **Expected Result**: `sample_override.tex` contains `\usepackage{extra_custom}` added to the preamble alongside packages from `config.yaml`.
