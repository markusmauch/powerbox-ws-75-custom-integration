import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_UNIT_ID, CONF_POLLING_INTERVAL, CONF_NAME

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default="Powerbox", description="Device name"): str,
    vol.Required(CONF_HOST, default="powerbox.local", description="Powerbox hostname or IP address"): str,
    vol.Required(CONF_PORT, default=502, description="Modbus TCP port of the powerbox"): int,
    vol.Required(CONF_UNIT_ID, default=10, description="Modbus Unit ID of the powerbox"): int,
    vol.Required(CONF_POLLING_INTERVAL, default=5, description="Modbus polling interval"): int,
})

@config_entries.HANDLERS.register(DOMAIN)
class PowerboxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Modbus Integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=f"{user_input[CONF_NAME]}", data=user_input)

        # placeholders = {
        #     "host": self.hass.config.components["homeassistant"].translations["en"]["config"]["step"]["user"]["host"],
        #     "port": self.hass.config.components["homeassistant"].translations["en"]["config"]["step"]["user"]["port"],
        # }
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

#     @staticmethod
#     @callback
#     def async_get_options_flow(config_entry):
#         """Return the options flow."""
#         return OptionsFlow(config_entry)

# class OptionsFlow(config_entries.OptionsFlow):
#     """Options flow for Modbus Integration."""

#     def __init__(self, config_entry):
#         self.config_entry = config_entry

#     async def async_step_init(self, user_input=None):
#         if user_input is not None:
#             return self.async_create_entry(title="", data=user_input)

#         data_schema = vol.Schema(DATA_SCHEMA)
#         self.add_suggested_values_to_schema
#         current_options = self.config_entry.options
#         # vol.Schema({
#         #     vol.Required(CONF_HOST, default=current_options.get(CONF_HOST, "powerbox.local")): str,
#         #     vol.Required(CONF_PORT, default=current_options.get(CONF_PORT, 502)): int,
#         #     vol.Required(CONF_UNIT_ID, default=current_options.get(CONF_UNIT_ID, 10)): int,
#         #     vol.Required(CONF_POLLING_INTERVAL, default=current_options.get(CONF_POLLING_INTERVAL, 5)): int,
#         # })

#         return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
