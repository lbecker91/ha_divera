from datetime import timedelta
import aiohttp, logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class DiveraDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_key):
        super().__init__(
            hass,
            _LOGGER,
            name="Divera API",
            update_interval=timedelta(seconds=5),  # alle 5 Sekunden
        )
        self.api_key = api_key

    async def _async_update_data(self):
        url = f"https://app.divera247.com/api/v2/alarms?accesskey={self.api_key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"API Fehler: {resp.status}")
                    return await resp.json()
        except Exception as err:
            raise UpdateFailed(f"API Abfrage fehlgeschlagen: {err}")