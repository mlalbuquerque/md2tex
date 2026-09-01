# Implementation Plan: Atualizar memória de reunião

**Branch**: `004-update-meeting-minutes` | **Date**: 2026-08-31 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-update-meeting-minutes/spec.md`

## Summary

Evoluir o perfil `meeting-minutes` para receber metadados YAML estruturados, validar os campos obrigatórios da memória de reunião antes da conversão e renderizar identificação, participantes e pendências no modelo corporativo configurado pelo usuário. O padrão letterhead continua sendo definido apenas em `config.yaml`; o perfil não introduz estilo corporativo embutido.

## Technical Context

**Language/Version**: Python >= 3.10

**Primary Dependencies**: Click, PyYAML, Jinja2; Pandoc para converter o corpo Markdown; LaTeX/PDF continua opcional e externo.

**Storage**: Um arquivo Markdown com YAML front matter e regras YAML locais já suportadas pelo projeto; nenhuma persistência remota.

**Testing**: pytest, Click `CliRunner`, testes unitários de front matter/metadados/validador, testes de integração de conversão e de preservação de saída em modo estrito.

**Target Platform**: CLI local em plataformas com Python; PDF requer a cadeia LaTeX compatível com o estilo configurado.

**Project Type**: CLI de conversão Markdown para LaTeX/PDF.

**Performance Goals**: Uma leitura e validação linear do front matter e do Markdown, concluída antes de Mermaid, Pandoc e escrita; nenhuma chamada externa adicional para validar metadados.

**Constraints**: O estilo continua sendo a única responsabilidade de `config.yaml`; campos da memória usam YAML front matter; `--strict` não pode criar nem alterar a saída se houver pendências; os demais perfis preservam o comportamento atual; participantes e pendências são condicionais conforme a especificação.

**Scale/Scope**: Um perfil existente (`meeting-minutes`), uma estrutura de metadados, um template específico, validação e documentação/exemplos; um documento por execução.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Generic & Decoupled Architecture — PASS**: a estrutura pertence ao perfil documental existente, sem embutir caminhos, marca ou macros corporativas no motor; o estilo letterhead é fornecido pela configuração externa.
- **II. Single Source of Truth for Defaults — PASS**: nenhum `.sty`, classe, margem ou tipografia será definido pelo perfil; `config.yaml` continua sendo a fonte única do estilo.
- **III. Strict CLI Precedence Hierarchy — PASS**: opções de metadados já existentes da CLI continuam vencendo valores equivalentes do front matter; a nova validação observa o resultado dessa precedência.
- **IV. Testability & Quality Assurance — PASS**: contrato de front matter, validação nominal, template, `Sem pendências`, grupos vazios, CLI e bloqueio estrito terão cobertura automatizada.

## Project Structure

```text
src/md2tex/
├── metadata.py                    # Constrói metadados e dados da memória
├── models.py                      # Representações tipadas de metadados
├── validator.py                   # Validação específica do perfil
├── converter.py                   # Gate pré-conversão e contexto do template
├── profiles.py                    # Perfil meeting-minutes existente
└── templates/meeting-minutes.tex.j2

tests/
├── test_metadata.py               # Front matter e normalização (novo ou ampliado)
├── test_validator.py              # Campos obrigatórios e casos de borda
├── test_integration.py            # Conversão/renderização e modo estrito
└── test_cli.py                    # Diagnósticos e precedência pela CLI

specs/004-update-meeting-minutes/
├── research.md
├── data-model.md
├── contracts/meeting-minutes-frontmatter.md
└── quickstart.md
```

**Structure Decision**: Manter o projeto único. Dados e validação exclusivos da memória ficam no domínio do perfil, enquanto o conversor apenas coordena validação precoce e a passagem de contexto ao template. O pacote de estilo não é alterado nem incluído no código.

## Complexity Tracking

Nenhuma violação constitucional exige justificativa.

## Post-Design Constitution Check

- **I. Generic & Decoupled Architecture — PASS**: o contrato do perfil documenta dados, não um estilo ou organização embutidos no motor.
- **II. Single Source of Truth for Defaults — PASS**: o quickstart exige configurar o letterhead em `config.yaml`; template não fornece fallback de estilo.
- **III. Strict CLI Precedence Hierarchy — PASS**: o contrato preserva a precedência CLI → front matter para campos equivalentes.
- **IV. Testability & Quality Assurance — PASS**: contrato e quickstart definem cenários independentes, incluindo saída inalterada no modo estrito.
