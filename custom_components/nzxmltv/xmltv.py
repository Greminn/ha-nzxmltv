"""Minimal XMLTV parsing (blocking; run in an executor)."""

from __future__ import annotations

import gzip
import io
from dataclasses import dataclass
from datetime import datetime, timezone
from xml.etree import ElementTree as ET


@dataclass(slots=True)
class Programme:
    """A single scheduled programme."""

    channel: str
    start: datetime
    stop: datetime
    title: str
    description: str | None = None
    category: str | None = None
    icon: str | None = None
    episode: str | None = None


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y%m%d%H%M%S %z", "%Y%m%d%H%M %z", "%Y%m%d%H%M%S", "%Y%m%d%H%M"):
        try:
            dt = datetime.strptime(value, fmt)
        except ValueError:
            continue
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    return None


def _open(raw: bytes) -> io.BytesIO:
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return io.BytesIO(raw)


def parse_channels(raw: bytes) -> dict[str, str]:
    """Return {channel_id: display name}."""
    channels: dict[str, str] = {}
    for _, elem in ET.iterparse(_open(raw), events=("end",)):
        if elem.tag == "channel":
            cid = elem.get("id")
            name = elem.findtext("display-name")
            if cid:
                channels[cid] = (name or cid).strip()
            elem.clear()
        elif elem.tag == "programme":
            break  # channels precede programmes in XMLTV
    return channels


def parse_guide(
    raw: bytes, wanted: set[str] | None = None
) -> tuple[dict[str, str], dict[str, list[Programme]]]:
    """Parse channels and programmes, keeping only `wanted` channels' programmes."""
    channels: dict[str, str] = {}
    programmes: dict[str, list[Programme]] = {}

    for _, elem in ET.iterparse(_open(raw), events=("end",)):
        if elem.tag == "channel":
            cid = elem.get("id")
            if cid:
                channels[cid] = (elem.findtext("display-name") or cid).strip()
            elem.clear()
        elif elem.tag == "programme":
            cid = elem.get("channel")
            if cid and (wanted is None or cid in wanted):
                start = _parse_time(elem.get("start"))
                stop = _parse_time(elem.get("stop"))
                if start and stop:
                    icon = elem.find("icon")
                    programmes.setdefault(cid, []).append(
                        Programme(
                            channel=cid,
                            start=start,
                            stop=stop,
                            title=(elem.findtext("title") or "Unknown").strip(),
                            description=(elem.findtext("desc") or None),
                            category=(elem.findtext("category") or None),
                            icon=icon.get("src") if icon is not None else None,
                            episode=(elem.findtext("sub-title") or None),
                        )
                    )
            elem.clear()

    for items in programmes.values():
        items.sort(key=lambda p: p.start)
    return channels, programmes
