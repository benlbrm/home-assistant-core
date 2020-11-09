# coding: utf-8

import asyncio
import socket
from .request import Request
from .const import *
from .stove import Stove
from .chrono import Chrono
from .boiler import Boiler


class Hottoh:
    def __init__(self, ip="192.168.1.56", port=5001):
        """Communicate with HottoH stove wifi module"""
        self.port = port
        self.ip = ip
        self._stove = None
        self._boiler = None
        self._chrono = None
        self._buffsize = 2048
        self.Boiler = Boiler(self._boiler)
        self.Stove = Stove(self._stove)
        self.Chrono = Chrono(self._chrono)

    async def test_connection(self):
        """Test connectivity with the stove."""
        request = Request(parameters=["0"])
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        writer.write(request.getRequest())
        await writer.drain()
        data = await reader.read(self._buffsize)
        writer.close()
        await writer.wait_closed()
        if len(data) > 0:
            return True
        else:
            return False

    def refreshData(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((self.ip, self.port))

        ## Get Stove Data ##
        request = Request(parameters=["0"])
        s.send(request.getRequest())
        temp = s.recv(self._buffsize)
        self._stove = self._extractData(str(temp))

        ## Get Chrono data ##
        request = Request(parameters=["1"])
        s.send(request.getRequest())
        temp = s.recv(self._buffsize)
        self._chrono = self._extractData(str(temp))

        ## Get Boiler Data ##
        request = Request(parameters=["2"])
        s.send(request.getRequest())
        temp = s.recv(self._buffsize)
        self._boiler = self._extractData(str(temp))

        s.close()

    def toJson(self):
        self.Stove = Stove(self._stove)
        self.Chrono = Chrono(self._chrono)
        self.Boiler = Boiler(self._boiler)
        j = "'timestamp': '', 'stove': {1}, 'chrono': {2}, 'boiler': {2}".format(
            self.Stove.toJson(), self.Chrono.toJson(), self.Boiler.toJson()
        )
        return "{" + j + "}"

    def _extractData(self, data):
        # Split data to an array
        return data.split(";")
