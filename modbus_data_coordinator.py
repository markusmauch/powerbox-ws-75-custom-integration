import logging
from homeassistant.util import dt
from datetime import timedelta
from .const import MODBUS_REGISTERS
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient

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
        self._current_register = -1
        self._update_list = {}
        self._busy = False
        self._last_updated: str = None

    @property
    def last_updated(self):
        return self._last_updated

    def write(self, unique_id: str, value: int):
        self._update_list[unique_id] = value

    async def _async_update_data(self):
        if self._busy == False:
            self._busy = True
            if self._update_list.__len__() != 0:
                (unique_id, value) = self._update_list.popitem()
                address = self._address_by_uniqe_id(unique_id)
                try:
                    self._modbus_client.write_registers(address, value)
                    self._data[unique_id] = value
                    self._last_updated = dt.now().isoformat()
                except Exception as e:
                    self._data[unique_id] = None
                    self.logger.error(f"Error writing '{unique_id}', register {address}.")
            else:
                modbus_register = self._next_register()
                address = modbus_register.get("address")
                unique_id = modbus_register.get("unique_id")
                length = modbus_register.get("length")
                scale = modbus_register.get("scale", 1)
                try:
                    value = self._modbus_client.read_holding_registers(address, length).registers[length - 1] * scale
                    self._data[unique_id] = value
                    self._last_updated = dt.now().isoformat()
                except Exception as e:
                    self._data[unique_id] = None
                    self.logger.error(f"Error reading '{unique_id}', register {address}.")
            self._busy = False
        return self._data.copy()

    def _next_register(self):
        self._current_register = (self._current_register + 1) % MODBUS_REGISTERS.__len__()
        return MODBUS_REGISTERS[self._current_register]

    def _address_by_uniqe_id(self, unique_id: str) -> int:
        for modbus_register in MODBUS_REGISTERS:
            if modbus_register.get("unique_id") == unique_id:
                return modbus_register.get("address")