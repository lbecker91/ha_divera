from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        DiveraAlarmSensor(coordinator, "Divera Alarm Message", "title"),
        DiveraAlarmSensor(coordinator, "Divera Alarm Address", "address"),
        DiveraAlarmSensor(coordinator, "Divera Alarm Time", "date"),
    ]
    async_add_entities(sensors)


class DiveraAlarmSensor(SensorEntity):
    def __init__(self, coordinator, name, key):
        self.coordinator = coordinator
        self._attr_name = name
        self._key = key

    @property
    def native_value(self):
        """Hole Wert des ersten Alarms laut Sorting-Liste."""
        if not self.coordinator.data or "data" not in self.coordinator.data:
            return None

        data = self.coordinator.data.get("data", {})
        items = data.get("items", {})
        sorting = data.get("sorting", [])

        if not sorting:
            return None

        first_id = sorting[0]
        alarm = items.get(str(first_id))
        if not alarm:
            return None

        return alarm.get(self._key)

    async def async_update(self):
        await self.coordinator.async_request_refresh()