# Implementation Plan: custom-cover-support

**Branch**: `[008-custom-cover-support]` | **Date**: 2026-09-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/008-arch-doc-cover-update/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Decouple company-specific cover pages from the md2tex generic engine by introducing a `--cover` CLI argument that receives an external Jinja2 template. Enforce mutual exclusivity between `--template` and `--type`.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: `click` (CLI framework), `jinja2` (Template rendering)

**Storage**: Local Filesystem (I/O for reading .md, .j2.tex and writing .tex/.pdf)

**Testing**: `pytest` (local `.venv`)

**Target Platform**: Linux/macOS/Windows CLI environment

**Project Type**: CLI tool

**Performance Goals**: N/A (standard string replacement overhead)

**Constraints**: External covers must be Jinja2 compatible and fully override internal `type` covers.

**Scale/Scope**: Patch update adding one flag and one validation rule.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Generic & Decoupled Architecture**: PASS. The new `--cover` command explicitly removes the need to hardcode company-specific covers (like the architecture doc template) into the generic engine, deferring it to external user-provided assets.
- **II. Single Source of Truth for Defaults**: PASS. The cover definition continues to follow the hierarchy.
- **III. Strict CLI Precedence Hierarchy**: PASS. `--cover` passed via CLI overrides default internal behaviors.
- **IV. Testability & Quality Assurance**: PASS. Easily testable via `click.testing.CliRunner` in pytest.

## Project Structure

### Documentation (this feature)

```text
specs/008-arch-doc-cover-update/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
src/
└── md2tex/
    ├── cli.py           # Add --cover argument and exclusivity validation
    ├── models.py        # Add cover_path to ConversionOptions
    ├── converter.py     # Add logic to check for cover_path
    └── templates.py     # Add logic to load/render external Jinja2 cover
```

**Structure Decision**: Standard single Python package structure (src/md2tex/).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations found.
