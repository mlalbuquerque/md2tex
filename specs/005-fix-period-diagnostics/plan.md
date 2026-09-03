# Implementation Plan: Corrigir diagnósticos do período

**Branch**: `005-fix-period-diagnostics` | **Date**: 2026-09-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/005-fix-period-diagnostics/spec.md`

## Summary

Substituir apenas os identificadores internos de diagnóstico para início e fim do período da Memória de Reunião por rótulos documentais, preservar todas as demais mensagens e publicar como v2.5.1.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**: Click, PyYAML, Jinja2

**Storage**: Arquivos Markdown com front matter YAML; sem persistência.

**Testing**: pytest executado com `./.venv/bin/pytest`

**Target Platform**: CLI local em plataformas com Python

**Project Type**: CLI

**Performance Goals**: Nenhuma alteração perceptível no tempo de validação linear.

**Constraints**: Preservar chaves YAML, comportamento estrito e diagnósticos não relacionados; sem estilos embutidos.

**Scale/Scope**: Dois rótulos de diagnóstico, seus testes de regressão e versão pública.

## Constitution Check

- **I. Generic & Decoupled Architecture — PASS**: somente apresentação de diagnóstico do perfil existente.
- **II. Single Source of Truth for Defaults — PASS**: não envolve estilos nem defaults visuais.
- **III. Strict CLI Precedence Hierarchy — PASS**: não altera opções da CLI nem precedência.
- **IV. Testability & Quality Assurance — PASS**: testes unitários e de CLI cobrirão as duas mensagens e regressão.

## Project Structure

```text
src/md2tex/
├── validator.py       # Mapeia os dois caminhos internos para rótulos públicos
└── __init__.py        # Versão pública

tests/
├── test_validator.py  # Rótulos de período e mensagens não relacionadas
└── test_cli.py        # Saída estrita apresentada ao usuário

pyproject.toml         # Versão de distribuição
RELEASES.md            # Histórico da versão 2.5.1
specs/005-fix-period-diagnostics/
├── research.md
├── data-model.md
├── contracts/period-diagnostics.md
└── quickstart.md
```

**Structure Decision**: Manter a lógica no formatador de mensagens já responsável pelos diagnósticos da Memória de Reunião; não criar novo módulo para dois rótulos.

## Complexity Tracking

Nenhuma violação constitucional exige justificativa.

## Post-Design Constitution Check

- **I–IV — PASS**: o desenho mantém o escopo no validador, preserva o contrato YAML e adiciona cobertura automatizada no ambiente virtual local.
