from .const import DOMAIN, get_localized_name
from .modbus_data_coordinator import ModbusDataCoordinator, ModbusPollingRegister
from homeassistant.components.sensor import ConfigType, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import DiscoveryInfoType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.const import DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS, PERCENTAGE, DEVICE_CLASS_HUMIDITY, VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    sensors = [
        RoomTemperatureSensor(coordinator, device),
        OutsideTemperatureSensor(coordinator, device),
        AirHumiditySensor(coordinator, device),
        VolumeFlowSupplySensor(coordinator, device),
        VolumeFlowExhaustSensor(coordinator, device),
        CurrentErrorSensor(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxSensor(CoordinatorEntity, SensorEntity, ModbusPollingRegister):
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
            return self.coordinator.data[self.address] * self.scale
        else:
            return None


class RoomTemperatureSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        coordinator.add_polling_register(self)
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "room_temperature"

    @property
    def name(self):
        return "Temperatur Raum"

    @property
    def icon(self):
        return "mdi:thermometer"

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def device_class(self):
        return DEVICE_CLASS_TEMPERATURE

    @property
    def address(self) -> int:
        return 700

    @property
    def scale(self) -> float:
        return 0.1


class OutsideTemperatureSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        coordinator.add_polling_register(self)
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "outside_temperature"

    @property
    def name(self):
        return "Temperatur Lufteintritt"

    @property
    def icon(self):
        return "mdi:thermometer"

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def device_class(self):
        return DEVICE_CLASS_TEMPERATURE

    @property
    def address(self) -> int:
        return 703

    @property
    def scale(self) -> float:
        return 0.1


class AirHumiditySensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        coordinator.add_polling_register(self)
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "air_humidity"

    @property
    def name(self):
        return "Luftfeuchtigkeit"

    @property
    def icon(self):
        return "mdi:water-percent"

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

    @property
    def device_class(self):
        return DEVICE_CLASS_HUMIDITY

    @property
    def address(self) -> int:
        return 750


class VolumeFlowSupplySensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        coordinator.add_polling_register(self)
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "volume_flow_supply"

    @property
    def name(self):
        return "Volumenstrom Zuluft"

    @property
    def icon(self):
        return "mdi:waves-arrow-right"

    @property
    def unit_of_measurement(self):
        return VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR

    @property
    def address(self) -> int:
        return 653


class VolumeFlowExhaustSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        coordinator.add_polling_register(self)
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "volume_flow_exhaust"

    @property
    def name(self):
        return "Volumenstrom Abluft"

    @property
    def icon(self):
        return "mdi:waves-arrow-left"

    @property
    def unit_of_measurement(self):
        return VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR

    @property
    def address(self) -> int:
        return 654


class CurrentErrorSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        coordinator.add_polling_register(self)
        super().__init__(coordinator, device)

    @property
    def state(self):
        error = 0
        # error = self.coordinator.data.get(self.id)
        return error

    @property
    def id(self):
        return "error"

    @property
    def name(self):
        return "Aktueller Fehler"

    @property
    def icon(self):
        return "mdi:message-alert"

    @property
    def address(self) -> int:
        return 401

    @property
    def length(self) -> int:
        return 2

    @property
    def state(self):
        if self.coordinator.data is not None and (self.address in self.coordinator.data.keys() and self.address + 1 in self.coordinator.data.keys()):
            high_word = self.coordinator.data[self.address]
            low_word = self.coordinator.data[self.address + 1]
            return (high_word << 16) | low_word
        else:
            return None