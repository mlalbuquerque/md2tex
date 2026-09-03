# Implementation Plan: Configurar requisitos de validação

**Branch**: `006-configure-validation` | **Date**: 2026-09-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-configure-validation/spec.md`

## Summary

Adicionar ao `config.yaml` uma seção opcional que descreve requisitos por perfil e suas orientações públicas. O validador usará os requisitos declarativos para produzir diagnósticos copiáveis, preservando as validações estruturais, a precedência da CLI e o bloqueio antecipado de `--strict`.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**: Click, PyYAML, Jinja2

**Storage**: `config.yaml` local do usuário e Markdown com front matter YAML; sem persistência remota.

**Testing**: `./.venv/bin/pytest`, Click `CliRunner` e testes unitários de configuração/validação.

**Target Platform**: CLI local em plataformas com Python.

**Project Type**: CLI de conversão Markdown para LaTeX/PDF.

**Performance Goals**: Uma validação linear do YAML e do corpo Markdown, sem chamadas externas adicionais.

**Constraints**: A nova seção é opcional; nenhum tipo sem configuração muda de comportamento; CLI continua vencendo front matter; `--strict` não grava saída inválida; configurações inválidas falham antes da conversão.

**Scale/Scope**: Cinco perfis existentes, campos YAML e seções Markdown, uma regra por item exigido.

## Constitution Check

- **I. Generic & Decoupled Architecture — PASS**: requisitos, rótulos e exemplos pertencem à configuração do usuário, não ao mecanismo ou a uma marca.
- **II. Single Source of Truth for Defaults — PASS**: `config.yaml` permanece a fonte única para a nova configuração e não ganha estilos implícitos.
- **III. Strict CLI Precedence Hierarchy — PASS**: a avaliação de campos usa os metadados já resultantes da precedência CLI → front matter.
- **IV. Testability & Quality Assurance — PASS**: configuração válida/inválida, orientações, precedência e bloqueio estrito terão cobertura no ambiente virtual local.

## Project Structure

```text
src/md2tex/
├── config.py           # Carrega e valida requisitos declarativos
├── models.py           # Representações tipadas de regras e configuração
├── validator.py        # Avalia requisitos e formata orientações públicas
└── converter.py        # Encaminha a configuração ao gate de validação

tests/
├── test_config.py      # Schema e rejeição de configurações inválidas
├── test_validator.py   # Campos, seções, exemplos e itens opcionais
├── test_cli.py         # Mensagens e precedência visíveis na CLI
└── test_integration.py # Gate estrito e saída preservada

src/md2tex/templates/config.yaml  # Modelo comentado
README.md                          # Referência de usuário
specs/006-configure-validation/
├── research.md
├── data-model.md
├── contracts/config-document-requirements.md
└── quickstart.md
```

**Structure Decision**: Manter parsing e schema em `config.py`, dados tipados em `models.py` e avaliação no validador. O conversor só coordena o gate e evita que detalhes de configuração contaminem templates ou CLI.

## Complexity Tracking

Nenhuma violação constitucional exige justificativa.

## Post-Design Constitution Check

- **I–IV — PASS**: a configuração é declarativa, opcional, isolada por perfil e coberta por testes; não introduz estilos, precedência nova ou trabalho externo.
