from .const import DOMAIN
from .modbus_data_coordinator import ModbusDataCoordinator
from homeassistant.components.sensor import ConfigType, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import DiscoveryInfoType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.const import DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS, PERCENTAGE, DEVICE_CLASS_HUMIDITY


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    sensors = [
        RoomTemperatureSensor(coordinator, device),
        OutsideTemperatureSensor(coordinator, device),
        AirHumiditySensor(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxSensor(CoordinatorEntity, SensorEntity):
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
        return None if self.coordinator.data is None else self.coordinator.data.get(self.id)


class RoomTemperatureSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def name(self):
        return "Raumtemperatur"

    @property
    def id(self):
        return "room_temperature"

    @property
    def icon(self):
        return "mdi:thermometer"

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def device_class(self):
        return DEVICE_CLASS_TEMPERATURE


class OutsideTemperatureSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def name(self):
        return "Außentemperatur"

    @property
    def id(self):
        return "outside_temperature"

    @property
    def icon(self):
        return "mdi:thermometer"

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def device_class(self):
        return DEVICE_CLASS_TEMPERATURE


class AirHumiditySensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def name(self):
        return "Luftfeuchtigkeit"

    @property
    def id(self):
        return "air_humidity"

    @property
    def icon(self):
        return "mdi:water-percent"

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

    @property
    def device_class(self):
        return DEVICE_CLASS_HUMIDITY