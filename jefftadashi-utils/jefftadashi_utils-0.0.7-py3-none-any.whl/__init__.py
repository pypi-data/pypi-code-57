#!/usr/bin/env python3

# jefftadashi_utils/__init__.py

# Suggested Call:
# from jefftadashi_utils import jtu

# TODO: Function to normalize Cisco interface name (short to long, etc)

# TODO: General function for sendmail API

import re
from . import oui


################
#   MAC OUI    #
################
oui = oui.oui #from file oui.py
# This is simply to make calling this simpler, jefftadashi_utils.oui works instead of jefftadashi_utils.oui.oui

################
# ASCII Colors #
################
# see https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
class color:
    darkpurple = '\033[35m'
    darkcyan = '\033[36m'
    darkblue = '\033[34m'
    darkgreen = '\033[32m'
    darkyellow = '\033[33m'
    darkred = '\033[31m'

    purple = '\033[95m'
    cyan = '\033[96m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    
    bold = '\033[1m'
    underline = '\033[4m'
    # End is important! It is used to revert color to normal.
    end = '\033[0m'

################
# Common Regex #
################
class regex:
    #Cisco Mac Address format: 1234.abcd.ab34 (case insensitive, although lowercase is norm)
    mac_cisco = r"[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}" 
    #General Mac Address format: 12:34:ab:cd:ab:34 or 12-34-ab-cd-ab-34 (case insensitive) 
    #mac_general = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
    mac_general = r"[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}"
    # Combined
    mac_all = r"(" + mac_cisco + r"|" + mac_general + r")"

    #For Cisco, matches short/long name of interface or vlan/portchannel, etc. (GigabitEthernet1/2/3 or Vl200, etc)
    int_cisco = r"([A-Z][a-zA-Z]{1,}\d{1,2}/\d{1,2}(/\d{1,2})?|(Vl|Vlan)\d{1,4}|(Po|Port-channel)\d{1,3}|(Lo|Loopback)\d{1,10}|(Tu|Tunnel)\d{1,10}|(Nu|Null)\d{1,1})"

    #For Juniper, match interface without the trailing .0 . In particular, ae0 has negative lookbehind to avoid match like bae0 
    int_juniper = r"[a-z]{2}-[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2}|(?<![0-9a-zA-Z])ae[0-9]{1,2}"

    int_all = r"(" + int_cisco + r"|" + int_juniper + r")"

    # Simple version, will match things like 555.555.555.555
    ip = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    # Full CIDR notation match, IP + CIDR extention. Mandatory all (e.g. 10.0.0.0/24)
    cidr = r"(" + ip + r")" + r"(/[0-9]{1,2})"
    # Match CIDR or just plain IP. In other words, CIDR extention is optional
    ip_or_cidr = cidr + r"?" 

    vlan_base = r"(Vlan|Vl|irb\.)"   # for cisco and juniper, E.G. "Vlan" or "irb."
    vlan_full = vlan_base + r"\d{1,4}" #adding numbers to vlan E.G. "Vlan100"


#########################
# MAC VENDOR OUI Lookup #
#########################
def get_mac_vendor(maca):
    # Input: Mac Address as string (or just first 6 digits, the OUI)
    # Output: Vendor Organization as string

    # First, convert mac to "base 16" non-symboled format, all uppercase, and only keep first 6 characters
    maca = re.sub(r"[:\.-]", "", maca)
    maca = maca.upper()
    maca = maca[:6]

    # Now search for match (first 6 characters of mac address) in oui->mac->organization dict and return vendor
    try:
        return oui[maca]['organization']
    except:
        return "(NO VENDOR MATCH)"
    
    

#########################
# MAC Address Converter #
#########################
def convert_mac(mac_adr, separator=":", separate_length=2, uppercase=True):
# INPUTS: 
# 1st - mac address as string, any format
# 2nd - separator character, E.G. "." or ":" or "-". Default is colon.
# 3rd - length between separators. Default is 2, e.g. aa:bb:cc:dd:ee:ff. Cisco format would be 4, e.g. aaaa.bbbb.cccc
#     - Values of 0,2,3,4,6 are allowed.
# 4th - Uppercase for True (default). Lowercase for False.

    # First, remove all separators (get alphanumeric string)
    mac_adr = re.sub(r"[^a-zA-Z0-9]", "", mac_adr)

    # Next, set case
    if uppercase == False:
        mac_adr = mac_adr.lower()
    else: # If true or otherwise
        mac_adr = mac_adr.upper()

    # Next, add separators
    if separate_length == 2:
        mac_adr = mac_adr[:2] + separator + mac_adr[2:4] + separator + mac_adr[4:6] + separator + mac_adr[6:8] + separator + mac_adr[8:10] + separator + mac_adr[10:12]
    elif separate_length == 3:
        mac_adr = mac_adr[:3] + separator + mac_adr[3:6] + separator + mac_adr[6:9] + separator + mac_adr[9:12]
    elif separate_length == 4:
        mac_adr = mac_adr[:4] + separator + mac_adr[4:8] + separator + mac_adr[8:12]
    elif separate_length == 6:
        mac_adr = mac_adr[:6] + separator + mac_adr[6:12]
    else:
        pass # Don't add any separators in any other cases, such as 0

    # Should be all done!
    return mac_adr
