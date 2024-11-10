import logging
from homeassistant.components.powerbox.modbus_data_coordinator import ModbusDataCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from pymodbus.client.tcp import ModbusTcpClient as ModbusClient
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_UNIT_ID
from homeassistant.helpers import device_registry as dr
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    data = {}

    # Create the Modbus client
    modbus_client = ModbusClient(host, port=port)
    data["client"] = modbus_client

    device_registry = dr.async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, "powerbox_ws_75")},
        name="Powerbox",
        model="WS 75",
        manufacturer="Maico"
    )
    data["device"] = device

    coordinator = ModbusDataCoordinator(hass, modbus_client)
    data["coordinator"] = coordinator

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = data

    # Forward entry setup to the sensor platform
    await hass.config_entries.async_forward_entry_setup(entry, Platform.SENSOR)
    await hass.config_entries.async_forward_entry_setup(entry, Platform.BINARY_SENSOR)
    await hass.config_entries.async_forward_entry_setup(entry, Platform.SELECT)
    await hass.config_entries.async_forward_entry_setup(entry, Platform.BUTTON)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    domain_data = hass.data[DOMAIN]
    await hass.config_entries.async_forward_entry_unload(entry, Platform.SENSOR)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.BINARY_SENSOR)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.SELECT)
    await hass.config_entries.async_forward_entry_unload(entry, Platform.BUTTON)
    client: ModbusClient = domain_data[entry.entry_id].get("client")
    client.close()  # Close the Modbus client connection
    domain_data.pop(entry.entry_id)
    return True
