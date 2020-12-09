from zeroconf import ip6_addresses_to_indexes
from .const import StoveRegisters, StoveState
from .request import Request
import asyncio
import json
from .hottoh import Hottoh


class Stove(Hottoh):
    def __init__(self, ip="192.168.1.56", port=5001):
        super().__init__(ip, port)
        self._data = None
        self._info = None

    async def refresh(self):
        """Fetch data from the stove"""
        try:
            # Get info data from the stove
            self._info = await self._fetch("INF", [""])

            # Get working data from the stove
            self._data = await self._fetch("DAT", ["0"])

            # Get Chrono data from the stove
            self._chrono = await self._fetch("DAT", ["2"])

            return [
                {"item": "info", "value": self._formatInfo()},
                {"item": "data", "value": self._formatData()},
            ]
        except:
            raise

    def _formatData(self):
        js = []
        data = {"name": "state", "unit": "", "value": self._getStoveState()}
        js.append(data)
        data = {"name": "is_on", "unit": "", "value": self._getStoveIsOn()}
        js.append(data)
        data = {"name": "eco_mode", "unit": "", "value": self._getEcoMode()}
        js.append(data)
        data = {"name": "chrono_mode", "unit": "", "value": self._getChronoMode()}
        js.append(data)
        data = {
            "name": "temperature_room_1",
            "unit": "°C",
            "value": self._getTemperatureRoom1(),
        }
        js.append(data)
        data = {
            "name": "set_temperature_room_1",
            "unit": "°C",
            "value": self._getSetTemperatureRoom1(),
        }
        js.append(data)
        data = {
            "name": "smoke_temperature",
            "unit": "°C",
            "value": self._getSmokeTemperature(),
        }
        js.append(data)
        data = {"name": "power_level", "unit": "%", "value": self._getPowerLevel()}
        js.append(data)
        data = {
            "name": "set_power_level",
            "unit": "%",
            "value": self._getSetPowerLevel(),
        }
        js.append(data)
        data = {
            "name": "speed_fan_smoke",
            "unit": "rpm",
            "value": self._getSpeedFanSmoke(),
        }
        js.append(data)
        # data = {"name": "speed_fan_1", "unit": "rpm", "value": self._getSpeedFan1()}
        # js.append(data)
        # return json.dumps(js)
        return js

    def _formatInfo(self):
        js = []
        data = {"name": "fw", "unit": "", "value": self._getFirmwareVersion()}
        js.append(data)

        data = {"name": "wifi", "unit": "", "value": self._getWifiSignal()}
        js.append(data)

        data = {"name": "model", "unit": "", "value": self._getStoveType()}
        js.append(data)

        data = {"name": "manufacturer", "unit": "", "value": self._getManufacturer()}
        js.append(data)

        data = {"name": "mac", "unit": "", "value": self._getMac()}
        js.append(data)

        return js

    def _getFirmwareVersion(self):
        return self._info[StoveRegisters.INDEX_FW]

    def _getWifiSignal(self):
        return self._info[StoveRegisters.INDEX_WIFI]

    def _getPageIndex(self):
        return self._data[StoveRegisters.INDEX_PAGE]

    def _getManufacturer(self):
        if self._data[StoveRegisters.INDEX_MANUFACTURER] == "9":
            return "CMG"
        else:
            return str(self._data[StoveRegisters.INDEX_MANUFACTURER])

    def _getIsBitmapVisible(self):
        return self._data[StoveRegisters.INDEX_BITMAP_VISIBLE]

    def _getIsValid(self):
        return self._data[StoveRegisters.INDEX_VALID]

    def _getStoveType(self):
        return str(self._data[StoveRegisters.INDEX_STOVE_TYPE])

    def _getStoveState(self):
        if StoveState.STATUS_OFF == int(self._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "off_switched_off"
        if StoveState.STATUS_STARTING_1 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_1_check"
        if StoveState.STATUS_STARTING_2 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_2_clean_all"
        if StoveState.STATUS_STARTING_3 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_3_loading"
        if StoveState.STATUS_STARTING_4 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_4_loading"
        if StoveState.STATUS_STARTING_5 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_5_waiting"
        if StoveState.STATUS_STARTING_6 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_6_ignition"
        if StoveState.STATUS_STARTING_7 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "starting_7_stabilization"
        if StoveState.STATUS_POWER == int(self._data[StoveRegisters.INDEX_STOVE_STATE]):
            return "power"
        if StoveState.STATUS_STOPPING_1 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "stopping_1_wait_standby"
        if StoveState.STATUS_STOPPING_2 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "stopping_2_wait_standby"
        if StoveState.STATUS_ECO_STOP_1 == int(
            self._data[StoveRegisters.INDEX_STOVE_STATE]
        ):
            return "eco_stop_1_standby"
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

    def _getStoveIsOn(self):
        if self._data[StoveRegisters.INDEX_STOVE_ON] == "1":
            return "on"
        else:
            return "off"

    def _getEcoMode(self):
        if self._data[StoveRegisters.INDEX_ECO_MODE] == "1":
            return "on"
        else:
            return "off"

    def _getChronoMode(self):
        if self._data[StoveRegisters.INDEX_TIMER_ON] == "1":
            return "on"
        else:
            return "off"

    def _getTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1]) / 10)

    def _getSetTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1_SET]) / 10)

    def _getSetMaxTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MAX]) / 10)

    def _getSetMinTemperatureRoom1(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T1_SET_MIN]) / 10)

    def _getTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2]) / 10)

    def _getSetTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2_SET]) / 10)

    def _getSetMaxTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MAX]) / 10)

    def _getSetMinTemperatureRoom2(self):
        return str(int(self._data[StoveRegisters.INDEX_AMBIENT_T2_SET_MIN]) / 10)

    def _getTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER]) / 10)

    def _getSetTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER_SET]) / 10)

    def _getSetMaxTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER_SET_MAX]) / 10)

    def _getSetMinTemperatureWater(self):
        return str(int(self._data[StoveRegisters.INDEX_WATER_SET_MIN]) / 10)

    def _getSmokeTemperature(self):
        return str(int(self._data[StoveRegisters.INDEX_SMOKE_T]) / 10)

    def _getPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_LEVEL]

    def _getSetPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_SET]

    def _getSetMaxPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_MAX]

    def _getSetMinPowerLevel(self):
        return self._data[StoveRegisters.INDEX_POWER_MIN]

    def _getSpeedFanSmoke(self):
        return self._data[StoveRegisters.INDEX_FAN_SMOKE]

    def _getSpeedFan1(self):
        return self._data[StoveRegisters.INDEX_FAN_1]

    def _getSetSpeedFan1(self):
        return self._data[StoveRegisters.INDEX_FAN_1_SET]

    def _getSetMaxSpeedFan1(self):
        return self._data[StoveRegisters.INDEX_FAN_1_SET_MAX]

    def _getSpeedFan2(self):
        return self._data[StoveRegisters.INDEX_FAN_2]

    def _getSetSpeedFan2(self):
        return self._data[StoveRegisters.INDEX_FAN_2_SET]

    def _getSetMaxSpeedFan2(self):
        return self._data[StoveRegisters.INDEX_FAN_2_SET_MAX]

    def _getSpeedFan3(self):
        return self._data[StoveRegisters.INDEX_FAN_3]

    def _getSetSpeedFan3(self):
        return self._data[StoveRegisters.INDEX_FAN_3_SET]

    def _getSetMaxSpeedFan3(self):
        return self._data[StoveRegisters.INDEX_FAN_3_SET_MAX]
