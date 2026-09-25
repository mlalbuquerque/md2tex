# Quickstart: Perfil Documento de Arquitetura de Software

## Prerequisites

- Configuração válida criada com `md2tex init` (inclua os pacotes exigidos pelo estilo institucional no `config.yaml`).
- Python e dependências do md2tex instalados; Pandoc disponível para conversão. A compilação PDF é opcional e exige uma cadeia LaTeX externa.

## Example Input

Crie `arquitetura.md`:

```markdown
---
title: Arquitetura do Sistema Aurora
author: Ana Silva
date: 2026-09-25
version: "1.0"
client: Projeto Aurora
system-name: Sistema Aurora
revision-history:
  - date: 2026-09-25
    version: "1.0"
    description: Criação do documento
    author: Ana Silva
---

# Visão geral

Descrição da arquitetura.
```

## Generate TEX

```bash
md2tex arquitetura.md --type software-architecture --config ./config.yaml
```

Override the system name from the command line:

```bash
md2tex arquitetura.md --type software-architecture --system-name "Sistema Aurora 2" --config ./config.yaml
```

The expected output order is cover, a dedicated revision history page, optional TOC, then converted Markdown body. Omitting `system-name` leaves the cover field blank. Leading and trailing spaces are removed; a whitespace-only value is blank. A provided empty `--system-name` overrides a non-empty front matter value and leaves the cover field blank. Omitting `revision-history` still emits the page and an initial row using the document date, version and author.

To omit the TOC while keeping revision history:

```bash
md2tex arquitetura.md --type software-architecture --no-toc --config ./config.yaml
```

## Automated Validation

Run the full suite with the repository-local environment:

```bash
./.venv/bin/pytest -q
```

Coverage for the feature belongs in `tests/test_metadata.py`, `tests/test_cli.py`, `tests/test_rules.py` and `tests/test_integration.py`. Verify profile isolation, CLI precedence, absent/empty metadata, ordered table rows, LaTeX escaping and TOC/no-TOC output order.
