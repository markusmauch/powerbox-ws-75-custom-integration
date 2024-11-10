from datetime import timedelta
import logging
from .const import MODBUS_REGISTERS
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient

_LOGGER = logging.getLogger(__name__)

class ModbusDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, modbus_client: ModbusClient):
        super().__init__(
            hass,
            _LOGGER,
            name="Modbus Coordinator",
            update_interval=timedelta(seconds=5),
        )
        self._update_cache = {}
        self._modbus_client = modbus_client

    async def _async_update_data(self):
        data = {}
        update_cache = self._update_cache.copy()
        processed_updates = self._process_updates()
        for modbus_register in MODBUS_REGISTERS:
            address = modbus_register.get("address")
            unique_id = modbus_register.get("unique_id")
            length = modbus_register.get("length")
            scale = modbus_register.get("scale", 1)
            if unique_id in processed_updates:
                data[unique_id] = update_cache.get(unique_id)
            else:
                try:
                    data[unique_id] = self._modbus_client.read_holding_registers(address, length).registers[length - 1] * scale
                except Exception as e:
                    unique_id = modbus_register.get("unique_id")
                    address = modbus_register.get("address")
                    data[modbus_register.get("unique_id")] = None
        return data

    def write(self, unique_id: str, value: int):
        self._update_cache[unique_id] = value

    def _process_updates(self):
        processed_updates = []
        if self._modbus_client.connect() == True:
            for (unique_id, value) in self._update_cache.items():
                address = self._address_by_uniqe_id(unique_id)
                try:
                    self._modbus_client.write_registers(address, value)
                    processed_updates.append(unique_id)
                except Exception as e:
                    _LOGGER.log(f"Error writing value for '{unique_id}': {e}")
            self._update_cache.clear()
        return processed_updates

    def _address_by_uniqe_id(self, unique_id: str) -> int:
        for modbus_register in MODBUS_REGISTERS:
            if modbus_register.get("unique_id") == unique_id:
                return modbus_register.get("address")