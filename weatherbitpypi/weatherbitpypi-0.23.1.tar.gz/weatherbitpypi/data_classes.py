from datetime import datetime as dt
from dateutil import tz
from weatherbitpypi.const import SUPPORTED_LANGUAGES
import json
import os

"""Defines the Data Classes used."""

class CurrentData:
    """A representation of Current Weather Data."""

    def __init__(self, data):
        self._station = data["station"]
        self._city_name = data["city_name"]
        self._ob_time = data["ob_time"]
        self._datetime = data["datetime"]
        self._ts = data["ts"]
        self._temp = data["temp"]
        self._app_temp = data["app_temp"]
        self._humidity = data["rh"]
        self._pres = data["pres"]
        self._clouds = data["clouds"]
        self._solar_rad = data["solar_rad"]
        self._wind_spd = data["wind_spd"]
        self._wind_cdir = data["wind_cdir"]
        self._wind_dir = data["wind_dir"]
        self._dewpt = data["dewpt"]
        self._pod = data["pod"]
        self._weather_icon = data["weather_icon"]
        self._weather_code = data["weather_code"]
        self._weather_text = data["weather_text"]
        self._vis = data["vis"]
        self._precip = data["precip"]
        self._snow = data["snow"]
        self._uv = data["uv"]
        self._aqi = data["aqi"]
        self._dhi = data["dhi"]
        self._dni = data["dni"]
        self._ghi = data["ghi"]
        self._elev_angle = data["elev_angle"]
        self._h_angle = data["h_angle"]
        self._timezone = data["timezone"]
        self._sunrise = data["sunrise"]
        self._sunset = data["sunset"]
        self._units = data["units"]
        self._language = data["language"]

    @property
    def station(self) -> str:
        """Source station ID."""
        return self._station

    @property
    def city_name(self) -> str:
        """City Name."""
        return self._city_name

    @property
    def ob_time(self) -> str:
        """Last observation time (YYYY-MM-DD HH:MM)."""
        return self._ob_time

    @property
    def ts(self) -> float:
        """Return UNIX Timestamp. (Local Time)"""
        return self._ts

    @property
    def timestamp(self) -> str:
        """Date the forecast is valid for (YYYY-MM-DD HH:MM:SS)"""
        return dt.fromtimestamp(self._ts)

    @property
    def temp(self) -> float:
        """Temperature."""
        return self._temp

    @property
    def app_temp(self) -> float:
        """Apparent/"Feels Like" temperature."""
        return self._app_temp

    @property
    def humidity(self) -> int:
        """Relative humidity (%)."""
        return self._humidity

    @property
    def pres(self) -> float:
        """Pressure."""
        return self._pres

    @property
    def clouds(self) -> int:
        """Cloud coverage (%)."""
        return self._clouds

    @property
    def solar_rad(self) -> int:
        """Estimated Solar Radiation (W/m^2)."""
        return self._solar_rad

    @property
    def wind_spd(self) -> float:
        """Wind speed."""
        return self._wind_spd

    @property
    def wind_cdir(self) -> str:
        """Abbreviated wind direction.."""
        direction_array = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
        direction = direction_array[int((self._wind_dir + 11.25) / 22.5)]
        return get_localized_text(self._language, direction, "wind_dir")

    @property
    def wind_dir(self) -> int:
        """Wind direction (degrees)."""
        return self._wind_dir

    @property
    def dewpt(self) -> float:
        """Dew point."""
        return self._dewpt

    @property
    def pod(self) -> str:
        """Part of the day (d = day / n = night)."""
        return self._pod

    @property
    def weather_icon(self) -> str:
        """Weather icon code."""
        return self._weather_icon

    @property
    def weather_code(self) -> int:
        """Weather code."""
        return self._weather_code

    @property
    def weather_text(self) -> str:
        """Weather Description."""
        return self._weather_text

    @property
    def vis(self) -> float:
        """Visibility (default KM)."""
        return self._vis

    @property
    def precip(self) -> float:
        """Liquid equivalent precipitation rate."""
        return self._precip

    @property
    def snow(self) -> float:
        """Snowfall (default mm/hr)."""
        return self._snow

    @property
    def uv(self) -> float:
        """UV Index."""
        return self._uv

    @property
    def aqi(self) -> float:
        """Air Quality Index [US - EPA standard 0 - +500]."""
        return self._aqi

    @property
    def dhi(self) -> float:
        """Diffuse horizontal solar irradiance (W/m^2) [Clear Sky]."""
        return self._dhi

    @property
    def dni(self) -> float:
        """Direct normal solar irradiance (W/m^2) [Clear Sky]."""
        return self._dni

    @property
    def ghi(self) -> float:
        """Global horizontal solar irradiance (W/m^2) [Clear Sky]."""
        return self._ghi

    @property
    def elev_angle(self) -> int:
        """Solar elevation angle (degrees)."""
        return self._elev_angle

    @property
    def h_angle(self) -> int:
        """Solar hour angle (degrees)."""
        return self._h_angle

    @property
    def timezone(self) -> str:
        """Local IANA Timezone."""
        return self._timezone

    @property
    def sunrise(self) -> str:
        """Sunrise time (HH:MM)."""
        return self._sunrise

    @property
    def sunset(self) -> str:
        """Suntime time (HH:MM)."""
        return self._sunset

    @property
    def datetime(self) -> str:
        """Current cycle hour (YYYY-MM-DD:HH)."""
        return self._datetime

    @property
    def is_night(self) -> bool:
        """Returns True if night at location."""

        if self._pod == "n":
            return True
        else:
            return False

    @property
    def obs_time_local(self) -> str:
        """Observation Time at Location."""
        from_zone = tz.gettz("UTC")
        to_zone = tz.gettz(self.timezone)
        obs_time = dt.strptime(self.ob_time, "%Y-%m-%d %H:%M")
        obs_day = obs_time.replace(tzinfo=from_zone)
        obs_local = obs_day.astimezone(to_zone)

        return obs_local.strftime("%Y-%m-%d %H:%M")

    @property
    def beaufort_value(self) -> int:
        """Return the beaufort value based on current Wind Speed."""
        if self._units != "M":
            wind_speed_ms = self.wind_spd * 0.44704
        else:
            wind_speed_ms = self.wind_spd
        
        if (wind_speed_ms >= 32.6):
            return 12
        elif (wind_speed_ms >= 28.4):
            return 11
        elif (wind_speed_ms >= 24.5):
            return 10
        elif (wind_speed_ms >= 20.7):
            return 9
        elif (wind_speed_ms >= 17.2):
            return 8
        elif (wind_speed_ms >= 13.9):
            return 7
        elif (wind_speed_ms >= 10.8):
            return 6
        elif (wind_speed_ms >= 8.0):
            return 5
        elif (wind_speed_ms >= 5.5):
            return 4
        elif (wind_speed_ms >= 3.3):
            return 3
        elif (wind_speed_ms >= 1.5):
            return 2
        elif (wind_speed_ms >= 0.3):
            return 1
        else:
            return 0

    @property
    def beaufort_text(self) -> str:
        """Return Beaufort Description based on current wind speed."""
        return get_localized_text(self._language, self.beaufort_value, "beaufort")


