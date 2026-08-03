from __future__ import annotations

from typing import Any

import yaml


FRONTMATTER_SEPARATOR = "---"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_SEPARATOR:
        return {}, text

    end_index: int | None = None
    for index in range(1, len(lines)):
        if lines[index].strip() in {"---", "..."}:
            end_index = index
            break

    if end_index is None:
        return {}, text

    raw_yaml = "\n".join(lines[1:end_index])
    metadata = yaml.safe_load(raw_yaml) or {}
    if not isinstance(metadata, dict):
        metadata = {}
    body = "\n".join(lines[end_index + 1 :])
    if text.endswith("\n"):
        body += "\n"
    return metadata, body
