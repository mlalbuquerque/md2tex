# Tasks: Atualizar memória de reunião

**Input**: Design documents from `/specs/004-update-meeting-minutes/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [front matter contract](contracts/meeting-minutes-frontmatter.md), [quickstart.md](quickstart.md)

**Tests**: Incluídos porque a constituição exige cobertura automatizada e a especificação requer cenários verificáveis de conversão, validação e modo estrito.

**Organization**: Tarefas agrupadas por história para permitir entrega e verificação independentes após a fundação compartilhada.

## Phase 1: Setup

**Purpose**: Preparar exemplos reutilizáveis e a cobertura focada na estrutura de memória de reunião.

- [X] T001 Create canonical complete and no-pendency Markdown fixtures from the front matter contract in tests/fixtures/meeting_minutes/
- [X] T002 [P] Create focused front matter and profile-metadata test module in tests/test_metadata.py
- [X] T003 [P] Add meeting-minutes validation cases for metadata, sections, participants, and pendency rows in tests/test_validator.py

---

## Phase 2: Foundational

**Purpose**: Criar a representação estruturada da memória e o fluxo comum de validação antes da conversão.

- [X] T004 Add typed Participant and MeetingMinutesData representations to src/md2tex/models.py
- [X] T005 Parse and normalize `period` and `participants` front matter for the `meeting-minutes` profile in src/md2tex/metadata.py
- [X] T006 Validate the normalized profile-specific data and required body-section content with named diagnostics in src/md2tex/validator.py
- [X] T007 Forward profile-specific metadata validation messages before Mermaid, Pandoc, template rendering, and output writes in src/md2tex/converter.py
- [X] T008 Run foundational metadata and validator tests in tests/test_metadata.py and tests/test_validator.py

**Checkpoint**: A estrutura YAML e o conteúdo obrigatório da memória podem ser interpretados e validados sem afetar outros perfis.

---

## Phase 3: User Story 1 - Gerar uma memória no padrão Netra (Priority: P1) 🎯 MVP

**Goal**: Converter uma memória completa, estruturando identificação, período, participantes e pendências no template do perfil, com o estilo letterhead vindo exclusivamente da configuração do usuário.

**Independent Test**: Um Markdown completo do contrato, convertido com `--type meeting-minutes` e uma configuração que referencia o letterhead, gera TEX com todos os dados estruturados e sem pendências de validação.

### Tests for User Story 1

- [X] T009 [P] [US1] Add integration coverage for a documented complete meeting-minutes example with at least two participants and two pendencies, including participant groups and the pendency table in tests/test_integration.py
- [X] T010 [P] [US1] Add CLI coverage for `--type meeting-minutes` using YAML front matter and configured style packages in tests/test_cli.py

### Implementation for User Story 1

- [X] T011 [US1] Extend the meeting-minutes template context with normalized meeting data in src/md2tex/converter.py
- [X] T012 [US1] Render identification, period, client and Netra participant groups, and pendency table without embedding style defaults in src/md2tex/templates/meeting-minutes.tex.j2
- [X] T013 [US1] Preserve CLI-over-front-matter precedence for `client`, `author`, and `date` in meeting-minutes data in src/md2tex/metadata.py
- [X] T014 [US1] Run the complete-memory scenarios from tests/test_metadata.py tests/test_validator.py tests/test_cli.py and tests/test_integration.py

**Checkpoint**: Uma memória completa é convertida no layout estrutural esperado, mantendo o style letterhead sob controle de `config.yaml`.

---

## Phase 4: User Story 2 - Identificar informação obrigatória ausente (Priority: P2)

**Goal**: Informar toda ausência ou estrutura inválida e bloquear a saída de forma segura em modo estrito.

**Independent Test**: Cada campo obrigatório ou componente estrutural omitido produz diagnóstico nominal; com `--strict`, a saída inexistente não é criada e a saída existente não é modificada.

### Tests for User Story 2

- [X] T015 [P] [US2] Add parameterized tests for every required metadata field, required section, and invalid participant or pendency shape in tests/test_validator.py
- [X] T016 [P] [US2] Add integration tests proving strict mode avoids Mermaid/Pandoc and preserves missing or existing output for invalid meeting minutes in tests/test_integration.py
- [X] T017 [P] [US2] Add CLI diagnostic and exit-behavior coverage for invalid meeting-minutes metadata in tests/test_cli.py

### Implementation for User Story 2

- [X] T018 [US2] Treat meeting-minutes validation pendencies as a pre-output strict gate with actionable ValidationError messages in src/md2tex/converter.py
- [X] T019 [US2] Ensure normal validation reports every named meeting-minutes pendency while preserving normal TEX generation in src/md2tex/converter.py
- [X] T020 [US2] Run missing-field and strict-preservation scenarios in tests/test_validator.py tests/test_cli.py and tests/test_integration.py

**Checkpoint**: Campos ausentes são diagnosticados nominalmente e o modo estrito protege o destino de saída antes de trabalho externo.

---

## Phase 5: User Story 3 - Registrar reunião sem pendências (Priority: P3)

**Goal**: Aceitar e apresentar `Sem pendências`, além de permitir grupos de participantes vazios, sem aceitar tabelas de pendências incompletas.

**Independent Test**: Uma memória com as seções obrigatórias, grupos omitidos e a declaração `Sem pendências` converte sem aviso; uma tabela parcial continua inválida.

### Tests for User Story 3

- [ ] T021 [P] [US3] Add validator cases for `Sem pendências`, empty participant groups, and incomplete pendency tables in tests/test_validator.py
- [ ] T022 [P] [US3] Add integration coverage for rendering the no-pendency declaration and omitting empty participant groups in tests/test_integration.py

### Implementation for User Story 3

- [ ] T023 [US3] Recognize the exclusive `Sem pendências` declaration and distinguish it from missing or incomplete pendency content in src/md2tex/validator.py
- [ ] T024 [US3] Render the no-pendency declaration and avoid empty participant-group artifacts in src/md2tex/templates/meeting-minutes.tex.j2
- [ ] T025 [US3] Run no-pendency and empty-group scenarios in tests/test_validator.py and tests/test_integration.py

**Checkpoint**: Reuniões internas ou sem ações são documentos válidos e continuam claramente representadas.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentar o contrato público, validar o fluxo completo e preservar a qualidade do projeto.

- [ ] T026 [P] Document the meeting-minutes front matter, required fields, `Sem pendências`, and configured letterhead prerequisite in README.md
- [ ] T027 [P] Add a versioned meeting-minutes example matching the contract, with at least two participants and two pendencies, in examples/meeting-minutes.md
- [ ] T028 [P] Update release notes and the public version for the completed feature in RELEASES.md pyproject.toml and src/md2tex/__init__.py
- [ ] T029 Run ruff and the complete pytest suite in pyproject.toml
- [ ] T030 Execute every scenario in specs/004-update-meeting-minutes/quickstart.md and correct documentation discrepancies in README.md

---

## Dependencies & Execution Order

- Phase 1 has no dependencies.
- Phase 2 depends on T001–T003 and blocks all stories.
- US1 depends on T004–T008 and provides the renderable MVP.
- US2 depends on T004–T008 and the pre-output integration in US1; it may be developed after the shared foundation but should merge after US1.
- US3 depends on T004–T008 and can be implemented independently of US2 once the shared parser and validator exist.
- Polish depends on completed user stories.

```text
Setup → Foundational → US1 (MVP) → US2 → Polish
                     └──────────→ US3 ─┘
```

## Parallel Opportunities

- T002 and T003 can proceed in parallel with T001.
- Within US1, T009 and T010 can proceed in parallel before T011–T013.
- Within US2, T015, T016, and T017 can proceed in parallel.
- Within US3, T021 and T022 can proceed in parallel.
- T026, T027, and T028 modify distinct public-facing files and can proceed in parallel after behavior stabilizes.

## Implementation Strategy

### MVP First

1. Complete T001–T008.
2. Complete T009–T014.
3. Demonstrate a complete memory using YAML front matter and a user-configured letterhead style.

### Incremental Delivery

1. Add typed data, parser, and common validation foundation.
2. Add the complete rendered memory (US1).
3. Add named diagnostics and strict early blocking (US2).
4. Add the `Sem pendências` and empty-groups flow (US3).
5. Document the public contract and run the complete validation suite.


---

## Phase 7: Convergence

- [X] T031 Assert absent output and byte-for-byte preservation of existing output after strict meeting-minutes validation failure per T016 / US2 (partial)
