from .const import DOMAIN
from .modbus_data_coordinator import ModbusDataCoordinator, ModbusInfo
from datetime import timedelta
from homeassistant.util import dt
from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
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
        IsAliveBinarySensor(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxBinarySensor(CoordinatorEntity, BinarySensorEntity, ModbusInfo):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._device = device
        self._attr_unique_id = f"{self._device.name.lower()}_{self.id}"
        self._attr_name = self.name
        self.entity_id = f"binary_sensor.{self._attr_unique_id}"
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
    def state(self):
        if self.coordinator.data is not None and self.address in self.coordinator.data.keys():
            value = self.coordinator.data[self.address]
            return "on" if value == 1 else "off"
        else:
            return None


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
        return BinarySensorDeviceClass.RUNNING

    @property
    def state(self):
        if self.coordinator.last_updated == None:
            return "off"
        else:
            time_difference = abs(self.coordinator.last_updated - dt.now())
            return "off" if time_difference > timedelta(minutes=5) else "on"