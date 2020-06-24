import fnmatch
import os


def find_esp_bsa(directory):
    """
    Finds bsas and esps in a mod installation directory
    """
    esps = []
    bsas = []
    for file in os.listdir(os.path.normpath(directory)):
        if fnmatch.fnmatch(file, "*.[bB][sS][aA]"):
            bsas.append(file)
        elif (
            fnmatch.fnmatch(file, "*.[eE][sS][pPmM]")
            or fnmatch.fnmatch(file, "*.[oO][mM][wW][aA][dD][dD][oO][nN]")
            or fnmatch.fnmatch(file, "*.[oO][mM][wW][gG][aA][mM][eE]")
        ):
            esps.append(file)
    return (esps, bsas)
