from .const import DOMAIN, get_localized_name
from .modbus_data_coordinator import ModbusDataCoordinator, ModbusInfo
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
        ResetErrorButton(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)

class PowerboxButton(CoordinatorEntity, ButtonEntity, ModbusInfo):
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

    def press(self) -> None:
        """Press the button."""
        raise NotImplementedError()


class ResetErrorButton(PowerboxButton):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "reset_error"

    @property
    def name(self):
        return "Fehlerspeicher zurücksetzen"

    @property
    def icon(self):
        return "mdi:restart-alert"

    @property
    def address(self) -> int:
        return 559

    def press(self):
        self.coordinator.write(self.address, 1)
