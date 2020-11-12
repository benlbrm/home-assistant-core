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
    TEMP_CELSIUS,
    DEVICE_CLASS_ILLUMINANCE,
    STATE_UNKNOWN,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .const import DOMAIN

from homeassistant.const import ATTR_VOLTAGE

_LOGGER = logging.getLogger(__name__)
# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    entities = []
    for info in coordinator.data:
        entities.append(StoveSensor(coordinator, info))

    _LOGGER.debug(entities)
    async_add_entities(entities, True)


class StoveSensor(CoordinatorEntity):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = DEVICE_CLASS_TEMPERATURE

    def __init__(self, coordinator, info):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._state = STATE_UNKNOWN
        self._info = info

    # As per the sensor, this must be a unique value within this domain. This is done
    # by using the device ID, and appending "_battery"
    @property
    def unique_id(self):
        """Return Unique ID string."""
        return "stove" + "AAAAA" + self._info["name"]

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
        for info in self.coordinator.data:
            if info["name"] is self._info["name"]:
                _LOGGER.debug(
                    "name: {} - value: {}".format(self._info["name"], info["value"])
                )
                return info["value"]

    # The unit of measurement for this entity. As it's a DEVICE_CLASS_BATTERY, this
    # should be UNIT_PERCENTAGE. A number of units are supported by HA, for some
    # examples, see:
    # https://developers.home-assistant.io/docs/core/entity/sensor#available-device-classes
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
        # TODO: Create a uid based on mac adress
        return {
            "identifiers": {(DOMAIN, "stove")},
            "name": "Hottoh",  # self._hottoh.name,
            "sw_version": "1.0.0",  # self._hottoh.sw_version,
            "model": "Drum",  # self._hottoh.model,
            "manufacturer": "CMG",  # self._hottoh.manufacturer,
        }
