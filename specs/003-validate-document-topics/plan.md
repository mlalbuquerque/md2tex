# Implementation Plan: md2tex 2.4.0 — Validar tópicos por tipo documental

**Branch**: `003-validate-document-topics` | **Date**: 2026-08-18 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-validate-document-topics/spec.md`

## Summary

Adicionar regras YAML independentes de estilo para tópicos obrigatórios por perfil documental. A CLI permitirá criar um modelo comentado com `md2tex rules init`, selecionar um arquivo com `--rules` e converter com avisos ou interromper antecipadamente com `--strict`. A versão pública passa a 2.4.0.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**: Click, PyYAML, Jinja2; Pandoc já é dependência externa de conversão

**Storage**: Markdown e YAML locais; regras padrão em `~/.config/md2tex/rules.yaml`

**Testing**: pytest com ClickCliRunner, testes unitários de regras/validador e integração

**Target Platform**: CLI local; PDF continua requerendo LaTeX compatível

**Project Type**: CLI de conversão Markdown para LaTeX/PDF

**Performance Goals**: Uma leitura YAML e varredura linear dos títulos antes de Pandoc/Mermaid; nenhuma chamada externa adicional

**Constraints**: `--rules` explícito inválido falha sempre; ausência do padrão é silenciosa; `--strict` não escreve TEX com pendências; exemplos inativos; estilos continuam em `config.yaml`

**Scale/Scope**: Cinco perfis, um arquivo por execução, uma opção, um subcomando, testes e atualização de documentação/versão

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Generic & Decoupled Architecture — PASS**: regras editáveis e perfis genéricos, sem conteúdo institucional.
- **II. Single Source of Truth for Defaults — PASS**: regras de conteúdo não alteram ou ampliam o YAML de estilo.
- **III. Strict CLI Precedence Hierarchy — PASS**: `--rules` vence a localização padrão e `--strict` é explícito.
- **IV. Testability & Quality Assurance — PASS**: schema, normalização, avisos, bloqueio pré-saída, inicialização, ajuda e versão serão testados.

## Project Structure

```text
src/md2tex/{cli.py,rules.py,models.py,converter.py,validator.py,profiles.py}
src/md2tex/templates/rules.yaml
tests/{test_rules.py,test_validator.py,test_cli.py,test_integration.py}
README.md  RELEASES.md  pyproject.toml
specs/003-validate-document-topics/{research.md,data-model.md,contracts/cli-rules.md,quickstart.md}
```

**Structure Decision**: Manter o projeto único. Um módulo de regras separa conteúdo do schema estrito de estilo; o conversor coordena a validação precoce e o validador produz mensagens normalizadas.

## Complexity Tracking

Nenhuma violação constitucional exige justificativa.

## Post-Design Constitution Check

- **I. Generic & Decoupled Architecture — PASS**: o template somente orienta, sem regras implícitas.
- **II. Single Source of Truth for Defaults — PASS**: `rules.yaml` não contém defaults de apresentação.
- **III. Strict CLI Precedence Hierarchy — PASS**: contrato define `--rules` como seleção explícita.
- **IV. Testability & Quality Assurance — PASS**: quickstart e contrato cobrem, inclusive, não escrita em modo estrito.
