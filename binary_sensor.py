import logging
from datetime import timedelta
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.powerbox.modbus_data_coordinator import ModbusDataCoordinator
from homeassistant.components.powerbox.select import OperatingModeSelect
from homeassistant.components.sensor import ConfigType, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback, DiscoveryInfoType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.const import CONF_NAME
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from .const import DOMAIN, MODBUS_REGISTERS
from homeassistant.const import DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS, PERCENTAGE, DEVICE_CLASS_HUMIDITY


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    sensors = [
        SleepFunctionBinarySensor(coordinator, device),
        PurgeVentilationBinarySensor(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._device = device
        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        return {
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.model,
            "identifiers": self._device.identifiers,
            "connections": self._device.connections,
            "sw_version": self._device.sw_version,
            "hw_version": self._device.hw_version,
        }

    @property
    def unique_id(self):
        return f"{self.id}_{self._device.id}"

    @property
    def state(self):
        if self.coordinator.data is None:
            return None
        else:
            value = self.coordinator.data.get(self.id)
            return "on" if value == 1 else "off"


class SleepFunctionBinarySensor(PowerboxBinarySensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def name(self):
        return "Einschlaffunktion"

    @property
    def id(self):
        return "sleep_function"

    @property
    def icon(self):
        return "mdi:bed-clock"


class PurgeVentilationBinarySensor(PowerboxBinarySensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def name(self):
        return "Einschlaffunktion"

    @property
    def id(self):
        return "purge_ventilation"

    @property
    def icon(self):
        return "mdi:weather-windy"