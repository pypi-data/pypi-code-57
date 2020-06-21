"""Define a client to interact with Weatherbit."""
import asyncio
import logging
from typing import Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from weatherbitpypi.errors import InvalidApiKey, RequestError
from weatherbitpypi.const import (
    BASE_URL,
    DEFAULT_TIMEOUT,
)
from weatherbitpypi.data_classes import (
    CurrentData,
    ForecastDailyData,
    ForecastHourlyData,
    WeatherAlerts,
)

_LOGGER = logging.getLogger(__name__)

class Weatherbit:
    """Weatherbit Current Conditions Client."""

    def __init__(
        self,
        api_key: str,
        latitude: float,
        longitude: float,
        language: str="en",
        units: str = "M",
        session: Optional[ClientSession] = None,
        ):
        self._api_key = api_key
        self._latitude = latitude
        self._longitude = longitude
        self._language = language
        self._units = units
        self._session: ClientSession = session
        self.req = session

    async def async_get_city_name(self) -> None:
        return await self._city_name_by_lat_lon()

    async def async_get_current_data(self) -> None:
        return await self._get_current_data()

    async def async_get_forecast_daily(self) -> None:
        return await self._get_forecast_daily()

    async def async_get_forecast_hourly(self) -> None:
        return await self._get_forecast_hourly()

    async def async_get_weather_alerts(self) -> None:
        return await self._get_weather_alert()

    async def _city_name_by_lat_lon(self) -> None:
        """Return City Name by providing Latitude and Longitude."""
        endpoint = f"current?lat={self._latitude}&lon={self._longitude}&lang={self._language}&units={self._units}&key={self._api_key}"
        json_data = await self.async_request("get", endpoint)

        for row in json_data["data"]:
            if row["city_name"]:
                return row["city_name"]
            else:
                return "No City Name"

    async def _get_current_data(self) -> None:
        """Return Current Data for Location."""

        endpoint = f"current?lat={self._latitude}&lon={self._longitude}&lang={self._language}&units={self._units}&key={self._api_key}"
        json_data = await self.async_request("get", endpoint)

        items = []
        for row in json_data["data"]:
            item = {
                "language": self._language,
                "units": self._units,
                "station": row["station"],
                "ob_time": row["ob_time"],
                "datetime": row["datetime"],
                "ts": row["ts"],
                "temp": row["temp"],
                "city_name": row["city_name"],
                "app_temp": row["app_temp"],
                "rh": row["rh"],
                "pres": row["pres"],
                "clouds": row["clouds"],
                "solar_rad": row["solar_rad"],
                "wind_spd": row["wind_spd"],
                "wind_cdir": row["wind_cdir"],
                "wind_dir": row["wind_dir"],
                "dewpt": row["dewpt"],
                "pod": row["pod"],
                "weather_icon": row["weather"]["icon"],
                "weather_code": row["weather"]["code"],
                "weather_text": row["weather"]["description"],
                "vis": row["vis"],
                "precip": row["precip"],
                "snow": row["snow"],
                "uv": row["uv"],
                "aqi": row["aqi"],
                "dhi": row["dhi"],
                "dni": row["dni"],
                "ghi": row["ghi"],
                "elev_angle": row["elev_angle"],
                "h_angle": row["h_angle"],
                "timezone": row["timezone"],
                "sunrise": row["sunrise"],
                "sunset": row["sunset"],
            }
            items.append(CurrentData(item))

        return items

    async def _get_forecast_daily(self) -> None:
        """Return Daily Forecast Data for Location."""

        endpoint = f"forecast/daily?lat={self._latitude}&lon={self._longitude}&lang={self._language}&units={self._units}&key={self._api_key}"
        json_data = await self.async_request("get", endpoint)
        
        items = []

        city_name = json_data["city_name"]
        timezone = json_data["timezone"]
        for row in json_data["data"]:
            item = {
                "city_name": city_name,
                "timezone": timezone,
                "valid_date": row["valid_date"],
                "ts": row["ts"],
                "temp": row["temp"],
                "max_temp": row["max_temp"],
                "min_temp": row["min_temp"],
                "app_max_temp": row["app_max_temp"],
                "app_min_temp": row["app_min_temp"],
                "rh": row["rh"],
                "pres": row["pres"],
                "clouds": row["clouds"],
                "wind_spd": row["wind_spd"],
                "wind_gust_spd": row["wind_gust_spd"],
                "wind_cdir": row["wind_cdir"],
                "wind_dir": row["wind_dir"],
                "dewpt": row["dewpt"],
                "pop": row["pop"],
                "weather_icon": row["weather"]["icon"],
                "weather_code": row["weather"]["code"],
                "weather_text": row["weather"]["description"],
                "vis": row["vis"],
                "precip": row["precip"],
                "snow": row["snow"],
                "uv": row["uv"],
                "ozone": row["ozone"],
            }
            items.append(ForecastDailyData(item))

        return items

    async def _get_weather_alert(self) -> None:
        """Return Severe Weather Alerts for Location."""

        endpoint = f"alerts?lat={self._latitude}&lon={self._longitude}&key={self._api_key}"
        json_data = await self.async_request("get", endpoint)

        items = []

        city_name = json_data["city_name"]
        timezone = json_data["timezone"]
        alert_count = len(json_data["alerts"])

        if alert_count == 0:
            item = {
                "alert_count": alert_count,
                "city_name": city_name,
                "timezone": timezone,
                "title": "No Weather Alerts",
                "description": None,
                "severity": None,
                "effective_local": None,
                "expires_local": None,
                "uri": None,
                "regions": [],
            }
            items.append(WeatherAlerts(item))
            return items
        else:
            for row in json_data["alerts"]:
                item = {
                    "alert_count": alert_count,
                    "city_name": city_name,
                    "timezone": timezone,
                    "title": row["title"],
                    "description": row["description"],
                    "severity": row["severity"],
                    "effective_local": row["effective_local"],
                    "expires_local": row["expires_local"],
                    "uri": row["uri"],
                    "regions": row["regions"],
                }
                items.append(WeatherAlerts(item))
            return items

    async def _get_forecast_hourly(self) -> None:
        """Return 48 Hourly Forecast Data for Location.
           Note: This will not work in the Free Version.
        """

        endpoint = f"forecast/hourly?lat={self._latitude}&lon={self._longitude}&lang={self._language}&units={self._units}&key={self._api_key}"
        json_data = await self.async_request("get", endpoint)
        
        items = []

        city_name = json_data["city_name"]
        timezone = json_data["timezone"]
        for row in json_data["data"]:
            item = {
                "city_name": city_name,
                "timezone": timezone,
                "timestamp": row["timestamp_local"],
                "temp": row["temp"],
                "app_temp": row["app_temp"],
                "rh": row["rh"],
                "pres": row["pres"],
                "clouds": row["clouds"],
                "wind_spd": row["wind_spd"],
                "wind_gust_spd": row["wind_gust_spd"],
                "wind_cdir": row["wind_cdir"],
                "wind_dir": row["wind_dir"],
                "dewpt": row["dewpt"],
                "pop": row["pop"],
                "weather_icon": row["weather"]["icon"],
                "weather_code": row["weather"]["code"],
                "weather_text": row["weather"]["description"],
                "vis": row["vis"],
                "precip": row["precip"],
                "snow": row["snow"],
                "uv": row["uv"],
                "ozone": row["ozone"],
                "solar_rad": row["solar_rad"],
            }
            items.append(ForecastHourlyData(item))

        return items

    async def async_request(self, method: str, endpoint: str) -> dict:
        """Make a request against the Weatherbit API."""

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(
                method, f"{BASE_URL}/{endpoint}"
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except asyncio.TimeoutError:
            raise RequestError("Request to endpoint timed out: {endpoint}")
        except ClientError as err:
            if err.message == "Forbidden":
                raise InvalidApiKey("Your API Key is invalid or does not support this operation")
            else:
                raise RequestError(
                    f"Error requesting data from {endpoint}: {err}"
                ) from None
        finally:
            if not use_running_session:
                await session.close()
