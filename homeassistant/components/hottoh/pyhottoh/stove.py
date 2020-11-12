from zeroconf import ip6_addresses_to_indexes
from .const import StoveRegisters, StoveState
from .request import Request
import asyncio
import json


class Stove:
    def __init__(self, data):
        self._data = data

    def getData(self):
        js = []
        data = {"name": "state", "unit": "", "value": self.getStoveState()}
        js.append(data)
        data = {"name": "is_on", "unit": "", "value": self.getStoveIsOn()}
        js.append(data)
        data = {"name": "eco_mode", "unit": "", "value": self.getEcoMode()}
        js.append(data)
        data = {"name": "chrono_mode", "unit": "", "value": self.getChronoMode()}
        js.append(data)
        data = {
            "name": "temperature_room_1",
            "unit": "°C",
            "value": self.getTemperatureRoom1(),
        }
        js.append(data)
        data = {
            "name": "set_temperature_room_1",
            "unit": "°C",
            "value": self.getSetTemperatureRoom1(),
        }
        js.append(data)
        data = {
            "name": "smoke_temperature",
            "unit": "°C",
            "value": self.getSmokeTemperature(),
        }
        js.append(data)
        data = {"name": "power_level", "unit": "%", "value": self.getPowerLevel()}
        js.append(data)
        data = {
            "name": "set_power_level",
            "unit": "%",
            "value": self.getSetPowerLevel(),
        }
        js.append(data)
        data = {
            "name": "speed_fan_smoke",
            "unit": "rpm",
            "value": self.getSpeedFanSmoke(),
        }
        js.append(data)
        # data = {"name": "speed_fan_1", "unit": "rpm", "value": self.getSpeedFan1()}
        # js.append(data)
        # return json.dumps(js)
        return js

    def getPageIndex(self):
        return self._data[StoveRegisters.INDEX_PAGE]

    def getManufacturer(self):
        return self._data[StoveRegisters.INDEX_MANUFACTURER]

    def getIsBitmapVisible(self):
        return self._data[StoveRegisters.INDEX_BITMAP_VISIBLE]

    def getIsValid(self):
        return self._data[StoveRegisters.INDEX_VALID]

    def getStoveType(self):
        return self._data[StoveRegisters.INDEX_STOVE_TYPE]

    def getStoveState(self):
        if StoveState.STATUS_OFF == int(self._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "off"
        if StoveState.STATUS_STARTING_1 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_1"
        if StoveState.STATUS_STARTING_2 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_2"
        if StoveState.STATUS_STARTING_3 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_3"
        if StoveState.STATUS_STARTING_4 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_4"
        if StoveState.STATUS_STARTING_5 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_5"
        if StoveState.STATUS_STARTING_6 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_6"
        if StoveState.STATUS_STARTING_7 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_7"
        if StoveState.STATUS_POWER == int(self._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "power"
        if StoveState.STATUS_STOPPING_1 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "stopping_1"
        if StoveState.STATUS_STOPPING_2 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "stopping_2"
        if StoveState.STATUS_ECO_STOP_1 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "eco_stop_1"
        if StoveState.STATUS_ECO_STOP_2 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "eco_stop_2"
        if StoveState.STATUS_ECO_STOP_3 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "eco_stop_3"
        if StoveState.STATUS_LOW_PELLET == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "low_pellet"
        if StoveState.STATUS_END_PELLET == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "end_pellet"
        if StoveState.STATUS_BLACK_OUT == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "black_out"
        if (
            StoveState.STATUS_ANTI_FREEZE
            == self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "anti_freeze"

    def getStoveIsOn(self):
        if self._data[StoveRegisters.INDEX_STOVE_ON] == "1":
            return "on"
        else:
            return "off"

    def getEcoMode(self):
        if self._data[StoveRegisters.INDEX_ECO_MODE] == "1":
            return "on"
        else:
            return "off"

    def getChronoMode(self):
        if self._data[StoveRegisters.INDEX_TIMER_ON] == "1":
            return "on"
        else:
            return "off"

    def getTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1]) / 10)

    def getSetTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1_SET]) / 10)

    def getSetMaxTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MAX]) / 10)

    def getSetMinTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MIN]) / 10)

    def getTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2]) / 10)

    def getSetTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2_SET]) / 10)

    def getSetMaxTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MAX]) / 10)

    def getSetMinTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MIN]) / 10)

    def getTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER]) / 10)

    def getSetTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER_SET]) / 10)

    def getSetMaxTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER_SET_MAX]) / 10)

    def getSetMinTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER_SET_MIN]) / 10)

    def getSmokeTemperature(self):
        return str(int(self._data[StoveRegisters.INDEX_SMOKE_T]) / 10)

    def getPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_LEVEL]

    def getSetPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_SET]

    def getSetMaxPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_MAX]

    def getSetMinPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_MIN]

    def getSpeedFanSmoke(self):
        return self._data[StoveRegisters.INDEX_FAN_SMOKE]

    def getSpeedFan1(self):
        return self._data[StoveRegisters.INDEX_FAN_1]

    def getSetSpeedFan1(self):
        return self._data[StoveRegisters.INDEX_FAN_1_SET]

    def getSetMaxSpeedFan1(self):
        return self._data[StoveRegisters.INDEX_FAN_1_SET_MAX]

    def getSpeedFan2(self):
        return self._data[StoveRegisters.INDEX_FAN_2]

    def getSetSpeedFan2(self):
        return self._data[StoveRegisters.INDEX_FAN_2_SET]

    def getSetMaxSpeedFan2(self):
        return self._data[StoveRegisters.INDEX_FAN_2_SET_MAX]

    def getSpeedFan3(self):
        return self._data[StoveRegisters.INDEX_FAN_3]

    def getSetSpeedFan3(self):
        return self._data[StoveRegisters.INDEX_FAN_3_SET]

    def getSetMaxSpeedFan3(self):
        return self._data[StoveRegisters.INDEX_FAN_3_SET_MAX]
