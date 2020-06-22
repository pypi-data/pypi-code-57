"""
tlnetcard_python.monitor.information.in_out_parameters.in_out_parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a ``InOutParameters`` object to provide the functionality of TLNET Supervisor
-> Monitor -> Information -> In/Out Parameters
"""

# Standard library.
from typing import Any, Dict
# Required internal classes/functions.
from tlnetcard_python.login import Login
from tlnetcard_python.monitor.information.information import get_with_snmp, scrape_with_selenium

class InOutParameters:
    """
    A TLNET Supervisor ``InOutParameters`` object. Provides the functionality of the equivalent
    webpage TLNET Supervisor -> Monitor -> Information -> In/Out Parameters. This functionality is
    provided through either SNMP or Selenium per the user's choice. While Selenium requires no
    additional arguments at runtime, it does require Google Chrome to be installed as well as the
    associated WebDriver (see the README.md for more details), as well as suffering from
    greatly-reduced speeds. As such, it is only recommended that Selenium be used on smaller
    workloads (if you must use it at all). Alternatively, SNMP can be used to retrieve values at a
    much greater speed, although this will require more arguments (SNMP user, auth key, and priv key
    as applicable), all of which can be retrieved using the
    ``tlnetcard_python.system.notification.Snmpv3Usm`` object.

    Basic Usage:

    >>> from tlnetcard_python import Login
    >>> from tlnetcard_python.monitor.information import InOutParameters
    >>> # As always, a tlnetcard_python.Login object must first be created. Then the Login object
    >>> # can be passed to the tlnetcard_python.monitor.information.InOutParameters object.
    >>> card = Login(user="admin", passwd="password", host="10.0.0.100")
    >>> card_io_parameters = InOutParameters(card)

    At this point, functions can either be run using SNMP:

    >>> card_io_parameters.get_output_measurements(snmp_user="admin", snmp_auth_key="imadethisup",
    >>>                                            snmp_priv_key="imadethisuptoo")
    {'Output Source': 'Normal', 'Frequency (Hz)': 59.9, 'Voltage (V)': 120.0, 'Current (A)': 3.6,
    'Power (Watt)': 409, 'Loading (%)': 30}

    Or they can be run using Selenium:

    >>> card_io_parameters.get_output_measurements(snmp=False)
    {'Output Source': 'Normal', 'Frequency (Hz)': 59.9, 'Voltage (V)': 120.0, 'Current (A)': 3.6,
    'Power (Watt)': 409, 'Loading (%)': 30}
    """
    def __init__(self, login_object: Login) -> None:
        """
        Initializes the ``InOutParameters`` object. Returns ``None``.

        :param login_object: A valid ``tlnetcard_python.Login`` object.
        :rtype: ``None``
        """
        self._login_object = login_object
        self._get_url = login_object.get_base_url() + "/en/ups/info_io.asp"
    def get_bypass_measurements(self, snmp: bool = True, snmp_user: str = "",
                                snmp_auth_key: str = "", snmp_priv_key: str = ""
                                ) -> Dict[str, Any]:
        """
        Returns battery bypass measurements as a dictionary.

        :param snmp: (optional) Whether SNMP should be used or not. Setting this value to ``False``
        will result in Selenium being used.
        :param snmp_user: (optional) The SNMP user to connect with.
        :param snmp_auth_key: (optional) The SNMP auth key to connect with.
        :param snmp_priv_key: (optional) The SNMP priv key to connect with.
        :rtype: ``Dict[str, Any]``
        """
        if snmp:
            # SNMP will be used to get values. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Frequency': 'iso.3.6.1.2.1.33.1.5.1', # In decihertz
                                                       # (i.e. divide this value by 10).
                'Voltage': 'iso.3.6.1.2.1.33.1.5.3.1.2.1',
                'Current': 'iso.3.6.1.2.1.33.1.5.3.1.3.1', # In deciamps
                                                           # (i.e. divide this value by 10).
                'Power': 'iso.3.6.1.2.1.33.1.5.3.1.4.1'
            }

            # Getting values.
            freq, volts, curr, power = get_with_snmp(self._login_object.get_host(),
                                                     [snmp_dict[i] for i in snmp_dict], snmp_user,
                                                     snmp_auth_key, snmp_priv_key,
                                                     self._login_object.get_timeout())

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq)/10,
                'Voltage (V)': float(volts),
                'Current (A)': float(curr)/10,
                'Power (Watt)': int(power)
            }
        else:
            # Selenium will be used to scrape values. This method is slower than using SNMP.
            # Getting values.
            freq, volts, curr, power = scrape_with_selenium(self._login_object.get_host(),
                                                            ["UPS_BYFREQ1", "UPS_BYVOLT1",
                                                             "UPS_BYAMP1", "UPS_BYPOWER1"],
                                                            self._get_url,
                                                            self._login_object.get_session(),
                                                            self._login_object.get_timeout())

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq),
                'Voltage (V)': float(volts),
                'Current (A)': float(curr),
                'Power (Watt)': int(power)
            }
        return out
    def get_input_measurements(self, snmp: bool = True, snmp_user: str = "",
                               snmp_auth_key: str = "", snmp_priv_key: str = ""
                               ) -> Dict[str, Any]:
        """
        Returns battery input measurements as a dictionary.

        :param snmp: (optional) Whether SNMP should be used or not. Setting this value to ``False``
        will result in Selenium being used.
        :param snmp_user: (optional) The SNMP user to connect with.
        :param snmp_auth_key: (optional) The SNMP auth key to connect with.
        :param snmp_priv_key: (optional) The SNMP priv key to connect with.
        :rtype: ``Dict[str, Any]``
        """
        if snmp:
            # SNMP will be used to get values. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Frequency': 'iso.3.6.1.2.1.33.1.3.3.1.2.1', # In decihertz
                                                             # (i.e. divide this number by 10).
                'Voltage': 'iso.3.6.1.2.1.33.1.3.3.1.3.1',
            }

            # Getting values.
            freq, volts = get_with_snmp(self._login_object.get_host(),
                                        [snmp_dict[i] for i in snmp_dict], snmp_user, snmp_auth_key,
                                        snmp_priv_key, self._login_object.get_timeout())

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq)/10,
                'Voltage (V)': float(volts)
            }
        else:
            # Selenium will be used to scrape values. This method is slower than using SNMP.
            # Getting values.
            freq, volts = scrape_with_selenium(self._login_object.get_host(),
                                               ["UPS_INFREQ1", "UPS_INVOLT1"], self._get_url,
                                               self._login_object.get_session(),
                                               self._login_object.get_timeout())

            # Generating out dictionary.
            out = {
                'Frequency (Hz)': float(freq),
                'Voltage (V)': float(volts),
            }
        return out
    # pylint: disable=too-many-locals
    def get_output_measurements(self, snmp: bool = True, snmp_user: str = "",
                                snmp_auth_key: str = "", snmp_priv_key: str = ""
                                ) -> Dict[str, Any]:
        """
        Returns battery output measurements as a dictionary.

        :param snmp: (optional) Whether SNMP should be used or not. Setting this value to ``False``
        will result in Selenium being used.
        :param snmp_user: (optional) The SNMP user to connect with.
        :param snmp_auth_key: (optional) The SNMP auth key to connect with.
        :param snmp_priv_key: (optional) The SNMP priv key to connect with.
        :rtype: ``Dict[str, Any]``
        """
        if snmp:
            # SNMP will be used to get values. This is the preferred method.
            # Generating SNMP ID dictionary.
            snmp_dict = {
                'Output': 'iso.3.6.1.2.1.33.1.4.1',
                'Frequency': 'iso.3.6.1.2.1.33.1.4.2', # In decihertz
                                                       # (i.e. divide this value by 10).
                'Voltage': 'iso.3.6.1.2.1.33.1.4.4.1.2.1',
                'Current': 'iso.3.6.1.2.1.33.1.4.4.1.3.1', # In deciamps
                                                           # (i.e. divide this value by 10).
                'Power': 'iso.3.6.1.2.1.33.1.4.4.1.4.1',
                'Loading': 'iso.3.6.1.2.1.33.1.4.4.1.5.1'
            }

            # Getting values.
            out, freq, volts, curr, power, load = get_with_snmp(self._login_object.get_host(),
                                                                [snmp_dict[i] for i in snmp_dict],
                                                                snmp_user, snmp_auth_key,
                                                                snmp_priv_key,
                                                                self._login_object.get_timeout())
            # Output source status is actually returned as an integer whose values map as follows:
            status_dict = {
                1: 'Other',
                2: 'None',
                3: 'Normal',
                4: 'Bypass',
                5: 'Battery',
                6: 'Booster',
                7: 'Reducer'
            }

            # Generating out dictionary.
            out = {
                'Output Source': status_dict[int(out)],
                'Frequency (Hz)': float(freq)/10,
                'Voltage (V)': float(volts),
                'Current (A)': float(curr)/10,
                'Power (Watt)': int(power),
                'Loading (%)': int(load)
            }
        else:
            # Selenium will be used to scrape values. This method is slower than using SNMP.
            # Getting values.
            host = self._login_object.get_host()
            session = self._login_object.get_session()
            timeout = self._login_object.get_timeout()
            out, freq, volts, curr, power, load = scrape_with_selenium(host,
                                                                       ["UPS_OUTSRC", "UPS_OUTFREQ",
                                                                        "UPS_OUTVOLT1",
                                                                        "UPS_OUTAMP1",
                                                                        "UPS_OUTPOWER1",
                                                                        "UPS_OUTLOAD1"],
                                                                       self._get_url, session,
                                                                       timeout)

            # Generating out dictionary.
            out = {
                'Output Source': out,
                'Frequency (Hz)': float(freq),
                'Voltage (V)': float(volts),
                'Current (A)': float(curr),
                'Power (Watt)': int(power),
                'Loading (%)': int(load)
            }
        return out
