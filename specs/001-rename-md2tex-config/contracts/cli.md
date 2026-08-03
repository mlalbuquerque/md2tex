# Interface Contract: md2tex CLI Command Schema

**Feature**: `001-rename-md2tex-config`  
**Date**: 2026-08-03  
**Spec**: [spec.md](file:///home/mlalbuquerque/Dropbox/Netra/projetos/md2tex/app/specs/001-rename-md2tex-config/spec.md)

## Command Line Interface (`md2tex`)

### Synopsis

```bash
md2tex [OPTIONS] INPUT_FILE
```

### Options

| Flag | Short | Type | Description |
|---|---|---|---|
| `--output` | `-o` | `PATH` | Path to destination file (`.tex` or `.pdf`). Defaults to `INPUT_FILE` with `.tex` extension. |
| `--config` | `-c` | `PATH` | Path to custom YAML configuration file. Defaults to `~/.config/md2tex/config.yaml`. |
| `--style` | `-s` | `TEXT` | Additional `.sty` package to include (can be specified multiple times). |
| `--engine` | `-e` | `CHOICE` | TeX compiler engine (`pdflatex`, `xelatex`, `lualatex`). |
| `--pdf` | | `FLAG` | Compile generated `.tex` file directly to `.pdf`. |
| `--version` | `-v` | `FLAG` | Show version and exit. |
| `--help` | `-h` | `FLAG` | Show help message and exit. |

### Exit Codes

- `0`: Successful conversion.
- `1`: Missing configuration file or malformed configuration YAML.
- `2`: Invalid input file or filesystem error.
- `3`: TeX compilation failure (when `--pdf` is active).

### Examples

```bash
# Convert Markdown to LaTeX using user config (~/.config/md2tex/config.yaml)
md2tex document.md -o document.tex

# Convert Markdown to PDF with custom config file
md2tex document.md -c ./my_project_config.yaml --pdf

# Override style package via CLI
md2tex document.md -s extra_style.sty -o document.tex
```
