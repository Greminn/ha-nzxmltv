"""Data coordinator for NZ XMLTV."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_CHANNELS, CONF_PROVIDER, CONF_VARIANT, DOMAIN, UPDATE_INTERVAL, guide_url
from .xmltv import Programme, parse_guide

_LOGGER = logging.getLogger(__name__)


async def async_download(hass: HomeAssistant, url: str) -> bytes:
    """Download a guide file."""
    session = async_get_clientsession(hass)
    async with session.get(url, timeout=120) as resp:
        resp.raise_for_status()
        return await resp.read()


class NZXMLTVCoordinator(DataUpdateCoordinator[dict[str, list[Programme]]]):
    """Fetch and parse the guide for the selected channels."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, config_entry=entry, update_interval=UPDATE_INTERVAL
        )
        self.channel_names: dict[str, str] = {}

    async def _async_update_data(self) -> dict[str, list[Programme]]:
        entry = self.config_entry
        url = guide_url(entry.data[CONF_PROVIDER], entry.data[CONF_VARIANT])
        wanted = set(entry.options.get(CONF_CHANNELS, entry.data.get(CONF_CHANNELS, [])))
        try:
            raw = await async_download(self.hass, url)
            channels, programmes = await self.hass.async_add_executor_job(
                parse_guide, raw, wanted
            )
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Error fetching {url}: {err}") from err
        self.channel_names = channels
        return programmes
