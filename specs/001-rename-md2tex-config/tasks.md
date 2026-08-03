# Tasks: Renaming to md2tex and Generic Style Configuration

**Input**: Design documents from `specs/001-rename-md2tex-config/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Explicit file paths included in every description

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Rename package directory structure and update build metadata

- [X] T001 Rename package directory `src/netra_md2tex` to `src/md2tex`
- [X] T002 Update package name, scripts entrypoint (`md2tex = "md2tex.cli:main"`), and packages lookup in `pyproject.toml`
- [X] T003 [P] Update module import statements across test files in `tests/test_compiler.py`, `tests/test_frontmatter.py`, `tests/test_integration.py`, `tests/test_utils.py`, and `tests/test_validator.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core configuration data models and loading infrastructure that MUST be complete before user stories

- [X] T004 Create `UserConfig` configuration data model in `src/md2tex/models.py`
- [X] T005 [P] Implement YAML configuration loading and error handling functions in `src/md2tex/config.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - System Renaming and Netra Decoupling (Priority: P1) 🎯 MVP

**Goal**: Rename CLI entry points to `md2tex` and remove all Netra-specific macros, templates, and branding from the codebase.

**Independent Test**: Execute `md2tex input.md -o output.tex` and verify that the generated LaTeX document is completely generic with no Netra headers or macros.

### Implementation for User Story 1

- [X] T006 [P] [US1] Add unit tests for system renaming and CLI identity in `tests/test_cli.py`
- [X] T007 [US1] Update main CLI entry points in `src/md2tex/cli.py` and `src/md2tex/__main__.py` to use `md2tex` name and branding
- [X] T008 [US1] Decouple LaTeX templates by removing Netra-specific preamble macros and logos from `src/md2tex/templates.py` and `src/md2tex/templates/`
- [X] T009 [US1] Refactor document conversion logic in `src/md2tex/converter.py` and `src/md2tex/compiler.py` to produce domain-agnostic LaTeX output
- [X] T010 [US1] Update user-facing documentation and usage examples in `README.md`

**Checkpoint**: User Story 1 fully functional and testable independently (MVP ready)

---

## Phase 4: User Story 2 - User Configuration File for Styling and Defaults (Priority: P1)

**Goal**: Load styling (`.sty` packages, document classes, page geometry, typography) exclusively from `~/.config/md2tex/config.yaml` without hardcoded code defaults.

**Independent Test**: Create `~/.config/md2tex/config.yaml` with custom style packages and page geometry, run `md2tex input.md`, and verify the generated LaTeX output includes those config settings.

### Implementation for User Story 2

- [X] T011 [P] [US2] Add unit tests for user configuration file loading and missing config error handling in `tests/test_config.py`
- [X] T012 [US2] Implement configuration resolution logic in `src/md2tex/config.py` to read `~/.config/md2tex/config.yaml` or path specified by `--config`
- [X] T013 [US2] Connect `UserConfig` into `src/md2tex/converter.py` and `src/md2tex/templates.py` to inject style packages (`.sty`) and preamble directives dynamically from config
- [X] T014 [US2] Update `src/md2tex/cli.py` to halt with a clear user notice when `~/.config/md2tex/config.yaml` is missing and no `--config` flag is passed
- [X] T014b [US2] Implement local `.sty` file path validation in `src/md2tex/config.py` and `src/md2tex/validator.py` and emit clear error warnings for unreachable paths

**Checkpoint**: User Stories 1 AND 2 functional independently

---

## Phase 5: User Story 3 - CLI Override and Precedence Hierarchy (Priority: P2)

**Goal**: Allow explicit CLI flags (`-s`, `-c`, `-e`, `-o`) to override values defined in `~/.config/md2tex/config.yaml`.

**Independent Test**: Pass `-s custom_extra.sty` on the command line and verify it overrides or appends to settings in `config.yaml`.

### Implementation for User Story 3

- [X] T015 [P] [US3] Add unit tests for CLI flag precedence over `config.yaml` settings in `tests/test_cli.py`
- [X] T016 [US3] Implement parameter merging in `src/md2tex/cli.py` ensuring CLI arguments take precedence over user config values

**Checkpoint**: All user stories functional independently

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end verification and code quality checks

- [X] T017 [P] Execute complete test suite using `pytest`, including execution time assertion (< 1s per standard conversion)
- [X] T018 Execute quickstart validation scenarios from `specs/001-rename-md2tex-config/quickstart.md`

---

## Phase 7: Packaging, Distribution & CI/CD Pipeline

**Purpose**: Interactive dependency manager (`md2tex setup`), PyInstaller standalone builds, and multi-OS GitHub Actions CI/CD matrix.

- [X] T019 Implement interactive dependency checker and installer (`md2tex setup` / `--check-deps`) in `src/md2tex/setup.py` and `src/md2tex/cli.py` to prompt and install TinyTeX / Mermaid CLI.
- [X] T020 Create `.github/workflows/ci.yml` GitHub Actions pipeline for testing matrix (Linux, macOS, Windows) and PyInstaller standalone build artifact generation with bundled Pandoc.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion
- **User Story 2 (Phase 4)**: Depends on Phase 2 completion
- **User Story 3 (Phase 5)**: Depends on Phase 3 and Phase 4 completion
- **Polish (Phase 6)**: Depends on completion of User Stories 1, 2, and 3

### Parallel Opportunities

- **T003** [P] can run in parallel with package structure updates.
- **T005** [P] can run in parallel with data model creation.
- **T006**, **T011**, **T015** test tasks can run in parallel within their respective phases.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete Phase 3 (User Story 1 - System Renaming and Netra Decoupling).
3. Validate MVP independently.

### Incremental Delivery

1. Setup + Foundational → Code structure ready.
2. User Story 1 → Renamed generic system (`md2tex`).
3. User Story 2 → User configuration file (`~/.config/md2tex/config.yaml`).
4. User Story 3 → CLI overrides and precedence hierarchy.
5. Polish → Full test suite and quickstart validation.
