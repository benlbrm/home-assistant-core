"""Support for Hottoh Stove sensor."""

# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
import logging
import json
import async_timeout
from datetime import timedelta
from homeassistant.const import (
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_POWER,
    TEMP_CELSIUS,
    PERCENTAGE,
    STATE_UNKNOWN,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .const import DOMAIN

from homeassistant.const import ATTR_VOLTAGE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    await coordinator.async_refresh()

    entities = []

    for data in coordinator.data:
        if data["item"] == "info":
            _LOGGER.debug(f"info: {data['value']}")
        if data["item"] == "data":
            _LOGGER.debug(f"data: {data['value']}")
            for info in data["value"]:
                _LOGGER.debug(info)
                entities.append(StoveSensor(coordinator, info))

    _LOGGER.debug(entities)
    async_add_entities(entities, True)


class StoveSensor(CoordinatorEntity):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor

    def __init__(self, coordinator, info):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._state = STATE_UNKNOWN
        self._info = info

    @property
    def device_class(self):
        if self._info["unit"] is TEMP_CELSIUS:
            return DEVICE_CLASS_TEMPERATURE
        elif self._info["unit"] is PERCENTAGE:
            return DEVICE_CLASS_POWER
        else:
            return None

    @property
    def icon(self):
        if self._info["unit"] == "rpm":
            return "mdi:fan"
        if self._info["name"] == "state":
            return "mdi:fire"
        else:
            return None

    # As per the sensor, this must be a unique value within this domain. This is done
    # by using the device ID, and appending "_battery"
    @property
    def unique_id(self):
        """Return Unique ID string."""
        mac = ""
        for data in self.coordinator.data:
            if data["item"] == "info":
                for info in data["value"]:
                    if info["name"] == "mac":
                        mac = info["value"]
        return DOMAIN + f".{mac}." + self._info["name"]

    # This property can return additional metadata about this device. Here it's
    # returning the voltage of the battery. The actual percentage is returned in
    # the state property below. These values are displayed in the entity details
    # screen at the bottom below the history graph.
    # A number of defined attributes are available, see the homeassistant.const module
    # for constants starting with ATTR_*.
    # Again, if these values change, the async_write_ha_state method should be called.
    # in this implementation, these values are assumed to be static.
    # Note this functionality to display addition data on an entity appears to be
    # exclusive to sensors. This information is not shown in the UI for a cover.
    # @property
    # def device_state_attributes(self):
    #     """Return the state attributes of the device."""
    #     attr = {}
    #     attr[ATTR_VOLTAGE] = self._hottoh.getPowerLevel()
    #     return attr

    # The value of this sensor. As this is a DEVICE_CLASS_BATTERY, this value must be
    # the battery level as a percentage (between 0 and 100)
    @property
    def state(self):
        """Return the state of the sensor."""
        for data in self.coordinator.data:
            if data["item"] == "data":
                for info in data["value"]:
                    if info["name"] is self._info["name"]:
                        _LOGGER.debug(
                            "name: {} - value: {}".format(
                                self._info["name"], info["value"]
                            )
                        )
                        return info["value"]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._info["unit"]

    # The same of this entity, as displayed in the entity UI.
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._info["name"]

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        fw = ""
        model = ""
        manufacturer = ""
        mac = ""
        for data in self.coordinator.data:
            if data["item"] == "info":
                for info in data["value"]:
                    if info["name"] == "fw":
                        fw = info["value"]
                    if info["name"] == "model":
                        model = info["value"]
                    if info["name"] == "manufacturer":
                        manufacturer = info["value"]
                    if info["name"] == "mac":
                        mac = info["value"]
        return {
            "identifiers": {(DOMAIN, mac)},
            "name": "Hottoh",  # self._hottoh.name,
            "sw_version": fw,  # self._hottoh.sw_version,
            "model": model,  # self._hottoh.model,
            "manufacturer": manufacturer,  # self._hottoh.manufacturer,
            # "via_device": (DOMAIN, mac),
        }
