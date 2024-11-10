import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_UNIT_ID

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST, default="192.168.0.197"): str,
    vol.Required(CONF_PORT, default=502): int,
    vol.Required(CONF_UNIT_ID, default=10): int,
})

class PowerboxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Modbus Integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=f"Powerbox {user_input[CONF_HOST]}", data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow."""
        return OptionsFlow(config_entry)

class OptionsFlow(config_entries.OptionsFlow):
    """Options flow for Modbus Integration."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Optional(CONF_PORT, default=self.config_entry.data.get(CONF_PORT, 502)): int,
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