def get_localized_text(language, value, index):
    """Read the localized string from the Language file."""
    if language not in SUPPORTED_LANGUAGES:
        filename = f"/translations/en.json"
    else:
        filename = f"/translations/{language}.json"

    # Build filepath
    cwd = __file__
    path_index = cwd.rfind("/")
    top_path = cwd[0:path_index]
    filepath = f"{top_path}{filename}"

    # Return Value from language string
    with open(filepath) as json_file:
        data = json.load(json_file)
        return data[index][str(value)]

class ForecastDailyData:
    """A representation of Daily Forecast Weather Data."""

    def __init__(self, data):
        self._city_name = data["city_name"]
        self._valid_date = data["valid_date"]
        self._ts = data["ts"]
        self._temp = data["temp"]
        self._max_temp = data["max_temp"]
        self._min_temp = data["min_temp"]
        self._app_max_temp = data["app_max_temp"]
        self._app_min_temp = data["app_min_temp"]
        self._humidity = data["rh"]
        self._pres = data["pres"]
        self._clouds = data["clouds"]
        self._wind_spd = data["wind_spd"]
        self._wind_gust_spd = data["wind_gust_spd"]
        self._wind_cdir = data["wind_cdir"]
        self._wind_dir = data["wind_dir"]
        self._dewpt = data["dewpt"]
        self._pop = data["pop"]
        self._weather_icon = data["weather_icon"]
        self._weather_code = data["weather_code"]
        self._weather_text = data["weather_text"]
        self._vis = data["vis"]
        self._precip = data["precip"]
        self._snow = data["snow"]
        self._uv = data["uv"]
        self._ozone = data["ozone"]
        self._timezone = data["timezone"]

    @property
    def city_name(self) -> str:
        """Nearest city name."""
        return self._city_name

    @property
    def valid_date(self) -> str:
        """Date the forecast is valid for (YYYY-MM-DD)"""
        return self._valid_date

    @property
    def local_time(self) -> dt:
        """Return Time at Location."""
        return dt.strptime(self._valid_date, "%Y-%m-%d").isoformat()

    @property
    def timestamp(self) -> dt:
        """Date the forecast is valid for (YYYY-MM-DD HH:MM:ss)"""
        from_zone = tz.gettz("UTC")
        to_zone = tz.gettz(self._timezone)
        ts = dt.fromtimestamp(self._ts)
        date_notz = ts.replace(tzinfo=from_zone)
        return date_notz.astimezone(to_zone)

    @property
    def ts(self) -> float:
        """Return UNIX Timestamp. (UTC)"""
        return self._ts

    @property
    def temp(self) -> float:
        """Average Temperature."""
        return self._temp

    @property
    def max_temp(self) -> float:
        """Maximum Temperature."""
        return self._max_temp

    @property
    def min_temp(self) -> float:
        """Minimum Temperature."""
        return self._min_temp

    @property
    def app_max_temp(self) -> float:
        """ Apparent/"Feels Like" temperature at max_temp time."""
        return self._app_max_temp

    @property
    def app_min_temp(self) -> float:
        """ Apparent/"Feels Like" temperature at min_temp time."""
        return self._app_min_temp

    @property
    def humidity(self) -> int:
        """Relative humidity (%)."""
        return self._humidity

    @property
    def pres(self) -> float:
        """Pressure."""
        return self._pres

    @property
    def clouds(self) -> int:
        """Cloud coverage (%)."""
        return self._clouds

    @property
    def wind_spd(self) -> float:
        """Wind speed."""
        return self._wind_spd

    @property
    def wind_gust_spd(self) -> float:
        """Wind gust speed."""
        return self._wind_gust_spd

    @property
    def wind_cdir(self) -> str:
        """Abbreviated wind direction.."""
        return self._wind_cdir

    @property
    def wind_dir(self) -> int:
        """Wind direction (degrees)."""
        return self._wind_dir

    @property
    def dewpt(self) -> float:
        """Dew point."""
        return self._dewpt

    @property
    def pop(self) -> int:
        """Probability of Precipitation (%)."""
        return self._pop

    @property
    def weather_icon(self) -> str:
        """Weather icon code."""
        return self._weather_icon

    @property
    def weather_code(self) -> int:
        """Weather code."""
        return self._weather_code

    @property
    def weather_text(self) -> str:
        """Weather Description."""
        return self._weather_text

    @property
    def vis(self) -> int:
        """Visibility (default KM)."""
        return self._vis

    @property
    def precip(self) -> float:
        """Accumulated liquid equivalent precipitation."""
        return self._precip

    @property
    def snow(self) -> float:
        """Accumulated snowfall (default mm)."""
        return self._snow

    @property
    def uv(self) -> float:
        """UV Index."""
        return self._uv

    @property
    def ozone(self) -> float:
        """Average Ozone (Dobson units)."""
        return self._ozone

    @property
    def timezone(self) -> str:
        """Local IANA Timezone."""
        return self._timezone

class WeatherAlerts:
    """A representation of Severe Weather Alerts."""

    def __init__(self, data):
        self._alert_count = data["alert_count"]
        self._city_name = data["city_name"]
        self._timezone = data["timezone"]
        self._title = data["title"]
        self._description = data["description"]
        self._severity = data["severity"]
        self._effective_local = data["effective_local"]
        self._expires_local = data["expires_local"]
        self._uri = data["uri"]
        self._regions = data["regions"]

    @property
    def alert_count(self) -> int:
        """Number of Weather Alerts."""
        return self._alert_count

    @property
    def city_name(self) -> str:
        """Nearest city name."""
        return self._city_name

    @property
    def timezone(self) -> str:
        """Local IANA Timezone."""
        return self._timezone

    @property
    def title(self) -> str:
        """Brief description of the alert."""
        return self._title

    @property
    def description(self) -> str:
        """Detailed description of the alert."""
        return self._description

    @property
    def severity(self) -> str:
        """Severity of the weather phenomena - Either Advisory, Watch, or Warning."""
        return self._severity

    @property
    def effective_local(self) -> str:
        """Local time that alert was issued."""
        return self._effective_local

    @property
    def expires_local(self) -> str:
        """Local time that alert expires."""
        return self._expires_local

    @property
    def uri(self) -> str:
        """An HTTP(S) URI that one may refer to for more detailed alert information."""
        return self._uri

    @property
    def regions(self):
        """An array of affected regions."""
        return self._regions

