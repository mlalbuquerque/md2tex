# Tasks: md2tex 2.2.0

## Phase 1: Configuration foundation

- [X] T001 Implement strict `UserConfig` without style defaults in `src/md2tex/models.py`
- [X] T002 Implement required-key/type/schema validation in `src/md2tex/config.py`
- [X] T003 Add packaged initial YAML in `src/md2tex/templates/config.yaml`

## Phase 2: User Story 1 — Initialize configuration

- [X] T004 [US1] Implement `md2tex init` and overwrite protection in `src/md2tex/cli.py` and `src/md2tex/config.py`
- [X] T005 [P] [US1] Add init creation and overwrite tests in `tests/test_config.py` and `tests/test_cli.py`

## Phase 3: User Story 2 — Explicit conversion configuration

- [X] T006 [US2] Remove template style defaults in `src/md2tex/templates/*.tex.j2`
- [X] T007 [US2] Render typography and explicit YAML settings in `src/md2tex/templates/*.tex.j2`
- [X] T008 [P] [US2] Update configured conversion tests in `tests/test_integration.py`

## Phase 4: User Story 3 — Contract and legacy alignment

- [X] T009 [US3] Remove Netra compatibility aliases in `src/md2tex/errors.py` and `src/md2tex/filters/md2tex.lua`
- [X] T010 [US3] Validate CLI-provided style paths in `src/md2tex/cli.py`
- [X] T011 [P] [US3] Align feature docs, README and roadmap in `specs/`, `README.md` and `RELEASES.md`

## Phase 5: Validation and release

- [X] T012 Run the full pytest suite and compile a representative PDF
- [X] T013 Set package version 2.2.0 for release


## Release 2.2.0: Table configuration

- [X] T014 Add `tables` schema and CLI overrides in `src/md2tex/config.py`, `src/md2tex/cli.py` and `src/md2tex/models.py`
- [X] T015 Render configurable borders and zebra wrapping in `src/md2tex/pandoc.py` and `src/md2tex/filters/md2tex.lua`
- [X] T016 Update Netra style adapters in `/home/mlalbuquerque/Dropbox/Netra/projetos/netra-letterhead.sty`
- [X] T017 Validate table rendering and documentation for 2.2.0

## Phase 6: Convergence

- [X] T018 CRITICAL Make `--style` replace YAML `style_packages` and test CLI precedence per FR-006 / Constitution III (contradicts)
- [X] T019 Add invalid type, engine, and table-value schema tests per SC-003 / Constitution IV (partial)
- [X] T020 Normalize feature, plan, contract, and task release metadata to 2.2.0 (partial)

## Phase 7: PDF output convergence

- [X] T021 Ensure `--pdf --output FILE.pdf` renders TEX to a sibling `.tex` path before compilation (contradicts CLI output contract)
