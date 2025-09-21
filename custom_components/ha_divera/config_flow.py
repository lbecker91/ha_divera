import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_API_KEY

class DiveraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            api_key = user_input[CONF_API_KEY]

            # Optional: Probe-Request, um API-Key zu validieren
            if not api_key or len(api_key) < 10:
                errors["base"] = "invalid_auth"
            else:
                return self.async_create_entry(
                    title="Divera 24/7",
                    data={CONF_API_KEY: api_key},
                )

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str
        })

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )