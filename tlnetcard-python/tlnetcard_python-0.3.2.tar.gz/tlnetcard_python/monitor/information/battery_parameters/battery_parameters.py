"""
tlnetcard.monitor.information.battery_parameters.battery_parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``BatteryParameters`` object to provide the functionality of TLNET Supervisor
-> Monitor -> Information -> Battery Parameters.
"""

# Standard library.
from typing import Any, Dict
# Required internal classes/functions.
from tlnetcard_python.login import Login
from tlnetcard_python.monitor.information.information import get_with_snmp, scrape_with_selenium

class BatteryParameters:
    """
    A TLNET Supervisor ``BatteryParameters`` object. Provides the functionality of the equivalent
    webpage TLNET Supervisor -> Monitor -> Information -> About. This functionality is provided
    through either SNMP or Selenium per the user's choice. While Selenium requires no additional
    arguments at runtime, it does require Google Chrome to be installed as well as the associated
    WebDriver (see the README.md for more details), as well as suffering from greatly-reduced
    speeds. As such, it is only recommended that Selenium be used on smaller workloads (if you
    must use it at all). Alternatively, SNMP can be used to retrieve values at a much greater speed,
    although this will require more arguments (SNMP user, auth key, and priv key as applicable), all
    of which can be retrieved using the ``tlnetcard_python.system.adminitration.UserManager``
    object.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.information import BatteryParameters
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.information.BatteryParameters object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_batt_parameters = BatteryParameters(card)

    At this point, functions can either be run using SNMP:

    >>> card_batt_parameters.get_battery_status(snmp_user="admin", snmp_auth_key="imadethisup",
    >>>                                         snmp_priv_key="imadethisuptoo")
    {'Battery Status': 'Normal', 'On Battery Time (s)': 0}

    Or they can be run using Selenium:

    >>> card_batt_parameters.get_battery_status(snmp=False)
    {'Battery Status': 'Normal', 'On Battery Time (s)': 0}
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``BatteryParameters`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/ups/info_battery.asp"
    def get_battery_status(self, snmp: bool = True, snmp_user: str = "",
                           snmp_auth_key: str = "", snmp_priv_key: str = "") -> Dict[str, Any]:
        """
        Returns battery status information as a dictionary.

        :param snmp: (optional) Whether SNMP should be used or not. Setting this value to ``False``
        will result in Selenium being used.
        :param snmp_user: (optional) The SNMP user to connect with.
        :param snmp_auth_key: (optional) The SNMP auth key to connect with.
        :param snmp_priv_key: (optional) The SNMP priv key to connect with.
        :rtype: ``Dict[str, Any]``
        """
        if snmp:
            # SNMP will be used to get the value. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Battery Status': 'iso.3.6.1.2.1.33.1.2.1',
                'On Battery Time': 'iso.3.6.1.2.1.33.1.2.2'
            }

            # Getting values.
            batt_stat, batt_time = get_with_snmp(self._login_object.get_host(),
                                                 [snmp_dict[i] for i in snmp_dict], snmp_user,
                                                 snmp_auth_key, snmp_priv_key,
                                                 self._login_object.get_timeout())
            # Battery status is actually returned as an integer whose values map as follows:
            status_dict = {
                1: 'Unknown',
                2: 'Normal',
                3: 'Low',
                4: 'Depleted'
            }

            # Generating out dictionary.
            out = {
                'Battery Status': status_dict[int(batt_stat)],
                'On Battery Time (s)': int(batt_time)
            }
        else:
            # Selenium will be used to scrape the value. This method is slower than using SNMP.
            # Getting values.
            batt_stat, batt_time = scrape_with_selenium(self._login_object.get_host(),
                                                        ["UPS_BATTSTS", "UPS_ONBATTTIME"],
                                                        self._get_url,
                                                        self._login_object.get_session(),
                                                        self._login_object.get_timeout())

            # Generating out dictionary.
            out = {
                'Battery Status': batt_stat,
                'On Battery Time (s)': int(batt_time)
            }
        return out
    def get_battery_measurements(self, snmp: bool = True, snmp_user: str = "",
                                 snmp_auth_key: str = "", snmp_priv_key: str = ""
                                 ) -> Dict[str, Any]:
        """
        Gets information about battery capacity, temperature, and voltage. Returns this information
        as a dictionary.

        :param snmp: (optional) Whether SNMP should be used or not. Setting this value to ``False``
        will result in Selenium being used.
        :param snmp_user: (optional) The SNMP user to connect with.
        :param snmp_auth_key: (optional) The SNMP auth key to connect with.
        :param snmp_priv_key: (optional) The SNMP priv key to connect with.
        :rtype: ``Dict[str, Any]``
        """
        if snmp:
            # SNMP will be used to get the value. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Battery Capacity': 'iso.3.6.1.2.1.33.1.2.4',
                'Voltage': 'iso.3.6.1.2.1.33.1.2.5', # In decivolts (i.e. divide this value by 10).
                'Temperature': 'iso.3.6.1.2.1.33.1.2.7',
                'Remaining Minutes': 'iso.3.6.1.2.1.33.1.2.3',
            }

            # Getting values.
            batt_cap, volts, temp, rem_mins = get_with_snmp(self._login_object.get_host(),
                                                            [snmp_dict[i] for i in snmp_dict],
                                                            snmp_user, snmp_auth_key,
                                                            snmp_priv_key,
                                                            self._login_object.get_timeout())

            # Generating out dictionary.
            mins = int(rem_mins)
            hours = int((mins - (mins % 60))/60)
            rem_time = '{hours:02d}:{mins:02d}'.format(hours=hours, mins=mins % 60)
            out = {
                'Battery Capacity (%)': int(batt_cap),
                'Voltage (V)': float(volts)/10,
                'Temperature (°C)': int(temp),
                'Remaining Time (HH:MM)': rem_time
            }
        else:
            # Selenium will be used to scrape the value. This method is slower than using SNMP.
            # Getting values.
            batt_cap, volts, temp, time, = scrape_with_selenium(self._login_object.get_host(),
                                                                ["UPS_BATTLEVEL",
                                                                 "UPS_BATTVOLT",
                                                                 "UPS_TEMP",
                                                                 "UPS_BATTREMAIN"],
                                                                self._get_url,
                                                                self._login_object.get_session(),
                                                                self._login_object.get_timeout())

            # Generating out dictionary.
            out = {
                'Battery Capacity (%)': int(batt_cap),
                'Voltage (V)': float(volts),
                'Temperature (°C)': int(temp),
                'Remaining Time (HH:MM)': time
            }
        return out
    def get_last_replacement_date(self) -> str:
        """
        Gets the last date the UPS battery was changed and returns it as a string.

        :rtype: ``str``
        """
        # This value is not available with SNMP.
        return scrape_with_selenium(self._login_object.get_host(), ["UPS_BATTLAST"],
                                    self._get_url, self._login_object.get_session(),
                                    self._login_object.get_timeout())[0]
    def get_next_replacement_date(self) -> str:
        """
        Gets the next date the UPS battery should be changed and returns it as a string.

        :rtype: ``str``
        """
        # This value is not available with SNMP.
        return scrape_with_selenium(self._login_object.get_host(), ["UPS_BATTNEXT"],
                                    self._get_url, self._login_object.get_session(),
                                    self._login_object.get_timeout())[0]
