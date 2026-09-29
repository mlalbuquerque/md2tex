# Phase 1: Data Model

## `ConversionOptions` (Python Dataclass)

This feature introduces a modification to the core CLI options model `ConversionOptions` to support the new cover parameter.

### Added Fields
- **`cover_path: Path | None = None`**: Represents the optional path to the user-supplied external cover template (e.g., `my-cover.j2.tex`). Passed via the `--cover` CLI flag.

### State Transitions / Validation Rules
1. **Exclusivity Rule**: When `profile` (`--type`) is not "default" AND `template_path` (`--template`) is not `None`, the application MUST raise a `click.UsageError` indicating that `--type` and `--template` are mutually exclusive.
2. **Override Rule**: During LaTeX string generation, if `cover_path` is populated, the rendering engine MUST ignore the standard cover generation logic (whether from `--type` or default) and inject the Jinja2-rendered output of `cover_path` at the cover position.
