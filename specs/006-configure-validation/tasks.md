# Tasks: Configurar requisitos de validação

**Input**: Design documents from `/specs/006-configure-validation/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contract](contracts/config-document-requirements.md), [quickstart.md](quickstart.md)

**Tests**: Incluídos porque a especificação e a constituição exigem cobertura automatizada de configuração, CLI e integração.

**Organization**: Tarefas organizadas por história para permitir verificação independente após a fundação compartilhada.

## Phase 1: Setup

**Purpose**: Preparar o modelo de configuração e fixtures reutilizáveis.

- [X] T001 Add commented `document_requirements` examples for meeting-minutes in src/md2tex/templates/config.yaml
- [X] T002 [P] Add reusable config-with-requirements fixture helper in tests/test_config.py

---

## Phase 2: Foundational

**Purpose**: Criar dados tipados, schema seguro e encaminhamento ao fluxo de validação.

- [X] T003 Add typed document requirement and per-profile requirement representations in src/md2tex/models.py
- [X] T004 Add schema coverage for valid, absent, unknown-profile, duplicate, malformed, and optional requirement configurations in tests/test_config.py
- [X] T005 Parse and strictly validate optional `document_requirements` rules in src/md2tex/config.py
- [X] T006 Attach validated document requirements to UserConfig and conversion context in src/md2tex/models.py and src/md2tex/converter.py
- [X] T007 Run foundational configuration tests with ./.venv/bin/pytest in tests/test_config.py

**Checkpoint**: `config.yaml` pode transportar requisitos válidos; configuração inválida falha antes da conversão e configurações atuais continuam válidas.

---

## Phase 3: User Story 1 - Configurar requisitos de um tipo documental (Priority: P1) 🎯 MVP

**Goal**: Aplicar campos e seções obrigatórios configurados apenas ao tipo documental correspondente.

**Independent Test**: Uma regra de `meeting-minutes` é aplicada somente a esse perfil; outro perfil e uma configuração sem regras preservam o comportamento existente.

### Tests for User Story 1

- [X] T008 [P] [US1] Add validator coverage for required and optional configured fields, nested paths, sections, and profile isolation in tests/test_validator.py
- [X] T009 [P] [US1] Add conversion integration coverage for configured profile rules and unconfigured-profile compatibility in tests/test_integration.py

### Implementation for User Story 1

- [X] T010 [US1] Resolve configured field values after CLI-over-front-matter precedence in src/md2tex/metadata.py and src/md2tex/converter.py
- [X] T011 [US1] Evaluate configured field and section requirements while retaining structural validation in src/md2tex/validator.py
- [X] T012 [US1] Deduplicate equivalent configured and meeting-minutes diagnostics in src/md2tex/validator.py and src/md2tex/converter.py
- [X] T013 [US1] Run configured-profile scenarios with ./.venv/bin/pytest in tests/test_config.py tests/test_validator.py and tests/test_integration.py

**Checkpoint**: Requisitos declarados são aplicados por perfil, requisitos opcionais não geram pendência e tipos sem configuração mantêm o comportamento atual.

---

## Phase 4: User Story 2 - Corrigir o campo ausente com orientação (Priority: P1)

**Goal**: Apresentar diagnóstico copiável e público para campos e seções ausentes, incluindo Cliente/Projeto.

**Independent Test**: A mensagem para um campo, campo aninhado e seção contém rótulo, instrução e exemplo; `client` não aparece como rótulo público.

### Tests for User Story 2

- [X] T014 [P] [US2] Add validator assertions for public labels, multiline YAML/Markdown examples, instructions, and `Cliente/Projeto` in tests/test_validator.py
- [X] T015 [P] [US2] Add strict CLI diagnostics for field and section examples in tests/test_cli.py
- [X] T016 [P] [US2] Add strict output-preservation integration coverage for several configured pendencies in tests/test_integration.py

### Implementation for User Story 2

- [X] T017 [US2] Format configured requirement diagnostics with label, reason, instruction, and copyable example in src/md2tex/validator.py
- [X] T018 [US2] Apply configured public labels to equivalent meeting-minutes field diagnostics, including `client`, in src/md2tex/validator.py
- [X] T019 [US2] Preserve all formatted configured pendencies at the strict pre-output gate in src/md2tex/converter.py
- [X] T020 [US2] Run guidance and strict-mode scenarios with ./.venv/bin/pytest in tests/test_validator.py tests/test_cli.py and tests/test_integration.py

**Checkpoint**: Cada pendência configurada é clara e copiável, e `--strict` continua a proteger o destino.

---

## Phase 5: User Story 3 - Manter uma configuração segura (Priority: P2)

**Goal**: Rejeitar regras declarativas inválidas antes de qualquer conversão e preservar precedência da CLI.

**Independent Test**: Configurações inválidas apontam a regra defeituosa; um valor de CLI satisfaz o campo configurado equivalente.

### Tests for User Story 3

- [X] T021 [P] [US3] Add config error assertions for missing label, instruction, example, required flag, and extra keys in tests/test_config.py
- [X] T022 [P] [US3] Add CLI precedence and invalid-config-before-output coverage in tests/test_cli.py

### Implementation for User Story 3

- [X] T023 [US3] Produce actionable requirement-path errors during config schema validation in src/md2tex/config.py
- [X] T024 [US3] Preserve CLI metadata precedence during configured-requirement evaluation in src/md2tex/converter.py and src/md2tex/metadata.py
- [X] T025 [US3] Run invalid-config and CLI-precedence scenarios with ./.venv/bin/pytest in tests/test_config.py and tests/test_cli.py

**Checkpoint**: Nenhuma configuração parcial é usada e a hierarquia de precedência permanece intacta.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentar o recurso e validar todo o fluxo.

- [X] T026 [P] Document `document_requirements`, orientações copiáveis, comportamento opcional e precedência in README.md
- [X] T027 [P] Update the public config example and initialization expectations in src/md2tex/templates/config.yaml and tests/test_cli.py
- [X] T028 Run ruff and the complete pytest suite with ./.venv/bin/ruff and ./.venv/bin/pytest
- [X] T029 Execute every scenario in specs/006-configure-validation/quickstart.md and reconcile documentation in README.md

## Dependencies & Execution Order

- Phase 1 has no dependencies.
- T003–T007 depend on setup and block all user stories.
- US1 depends on the foundation and provides the configurable validation MVP.
- US2 depends on US1 because it formats the pending items produced by configured rules.
- US3 depends on the foundation and may be completed after US1; it validates the CLI precedence used by US1.
- Phase 6 depends on all user stories.

```text
Setup → Foundational → US1 (MVP) → US2 → Polish
                         └──────→ US3 ─┘
