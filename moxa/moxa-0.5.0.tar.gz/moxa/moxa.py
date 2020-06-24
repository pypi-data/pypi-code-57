import socket
import re
import math
import os.path as path
import time
from datetime import datetime


class Moxa(object):
    """
    Interface with MOXA
    """

    MS_TO_KNOTS = 1.944

    config = {
            'MOXA_IP':      '172.18.74.241',
            'RMC_PATTERN':  '\$..RMC.*\*\w\w',
            'GLL_PATTERN':  '\$..GLL.*\*\w\w',
            'GGA_PATTERN':  '\$..GGA.*\*\w\w',
            'VTG_PATTERN':  '\$..VTG.*\*\w\w',
            'ZDA_PATTERN':  '\$..ZDA.*\*\w\w',
            'MMB_PATTERN':  '\$..MMB[,]{3}[\d]{4}.\d,B\*\w\w',
            'MWV_PATTERN':  '\$..MWV,\d*.\d,\w,\d*.\d,\w,\w\*\w\w',
            'MTA_PATTERN':  '\$..MTA,[\d]*.\d,\w\*[\w]{2}',
            'MHU_PATTERN':  '\$..MHU,.*\*[\w]{2}',
            'HDT_PATTERN':  '\$..HDT.*\*\w\w',
            'HDM_PATTERN':  '\$..HDM.*\*\w\w',
            'GPS_PORT':     957,
            'RMC_PORT':     957,
            'WX_PORT':      957,
            'HDG_PORT':     957,
            'CACHE_AGE':    5,  # 5 seconds
            'CACHE_DIR':     '/tmp',
            }

    def __init__(self, config={}):
        """
        Initialise the class
        """
        for key in config.keys():
            self.config[key] = config[key]

    def get_degrees(self, msgdegrees: str, msghem: str) -> float:
        """
        Convert degress in xxxx.xx format to +/-xxx.xxx format

        :param msgdegrees:
        :param msghem:
        :return:
        """
        parts = msgdegrees.split('.')

        wholedegrees = int(parts[0][:-2])
        minutes = float(parts[0][-2:] + '.' + parts[1]) / 60
        degs = wholedegrees + minutes

        if msghem in ['W', 'S']:
            degs = -degs

        return round(degs, 3)

    def writecache(self, cachename: str, data: str):
        """
        Writes data to a cache file.

        :param cachename:
        :param data
        :return:
        """
        with open(cachename, 'w') as f:
            f.write(data)

    def readcache(self, cachename: str) -> str:
        """
        Reads data from a cache file
        :param cachename:
        :return:
        """

        if path.isfile(cachename):
            with open(cachename) as f:
                return f.read()

        return

    def cacheexpired(self, cachename: str) -> bool:
        """
        Checks if a cache has expired and returns true if it has, false if it hasn't.

        :param cachename:
        :return: bool
        """

        if path.isfile(cachename) and \
                path.getmtime(cachename) > (time.time() - self.CACHE_AGE):
                    return False

        return True

    def pattern_to_cachename(self, pattern: str) -> str:
        """
        Given the NMEA message in pattern, return the filename of the corresponding cache.
        This will be the pattern - the leading $ suffixed with .txt. eg:
            >>>pattern_to_cachename('\$GPRMC.*\*\w\w')
            'GPRMC.txt'
        :param pattern:
        :return:
        """

        return '{}/{}.txt'.format(self.CACHE_DIR, pattern[4:7])

    def find_msg(self, pattern, port):
        # return readmoxa(pattern, port)
        cachename = self.pattern_to_cachename(pattern)
        if not self.cacheexpired(cachename):
            return self.readcache(cachename)

        data = self.readmoxa(pattern, port)
        if not data:
            return self.readcache(cachename)

        self.writecache(cachename, data)
        return self.readcache(cachename)

    def readmoxa(self, pattern, port):
        buffer = []
        try:
            with socket.socket() as sock:
                sock.settimeout(2)
                sock.connect((self.MOXA_IP, port))

                while True:
                    c = str(sock.recv(1))[1:]
                    buffer.append(c.strip("'"))
                    match = re.search(pattern, ''.join(buffer))
                    if match:
                        return match.group(0)
        except Exception as e:
            print(e)
            return

    def nmeasentence(self, pattern: str, port: int) -> [str]:
        """
        Read an NMEA sentence from MOXA

        :param pattern: A regex for the required string
        :type pattern: str
        :param port: The port number to read from
        :type port: int
        :return:  List of sentence parts
        :rtype: list of str
        """
        parts = self.find_msg(pattern, port)
        if parts:
            return parts.split(',')

    @property
    def pressure(self) -> float:
        """
        Get pressure in millibars from MOXA
        """
        parts = self.nmeasentence(self.MMB_PATTERN, self.WX_PORT)
        if len(parts) > 3:
            return float(parts[3])

    @property
    def relwind(self) -> dict:
        """
        Get wind speed and direction from MOXA
        """
        parts = self.nmeasentence(self.MWV_PATTERN, self.WX_PORT)
        if len(parts) > 3:
            result = {
                'dir': float(parts[1]),
                'knots': round(float(parts[3]) * self.MS_TO_KNOTS, 1),
                'meters_second': round(float(parts[3])),
            }
            return result

    @property
    def humidity(self) -> dict:
        """
        Get rel humidity and dewpoint temp
        """
        parts = self.nmeasentence(self.MHU_PATTERN, self.WX_PORT)
        if len(parts) > 3:
            result = {
                'rel_humidity': float(parts[1]),
                'dew_point':    float(parts[3]),
            }
            return result

    @property
    def temperature(self) -> float:
        """() -> float
        """
        parts = self.nmeasentence(self.MTA_PATTERN, self.WX_PORT)
        if len(parts) > 1:
            return float(parts[1])

    @property
    def truewind(self) -> tuple:
        return self._truewind(self.relwind, self.course, self.speed)

    @property
    def heading(self) -> float:
        parts = self.nmeasentence(self.HDT_PATTERN, self.HDG_PORT)
        return float(parts[1])


    @property
    def magnetic(self) -> float:
        parts = self.nmeasentence(self.HDM_PATTERN, self.HDG_PORT)
        return float(parts[1])


    @property
    def course(self) -> float:
        parts = self.nmeasentence(self.VTG_PATTERN, self.GPS_PORT)
        if len(parts) > 8:
            return float(parts[1])

    @property
    def speed(self) -> float:
        parts = self.nmeasentence(self.VTG_PATTERN, self.GPS_PORT)
        if len(parts) > 7:
            return float(parts[5])

    @property
    def position(self) -> (float, float):
        parts = self.nmeasentence(self.GGA_PATTERN, self.GPS_PORT)
        if len(parts) > 6:
            lat = self.get_degrees(parts[2], parts[3])
            lon = self.get_degrees(parts[4], parts[5])
            return lat, lon

    @property
    def utc(self) -> datetime:
        parts = self.nmeasentence(self.ZDA_PATTERN, self.GPS_PORT)
        return datetime(
            int(parts[4]),
            int(parts[3]),
            int(parts[2]),
            int(parts[1][:2]),
            int(parts[1][2:4]),
            int(parts[1][4:6]),
        )

    @property
    def all(self) -> dict:
        position = self.position
        return {
            'UTC': self.utc.strftime('%Y-%m-%d %H:%M:%S'),
            'lat': position[0],
            'lon': position[1],
            'vmg': self.speed,
            'cog': self.course,
            'hdg': self.heading,
        }

    @property
    def variation(self) -> float:
        parts = self.nmeasentence(self.RMC_PATTERN, self.RMC_PORT)
        var = float(parts[10])
        if parts[11] == 'E':
            var = -var
        return var

    def poshdegrees(self, pos: float, latlon: str) -> str:
        """
        Take a Lat or Long as a float and convert it to a nicely formatted
        string.

        >>> poshdegrees(53.5, 'N')
        53° 30.0' N

        :param pos: Lat or Long in decimal degrees
        :type pos: float
        :param latlon:
        :type latlon: str
        :return: A formatted string
        :rtype: str
        """
        if latlon == 'lat' and pos >= 0:
            hem = 'N'
        elif latlon == 'lat' and pos < 0:
            hem = 'S'

        elif latlon == 'lon' and pos >= 0:
            hem = 'E'
        elif latlon == 'lon' and pos < 0:
            hem = 'W'

        pos = abs(pos)
        degrees = int(pos)
        minutes = round((pos - degrees) * 60, 1)
        return '{}° {}\' {}'.format(str(degrees), str(minutes).zfill(4), hem)

    def _truewind(self, relwind, course, speed):
        """
        See http://coaps.fsu.edu/WOCE/truewind/paper/ for details on formula
        :param relwind:
        :param course:
        :param speed:
        :return: (true wind dir, true wind speed)
        """

        vlcourse = course
        vlspeed = -speed
        appwindangle = (relwind['dir'] + course) % 360
        appwindspeed = relwind['knots']

        # Vessel stopped - true wind = apparent wind
        if speed == 0:
            tangle, tspeed = appwindangle, appwindspeed

        # Headwind
        elif relwind['dir'] in [0, 360]:
            tangle, tspeed = appwindangle, appwindspeed - speed

        # Following wind
        elif relwind['dir'] == 180:
            tangle, tspeed = appwindangle, appwindspeed + speed

        else:
            tu = round(appwindspeed * math.cos(math.radians(appwindangle)) + vlspeed * math.cos(
                math.radians(vlcourse)), 6)
            tv = round(appwindspeed * math.sin(math.radians(appwindangle)) + vlspeed * math.sin(
                math.radians(vlcourse)), 6)
            tspeed = math.hypot(tu, tv)
            
            if 0 not in [tu, tv]:
                tangle = math.degrees(math.atan2(tu, tv))
                tangle %= 360
            elif tu == 0:
                tangle = 90 if tv >= 0 else 270
            elif tv == 0:
                tangle = 360 if tv >= 0 else 180

        return round(tangle, 1), round(tspeed, 1)

    def __getattr__(self, item):
        """
        Get attributes from config
        :param item:
        :return:
        """
        if item in self.config:
            return self.config.get(item)

