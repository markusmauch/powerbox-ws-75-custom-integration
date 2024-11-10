from homeassistant.components.powerbox.modbus_data_coordinator import ModbusDataCoordinator
from homeassistant.components.select import SelectEntity
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, MODBUS_REGISTERS

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    device: dr.DeviceEntry = hass.data[DOMAIN][entry.entry_id].get("device")
    coordinator: ModbusDataCoordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    sensors = [
        OperatingModeSelect(coordinator, device),
        VentilationLevelModeSelect(coordinator, device),
    ]
    async_add_entities(sensors, update_before_add=False)


class PowerboxSelect(CoordinatorEntity, SelectEntity):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        self._device = device
        # self._attr_options = self.options
        # self._attr_current_option = self.options[0]
        self._current_value = 0  # Internal integer state
        super().__init__(coordinator)

    @property
    def options(self):
        return list(self.options_map.values())

    @property
    def current_option(self):
        return self.options_map.get(self._current_value)

    @property
    def unique_id(self):
        return f"{self.id}_{self._device.id}"

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

    def select_option(self, option):
        # Convert the selected string back to its integer key and store it
        for key, value in self.options_map.items():
            if value == option:
                self._current_value = key
                self.coordinator.write(self.id, key)
                self.schedule_update_ha_state()
                return
        raise ValueError(f"Option '{option}' is not a valid choice.")

    async def async_added_to_hass(self):
        """When entity is added to hass, set up the data update listener."""
        # Listen to coordinator updates and call the callback on new data
        self.coordinator.async_add_listener(self._update_from_coordinator_data)
        # Call the update once in case the coordinator has data already
        self._update_from_coordinator_data()

    def _update_from_coordinator_data(self):
        """Callback triggered by DataUpdateCoordinator."""
        data = self.coordinator.data
        if data is not None:
            new_value = self.coordinator.data.get(self.id)
            keys = list(self.options_map.keys())
            if new_value in keys and new_value != self._current_value:
                self._current_value = new_value
                self.async_write_ha_state()

    async def async_update(self):
        new_value = self.coordinator.data.get(self.id)
        print(new_value)


class OperatingModeSelect(PowerboxSelect):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def options_map(self):
        return {
            0: "Aus",
            1: "Manuell",
            2: "Auto-Sensor",
            3: "Eco-Zuluft",
            4: "Eco-Abluft"
        }

    @property
    def name(self):
        return "Betriebsart"

    @property
    def id(self):
        return "operating_mode"

    @property
    def icon(self):
        return "mdi:power-settings"


class VentilationLevelModeSelect(PowerboxSelect):
    def __init__(self, coordinator: ModbusDataCoordinator, device: dr.DeviceEntry):
        super().__init__(coordinator, device)

    @property
    def options_map(self):
        return {
            0: "Aus",
            1: "Feuchteschutz",
            2: "Reduziert",
            3: "Nennlüftung",
        }

    @property
    def name(self):
        return "Luftstufe"

    @property
    def id(self):
        return "ventilation_level"

    @property
    def icon(self):
        return "mdi:fan"