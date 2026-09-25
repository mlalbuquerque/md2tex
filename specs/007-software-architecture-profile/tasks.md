# Tasks: Perfil Documento de Arquitetura de Software

**Input**: Design documents from `/specs/007-software-architecture-profile/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contract](contracts/software-architecture-profile.md), [quickstart](quickstart.md)

**Tests**: Incluídos porque a especificação exige cobertura automatizada de seleção, isolamento, precedência e renderização.

**Organization**: Tarefas agrupadas pelas histórias para permitir validação incremental.

## Phase 1: Setup

**Purpose**: Preparar um exemplo reutilizável do novo perfil.

- [X] T001 Add a representative Software Architecture Markdown example with front matter in examples/software-architecture.md

## Phase 2: Foundational

**Purpose**: Definir os dados tipados compartilhados necessários ao nome opcional e às revisões.

- [X] T002 Add typed revision entry and profile metadata fields in src/md2tex/models.py

**Checkpoint**: Os metadados podem representar o nome do sistema e uma sequência ordenada de revisões sem acoplar estilos ou marcas.

## Phase 3: User Story 1 - Gerar um Documento de Arquitetura de Software (Priority: P1) 🎯 MVP

**Goal**: Disponibilizar um perfil selecionável com template próprio, preservando os demais perfis.

**Independent Test**: Converter pelo perfil novo e pelo `default`; confirmar que somente o primeiro recebe o layout de Documento de Arquitetura e que os demais templates não mudam.

### Tests for User Story 1

- [X] T003 [P] [US1] Add CLI profile-choice coverage for software-architecture in tests/test_cli.py
- [X] T004 [P] [US1] Add profile registration and template mapping coverage in tests/test_profiles.py
- [X] T005 [US1] Add conversion coverage proving architecture output and default/profile isolation in tests/test_integration.py

### Implementation for User Story 1

- [X] T006 [US1] Register software-architecture label and template in src/md2tex/profiles.py
- [X] T007 [US1] Add software-architecture to the --type choices in src/md2tex/cli.py
- [X] T008 [US1] Create the dedicated architecture cover and body template with a reserved logo area in src/md2tex/templates/software-architecture.tex.j2
- [X] T009 [US1] Remove system-name and revision-history output from the generic template in src/md2tex/templates/base.tex.j2

**Checkpoint**: O perfil novo é selecionável e a conversão genérica e os outros perfis permanecem isolados.

## Phase 4: User Story 2 - Identificar o sistema na capa (Priority: P1)

**Goal**: Aceitar nome opcional por metadados ou CLI com precedência explícita da CLI.

**Independent Test**: Verificar capa com nome vindo do front matter, override da CLI e nome ausente.

### Tests for User Story 2

- [X] T010 [P] [US2] Add system-name trimming, whitespace-only, empty CLI override, front matter, and precedence coverage in tests/test_metadata.py
- [X] T011 [P] [US2] Add --system-name forwarding and help text coverage in tests/test_cli.py
- [X] T012 [US2] Add architecture cover rendering coverage for present and absent system name in tests/test_integration.py

### Implementation for User Story 2

- [X] T013 [US2] Scope system-name resolution to software-architecture while preserving CLI precedence in src/md2tex/metadata.py
- [X] T014 [US2] Scope --system-name help and cover placement below the reserved logo area to the architecture profile in src/md2tex/cli.py and src/md2tex/templates/software-architecture.tex.j2

**Checkpoint**: O nome é opcional, fica abaixo da área de logotipo no alto à direita, e não aparece em `default` ou em outros perfis.

## Phase 5: User Story 3 - Consultar o histórico de revisões (Priority: P1)

**Goal**: Gerar uma página própria, com tabela ordenada, antes do sumário opcional.

**Independent Test**: Converter com várias revisões, sem revisões e com TOC ligado/desligado; confirmar tabela, fallback e ordem.

### Tests for User Story 3

- [X] T015 [P] [US3] Add revision-history normalization and fallback coverage in tests/test_metadata.py
- [X] T016 [US3] Add table columns, row order, escaping, and blank-cell coverage in tests/test_integration.py
- [X] T017 [US3] Add output-order coverage for revision page before TOC and persistence with --no-toc in tests/test_integration.py

### Implementation for User Story 3

- [X] T018 [US3] Normalize ordered revision-history entries and synthesize the initial row when absent in src/md2tex/metadata.py
- [X] T019 [US3] Render a dedicated revision-history page before the optional TOC in src/md2tex/templates/software-architecture.tex.j2

**Checkpoint**: O perfil sempre imprime a página e tabela de revisões; `default` e outros perfis não recebem esse conteúdo.

## Phase 6: User Story 4 - Usar e compreender o perfil (Priority: P2)

**Goal**: Documentar uso, metadados e regras de tópicos e manter as listas públicas sincronizadas.

**Independent Test**: Seguir o quickstart e comparar lista de perfis, ajuda da CLI e regras documentadas.

### Tests for User Story 4

- [X] T020 [P] [US4] Add rules loader coverage accepting software-architecture and rejecting unknown profile names in tests/test_rules.py
- [X] T021 [US4] Add a CLI help assertion listing every accepted profile including default and software-architecture in tests/test_cli.py

### Implementation for User Story 4

- [X] T022 [US4] Add software-architecture to the commented rules profile examples in src/md2tex/templates/rules.yaml
- [X] T023 [US4] Document profile selection, system-name normalization/empty CLI override, revision-history, output order, and all --type choices in README.md
- [X] T024 [US4] Verify the documented architecture example matches the runnable example in examples/software-architecture.md and specs/007-software-architecture-profile/quickstart.md

**Checkpoint**: Usuários conseguem selecionar o perfil e preencher metadados seguindo somente a documentação.

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validar compatibilidade, checklist e cenários documentados.

- [X] T025 Run focused profile, metadata, rules, CLI, and integration tests with ./.venv/bin/pytest
- [X] T026 Run the full test suite with ./.venv/bin/pytest
- [X] T027 Execute scenarios in specs/007-software-architecture-profile/quickstart.md and reconcile README.md and examples/software-architecture.md

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup and supplies shared revision metadata.
- **US1 (Phase 3)**: Depends on Foundational; establishes profile selection and isolation.
- **US2 (Phase 4)** and **US3 (Phase 5)**: Depend on US1 because both render through the architecture profile. They can be developed in parallel after US1 if changes to shared metadata/template files are coordinated.
- **US4 (Phase 6)**: Depends on US1 so the documented identifier and options exist.
- **Polish (Phase 7)**: Depends on all stories.

### User Story Dependencies

- **US1 (P1)**: Independent after Foundation; MVP demonstrates a distinct profile without affecting other profiles.
- **US2 (P1)**: Depends on US1 for the dedicated cover.
- **US3 (P1)**: Depends on US1 for the dedicated template; independent of the system-name UI once the profile is established.
- **US4 (P2)**: Depends on the implemented CLI profile and metadata contract.

### Parallel Opportunities

- T003 and T004 can be written in parallel; T005 exercises their integration.
- Within US2, T010 and T011 are independent; T012 follows profile registration and metadata behavior.
- Within US3, T015 is independent of T016/T017; the integration tests T016 and T017 share one test file and should be implemented sequentially.
- T020 can proceed independently from documentation T023 after the profile registration exists.

## Implementation Strategy

### MVP First

1. Complete Setup and Foundation.
2. Complete US1 and prove the new profile has its own template while existing profiles remain isolated.
3. Validate the MVP with `./.venv/bin/pytest` for the profile selection and conversion tests.

### Incremental Delivery

1. Add optional system-name support and validate precedence.
2. Add revision table and document order behavior.
3. Update rules examples, README and runnable example.
4. Run focused tests, full suite, and quickstart scenarios.

## Phase 8: Convergence

- [X] T028 Fix default profile leakage: remove system_name and revision_history from base.tex.j2 per FR-002 (contradicts)
- [X] T029 Implement MVP profile: register software-architecture in profiles.py, add to CLI choices, and create dedicated software-architecture.tex.j2 template per FR-001, FR-002 (missing)
- [X] T030 Fix system-name spacing: trim external spaces and treat space-only values as empty in metadata.py per FR-003 (partial)
- [X] T031 Scope features: restrict system-name and revision-history resolution to the software-architecture profile in metadata.py and cli.py per FR-004, FR-006 (partial)
- [X] T032 Add documentation and examples: update README, rules.yaml, quickstart, and create examples/software-architecture.md per FR-011, FR-012, FR-013 (missing)
- [X] T033 Implement automated tests: add test coverage for profile selection, metadata trimming, and template isolation per SC-001, SC-002, SC-003, SC-004 (missing)
