from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .models import ConversionOptions, DocumentMetadata, MeetingMinutesData, Participant
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
    author = options.author or _as_text(raw.get("author")) or ""
    document_date = options.date or _as_text(raw.get("date")) or datetime.now(timezone.utc).date().isoformat()
    version = (
        options.document_version
        or _as_text(raw.get("version"))
        or _as_text(raw.get("document-version"))
        or "1.0"
    )
    client = options.client or _as_text(raw.get("client")) or ""
    subtitle_source = (
        options.subtitle if options.subtitle is not None else _as_text(raw.get("subtitle"))
    )
    subtitle = subtitle_source if subtitle_source.strip() else ""
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
    meeting_minutes = (
        build_meeting_minutes_data(raw) if options.profile == "meeting-minutes" else None
    )

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
            meeting_minutes=meeting_minutes,
        ),
        body_without_h1 if extracted_title else body,
    )


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)


def build_meeting_minutes_data(raw: dict[str, Any]) -> MeetingMinutesData:
    """Normaliza período e participantes sem ocultar erros do validador."""
    period = raw.get("period")
    period_values = period if isinstance(period, dict) else {}
    participants = raw.get("participants")
    participant_groups = participants if isinstance(participants, dict) else {}

    return MeetingMinutesData(
        period_start=_as_text(period_values.get("start")).strip(),
        period_end=_as_text(period_values.get("end")).strip(),
        client_participants=_normalize_participants(participant_groups.get("client"), "client"),
        netra_participants=_normalize_participants(participant_groups.get("netra"), "netra"),
    )


def _normalize_participants(value: Any, group: str) -> list[Participant]:
    if not isinstance(value, list):
        return []
    return [
        Participant(
            name=_as_text(item.get("name")).strip(),
            role=_as_text(item.get("role")).strip(),
            group=group,
        )
        for item in value
        if isinstance(item, dict)
    ]
