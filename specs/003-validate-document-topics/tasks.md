# Tasks: md2tex 2.4.0 — Validar tópicos por tipo documental

**Input**: Design documents from `/specs/003-validate-document-topics/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [CLI contract](contracts/cli-rules.md), [quickstart.md](quickstart.md)

**Tests**: Incluídos porque a especificação exige cenários verificáveis e a Constituição exige cobertura automatizada de funcionalidades e CLI.

**Organization**: Tarefas agrupadas por história para permitir entrega e verificação independentes após a fundação compartilhada.

## Phase 1: Setup

**Purpose**: Preparar os arquivos que expõem a nova configuração e a cobertura da feature.

- [X] T001 Create the packaged inactive rules template with complete examples for all five profiles in src/md2tex/templates/rules.yaml
- [X] T002 [P] Create focused rule-loading and initialization tests in tests/test_rules.py
- [X] T003 [P] Add focused required-topic extraction and comparison cases to tests/test_validator.py

---

## Phase 2: Foundational

**Purpose**: Criar a infraestrutura que bloqueia todas as histórias de usuário.

- [X] T004 Add rules path state to ConversionOptions in src/md2tex/models.py
- [X] T005 Implement strict YAML rule schema validation, default-path resolution, and safe template initialization in src/md2tex/rules.py
- [X] T006 Implement heading extraction outside fenced code and normalized required-topic comparison in src/md2tex/validator.py
- [X] T007 Refactor the Click entry point while preserving `md2tex [OPTIONS] INPUT_FILE` and `md2tex init` compatibility in src/md2tex/cli.py
- [X] T008 Add the packaged rules template to distribution metadata in pyproject.toml
- [X] T009 Run foundational unit and CLI compatibility tests in tests/test_rules.py tests/test_validator.py tests/test_cli.py

**Checkpoint**: regras podem ser carregadas integralmente e a CLI suporta a futura superfície de comandos sem quebrar conversões atuais.

---

## Phase 3: User Story 1 - Validar tópicos antes da conversão (Priority: P1) 🎯 MVP

**Goal**: Encontrar e informar tópicos obrigatórios ausentes antes da transformação, mantendo a conversão normal disponível.

**Independent Test**: Um Markdown com regras para o perfil selecionado gera avisos nominais para cada tópico ausente; títulos com caixa ou espaços distintos satisfazem a regra; sem regras, a conversão não muda.

- [X] T010 [P] [US1] Add converter integration tests for satisfied, missing, duplicated, and profile-isolated topics in tests/test_integration.py
- [X] T011 [P] [US1] Add CLI tests for `--rules`, default-rule absence, and explicit missing or invalid rules files in tests/test_cli.py
- [X] T012 [US1] Add the `--rules PATH` conversion option and forward its explicitness into ConversionOptions in src/md2tex/cli.py
- [X] T013 [US1] Load rules and append `topics` warnings after Markdown heading normalization but before Mermaid/Pandoc work in src/md2tex/converter.py
- [X] T014 [US1] Emit one actionable warning per original configured topic and preserve normal TEX generation in src/md2tex/converter.py
- [X] T015 [US1] Run the User Story 1 scenarios from tests/test_rules.py tests/test_validator.py tests/test_cli.py tests/test_integration.py

**Checkpoint**: US1 is independently usable as an opt-in warning-only validator.

---

## Phase 4: User Story 2 - Criar e personalizar regras de tópicos (Priority: P2)

**Goal**: Criar com segurança um modelo de regras editável e aplicar regras somente ao perfil selecionado.

**Independent Test**: `md2tex rules init` cria exemplos comentados para cinco perfis; a repetição sem `--force` preserva bytes; regras distintas para ADR e relatório só afetam o perfil indicado.

- [ ] T016 [P] [US2] Add CLI contract tests for `md2tex rules init`, explicit destination, safe overwrite refusal, and `--force` in tests/test_cli.py
- [ ] T017 [P] [US2] Add template-content tests covering commented inactive examples for all profiles in tests/test_rules.py
- [ ] T018 [US2] Implement the `md2tex rules init [--rules PATH] [--force]` command and actionable creation/overwrite diagnostics in src/md2tex/cli.py
- [ ] T019 [US2] Ensure the generated rules file remains separate from style configuration and uses only profile IDs from src/md2tex/profiles.py in src/md2tex/rules.py
- [ ] T020 [US2] Run the User Story 2 initialization and per-profile isolation scenarios in tests/test_rules.py tests/test_cli.py tests/test_integration.py

**Checkpoint**: US2 is independently usable to bootstrap and tailor content rules safely.

---

## Phase 5: User Story 3 - Escolher o impacto das pendências (Priority: P3)

**Goal**: Manter avisos em conversões normais e bloquear de forma segura no modo estrito.

**Independent Test**: O mesmo documento incompleto gera TEX com aviso normalmente, mas com `--strict` falha antes de criar ou modificar o arquivo de saída.

- [ ] T021 [P] [US3] Add strict-mode tests for absent output and byte-for-byte preserved existing output in tests/test_integration.py
- [ ] T022 [P] [US3] Add CLI diagnostic and exit-behavior tests for strict missing topics in tests/test_cli.py
- [ ] T023 [US3] Raise ValidationError for required-topic pendencies before Mermaid, Pandoc, template rendering, ensure_parent, and output writes in src/md2tex/converter.py
- [ ] T024 [US3] Preserve `--no-validate` suppression of topic checks while keeping explicitly selected invalid rules fatal in src/md2tex/converter.py
- [ ] T025 [US3] Run the User Story 3 normal-versus-strict scenarios in tests/test_cli.py tests/test_integration.py

**Checkpoint**: Todas as histórias são independentes e o modo estrito protege o destino de saída.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Publicar a feature, alinhar versão e validar o fluxo completo.

- [ ] T026 [P] Update the public version to 2.4.0 in pyproject.toml and src/md2tex/__init__.py
- [ ] T027 [P] Replace the planned 2.4.0 entry with released topic-validation functionality in RELEASES.md
- [ ] T028 [P] Document rule creation, YAML structure, customization, `--rules`, normal validation, strict validation, and `--no-validate` in README.md
- [ ] T029 Run ruff and the complete pytest suite for the feature in pyproject.toml
- [ ] T030 Execute every scenario in specs/003-validate-document-topics/quickstart.md and correct discrepancies in README.md

---

## Dependencies & Execution Order

- Phase 1 has no dependencies.
- Phase 2 depends on T001–T003 and blocks all stories.
- US1 depends on T004–T009.
- US2 depends on T004–T009 and validates its output through the US1 loading path; it can proceed after the foundation but should be merged after US1 for the clearest incremental release.
- US3 depends on the US1 converter integration (T012–T014).
- Polish depends on the completed stories.

```text
Setup → Foundational → US1 (MVP) → US2 → US3 → Polish
                        └────────→ US2 may develop in parallel after foundation
```

## Parallel Opportunities

- T002 and T003 can proceed in parallel with T001.
- Within US1, T010 and T011 can proceed in parallel; both precede T012–T014.
- Within US2, T016 and T017 can proceed in parallel.
- Within US3, T021 and T022 can proceed in parallel.
- T026, T027, and T028 modify distinct public-facing files and can proceed in parallel once behavior stabilizes.

## Implementation Strategy

### MVP First

1. Complete T001–T009.
2. Complete T010–T015.
3. Demonstrate a valid rule file that warns for missing topics and does not affect a conversion without rules.

### Incremental Delivery

1. Add safe rule loading and warning-only validation (US1).
2. Add self-service initialization and customization (US2).
3. Add strict pre-output blocking (US3).
4. Publish version, release notes, docs, and run the full suite.
