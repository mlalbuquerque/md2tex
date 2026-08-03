from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from .errors import DependencyError, Md2TexError


MANUAL_NUMBERING_RE = re.compile(
    r"^(?P<prefix>\s{0,3}#{1,6}\s+)"
    r"(?:\d+(?:\.\d+)*[.)]?\s+)"
    r"(?P<title>.*)$"
)

FIRST_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def executable(name: str) -> str | None:
    return shutil.which(name)


def require_executable(name: str, hint: str = "") -> str:
    path = executable(name)
    if not path:
        suffix = f" {hint}" if hint else ""
        raise DependencyError(f"Executável obrigatório não encontrado: {name}.{suffix}")
    return path


def run_command(
    command: list[str],
    *,
    cwd: Path | None = None,
    verbose: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    if verbose:
        print("$", " ".join(str(part) for part in command))
    process = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and process.returncode != 0:
        details = process.stderr.strip() or process.stdout.strip()
        raise Md2TexError(
            f"Comando falhou ({process.returncode}): {' '.join(command)}\n{details}"
        )
    return process


def strip_manual_heading_numbering(markdown: str) -> str:
    converted: list[str] = []
    in_fence = False
    fence_token = ""
    for line in markdown.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = ""
            converted.append(line)
            continue
        if not in_fence:
            match = MANUAL_NUMBERING_RE.match(line)
            if match:
                line = f"{match.group('prefix')}{match.group('title')}"
        converted.append(line)
    return "\n".join(converted) + ("\n" if markdown.endswith("\n") else "")



def normalize_heading_levels(markdown: str) -> str:
    """Promove o menor nível de título encontrado para H1, sem alterar fenced code."""
    lines = markdown.splitlines()
    in_fence = False
    fence_token = ""
    levels: list[int] = []

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = ""
            continue
        if in_fence:
            continue
        match = re.match(r"^\s{0,3}(#{1,6})\s+", line)
        if match:
            levels.append(len(match.group(1)))

    if not levels:
        return markdown
    shift = min(levels) - 1
    if shift <= 0:
        return markdown

    converted: list[str] = []
    in_fence = False
    fence_token = ""
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = ""
            converted.append(line)
            continue
        if not in_fence:
            match = re.match(r"^(\s{0,3})(#{1,6})(\s+.*)$", line)
            if match:
                new_level = max(1, len(match.group(2)) - shift)
                line = f"{match.group(1)}{'#' * new_level}{match.group(3)}"
        converted.append(line)
    return "\n".join(converted) + ("\n" if markdown.endswith("\n") else "")

def extract_title(markdown: str) -> tuple[str | None, str]:
    match = FIRST_H1_RE.search(markdown)
    if not match:
        return None, markdown
    title = re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
    start, end = match.span()
    body = markdown[:start] + markdown[end:]
    body = body.lstrip("\n")
    return title, body


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9áàâãéêíóôõúüç\s-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "documento"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def unique_preserving_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
