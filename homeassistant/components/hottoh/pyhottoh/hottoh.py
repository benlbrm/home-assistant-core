# coding: utf-8

import asyncio
from .request import Request


class Hottoh:
    def __init__(self, ip="192.168.1.56", port=5001):
        """Communicate with HottoH stove wifi module"""
        self.port = port
        self.ip = ip
        self._data = None
        self._chrono = None
        self._info = None
        self._buffsize = 1024

    async def test_connection(self):
        """Test connectivity with the stove."""
        data = await self._fetch(command="DAT", parameters=["0"])
        if len(data) > 0:
            return True
        else:
            return False

    def _extractData(self, data):
        # Split data to an array
        return data.split(";")

    async def _fetch(self, command, parameters):
        """Get data from the stove"""
        request = Request(command=command, parameters=parameters)
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        writer.write(request.getRequest())
        await writer.drain()
        data = await reader.read(self._buffsize)
        writer.close()
        await writer.wait_closed()

        return self._extractData(f"{data}")

    def _getMac(self):
        return "aabbccddeeff"

    # def refreshData(self):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.settimeout(5)
    #     s.connect((self.ip, self.port))

    #     ## Get Stove Data ##
    #     request = Request(command="INF", parameters=[""])
    #     s.send(request.getRequest())
    #     temp = s.recv(self._buffsize)
    #     self._inf = self._extractData(str(temp))

    #     ## Get Stove Data ##
    #     request = Request(parameters=["0"])
    #     s.send(request.getRequest())
    #     temp = s.recv(self._buffsize)
    #     self._stove = self._extractData(str(temp))

    #     ## Get Chrono data ##
    #     request = Request(parameters=["1"])
    #     s.send(request.getRequest())
    #     temp = s.recv(self._buffsize)
    #     self._chrono = self._extractData(str(temp))

    #     ## Get Boiler Data ##
    #     request = Request(parameters=["2"])
    #     s.send(request.getRequest())
    #     temp = s.recv(self._buffsize)
    #     self._boiler = self._extractData(str(temp))

    #     s.close()

    #     self.Boiler = Boiler(self._boiler)
    #     self.Stove = Stove(self._stove)
    #     self.Chrono = Chrono(self._chrono)

    # def toJson(self):
    #     self.Stove = Stove(self._stove)
    #     self.Chrono = Chrono(self._chrono)
    #     self.Boiler = Boiler(self._boiler)
    #     j = "'timestamp': '', 'stove': {1}, 'chrono': {2}, 'boiler': {2}".format(
    #         self.Stove.toJson(), self.Chrono.toJson(), self.Boiler.toJson()
    #     )
    #     return "{" + j + "}"
