import asyncio
import logging
import datetime
from homeassistant.util import dt
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from typing import List


class ModbusInfo:
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


class AddressBlock:
    def __init__(self, address: int, length: int):
        self._address = address
        self._length = length

    @property
    def address(self) -> int:
        return self._address

    @property
    def length(self) -> int:
        return self._length


class ModbusDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host: str, port: int, update_interval: int):
        super().__init__(
            hass,
            logging.getLogger(__name__),
            name="Modbus Coordinator",
            update_interval=timedelta(seconds=update_interval),
        )
        self._host = host
        self._port = port
        self._data = {}
        self._write_cache = {}
        self._current_address_block_index = -1
        self._busy = False
        self._last_updated: datetime = None
        self._address_blocks: List[AddressBlock] = [
            AddressBlock(160, 1),
            AddressBlock(401, 5),
            AddressBlock(550, 2),
            AddressBlock(553, 2),
            AddressBlock(559, 1),
            AddressBlock(650, 8),
            AddressBlock(700, 1),
            AddressBlock(703, 5),
            AddressBlock(750, 3),
        ]

    @property
    def last_updated(self):
        return self._last_updated

    def write(self, address: int, value: int):
        self._write_cache[address] = value

    def soft_write(self, address: int, value: int):
        self._data[address] = value

    async def _async_update_data(self):
        if self._busy == False:
            self._busy = True
            modbus_client = ModbusClient(host=self._host, port=self._port)
            connected = modbus_client.connect()
            if connected == True:
                if self._write_cache.__len__() != 0:
                    (address, value) = self._write_cache.popitem()
                    try:
                        result = await asyncio.to_thread(
                            lambda: modbus_client.write_registers(address, [value])
                        )
                        if result.isError():
                            self._data[address] = None
                            self.logger.error(
                                f"Error writing value '{value}' to register {address}."
                            )
                        else:
                            self._data[address] = value
                            self._last_updated = dt.now()
                    except Exception as e:
                        self._data[address] = None
                        self.logger.error(
                            f"Error writing value '{value}' to register {address}."
                        )
                else:
                    address_block = self._next_address_block()
                    address = address_block.address
                    length = address_block.length
                    try:
                        result = await asyncio.to_thread(
                            lambda: modbus_client.read_holding_registers(
                                address, count=length
                            )
                        )
                        if result.isError():
                            self._data[address] = None
                            self.logger.error(f"Error reading register {address}.")
                        else:
                            registers = result.registers
                            for i in range(0, length):
                                self._data[address + i] = registers[i]
                            self._last_updated = dt.now()
                    except Exception as e:
                        self._data[address] = None
                        self.logger.error(f"Error reading register {address}.")
                self._busy = False
                modbus_client.close()
            else:
                self.logger.error(f"Unable to connect to modbus slave.")
        return self._data.copy()

    def worker():
        return 1

    def _next_address_block(self) -> AddressBlock:
        self._current_address_block_index = (
            self._current_address_block_index + 1
        ) % self._address_blocks.__len__()
        return self._address_blocks[self._current_address_block_index]
