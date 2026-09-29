# Implementation Tasks: custom-cover-support

**Branch**: `[008-custom-cover-support]` | **Date**: 2026-09-28
**Plan**: `/specs/008-arch-doc-cover-update/plan.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

*(Project is already initialized; no foundational setup tasks required)*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T001 Update `ConversionOptions` model with `cover_path` property in `src/md2tex/models.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Apply custom cover overlay (Priority: P1) 🎯 MVP

**Goal**: Implement the `--cover` argument to supply a custom external Jinja2 template overriding default cover generation.

**Independent Test**: Execute the command described in `quickstart.md` Scenario 2. Verify that the generated `.tex` file begins with the content defined in the external cover template, and that template variables (like title) are correctly resolved.

### Implementation for User Story 1

- [x] T002 [US1] Add `--cover` CLI flag mapped to `cover_path` in `src/md2tex/cli.py`, ensuring `click.Path(exists=True)` is configured for file validation.
- [x] T003 [US1] Modify template rendering logic in `src/md2tex/converter.py` (and/or `src/md2tex/templates.py`) to inject and process the external Jinja2 `--cover` file, catching Jinja2 template errors to provide a clear error message.
- [x] T004 [US1] Add unit test for `--cover` functionality in `tests/test_cli.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Prevent conflicting configurations (Priority: P2)

**Goal**: Raise a validation error when both `--template` and `--type` (non-default) are provided.

**Independent Test**: Execute the command described in `quickstart.md` Scenario 1. Verify that `click.UsageError` correctly blocks execution immediately.

### Implementation for User Story 2

- [x] T005 [US2] Add mutual exclusivity validation block in `src/md2tex/cli.py` that raises a `click.UsageError` if both `--template` and `--type` are used.
- [x] T006 [US2] Add unit test for mutual exclusivity rule in `tests/test_cli.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T007 Run `specs/008-arch-doc-cover-update/quickstart.md` validation to guarantee all scenarios pass.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: Starts immediately.
- **User Stories (Phase 3+)**: Depend on Foundational phase completion.
  - User stories can then proceed in sequential priority order (P1 → P2).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2). No dependencies on US2.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2). Totally independent from US1. Can be done in parallel.

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- US1 (T002, T003, T004) and US2 (T005, T006) can be developed entirely in parallel since they touch different behaviors of `cli.py`.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
2. Complete Phase 3: User Story 1
3. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Complete Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP!
3. Add User Story 2 → Test independently
