from __future__ import annotations

from datetime import date
from typing import Any

from .models import ConversionOptions, DocumentMetadata
from .profiles import get_profile
from .utils import extract_title


def build_metadata(
    raw: dict[str, Any], body: str, options: ConversionOptions
) -> tuple[DocumentMetadata, str]:
    profile = get_profile(options.profile)
    extracted_title, body_without_h1 = extract_title(body)

    title = (
        options.title
        or _as_text(raw.get("title"))
        or extracted_title
        or options.input_path.stem.replace("-", " ").strip().title()
    )
    author = options.author or _as_text(raw.get("author")) or "Netra Tecnologia"
    document_date = options.date or _as_text(raw.get("date")) or date.today().isoformat()
    version = (
        options.document_version
        or _as_text(raw.get("version"))
        or _as_text(raw.get("document-version"))
        or "1.0"
    )
    client = options.client or _as_text(raw.get("client")) or ""
    subtitle = _as_text(raw.get("subtitle")) or ""
    status = _as_text(raw.get("status")) or ""
    document_type = _as_text(raw.get("document-type")) or profile["label"]

    known = {
        "title",
        "author",
        "date",
        "version",
        "document-version",
        "client",
        "subtitle",
        "status",
        "document-type",
    }
    extra = {key: value for key, value in raw.items() if key not in known}

    return (
        DocumentMetadata(
            title=title,
            author=author,
            date=document_date,
            version=version,
            client=client,
            document_type=document_type,
            subtitle=subtitle,
            status=status,
            extra=extra,
        ),
        body_without_h1 if extracted_title else body,
    )


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)
