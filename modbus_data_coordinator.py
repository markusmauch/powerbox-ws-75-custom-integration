import logging
import datetime
from homeassistant.util import dt
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from typing import List

class ModbusPollingRegister():
    @property
    def unique_id(self) -> str:
        return None

    @property
    def address(self) -> int:
        return None

    @property
    def length(self) -> int:
        return 1

    @property
    def scale(self) -> float:
        return 1

    @property
    def precision(self) -> float:
        return 1

class ModbusDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, modbus_client: ModbusClient):
        super().__init__(
            hass,
            logging.getLogger(__name__),
            name="Modbus Coordinator",
            update_interval=timedelta(seconds=2),
        )
        self._modbus_client = modbus_client
        self._data = {}
        self._write_cache = {}
        self._polling_registers: List[ModbusPollingRegister] = []
        self._current_polling_register_index = -1
        self._busy = False
        self._last_updated: datetime = None

    @property
    def last_updated(self):
        return self._last_updated

    def add_polling_register(self, polling_register: ModbusPollingRegister):
        self._polling_registers.append( polling_register )

    def write(self, address: int, value: int):
        self._write_cache[address] = value

    async def _async_update_data(self):
        if self._busy == False:
            self._busy = True
            if self._write_cache.__len__() != 0:
                (address, value) = self._write_cache.popitem()
                try:
                    self._modbus_client.write_registers(address, value)
                    self._data[address] = value
                    self._last_updated = dt.now()
                except Exception as e:
                    self._data[address] = None
                    self.logger.error(f"Error writing value '{value}' to register {address}.")
            else:
                polling_register = self._next_polling_register()
                address = polling_register.address
                length = polling_register.length
                try:
                    registers = self._modbus_client.read_holding_registers(address, length).registers
                    for i in range(0, length):
                        self._data[address + i] = registers[i]
                    self._last_updated = dt.now()
                except Exception as e:
                    self._data[address] = None
                    self.logger.error(f"Error reading register {address}.")
            self._busy = False
        return self._data.copy()

    def _next_polling_register(self):
        self._current_polling_register_index = (self._current_polling_register_index + 1) % self._polling_registers.__len__()
        return self._polling_registers[self._current_polling_register_index]