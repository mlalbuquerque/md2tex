# Implementation Plan: md2tex 2.3.0 — Subtítulo pela CLI

**Branch**: `002-add-cli-subtitle` | **Date**: 2026-08-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-add-cli-subtitle/spec.md`

## Summary

Adicionar `--subtitle` com precedência explícita sobre o front matter; subtítulo vazio não é exibido e o tipo documental integra o bloco de identificação da capa. Atualizar versão e documentação para 2.3.0.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**: Click, Jinja2, PyYAML

**Storage**: Arquivos locais de Markdown e YAML

**Testing**: pytest

**Target Platform**: CLI local; geração PDF requer distribuição LaTeX compatível

**Project Type**: CLI de conversão Markdown para LaTeX/PDF

**Performance Goals**: Preservar as metas de conversão atuais, sem etapa externa adicional

**Constraints**: Distinguir `--subtitle` omitido de valor vazio; aplicar a mudança aos cinco templates de capa; não adicionar defaults de estilo

**Scale/Scope**: Uma opção CLI, resolução de metadados, cinco templates, testes, README e versão pública

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Generic & Decoupled Architecture — PASS**: metadados e opção são genéricos, sem branding.
- **II. Single Source of Truth for Defaults — PASS**: não altera estilo, classe, geometria ou tipografia.
- **III. Strict CLI Precedence Hierarchy — PASS**: o design preserva a presença explícita da opção para a CLI vencer inclusive quando vazia.
- **IV. Testability & Quality Assurance — PASS**: inclui testes de ajuda, precedência, capa e versão.

## Project Structure

```text
src/md2tex/{__init__.py,cli.py,models.py,metadata.py}
src/md2tex/templates/{base,report,meeting-minutes,adr,technical-plan}.tex.j2
tests/{test_cli.py,test_cli_subtitle.py,test_metadata.py}
README.md
pyproject.toml
specs/002-add-cli-subtitle/{research.md,data-model.md,contracts/cli-subtitle.md,quickstart.md}
```

**Structure Decision**: Manter o projeto único: a CLI encaminha a opção, a resolução central produz metadados efetivos e os templates exibem a capa uniformemente.

## Complexity Tracking