class ForecastHourlyData:
    """A representation of Hourly Forecast Weather Data."""

    def __init__(self, data):
        self._city_name = data["city_name"]
        self._timestamp = data["timestamp"]
        self._temp = data["temp"]
        self._app_temp = data["app_temp"]
        self._humidity = data["rh"]
        self._pres = data["pres"]
        self._clouds = data["clouds"]
        self._wind_spd = data["wind_spd"]
        self._wind_gust_spd = data["wind_gust_spd"]
        self._wind_cdir = data["wind_cdir"]
        self._wind_dir = data["wind_dir"]
        self._dewpt = data["dewpt"]
        self._pop = data["pop"]
        self._weather_icon = data["weather_icon"]
        self._weather_code = data["weather_code"]
        self._weather_text = data["weather_text"]
        self._vis = data["vis"]
        self._precip = data["precip"]
        self._snow = data["snow"]
        self._uv = data["uv"]
        self._ozone = data["ozone"]
        self._solar_rad = data["solar_rad"]
        self._timezone = data["timezone"]

    @property
    def city_name(self):
        """Nearest city name."""
        return self._city_name

    @property
    def timestamp(self):
        """Timestamp at local time"""
        return self._timestamp

    @property
    def temp(self):
        """Average Temperature."""
        return self._temp

    @property
    def app_temp(self):
        """Apparent/"Feels Like" temperature."""
        return self._app_temp

    @property
    def humidity(self):
        """Relative humidity (%)."""
        return self._humidity

    @property
    def pres(self):
        """Pressure."""
        return self._pres

    @property
    def clouds(self):
        """Cloud coverage (%)."""
        return self._clouds

    @property
    def solar_rad(self):
        """Estimated Solar Radiation (W/m^2)."""
        return self._solar_rad

    @property
    def wind_spd(self):
        """Wind speed."""
        return self._wind_spd

    @property
    def wind_gust_spd(self):
        """Wind gust speed."""
        return self._wind_gust_spd

    @property
    def wind_cdir(self):
        """Abbreviated wind direction.."""
        return self._wind_cdir

    @property
    def wind_dir(self):
        """Wind direction (degrees)."""
        return self._wind_dir

    @property
    def dewpt(self):
        """Dew point."""
        return self._dewpt

    @property
    def pop(self):
        """Probability of Precipitation (%)."""
        return self._pop

    @property
    def weather_icon(self):
        """Weather icon code."""
        return self._weather_icon

    @property
    def weather_code(self):
        """Weather code."""
        return self._weather_code

    @property
    def weather_text(self):
        """Weather Description."""
        return self._weather_text

    @property
    def vis(self):
        """Visibility (default KM)."""
        return self._vis

    @property
    def precip(self):
        """Accumulated liquid equivalent precipitation."""
        return self._precip

    @property
    def snow(self):
        """Accumulated Snowfall."""
        return self._snow

    @property
    def uv(self):
        """UV Index."""
        return self._uv

    @property
    def ozone(self):
        """Average Ozone (Dobson units)."""
        return self._ozone

    @property
    def timezone(self):
        """Local IANA Timezone."""
        return self._timezone
