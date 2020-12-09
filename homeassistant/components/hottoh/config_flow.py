"""Config flow for Hottoh."""
import logging
from functools import partial
import voluptuous as vol
from getmac import get_mac_address

from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_IP_ADDRESS, CONF_MAC, CONF_PORT
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.device_registry import format_mac

from .const import (
    DOMAIN,
    HOTTOH_DEFAULT_IP_ADDRESS,
    HOTTOH_DEFAULT_PORT,
)  # pylint:disable=unused-import
from .pyhottoh import Stove

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS, default=HOTTOH_DEFAULT_IP_ADDRESS): cv.string,
        vol.Optional(CONF_MAC): cv.string,
        vol.Required(CONF_PORT, default=HOTTOH_DEFAULT_PORT): int,
    }
)


async def validate_input(hass: core.HomeAssistant, data: dict):
    """Validate the user input allows us to connect."""

    hottoh = Stove(data[CONF_IP_ADDRESS], data[CONF_PORT])
    result = await hottoh.test_connection()
    if not result:
        raise CannotConnect

    # data[CONF_MAC] = await async_get_mac(hass, data[CONF_IP_ADDRESS])

    return {"title": data[CONF_IP_ADDRESS]}


async def async_get_mac(hass: core.HomeAssistant, host):
    """Get the mac address of the hottoh module."""
    try:
        mac_address = await hass.async_add_executor_job(
            partial(get_mac_address, **{"ip": host})
        )
        if not mac_address:
            mac_address = await hass.async_add_executor_job(
                partial(get_mac_address, **{"hostname": host})
            )
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error("Unable to get mac address: %s", err)
        mac_address = None

    if mac_address is not None:
        mac_address = format_mac(mac_address)
    else:
        raise CannotGetMacAddress
    return mac_address


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hottoh stove."""

    VERSION = 1
    # Pick one of the available connection classes in homeassistant/config_entries.py
    # This tells HA if it should be asking for updates, or it'll be notified of updates
    # automatically. This example uses PUSH, as the dummy hub will notify HA of
    # changes.
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # This goes through the steps to take the user through the setup process.
        # Using this it is possible to update the UI and prompt for additional
        # information. This example provides a single form (built from `DATA_SCHEMA`),
        # and when that has some validated input, it calls `async_create_entry` to
        # actually create the HA config entry. Note the "title" value is returned by
        # `validate_input` above.
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidIp:
                # The error string is set here, and should be translated.
                # This example does not currently cover translations, see the
                # comments on `DATA_SCHEMA` for further details.
                # Set the error on the `host` field, not the entire form.
                errors["ip_address"] = "wrong_ip_address"
            except InvalidPort:
                errors["port"] = "wrong_port_number"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidIp(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid ip address."""


class InvalidPort(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid connection port."""


class CannotGetMacAddress(exceptions.HomeAssistantError):
    """Error cannot get mac address of the device"""
