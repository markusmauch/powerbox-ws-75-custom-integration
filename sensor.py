from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .low_pass_filter import LowPassFilter
from .modbus_data_coordinator import ModbusDataCoordinator, ModbusInfo


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get(
        "coordinator"
    )
    sensors = [
        RoomTemperatureSensor(coordinator, device),
        OutsideTemperatureSensor(coordinator, device),
        AirHumiditySensor(coordinator, device),
        VolumeFlowSupplySensor(coordinator, device),
        VolumeFlowExhaustSensor(coordinator, device),
        RemainingTimeDeviceFilterSensor(coordinator, device),
        CurrentErrorSensor(coordinator, device),
        CurrentHintSensor(coordinator, device),
        PowerSensor(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxSensor(CoordinatorEntity, SensorEntity, ModbusInfo):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._device = device
        self._attr_unique_id = f"{self._device.name.lower()}_{self.id}"
        self._attr_name = self.name
        self.entity_id = f"sensor.{self._attr_unique_id}"
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
        if (
            self.coordinator.data is not None
            and self.address in self.coordinator.data.keys()
        ):
            value = self.coordinator.data[self.address]
            return (
                self.round_with_precision(value * self.scale)
                if value is not None
                else None
            )
        else:
            return None

    def round_with_precision(self, value):
        return round(value / self.precision) * self.precision


class RoomTemperatureSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._filter = LowPassFilter()
        super().__init__(coordinator, device)

    @property
    def state(self):
        if (
            self.coordinator.data is not None
            and self.address in self.coordinator.data.keys()
        ):
            value = self.coordinator.data[self.address]
            if value is not None:
                if value > 32767:
                    value = value - 65536
                value = self.round_with_precision(value * self.scale)
                self._filter.add(value)
                return super().round_with_precision(self._filter.value)
        return None

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
        return UnitOfTemperature.CELSIUS

    @property
    def device_class(self):
        return SensorDeviceClass.TEMPERATURE

    @property
    def address(self) -> int:
        return 700

    @property
    def scale(self) -> float:
        return 0.1

    @property
    def precision(self) -> float:
        return 0.1


class OutsideTemperatureSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._filter = LowPassFilter()
        super().__init__(coordinator, device)

    @property
    def state(self):
        if (
            self.coordinator.data is not None
            and self.address in self.coordinator.data.keys()
        ):
            value = self.coordinator.data[self.address]
            if value is not None:
                if value > 32767:
                    value = value - 65536
                value = self.round_with_precision(value * self.scale)
                self._filter.add(value)
                return super().round_with_precision(self._filter.value)
        return None

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
        return UnitOfTemperature.CELSIUS

    @property
    def device_class(self):
        return SensorDeviceClass.TEMPERATURE

    @property
    def address(self) -> int:
        return 703

    @property
    def scale(self) -> float:
        return 0.1

    @property
    def precision(self) -> float:
        return 0.1


class AirHumiditySensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
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
        return SensorDeviceClass.HUMIDITY

    @property
    def address(self) -> int:
        return 750


class VolumeFlowSupplySensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
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
        return UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR

    @property
    def address(self) -> int:
        return 653


class VolumeFlowExhaustSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
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
        return UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR

    @property
    def address(self) -> int:
        return 654


class RemainingTimeDeviceFilterSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "remaining_time_device_filter"

    @property
    def name(self):
        return "Restlaufzeit Gerätefilter"

    @property
    def icon(self):
        return "mdi:air-filter"

    @property
    def unit_of_measurement(self):
        return UnitOfTime.DAYS

    @property
    def address(self) -> int:
        return 655


class RemainingTimeOutdoorFilterSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "remaining_time_outdoor_filter"

    @property
    def name(self):
        return "Restlaufzeit Außenfilter"

    @property
    def icon(self):
        return "mdi:filter-outline"

    @property
    def unit_of_measurement(self):
        return UnitOfTime.DAYS

    @property
    def address(self) -> int:
        return 656


class RemainingTimeRoomFilterSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "remaining_time_room_filter"

    @property
    def name(self):
        return "Restlaufzeit Raumfilter"

    @property
    def icon(self):
        return "mdi:air-filter"

    @property
    def unit_of_measurement(self):
        return UnitOfTime.DAYS

    @property
    def address(self) -> int:
        return 657


class CurrentErrorSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "current_error"

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
        if self.coordinator.data is not None:
            if (
                self.address in self.coordinator.data.keys()
                and self.address + 1 in self.coordinator.data.keys()
            ):
                if (
                    self.coordinator.data[self.address] is not None
                    and self.coordinator.data[self.address + 1] is not None
                ):
                    high_word: int = self.coordinator.data[self.address]
                    low_word: int = self.coordinator.data[self.address + 1]
                    return (high_word << 16) | low_word
        return None


class CurrentHintSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        super().__init__(coordinator, device)

    @property
    def id(self):
        return "current_hint"

    @property
    def name(self):
        return "Aktueller Hinweis"

    @property
    def icon(self):
        return "mdi:message-text"

    @property
    def address(self) -> int:
        return 403

    @property
    def length(self) -> int:
        return 2

    @property
    def state(self):
        if self.coordinator.data is not None:
            if (
                self.address in self.coordinator.data.keys()
                and self.address + 1 in self.coordinator.data.keys()
            ):
                if (
                    self.coordinator.data[self.address] is not None
                    and self.coordinator.data[self.address + 1] is not None
                ):
                    high_word: int = self.coordinator.data[self.address]
                    low_word: int = self.coordinator.data[self.address + 1]
                    return (high_word << 16) | low_word
        return None


class PowerSensor(PowerboxSensor):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def unit_of_measurement(self):
        return UnitOfPower.WATT

    @property
    def device_class(self):
        return SensorDeviceClass.POWER

    @property
    def id(self):
        return "power"

    @property
    def name(self):
        return "Leistung"

    @property
    def icon(self):
        """lightning-bolt"""
        return "mdi:flash"

    @property
    def address(self) -> int:
        return 650

    @property
    def length(self) -> int:
        return 1

    @property
    def state(self):
        if (
            self.coordinator.data is not None
            and self.address in self.coordinator.data.keys()
        ):
            value = self.coordinator.data[self.address]
            power_map = {
                0: 1,
                1: 5.2,
                2: 6.1,
                3: 8.3,
                4: 11.5,
            }
            return power_map.get(value)
        else:
            return None
