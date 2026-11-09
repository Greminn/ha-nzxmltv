"""Calendar platform: one calendar per channel."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import NZXMLTVConfigEntry
from .const import CONF_CHANNELS
from .coordinator import NZXMLTVCoordinator
from .entity import NZXMLTVEntity
from .xmltv import Programme


def _event(p: Programme) -> CalendarEvent:
    desc = " - ".join(x for x in (p.episode, p.description) if x) or None
    return CalendarEvent(start=p.start, end=p.stop, summary=p.title, description=desc)


async def async_setup_entry(
    hass: HomeAssistant, entry: NZXMLTVConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    coordinator = entry.runtime_data
    channels = entry.options.get(CONF_CHANNELS, entry.data.get(CONF_CHANNELS, []))
    async_add_entities(NZXMLTVCalendar(coordinator, c) for c in channels)


class NZXMLTVCalendar(NZXMLTVEntity, CalendarEntity):
    """Programme schedule for a channel."""

    def __init__(self, coordinator: NZXMLTVCoordinator, channel_id: str) -> None:
        super().__init__(coordinator, channel_id)
        self._attr_unique_id = f"{self._base_id}_calendar"
        self._attr_name = None

    @property
    def name(self) -> str:  # type: ignore[override]
        return self.channel_name

    @property
    def event(self) -> CalendarEvent | None:
        current, next_ = self.current_and_next()
        p = current or next_
        return _event(p) if p else None

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        return [_event(p) for p in self.programmes if p.stop > start_date and p.start < end_date]
