"""The Hottoh integration."""

import asyncio
import logging
import json
from datetime import timedelta
from typing import Protocol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
    CoordinatorEntity,
)

from .pyhottoh import Stove
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Hottoh component."""
    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HHottoh from a config entry."""

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    async def async_update_data():
        """Fetch data from API endpoint."""
        try:
            hottoh = Stove(entry.data["ip_address"], entry.data["port"])
            _LOGGER.debug("Updating data from the stove")
            data = await hottoh.refresh()
            _LOGGER.debug(data)
            return data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with device: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="hottoh",
        update_method=async_update_data,
        update_interval=timedelta(seconds=15),
    )

    hass.data[DOMAIN][entry.entry_id] = coordinator

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
