"""Sensor platform: now/next per channel."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import NZXMLTVConfigEntry
from .const import CONF_CHANNELS
from .coordinator import NZXMLTVCoordinator
from .entity import NZXMLTVEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: NZXMLTVConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    coordinator = entry.runtime_data
    channels = entry.options.get(CONF_CHANNELS, entry.data.get(CONF_CHANNELS, []))
    async_add_entities(NZXMLTVNowSensor(coordinator, c) for c in channels)


class NZXMLTVNowSensor(NZXMLTVEntity, SensorEntity):
    """Currently airing programme, with the next one as attributes."""

    def __init__(self, coordinator: NZXMLTVCoordinator, channel_id: str) -> None:
        super().__init__(coordinator, channel_id)
        self._attr_unique_id = f"{self._base_id}_now"

    @property
    def name(self) -> str:  # type: ignore[override]
        return f"{self.channel_name} now"

    @property
    def native_value(self) -> str | None:
        current, _ = self.current_and_next()
        return current.title if current else None

    @property
    def entity_picture(self) -> str | None:
        current, _ = self.current_and_next()
        return current.icon if current else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        current, next_ = self.current_and_next()
        attrs: dict[str, Any] = {"channel": self.channel_name}
        if current:
            attrs |= {
                "description": current.description,
                "category": current.category,
                "episode": current.episode,
                "start": current.start.isoformat(),
                "end": current.stop.isoformat(),
            }
        if next_:
            attrs |= {
                "next_title": next_.title,
                "next_start": next_.start.isoformat(),
                "next_end": next_.stop.isoformat(),
                "next_description": next_.description,
            }
        return attrs
