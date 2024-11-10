from datetime import timedelta
import logging
from .const import DOMAIN, MODBUS_REGISTERS
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
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
        self.modbus_client = modbus_client

    async def _async_update_data(self):
        data = {}
        for modbus_register in MODBUS_REGISTERS:
            try:
                address = modbus_register.get("address")
                unique_id = modbus_register.get("unique_id")
                length = modbus_register.get("length")
                scale = modbus_register.get("scale", 1)
                data[unique_id] = self.modbus_client.read_holding_registers(address, length).registers[length - 1] * scale
            except Exception as e:
                unique_id = modbus_register.get("unique_id")
                address = modbus_register.get("address")
                _LOGGER.error(f"Failed to read value '{unique_id}', register {address}: {e}")
                data[modbus_register.get("unique_id")] = None
        return data

    def write(self, unique_id: str, value: int):
        if self.modbus_client.connect() == True:

            for modbus_register in MODBUS_REGISTERS:
                if modbus_register.get("unique_id") == unique_id:
                    try:
                        self.modbus_client.write_registers(modbus_register.get("address"), value)
                    except Exception as e:
                        _LOGGER.log(f"Error writing value for '{unique_id}': {e}")