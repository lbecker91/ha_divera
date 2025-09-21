from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        DiveraAlarmSensor(coordinator, "Divera Alarm Message", "message"),
        DiveraAlarmSensor(coordinator, "Divera Alarm Address", "address"),
        DiveraAlarmSensor(coordinator, "Divera Alarm Time", "time"),
    ]
    async_add_entities(sensors)

class DiveraAlarmSensor(SensorEntity):
    def __init__(self, coordinator, name, key):
        self.coordinator = coordinator
        self._attr_name = name
        self._key = key

    @property
    def native_value(self):
        if not self.coordinator.data or "data" not in self.coordinator.data:
            return None
        alarms = self.coordinator.data.get("data", [])
        if alarms:
            return alarms[0].get(self._key)
        return None

    async def async_update(self):
        await self.coordinator.async_request_refresh()