"""Support for Hottoh Stove sensor."""

# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
import logging
import json
from homeassistant.const import (
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    DEVICE_CLASS_ILLUMINANCE,
    STATE_UNKNOWN,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN

from homeassistant.const import ATTR_VOLTAGE

_LOGGER = logging.getLogger(__name__)
# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hottoh = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug(hottoh.Stove.toJson())
    stovedata = json.loads(hottoh.Stove.toJson())

    entities = []
    for info in stovedata:
        entities.append(StoveSensor(hottoh, info))

    _LOGGER.debug(entities)
    async_add_entities(entities, True)
    # new_devices = []
    # # for roller in hottoh.rollers:
    # new_devices.append(StoveSensor(hottoh.Stove())
    # # new_devices.append(IlluminanceSensor(roller))
    # async_add_devices(new_devices)


# This base class shows the common properties and methods for a sensor as used in this
# example. See each sensor for further details about properties and methods that
# have been overridden.
class SensorBase(Entity):
    """Base representation of a Hello World Sensor."""

    # should_poll = False

    def __init__(self, hottoh, info):
        """Initialize the sensor."""
        self._hottoh = hottoh
        self._info = info

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        # TODO: Create a uid based on mac adress
        # return {"identifiers": {(DOMAIN, self._hottoh.roller_id)}}
        return {"identifiers": {(DOMAIN, "stove")}}

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        # self._roller.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        # self._roller.remove_callback(self.async_write_ha_state)


class StoveSensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = DEVICE_CLASS_TEMPERATURE

    def __init__(self, hottoh, info):
        """Initialize the sensor."""
        super().__init__(hottoh, info)
        self._state = STATE_UNKNOWN
        self._hottoh
        self._info = info

    # As per the sensor, this must be a unique value within this domain. This is done
    # by using the device ID, and appending "_battery"
    @property
    def unique_id(self):
        """Return Unique ID string."""
        return "stove" + self._info["name"]

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
        return self._info["value"]

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


# This is another sensor, but more simple compared to the battery above. See the
# comments above for how each field works.
class IlluminanceSensor(SensorBase):
    """Representation of a Sensor."""

    device_class = DEVICE_CLASS_ILLUMINANCE

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._roller.roller_id}_illuminance"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._roller.name} Illuminance"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._roller.illuminance

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "lx"
