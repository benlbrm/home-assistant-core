from .const import StoveRegisters
import json


class Stove:
    def __init__(self, data):
        self._data = data

    def toJson(self):
        js = []
        data = {"name": "page_index", "unit": "", "value": self.getPageIndex()}
        js.append(data)
        data = {"name": "manufacturer", "unit": "", "value": self.getManufacturer()}
        js.append(data)
        data = {
            "name": "is_bitmap_visible",
            "unit": "",
            "value": self.getIsBitmapVisible(),
        }
        js.append(data)
        data = {"name": "is_valid", "unit": "", "value": self.getIsValid()}
        js.append(data)
        data = {"name": "type", "unit": "", "value": self.getStoveType()}
        js.append(data)
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

        return json.dumps(js)

        # j += (
        #     "{'name': 'set_temperature_room_1', 'unit': '°C', 'value:"
        #     + self.getSetTemperatureRoom1()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_max_temperature_room_1', 'unit': '°C', 'value:"
        #     + self.getSetMaxTemperatureRoom1()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_min_temperature_room_1', 'unit': '°C', 'value:"
        #     + self.getSetMinTemperatureRoom1()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'temperature_room_2', 'unit': '°C', 'value:"
        #     + self.getTemperatureRoom2()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_temperature_room_2', 'unit': '°C', 'value:"
        #     + self.getSetTemperatureRoom2()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_max_temperature_room_2', 'unit': '°C', 'value:"
        #     + self.getSetMaxTemperatureRoom2()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_min_temperature_room_2', 'unit': '°C', 'value:"
        #     + self.getSetMinTemperatureRoom2()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'temperature_water', 'unit': '°C', 'value:"
        #     + self.getTemperatureWater()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_temperature_water', 'unit': '°C', 'value:"
        #     + self.getSetTemperatureWater()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_max_temperature_water', 'unit': '°C', 'value:"
        #     + self.getSetMaxTemperatureWater()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_min_temperature_water', 'unit': '°C', 'value:"
        #     + self.getSetMinTemperatureWater()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'power_level', 'unit': '%', 'value:" + self.getPowerLevel() + "},"
        # )
        # j += (
        #     "{'name': 'set_power_level', 'unit': '%', 'value:"
        #     + self.getSetPowerLevel()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_max_power_level', 'unit': '%', 'value:"
        #     + self.getSetMaxPowerLevel()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'set_min_power_level', 'unit': '%', 'value:"
        #     + self.getSetMinPowerLevel()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'speed_fan_smoke', 'unit': 'rpm', 'value:"
        #     + self.getSpeedFanSmoke()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'speed_fan_1', 'unit': 'rpm', 'value:"
        #     + self.getSpeedFan1()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'speed_max_fan_1', 'unit': 'rpm', 'value:"
        #     + self.getSetMaxSpeedFan1()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'speed_fan_smoke', 'unit': 'rpm', 'value:"
        #     + self.getSpeedFanSmoke()
        #     + "},"
        # )
        # j += (
        #     "{'name': 'speed_fan_smoke', 'unit': 'rpm', 'value:"
        #     + self.getSpeedFanSmoke()
        #     + "}"
        # )
        # j += "]"
        # return j.replace("'", '"')

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
        return self._data[StoveRegisters.INDEX_STOVE_STATE]

    def getStoveIsOn(self):
        return self._data[StoveRegisters.INDEX_STOVE_ON]

    def getEcoMode(self):
        return self._data[StoveRegisters.INDEX_ECO_MODE]

    def getChronoMode(self):
        return self._data[StoveRegisters.INDEX_TIMER_ON]

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
