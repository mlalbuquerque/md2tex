# Implementation Plan: Perfil Documento de Arquitetura de Software

**Branch**: `007-software-architecture-profile` | **Date**: 2026-09-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/007-software-architecture-profile/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Adicionar o perfil `software-architecture` com template próprio, nome de sistema opcional e página obrigatória de histórico de revisões. Restringir esses elementos ao novo perfil, preservando o comportamento genérico de `default` e dos demais perfis. O registro `PROFILES` continuará sendo a fonte de perfis reconhecidos pela CLI e pelas regras de tópicos.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**: Click, PyYAML, Jinja2; Pandoc para conversão Markdown; LaTeX externo e opcional para PDF.

**Storage**: Arquivo Markdown com YAML front matter e arquivo local YAML opcional de regras; sem persistência adicional.

**Testing**: `./.venv/bin/pytest`; testes unitários de metadados/perfis, CLI e integração de renderização com conversor externo simulado quando aplicável.

**Target Platform**: CLI local em plataformas com Python; PDF depende da cadeia LaTeX configurada pelo usuário.

**Project Type**: CLI de conversão Markdown para LaTeX/PDF.

**Performance Goals**: Processamento de metadados linear no número de revisões, sem chamadas externas adicionais.

**Constraints**: Estilo, geometria, tipografia e pacotes permanecem definidos pelo `config.yaml` do usuário; o núcleo não incorpora marca ou logotipo institucional. Precedência CLI sobre front matter. Os elementos novos ficam restritos ao perfil `software-architecture`.

**Scale/Scope**: Um perfil novo, seu template, metadados de nome/revisões, opção CLI, documentação, exemplos e cobertura automatizada; os perfis existentes permanecem compatíveis.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Generic & Decoupled Architecture — PASS**: o perfil representa estrutura documental genérica e não inclui marca UEFS/Netra nem um logotipo no código.
- **II. Single Source of Truth for Defaults — PASS**: nenhuma classe, fonte, geometria, cor, pacote ou estilo corporativo será embutido; o posicionamento visual usa o estilo externo configurado.
- **III. Strict CLI Precedence Hierarchy — PASS**: `--system-name` prevalece sobre `system-name` no front matter.
- **IV. Testability & Quality Assurance — PASS**: cenários de seleção, isolamento, precedência, tabela, ordem e documentação terão cobertura em `./.venv/bin/pytest`.

## Project Structure

### Documentation (this feature)

```text
specs/007-software-architecture-profile/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/software-architecture-profile.md
└── tasks.md
```

### Source Code (repository root)
```text
src/md2tex/
├── profiles.py                 # Registro de identificadores e templates
├── cli.py                      # Opções --type e --system-name
├── metadata.py                 # Metadados e histórico do perfil
├── models.py                   # Dados de metadados e revisões
├── rules.py                    # Validação de perfil via PROFILES
└── templates/
    ├── base.tex.j2             # Documento Padrão sem elementos arquiteturais
    └── software-architecture.tex.j2

tests/
├── test_metadata.py
├── test_cli.py
├── test_profiles.py
├── test_rules.py
└── test_integration.py

README.md
```

**Structure Decision**: Manter o projeto CLI único. Registrar o novo perfil em `profiles.py`, selecionar seu template pelo mecanismo existente, normalizar seus metadados no fluxo atual e garantir por testes que `base.tex.j2` e os demais perfis não recebem os elementos específicos de arquitetura. Regras YAML passam a reconhecer o perfil automaticamente pelo registro compartilhado.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Sem desvios constitucionais que exijam justificativa. | N/A | N/A |

## Post-Design Constitution Check

- **I–IV — PASS**: o design usa o registro/template existente, mantém os dados institucionais fora do núcleo, respeita configuração e precedência e define testes locais para os critérios funcionais.
