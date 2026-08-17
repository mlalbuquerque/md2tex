# Tasks: md2tex 2.3.0 — Subtítulo pela CLI

**Input**: Design documents from /specs/002-add-cli-subtitle/

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-subtitle.md, quickstart.md

**Organization**: Tasks are grouped by user story and use exact repository paths.

## Phase 1: Setup

**Purpose**: Prepare shared assertions and the version baseline.

- [X] T001 Update version 2.3.0 expectations and CLI help assertions in tests/test_cli.py and tests/test_cli_subtitle.py.

---

## Phase 2: Foundational

**Purpose**: Add the explicit subtitle-presence state needed by every story.

- [X] T002 Extend conversion option and metadata resolution contracts in src/md2tex/models.py and src/md2tex/metadata.py to distinguish an omitted subtitle option from an explicitly empty one.

**Checkpoint**: Precedence foundation is ready; user stories can now be implemented.

---

## Phase 3: User Story 1 - Definir subtítulo na conversão (Priority: P1) MVP

**Goal**: Let authors pass a subtitle through the CLI and override front matter.

**Independent Test**: Convert a document with both front matter and CLI subtitle and verify the generated TEX contains only the CLI value below the title.

### Tests for User Story 1

- [X] T003 [P] [US1] Add CLI option forwarding and help coverage for --subtitle in tests/test_cli.py and tests/test_cli_subtitle.py.
- [X] T004 [P] [US1] Add metadata and rendered-TEX precedence coverage for CLI subtitle over front matter in tests/test_metadata.py.

### Implementation for User Story 1

- [X] T005 [US1] Define --subtitle, capture whether it was supplied, and pass it into ConversionOptions in src/md2tex/cli.py.
- [X] T006 [US1] Resolve the explicit CLI subtitle before front matter; treat whitespace-only values as absent while preserving non-empty subtitle text exactly as supplied in src/md2tex/metadata.py.

**Checkpoint**: A CLI-provided subtitle is independently functional and wins over front matter.

---

## Phase 4: User Story 2 - Gerar capa sem subtítulo (Priority: P2)

**Goal**: Generate no subtitle line when no usable subtitle exists or when the CLI explicitly clears it.

**Independent Test**: Convert documents with absent, empty, whitespace-only, and explicitly cleared subtitles and verify no subtitle line is emitted.

### Tests for User Story 2

- [X] T007 [P] [US2] Add absent, empty, whitespace-only, and explicit-empty subtitle cases in tests/test_metadata.py.

### Implementation for User Story 2

- [X] T008 [US2] Preserve the conditional subtitle rendering and ensure normalized empty values suppress it in src/md2tex/metadata.py.
- [X] T009 [US2] Verify empty subtitle handling remains consistent in src/md2tex/templates/base.tex.j2, src/md2tex/templates/report.tex.j2, src/md2tex/templates/meeting-minutes.tex.j2, src/md2tex/templates/adr.tex.j2, and src/md2tex/templates/technical-plan.tex.j2.

**Checkpoint**: Documents without a subtitle render a blank subtitle area without fallback text.

---

## Phase 5: User Story 3 - Consultar identificação completa na capa (Priority: P3)

**Goal**: Group document type with author, version, and date on every supported cover.

**Independent Test**: Render each profile and verify document type is in the identification block, not between title and subtitle.

### Tests for User Story 3

- [X] T010 [P] [US3] Add profile-cover assertions for document type placement in tests/test_metadata.py.

### Implementation for User Story 3

- [X] T011 [P] [US3] Move document type into the identification block in src/md2tex/templates/base.tex.j2, src/md2tex/templates/report.tex.j2, src/md2tex/templates/meeting-minutes.tex.j2, src/md2tex/templates/adr.tex.j2, and src/md2tex/templates/technical-plan.tex.j2.

**Checkpoint**: All supported covers separate the optional subtitle from identification metadata.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Align packaging, documentation, and end-to-end validation.

- [X] T012 [P] Update the distribution and public CLI version to 2.3.0 in pyproject.toml and src/md2tex/__init__.py.
- [X] T013 [P] Document --subtitle, precedence, empty behavior, version 2.3.0, and revised CLI reference in README.md.
- [X] T014 Run pytest -q and the scenarios in specs/002-add-cli-subtitle/quickstart.md; resolve regressions in affected files.

---

## Dependencies & Execution Order

- Phase 1 precedes Phase 2.
- Phase 2 blocks US1, US2, and US3 because they share explicit subtitle-presence semantics.
- US1 is the MVP and should complete before US2; US3 can proceed after Phase 2 but touches the same rendered output, so merge after US1 verification.
- Polish follows all selected stories.

## Parallel Opportunities

- T003 and T004 can be prepared in parallel because they cover different test layers.
- T007 and T010 can be prepared in parallel once the shared resolution contract is established.
- T011, T012, and T013 affect distinct template, packaging, and documentation files and can proceed in parallel after functional behavior is stable.

## Implementation Strategy

1. Complete T001–T006 and validate US1 as the MVP.
2. Add the empty-value behavior with T007–T009 and retest the subtitle contract.
3. Apply the cover-layout change with T010–T011.
4. Finish version, documentation, and full quickstart validation with T012–T014.

---

## Phase 7: Convergence

- [X] T015 Preserve leading and trailing whitespace in non-empty CLI and front-matter subtitles while treating whitespace-only values as absent; add regression coverage in src/md2tex/metadata.py and tests/test_metadata.py per SC-001 and Edge Cases (contradicts)
