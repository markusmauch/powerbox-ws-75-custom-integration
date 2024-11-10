from .const import DOMAIN
from .modbus_data_coordinator import ModbusDataCoordinator
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    sensors = [
        SleepFunctionButton(coordinator, device),
        PurgeVentilationButton(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)

class PowerboxButton(CoordinatorEntity, ButtonEntity):
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


class SleepFunctionButton(PowerboxButton):
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

    async def async_press(self):
        self.coordinator.write(self.id, 1)


class PurgeVentilationButton(PowerboxButton):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def name(self):
        return "Stoßlüftung"

    @property
    def id(self):
        return "purge_ventilation"

    @property
    def icon(self):
        return "mdi:weather-windy"

    async def async_press(self):
        self.coordinator.write(self.id, 1)