from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DiveraAlarmBinarySensor(coordinator)])

class DiveraAlarmBinarySensor(BinarySensorEntity):
    _attr_name = "Divera Alarm Aktiv"

    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def is_on(self):
        if not self.coordinator.data or "data" not in self.coordinator.data:
            return False
        alarms = self.coordinator.data.get("data", [])
        return len(alarms) > 0

    async def async_update(self):
        await self.coordinator.async_request_refresh()