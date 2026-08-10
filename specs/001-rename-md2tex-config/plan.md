# Implementation Plan: md2tex 2.2.0

**Branch**: `001-rename-md2tex-config` | **Date**: 2026-08-06

## Summary

Remover defaults de estilo/compilação do conversor, validar um schema YAML explícito e disponibilizar `md2tex init`. A configuração inicial distribuída é um arquivo YAML, não um fallback de execução.

## Technical Context

**Language**: Python >= 3.10
**Dependencies**: Click, Jinja2, PyYAML
**Testing**: pytest
**Configuration**: `~/.config/md2tex/config.yaml` ou `--config`
**Version**: 2.2.0 (minor, pois exige configuração completa)

## Constitution Check

- A configuração é a única fonte de defaults de estilo: **PASS**.
- A CLI permanece genérica e sem branding específico: **PASS**.
- Novos comportamentos possuem testes automatizados: **PASS**.

## Design

- `config.py` valida chaves, tipos e engine antes de construir `UserConfig`.
- `templates/config.yaml` é copiado por `md2tex init`; `examples/config.yaml` documenta o mesmo contrato.
- Templates Jinja2 apenas renderizam dados fornecidos no YAML e metadados do documento.
- `typography` controla `babel`, tamanho de classe, fonte principal e espaçamento quando configurados.
- ``--style`, `--engine`, `--landscape-tables`, `--table-font`, `--table-width`, `--table-borders` e `--table-zebra` são as sobrescritas públicas nesta versão.

## Table Configuration

A seção `tables` controla `landscape`, `font`, `width`, `borders` e `zebra`. `grid` adiciona contornos completos; `outer` adiciona somente o contorno externo; `none` preserva o LaTeX do Pandoc.

## Out of Scope

Bibliografia, filtros Lua customizados, watch, temas de código e capas selecionáveis permanecem em versões futuras.
