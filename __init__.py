from .modbus_data_coordinator import ModbusDataCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_POLLING_INTERVAL
from homeassistant.helpers import device_registry as dr
from homeassistant.const import CONF_NAME, Platform

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    name = entry.data[CONF_NAME]
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    polling_interval = entry.data[CONF_POLLING_INTERVAL]
    data = {}

    device_registry = dr.async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.unique_id)},
        name=name,
        model="WS 75",
        manufacturer="Maico"
    )
    data["device"] = device

    coordinator = ModbusDataCoordinator(hass, host, port, polling_interval)
    data["coordinator"] = coordinator

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = data

    # Forward entry setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SELECT, Platform.SWITCH, Platform.BUTTON, Platform.NUMBER])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    domain_data = hass.data[DOMAIN]
    await hass.config_entries.async_forward_entry_unload(entry, Platform.SENSOR)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.BINARY_SENSOR)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.SELECT)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.SWITCH)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.BUTTON)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.NUMBER)
    domain_data.pop(entry.entry_id)
    return True
