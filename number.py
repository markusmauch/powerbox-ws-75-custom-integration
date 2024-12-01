from .const import DOMAIN
from .modbus_data_coordinator import ModbusDataCoordinator, ModbusInfo
from homeassistant.components.number import ConfigType, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import DiscoveryInfoType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.const import UnitOfTime
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
        self._attr_unique_id = f"{self._device.name.lower()}_{self.id}"
        self._attr_name = self.name
        self.entity_id = f"number.{self._attr_unique_id}"
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
        self._attr_min_value = 5
        self._attr_max_value = 90
        self._attr_native_step = 5
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
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
    def address(self) -> int:
        return 160

    @property
    def state(self):
        if self.coordinator.data is not None and self.address in self.coordinator.data.keys():
            value = self.coordinator.data[self.address]
            return value if value is not None else None
        else:
            return None

    def set_value(self, value: float) -> None:
        self.coordinator.write(self.address, int(value))
