"""Config flow for NZ XMLTV."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_CHANNELS,
    CONF_PROVIDER,
    CONF_VARIANT,
    DEFAULT_VARIANT,
    DOMAIN,
    PROVIDERS,
    guide_url,
)
from .coordinator import async_download
from .xmltv import parse_channels


def _channel_schema(channels: dict[str, str], default: list[str]) -> vol.Schema:
    options = [
        SelectOptionDict(value=cid, label=name)
        for cid, name in sorted(channels.items(), key=lambda kv: kv[1].lower())
    ]
    return vol.Schema(
        {
            vol.Required(CONF_CHANNELS, default=default): SelectSelector(
                SelectSelectorConfig(options=options, multiple=True, mode=SelectSelectorMode.DROPDOWN)
            )
        }
    )


class NZXMLTVConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._channels: dict[str, str] = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_PROVIDER])
            self._abort_if_unique_id_configured()
            try:
                raw = await async_download(
                    self.hass, guide_url(user_input[CONF_PROVIDER], user_input[CONF_VARIANT])
                )
                self._channels = await self.hass.async_add_executor_job(parse_channels, raw)
            except Exception:  # noqa: BLE001
                errors["base"] = "cannot_connect"
            else:
                if not self._channels:
                    errors["base"] = "no_channels"
                else:
                    self._data = user_input
                    return await self.async_step_channels()

        schema = vol.Schema(
            {
                vol.Required(CONF_PROVIDER, default="freeview"): SelectSelector(
                    SelectSelectorConfig(
                        options=[SelectOptionDict(value=k, label=v[0]) for k, v in PROVIDERS.items()],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(CONF_VARIANT, default=DEFAULT_VARIANT): SelectSelector(
                    SelectSelectorConfig(
                        options=["static", "standard", "lite"],
                        translation_key="variant",
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_channels(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            title = PROVIDERS[self._data[CONF_PROVIDER]][0]
            return self.async_create_entry(title=title, data={**self._data, **user_input})
        return self.async_show_form(
            step_id="channels", data_schema=_channel_schema(self._channels, [])
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return NZXMLTVOptionsFlow()


class NZXMLTVOptionsFlow(OptionsFlow):
    """Change the selected channels."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        entry = self.config_entry
        try:
            raw = await async_download(
                self.hass, guide_url(entry.data[CONF_PROVIDER], entry.data[CONF_VARIANT])
            )
            channels = await self.hass.async_add_executor_job(parse_channels, raw)
        except Exception:  # noqa: BLE001
            return self.async_abort(reason="cannot_connect")

        current = entry.options.get(CONF_CHANNELS, entry.data.get(CONF_CHANNELS, []))
        return self.async_show_form(
            step_id="init", data_schema=_channel_schema(channels, [c for c in current if c in channels])
        )
