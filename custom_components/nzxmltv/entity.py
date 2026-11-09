"""Base entity."""

from __future__ import annotations

from datetime import datetime

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import CONF_PROVIDER, DOMAIN, PROVIDERS
from .coordinator import NZXMLTVCoordinator
from .xmltv import Programme


class NZXMLTVEntity(CoordinatorEntity[NZXMLTVCoordinator]):
    """Entity bound to one channel."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: NZXMLTVCoordinator, channel_id: str) -> None:
        super().__init__(coordinator)
        self._channel_id = channel_id
        entry = coordinator.config_entry
        provider = entry.data[CONF_PROVIDER]
        self._base_id = f"{entry.entry_id}_{channel_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"NZXMLTV {PROVIDERS[provider][0]}",
            manufacturer="NZXMLTV",
            entry_type=None,
        )

    @property
    def channel_name(self) -> str:
        return self.coordinator.channel_names.get(self._channel_id, self._channel_id)

    @property
    def programmes(self) -> list[Programme]:
        return self.coordinator.data.get(self._channel_id, [])

    def current_and_next(self, now: datetime | None = None) -> tuple[Programme | None, Programme | None]:
        now = now or dt_util.utcnow()
        current = next_ = None
        for p in self.programmes:
            if p.start <= now < p.stop:
                current = p
            elif p.start > now:
                next_ = p
                break
        return current, next_
