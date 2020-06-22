"""
tlnetcard_python.monitor.information.information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides the get_with_snmp() and scrape_with_selenium() methods which can be used independently of
the rest of this class.
"""

# Standard library.
from time import sleep
from typing import List
from warnings import warn
# Related third-party library.
from pysnmp.hlapi import getCmd, SnmpEngine, UsmUserData, UdpTransportTarget
from pysnmp.hlapi import ContextData, ObjectType, ObjectIdentity
from requests import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize class methods.
# pylint: disable=too-many-arguments
def get_with_snmp(host: str, snmp_ids: List[str], snmp_user: str = "", snmp_auth_key: str = "",
                  snmp_priv_key: str = "", timeout: float = 10.0) -> List[str]:
    """
    Gets the provided SNMP values from their SNMP IDs. Returns ``List[str]``.

    :param host: The IP address/DNS name of the SNMP device.
    :param snmp_ids: A list of SNMP IDs to retrieve from the host.
    :param snmp_user: (optional) The username for the SNMP user to connect as.
    :param snmp_auth_key: (optional) The Auth key for the SNMP user to connect as.
    :param snmp_priv_key: (optional) The Priv key for the SNMP user to connect as.
    :param timeout: (optional) The number of seconds to wait for responses before quitting.
    :rtype: ``List[str]``
    """
    out = []

    if snmp_auth_key != "" and snmp_priv_key != "":
        usm_user_data = UsmUserData(snmp_user, authKey=snmp_auth_key, privKey=snmp_priv_key)
    elif snmp_auth_key != "":
        usm_user_data = UsmUserData(snmp_user, authKey=snmp_auth_key)
    elif snmp_priv_key != "":
        usm_user_data = UsmUserData(snmp_user, privKey=snmp_priv_key)
    else:
        usm_user_data = UsmUserData(snmp_user)

    for i in snmp_ids:
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   usm_user_data,
                   UdpTransportTarget((host, 161),
                                      timeout=timeout, retries=1),
                   ContextData(),
                   ObjectType(ObjectIdentity(i)))
        )
        # pylint: disable=no-else-return
        if error_indication:
            warn(error_indication, RuntimeError)
            # Creating an output list of the proper size.
            return ["" for i in snmp_ids]
        elif error_status:
            warn('%s at %s' % (error_status.prettyPrint(),
                               error_index and var_binds[int(error_index) - 1][0] or '?'),
                 RuntimeError)
            # Creating an output list of the proper size.
            return ["" for i in snmp_ids]
        else:
            out.append(str(var_binds[0]).split("=")[-1])
    return out
def scrape_with_selenium(host: str, element_ids: List[str], url: str, session: Session = None,
                         timeout: float = 10.0, xpath: bool = False) -> List[str]:
    """
    Scrapes the provided web elements by their ID from the provided webpage. Returns ``List[str]``.

    :param host: The IP address/DNS name of the web server.
    :param element_ids: A list of HTML element IDs to retrieve from the host. These will instead be
    Xpaths if ``xpath`` is set to ``True``.
    :param url: The specific URL from which element ID values will be scraped.
    :param session: (optional) A ``requests.Session`` object from which cookies will be transferred.
    :param timeout: (optional) The number of seconds to wait for responses before quitting.
    :param xpath: (optional) Whether Xpath should be used to find element values instead of IDs.
    :rtype: ``List[str]``
    """
    # Configuring Selenium to run headless (i.e. without a GUI).
    browser_options = Options()
    browser_options.add_argument("--headless")
    browser = webdriver.Chrome(options=browser_options)
    # Getting url.
    browser.get(url)
    if session is not None:
        # Adding cookies from requests session.
        requests_cookies = session.cookies.get_dict()
        for cookie in requests_cookies:
            browser.add_cookie({'name': cookie,
                                'domain': host,
                                'value': requests_cookies[cookie]})
        # Getting webpage again now that cookies are installed.
        browser.get(url)

    # Getting out dictionary.
    out = {}
    counter = 0.0
    while timeout > counter:
        # pylint: disable=consider-using-enumerate
        for i in range(0, len(element_ids)):
            if not xpath:
                out[i] = browser.find_element_by_id(element_ids[i]).text
            else:
                out[i] = browser.find_element_by_xpath(element_ids[i]).text
        if '' not in [out[j] for j in out]:
            break
        sleep(0.5)
        counter += 0.5

    # Closing browser and returning.
    browser.close()
    return [out[i] for i in out]
