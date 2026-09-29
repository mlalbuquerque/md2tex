# CLI Interface Contract

This feature modifies the public CLI interface for the `md2tex` command.

## New Arguments
- **`--cover FILE`**: Specifies a custom external template (Jinja2 format expected) that completely replaces the cover page.
  - **Type**: Path (must exist).
  - **Interaction**: Overrides cover logic for both `--type` and default templates. Can be used alongside either.

## Modified Rules
- **Mutual Exclusivity**: `--template FILE` and `--type PROFILE` cannot be used together in the same command execution.
  - **Error Output**: If both are provided, the CLI will immediately abort with a validation error (e.g., `Error: --template and --type are mutually exclusive. Please use only one.`).