```

## Parallel Opportunities

- T001 and T002 can run in parallel.
- T008 and T009 affect different test modules and can run in parallel.
- T014, T015 and T016 affect different test modules and can run in parallel.
- T021 and T022 affect different test modules and can run in parallel.
- T026 and T027 affect separate documentation/configuration surfaces and can run in parallel after behavior stabilizes.

## Implementation Strategy

### MVP First

1. Complete setup and foundation.
2. Complete US1 and prove profile isolation, nested paths and optional requirements.
3. Demonstrate one configured Meeting Minutes validation before progressing.

### Incremental Delivery

1. Introduce schema and typed requirements.
2. Apply per-profile requirements and preserve existing behavior.
3. Add guided diagnostics and strict protection.
4. Harden invalid configuration and CLI precedence.
5. Document and run the complete validation suite.

## Phase 7: Convergence

- [X] T030 Validate malformed dotted field paths and add schema coverage for missing label, instruction, required, extra keys, and duplicate requirements per FR-008 (partial)
- [X] T031 Recognize Setext Markdown headings when evaluating configured section requirements and add coverage per FR-001 / FR-005 / US1-AC1 (partial)
- [X] T032 Add CLI coverage for complete configured field and section diagnostics, including multiline YAML and Markdown examples, per FR-003 / FR-004 / FR-005 / US2-AC1–AC3 (partial)
- [X] T033 Add strict integration coverage proving configured requirement pendencies block Mermaid/Pandoc and preserve missing or existing output per FR-009 / SC-004 (partial)
- [X] T034 Add CLI coverage for invalid `document_requirements` before output and CLI `--client` precedence satisfying a configured rule per FR-008 / FR-009 / US3-AC1–AC2 (partial)
- [X] T035 Deduplicate configured and structural meeting-minutes section diagnostics per plan decision / T012 (partial)

## Phase 8: Convergence

- [X] T036 CRITICAL Restore the converter-to-meeting-minutes validator interface so configured-requirement suppression and strict conversion work without TypeError per FR-001 / FR-007 / FR-009 / plan: converter coordination (partial)
