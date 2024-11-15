from .const import DOMAIN
from .modbus_data_coordinator import ModbusDataCoordinator, ModbusInfo
from homeassistant.components.number import ConfigType, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import DiscoveryInfoType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.const import DEVICE_CLASS_TEMPERATURE, TIME_MINUTES
from homeassistant.helpers.entity import EntityCategory

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    sensors = [
        SleepFuctionDurationSensor(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxNumber(CoordinatorEntity, NumberEntity, ModbusInfo):
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
        if self.coordinator.data is not None and self.address in self.coordinator.data.keys():
            value = self.coordinator.data[self.address]
            return value * self.scale if value is not None else None
        else:
            return None


class SleepFuctionDurationSensor(PowerboxNumber):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.CONFIG
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "sleep_function_duration"

    @property
    def name(self):
        return "Dauer Einschlaffunktion"

    @property
    def icon(self):
        return "mdi:clock-start"

    @property
    def unit_of_measurement(self):
        return TIME_MINUTES

    @property
    def address(self) -> int:
        return 160

    @property
    def min_value(self):
        return 5

    @property
    def max_value(self):
        return 90

    @property
    def step(self):
        return 5

    @property
    def state(self):
        if self.coordinator.data is not None and self.address in self.coordinator.data.keys():
            value = self.coordinator.data[self.address]
            return value if value is not None else None
        else:
            return None

    def set_value(self, value: float) -> None:
        self.coordinator.write(self.address, int(value))
