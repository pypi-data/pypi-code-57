#!/usr/bin/env python3

# This is used only to rebuild the oui.py database. Should not be needed in normal usage.

# Once output is generated, renamd oui.json to oui.py AND ADD THE FOLLOWING:
# AT BEGINNING: oui= 

# MAC OUI list from http://standards-oui.ieee.org/oui.txt

# outputs: DICT: oui_base16 (as key), oui_hex, organization, address_1, address_2, country

# Spot check 1100AA has no address

import urllib.request
import re
import json

tlist = []
mdict = {} 

#gather initial data as a straight list
for line in urllib.request.urlopen("http://standards-oui.ieee.org/oui.txt"):
    tlist.append(line.decode("utf-8").rstrip())

#print(tlist)

#iterate through list to build dict
for k in range(len(tlist)):
    # search for 11-22-33 oui format
    find_oui_hex = re.search(r"[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}", tlist[k])
    if find_oui_hex:

        find_organization = re.search(r"(?<=\t\t)[^\t\n]+", tlist[k])
        organization = find_organization.group(0)

        #Search 2 lines ahead for first address line. Doing tab (\t) backwards looks.
        find_address_1 = re.search(r"(?<=\t\t\t\t)[^\t\n]+", tlist[k+2])
        if find_address_1:
            address_1 = find_address_1.group(0)
        else:
            address_1 = ""

        # Address_2
        find_address_2 = re.search(r"(?<=\t\t\t\t)[^\t\n]+", tlist[k+3])
        if find_address_2:
            address_2 = find_address_2.group(0)
        else:
            address_2 = ""

        # Country, US or CA or such
        find_country = re.search(r"(?<=^\t\t\t\t)[A-Z]{2}$", tlist[k+4])
        if find_country:
            country = find_country.group(0)
        else:
            country = ""

        oui_hex = find_oui_hex.group(0)
        oui_base16 = re.sub("-", "", oui_hex)
        
        mdict[oui_base16] = {"oui_hex":oui_hex, "organization":organization, "address_1":address_1, "address_2":address_2, "country":country}


#print (mdict)

# Now export to json
with open('oui.json', 'w', encoding='utf-8') as file:
    json.dump(mdict, file, ensure_ascii=False, indent=4)