from .const import DOMAIN, get_localized_name
from .modbus_data_coordinator import ModbusDataCoordinator, ModbusInfo
from datetime import timedelta
from homeassistant.util import dt
from homeassistant.components.binary_sensor import DEVICE_CLASS_CONNECTIVITY, DEVICE_CLASS_RUNNING, BinarySensorEntity
from homeassistant.components.sensor import ConfigType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import DiscoveryInfoType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import EntityCategory

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    sensors = [
        SleepFunctionBinarySensor(coordinator, device),
        PurgeVentilationBinarySensor(coordinator, device),
        IsAliveBinarySensor(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxBinarySensor(CoordinatorEntity, BinarySensorEntity, ModbusInfo):
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
            return "on" if value == 1 else "off"
        else:
            return None


class SleepFunctionBinarySensor(PowerboxBinarySensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "sleep_function"

    @property
    def name(self):
        return "Einschlaffunktion"

    @property
    def icon(self):
        return "mdi:bed-clock"

    @property
    def address(self) -> int:
        return 559


class PurgeVentilationBinarySensor(PowerboxBinarySensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "purge_ventilation"

    @property
    def name(self):
        return "Stoßlüftung"

    @property
    def icon(self):
        return "mdi:weather-windy"

    @property
    def address(self) -> int:
        return 551


class IsAliveBinarySensor(PowerboxBinarySensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "last_updated"

    @property
    def name(self):
        return "Status"

    @property
    def icon(self):
        return "mdi:play-network"

    @property
    def device_class(self):
        return DEVICE_CLASS_RUNNING

    @property
    def state(self):
        if self.coordinator.last_updated == None:
            return "off"
        else:
            time_difference = abs(self.coordinator.last_updated - dt.now())
            return "off" if time_difference > timedelta(minutes=5) else "on"