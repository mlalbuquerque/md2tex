from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .models import ConversionOptions, DocumentMetadata, MeetingMinutesData, Participant, RevisionEntry
from .profiles import get_profile
from .utils import extract_title
from .validator import has_no_pending_items


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
    if options.profile == "software-architecture":
        system_name_raw = options.system_name if options.system_name is not None else _as_text(raw.get("system-name"))
        system_name = system_name_raw.strip()
        revisions = _normalize_revision_history(raw.get("revision-history"))
        if not revisions:
            revisions = [RevisionEntry(date=document_date, version=version, author=author)]
    else:
        system_name = ""
        revisions = []

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
        "system-name",
        "revision-history",
    }
    extra = {key: value for key, value in raw.items() if key not in known}
    meeting_minutes = (
        build_meeting_minutes_data(raw, body) if options.profile == "meeting-minutes" else None
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
            system_name=system_name,
            revision_history=revisions,
            extra=extra,
            meeting_minutes=meeting_minutes,
        ),
        body_without_h1 if extracted_title and not (options.title or _as_text(raw.get("title"))) else body,
    )


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)


def build_effective_raw_metadata(raw: dict[str, Any], options: ConversionOptions) -> dict[str, Any]:
    """Aplica ao front matter somente as sobrescritas explícitas da CLI."""
    effective = dict(raw)
    overrides = {
        "title": options.title,
        "author": options.author,
        "date": options.date,
        "version": options.document_version,
        "client": options.client,
        "system-name": options.system_name,
    }
    for key, value in overrides.items():
        if value is not None:
            effective[key] = value
    return effective


def _normalize_revision_history(value: Any) -> list[RevisionEntry]:
    if not isinstance(value, list):
        return []
    entries: list[RevisionEntry] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        entries.append(RevisionEntry(
            date=_as_text(item.get("date")).strip(),
            version=_as_text(item.get("version")).strip(),
            description=_as_text(item.get("description")).strip(),
            author=_as_text(item.get("author")).strip(),
        ))
    return entries


def build_meeting_minutes_data(raw: dict[str, Any], body: str = "") -> MeetingMinutesData:
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
        has_no_pending_items=has_no_pending_items(body),
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
