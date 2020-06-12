#!/usr/bin/env python3

import sys
import os
import socket
import time
import difflib
import re
import argparse
import fileinput
import binascii
import datetime
import tempfile
import json

from select import select

have_scapy = False
have_paramiko = False
have_colorama = False
have_ssl = False
have_requests = False
have_socks = False
have_crypto = False

option_dump_received_correct = False
option_dump_received_different = True
option_auto_send = 5

option_socks = None


pplay_version = "2.0.0"


# EMBEDDED DATA BEGIN
# EMBEDDED DATA END

title = 'pplay - application payload player - %s' % (pplay_version,)
copyright = "written by Ales Stibal <astib@mag0.net> (c) 2014"

g_script_module = None
g_delete_files = []

g_hostname = socket.gethostname()

try:
    from scapy.all import rdpcap
    from scapy.all import IP
    from scapy.all import TCP
    from scapy.all import UDP
    from scapy.all import Padding

    have_scapy = True
except ImportError as e:
    print('== No scapy, pcap files not supported.', file=sys.stderr)

## try to import colorama, indicate with have_ variable
try:
    import colorama
    from colorama import Fore, Back, Style

    have_colorama = True
except ImportError as e:
    print('== No colorama library, enjoy.', file=sys.stderr)

# try to import ssl, indicate with have_ variable
try:
    import ssl

    have_ssl = True
except ImportError as e:
    print('== No SSL python support!', file=sys.stderr)

# try to import paramiko, indicate with have_ variable
try:
    import paramiko

    have_paramiko = True
except ImportError as e:
    print('== No paramiko library, use ssh with pipes!', file=sys.stderr)

# try to import paramiko, indicate with have_ variable
try:
    import requests

    have_requests = True
except ImportError as e:
    print('== No requests library support, files on http(s) won\'t be accessible!', file=sys.stderr)

# try to import paramiko, indicate with have_ variable
try:
    import socks

    have_socks = True
except ImportError as e:
    print('== No pysocks library support, can\'t use SOCKS proxy!', file=sys.stderr)


try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import AuthorityInformationAccessOID
    from cryptography.x509.oid import NameOID

    have_crypto = True
except ImportError as e:
    print('== no cryptography library support, can\'t use CA to sign dynamic certificates based on SNI!', file=sys.stderr)


def str_time():
    t = None
    failed = False
    try:
        t = datetime.now()
    except AttributeError as e:
        failed = True

    if not t and failed:
        try:
            t = datetime.datetime.now()
        except Exception as e:
            t = "<?>"

    return socket.gethostname() + "@" + str(t)


def print_green_bright(what):
    if have_colorama:
        print(Fore.GREEN + Style.BRIGHT + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


def print_green(what):
    if have_colorama:
        print(Fore.GREEN + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


def print_yellow_bright(what):
    if have_colorama:
        print(Fore.YELLOW + Style.BRIGHT + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


def print_yellow(what):
    if have_colorama:
        print(Fore.YELLOW + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


def print_red_bright(what):
    if have_colorama:
        print(Fore.RED + Style.BRIGHT + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


def print_red(what):
    if have_colorama:
        print(Fore.RED + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


def print_white_bright(what):
    if have_colorama:
        print(Fore.WHITE + Style.BRIGHT + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


def print_white(what):
    if have_colorama:
        print(Fore.WHITE + what + Style.RESET_ALL, file=sys.stderr)
    else:
        print(what, file=sys.stderr)


__vis_filter = """................................ !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[.]^_`abcdefghijklmnopqrstuvwxyz{|}~................................................................................................................................."""


def hexdump(xbuf, length=16):
    """Return a hexdump output string of the given buffer."""
    n = 0
    res = []

    buf = xbuf.decode('ascii', errors="ignore")

    while buf:
        line, buf = buf[:length], buf[length:]
        hexa = ' '.join(['%02x' % ord(x) for x in line])
        line = line.translate(__vis_filter)
        res.append('  %04d:  %-*s %s' % (n, length * 3, hexa, line))
        n += length
    return '\n'.join(res)


def colorize(s, keywords):
    t = s
    for k in keywords:
        t = re.sub(k, Fore.CYAN + Style.BRIGHT + k + Fore.RESET + Style.RESET_ALL, t)

    return t


# print_green_bright("TEST%d:%s" % (12,54))


# download file from HTTP and store it in /tmp/, add it to g_delete_files
# so they are deleted at end of the program
def http_download_temp(url):
    r = requests.get(url, stream=True)
    if not r:
        print_red_bright("cannot download: " + url)
        sys.exit(1)

    local_filename = tempfile.mkstemp(prefix="pplay_dwn_")[1]
    g_delete_files.append(local_filename)

    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

        r.close()
        print_green("downloaded file into " + local_filename)

    return local_filename


class SxyCA:

    SETTINGS = {
        "ca": {},
        "srv": {},
        "clt": {},
        "prt": {},
        "path": "/tmp/",
        "ttl": 60
    }

    class Options:
        indent = 0
        debug = False

    @staticmethod
    def pref_choice(*args):
        for a in args:
            if a:
                return a
        return None

    @staticmethod
    def init_directories(etc_dir):

        SxyCA.SETTINGS["path"] = etc_dir

        for X in [
            SxyCA.SETTINGS["path"],
            os.path.join(SxyCA.SETTINGS["path"], "certs/"),
            os.path.join(SxyCA.SETTINGS["path"], "certs/", "default/")]:

            if not os.path.isdir(X):
                try:
                    os.mkdir(X)
                except FileNotFoundError:
                    print(SxyCA.Options.indent*" " + "fatal: path {} doesn't exit".format(X))
                    return

                except PermissionError:
                    print(SxyCA.Options.indent*" " + "fatal: Permission denied: {}".format(X))
                    return

        SxyCA.SETTINGS["path"] = os.path.join(SxyCA.SETTINGS["path"], "certs/", "default/")

    @staticmethod
    def init_settings(cn, c, ou=None, o=None, l=None, s=None, def_subj_ca=None, def_subj_srv=None, def_subj_clt=None):

        # we want to extend, but not overwrite already existing settings
        SxyCA.load_settings()

        r = SxyCA.SETTINGS

        for k in ["ca", "srv", "clt", "prt"]:
            if k not in r:
                r[k] = {}

        for k in ["ca", "srv", "clt", "prt"]:
            if "ou" not in r[k]: r[k]["ou"] = pref_choice(ou)
            if "o" not in r[k]:  r[k]["o"] = pref_choice("Smithproxy Software")
            if "s" not in r[k]:  r[k]["s"] = pref_choice(s)
            if "l" not in r[k]:  r[k]["l"] = pref_choice(l)
            if "c" not in r[k]:  r[k]["c"] = pref_choice("CZ", c)

        if "cn" not in r["ca"]:   r["ca"]["cn"] = pref_choice(def_subj_ca, "Smithproxy Root CA")
        if "cn" not in r["srv"]:  r["srv"]["cn"] = pref_choice(def_subj_srv, "Smithproxy Server Certificate")
        if "cn" not in r["clt"]:  r["clt"]["cn"] = pref_choice(def_subj_clt, "Smithproxy Client Certificate")
        if "cn" not in r["prt"]:  r["prt"]["cn"] = "Smithproxy Portal Certificate"

        if "settings" not in r["ca"]: r["ca"]["settings"] = {
            "grant_ca": "false"
        }

        # print("config to be written: %s" % (r,))

        try:
            with open(os.path.join(SxyCA.SETTINGS["path"], "sslca.json"), "w") as f:
                json.dump(r, f, indent=4)

        except Exception as e:
            print(SxyCA.Options.indent*" " + "write_default_settings: exception caught: " + str(e))

    @staticmethod
    def load_settings():

        try:
            with open(os.path.join(SxyCA.SETTINGS["path"], "sslca.json"), "r") as f:
                r = json.load(f)
                if(SxyCA.Options.debug): print(SxyCA.Options.indent*" " + "load_settings: loaded settings: {}", str(r))

                SxyCA.SETTINGS = r

        except Exception as e:
            print(SxyCA.Options.indent*" " + "load_default_settings: exception caught: " + str(e))

    @staticmethod
    def generate_rsa_key(size):
        return rsa.generate_private_key(public_exponent=65537, key_size=size, backend=default_backend())

    @staticmethod
    def load_key(fnm, pwd=None):
        with open(fnm, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=pwd, backend=default_backend())

    @staticmethod
    def generate_ec_key(curve=ec.SECP256R1):
        return ec.generate_private_key(curve=curve, backend=default_backend())

    @staticmethod
    def save_key(key, keyfile, passphrase=None):
        # inner function
        def choose_enc(pwd):
            if not pwd:
                return serialization.NoEncryption()
            return serialization.BestAvailableEncryption(pwd)

        try:
            with open(os.path.join(SxyCA.SETTINGS['path'], keyfile), "wb") as f:
                f.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=choose_enc(passphrase),
                ))

        except Exception as e:
            print(SxyCA.Options.indent*" " + "save_key: exception caught: " + str(e))


    NameOIDMap = {
        "cn": NameOID.COMMON_NAME,
        "ou": NameOID.ORGANIZATIONAL_UNIT_NAME,
        "o": NameOID.ORGANIZATION_NAME,
        "l": NameOID.LOCALITY_NAME,
        "s": NameOID.STATE_OR_PROVINCE_NAME,
        "c": NameOID.COUNTRY_NAME
    }

    @staticmethod
    def construct_sn(profile, sn_override=None):
        snlist = []

        override = sn_override
        if not sn_override:
            override = {}

        for subj_entry in ["cn", "ou", "o", "l", "s", "c"]:
            if subj_entry in override and subj_entry in SxyCA.NameOIDMap:
                snlist.append(x509.NameAttribute(SxyCA.NameOIDMap[subj_entry], override[subj_entry]))

            elif subj_entry in SxyCA.SETTINGS[profile] and SxyCA.SETTINGS[profile][subj_entry] and subj_entry in SxyCA.NameOIDMap:
                snlist.append(x509.NameAttribute(SxyCA.NameOIDMap[subj_entry], SxyCA.SETTINGS[profile][subj_entry]))

        return snlist

    @staticmethod
    def generate_csr(key, profile, sans_dns=None, sans_ip=None, isca=False, custom_subj=None):

        cn = SxyCA.SETTINGS[profile]["cn"].replace(" ", "-")
        sn = x509.Name(SxyCA.construct_sn(profile, custom_subj))

        sans_list = [x509.DNSName(cn)]

        if sans_dns:
            for s in sans_dns:
                if s == cn:
                    continue
                sans_list.append(x509.DNSName(s))

        if sans_ip:
            try:
                import ipaddress
                for i in sans_ip:
                    ii = ipaddress.ip_address(i)
                    sans_list.append(x509.IPAddress(ii))
            except ImportError:
                # cannot use ipaddress module
                pass

        sans = x509.SubjectAlternativeName(sans_list)

        builder = x509.CertificateSigningRequestBuilder()
        builder = builder.subject_name(sn)

        if sans:
            builder = builder.add_extension(sans, critical=False)

        builder = builder.add_extension(
            x509.BasicConstraints(ca=isca, path_length=None), critical=True)

        if (isca):
            builder = builder.add_extension(x509.KeyUsage(crl_sign=True, key_cert_sign=True,
                                                          digital_signature=False, content_commitment=False,
                                                          key_encipherment=False, data_encipherment=False,
                                                          key_agreement=False, encipher_only=False,
                                                          decipher_only=False),
                                            critical=True)

        else:
            builder = builder.add_extension(x509.KeyUsage(crl_sign=False, key_cert_sign=False,
                                                          digital_signature=True, content_commitment=False,
                                                          key_encipherment=True, data_encipherment=False,
                                                          key_agreement=False, encipher_only=False,
                                                          decipher_only=False),
                                            critical=True)
            ex = []
            ex.append(x509.oid.ExtendedKeyUsageOID.SERVER_AUTH)
            ex.append(x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH)
            builder = builder.add_extension(x509.ExtendedKeyUsage(ex), critical=False)

        csr = builder.sign(key, hashes.SHA256(), default_backend())

        return csr

    @staticmethod
    def sign_csr(key, csr, caprofile, arg_valid=0, isca=False, cacert=None, aia_issuers=None, ocsp_responders=None):

        valid = 30
        if arg_valid > 0:
            valid = arg_valid
        else:
            try:
                valid = SxyCA.SETTINGS["ttl"]
            except KeyError:
                pass



        one_day = datetime.timedelta(1, 0, 0)

        builder = x509.CertificateBuilder()
        builder = builder.subject_name(csr.subject)

        if not cacert:
            builder = builder.issuer_name(x509.Name(construct_sn(caprofile)))
        else:
            builder = builder.issuer_name(cacert.subject)

        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * valid))
        # builder = builder.serial_number(x509.random_serial_number()) # too new to some systems
        builder = builder.serial_number(int.from_bytes(os.urandom(10), byteorder="big"))
        builder = builder.public_key(csr.public_key())

        builder = builder.add_extension(x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False)

        # more info about issuer

        has_ski = False
        try:
            if cacert:
                ski = cacert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier)
                builder = builder.add_extension(x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ski.value),
                                                critical=False)
                has_ski = True
        except AttributeError:
            # this is workaround for older versions of python cryptography, not having from_issuer_subject_key_identifier
            # -> which throws AttributeError
            has_ski = False
        except x509.extensions.ExtensionNotFound:
            has_ski = False

        if not has_ski:
            builder = builder.add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()),
                                            critical=False)

        all_aias = []
        if aia_issuers:
            for loc in aia_issuers:
                aia_uri = x509.AccessDescription(AuthorityInformationAccessOID.CA_ISSUERS,
                                                 x509.UniformResourceIdentifier(loc))
                all_aias.append(aia_uri)

        if ocsp_responders:
            for resp in ocsp_responders:
                aia_uri = x509.AccessDescription(AuthorityInformationAccessOID.OCSP, x509.UniformResourceIdentifier(resp))
                all_aias.append(aia_uri)

        if all_aias:
            alist = x509.AuthorityInformationAccess(all_aias)
            builder = builder.add_extension(alist, critical=False)

        if(SxyCA.Options.debug): print(SxyCA.Options.indent*" " + "sign CSR: == extensions ==")

        for e in csr.extensions:
            if isinstance(e.value, x509.BasicConstraints):
                if(SxyCA.Options.debug): print(SxyCA.Options.indent*" " + "sign CSR: %s" % (e.oid,))

                if e.value.ca:
                    if(SxyCA.Options.debug): print((SxyCA.Options.indent+2)*" " + "           CA=TRUE requested")

                    if isca and not SxyCA.SETTINGS["ca"]["settings"]["grant_ca"]:
                        if(SxyCA.Options.debug): print((SxyCA.Options.indent+2)*" " + "           CA not allowed but overridden")
                    elif not SxyCA.SETTINGS["ca"]["settings"]["grant_ca"]:
                        if(SxyCA.Options.debug): print((SxyCA.Options.indent+2)*" " + "           CA not allowed by rule")
                        continue
                    else:
                        if(SxyCA.Options.debug): print((SxyCA.Options.indent+2)*" " + "           CA allowed by rule")

            builder = builder.add_extension(e.value, e.critical)

        certificate = builder.sign(private_key=key, algorithm=hashes.SHA256(), backend=default_backend())
        return certificate

    @staticmethod
    def save_certificate(cert, certfile):
        try:
            with open(os.path.join(SxyCA.SETTINGS['path'], certfile), "wb") as f:
                f.write(cert.public_bytes(
                    encoding=serialization.Encoding.PEM))

        except Exception as e:
            print(SxyCA.Options.indent*" " + "save_certificate: exception caught: " + str(e))

    @staticmethod
    def load_certificate(fnm):
        with open(fnm, 'r', encoding='utf-8') as f:
            ff = f.read()
            return x509.load_pem_x509_certificate(ff.encode('ascii'), backend=default_backend())



class Repeater:

    def __init__(self, fnm, server_ip, custom_sport=None):

        self.fnm = fnm

        self.packets = []
        self.origins = {}

        # write this data :)
        self.to_send = b''

        # list of indexes in packets
        self.origins['client'] = []
        self.origins['server'] = []

        self.sock = None
        self.sock_upgraded = None

        self.server_port = 0
        self.custom_ip = server_ip
        self.custom_sport = custom_sport        # custom source port (only with for client connections)

        self.whoami = ""

        # index of our origin
        self.packet_index = 0

        # index of in all packets regardless of origin
        self.total_packet_index = 0

        # packet read counter (don't use it directly - for read_packet smart reads)
        self.read_packet_counter = 0

        self.use_ssl = False
        self.sslv = 0
        self.ssl_context = None
        self.ssl_cipher = None
        self.ssl_sni = None
        self.ssl_alpn = None
        self.ssl_ecdh_curve = None
        self.ssl_cert = None
        self.ssl_key = None
        self.ssl_ca_cert = None
        self.ssl_ca_key = None

        self.tstamp_last_read = 0
        self.tstamp_last_write = 0
        self._last_countdown_print = 0

        self.scripter = None
        self.scripter_args = None

        self.exitoneot = False
        self.nostdin = False
        self.nohexdump = False

        self.omexit = False

        self.is_udp = False

        # our peer (ip,port)
        self.target = (0, 0)

        # countdown timer for sending
        self.send_countdown = 0

    # write @txt to temp file and return its full path
    def deploy_tmp_file(self, text):
        h, fnm = tempfile.mkstemp()
        o = os.fdopen(h, "w")
        o.write(text)
        o.close()

        g_delete_files.append(fnm)
        return fnm

    def load_scripter_defaults(self):
        global g_delete_files

        if self.scripter:

            self.server_port = self.scripter.server_port
            self.packets = self.scripter.packets
            self.origins = self.scripter.origins

            has_cert = False
            has_ca = False

            if self.scripter.ssl_cert and self.scripter.ssl_key:
                has_cert = True

            if self.scripter.ssl_ca_cert and self.scripter.ssl_ca_key:
                has_ca = True

            try:
                if has_cert:
                    if self.scripter.ssl_cert and not self.ssl_cert:
                        self.ssl_cert = self.deploy_tmp_file(self.scripter.ssl_cert)

                    if self.scripter.ssl_key and not self.ssl_key:
                        self.ssl_key = self.deploy_tmp_file(self.scripter.ssl_key)

                if has_ca:
                    if self.scripter.ssl_ca_cert and not self.ssl_ca_cert:
                        self.ssl_ca_cert = self.deploy_tmp_file(self.scripter.ssl_ca_cert)
                        print("deployed temp ca cert:" + self.ssl_ca_cert)

                    if self.scripter.ssl_ca_key and not self.ssl_ca_key:
                        self.ssl_ca_key = self.deploy_tmp_file(self.scripter.ssl_ca_key)
                        print("deployed temp ca key:" + self.ssl_ca_key)
            except IOError as e:
                print("error deploying temporary files: " + str(e))

    def list_pcap(self, verbose=False):

        flows = {}
        ident = {}
        frame = -1

        if verbose:
            print_yellow("# >>> Flow list:")

        s = rdpcap(self.fnm)
        for i in s:

            frame += 1

            try:
                sip = i[IP].src
                dip = i[IP].dst
            except IndexError as e:
                # not even IP packet
                continue

            proto = "TCP"

            sport = ""
            dport = ""

            # TCP
            try:
                sport = str(i[TCP].sport)
                dport = str(i[TCP].dport)
            except IndexError as e:
                proto = "UDP"

            # UDP
            if proto == "UDP":
                try:
                    sport = str(i[UDP].sport)
                    dport = str(i[UDP].dport)
                except IndexError as e:
                    proto = "Unknown"

            # Unknown
            if proto == "Unknown":
                continue

            key = proto + " / " + sip + ":" + sport + " -> " + dip + ":" + dport
            ident1 = sip + ":" + sport
            ident2 = dip + ":" + dport

            if key not in flows:
                if verbose:
                    print_yellow("%s (starting at frame %d)" % (key, frame))
                flows[key] = (ident1, ident2)

                if ident1 not in ident.keys():
                    ident[ident1] = []
                if ident2 not in ident.keys():
                    ident[ident2] = []

                ident[ident1].append(key)
                ident[ident2].append(key)

        print_yellow("\n# >>> Usable connection IDs:")
        if verbose:
            print_white("   Yellow - probably services")
            print_white("   Green  - clients\n")

        print_white("# More than 2 simplex flows:\n"
                    "#   * source port reuse, or it's service")
        print_white("#   * can't be used to uniquely dissect data from file.")

        for unique_ident in ident.keys():

            port = unique_ident.split(":")[1]
            if int(port) < 1024:
                print_yellow(unique_ident + " # %d simplex flows" % (len(ident[unique_ident]),))
            else:
                flow_count = len(ident[unique_ident])

                if flow_count > 2:
                    # Fore.RED + Style.BRIGHT + what + Style.RESET_ALL
                    print_green(unique_ident + Fore.RED + " # %d simplex flows" % (len(ident[unique_ident]),))
                else:
                    print_green(unique_ident)

    def read_pcap(self, im_ip, im_port):

        s = rdpcap(self.fnm)

        # print("Looking for client connection %s:%s" % (im_ip,im_port))

        for i in s:

            try:
                sip = i[IP].src
                dip = i[IP].dst
                sport = 0
                dport = 0
                proto = i[IP].proto

                # print_white("debug: read_pcap: ip.proto " +  str(i[IP].proto))
                if i[IP].proto == 6:
                    sport = str(i[TCP].sport)
                    dport = str(i[TCP].dport)
                elif i[IP].proto == 17:
                    sport = str(i[UDP].sport)
                    dport = str(i[UDP].dport)

            except IndexError as e:
                # IndexError: Layer [TCP|UDP|IP] not found
                continue

            # print ">>> %s:%s -> %s:%s" % (sip,sport,dip,dport)

            origin = None

            if sip == im_ip and sport == im_port:
                origin = "client"
                if self.server_port == 0:
                    self.server_port = dport

            elif dip == im_ip and dport == im_port:
                origin = "server"

            if origin:
                p = ""

                if proto == 6:
                    p = i[TCP].payload
                elif proto == 17:
                    p = i[UDP].payload
                else:
                    print_red("read_cap: cannot find payload in packet")
                    continue

                if len(p) == 0:
                    # print "No payload"
                    continue

                # print("--")
                # print("Len: %s",help(p))
                if isinstance(p, Padding) or type(p) == type(Padding):
                    print("... reached end of tcp, frame contains padding")
                    continue
                # print(hexdump(str(p)))

                current_index = len(self.packets)

                self.packets.append(p)
                self.origins[origin].append(current_index)

                # print "%s payload:\n>>%s<<" % (origin,p,)

    def read_smcap(self, im_ip, im_port):
        file_packets = []

        self.packets = []
        self.origins["client"] = []
        self.origins["server"] = []

        this_packet_origin = None
        this_packet_index = 0
        this_packet_bytes = []

        have_connection = False

        fin = fileinput.input(files=[self.fnm, ])
        for line in fin:
            # print_yellow("Processing: " + line.strip())

            re_packet_start = re.compile(r'^\+\d+: +([^:]+):([^:]+)-([^:]+):([^:(]+)')
            re_packet_content_client = re.compile(r'^>\[([0-9a-f])+\][^0-9A-F]+([0-9A-F ]{2,49})')
            re_packet_content_server = re.compile(r'^ +<\[([0-9a-f])+\][^0-9A-F]+([0-9A-F ]{2,49})')

            sip = None
            dip = None
            sport = None
            dport = None

            if not have_connection:
                m = re_packet_start.search(line)
                if m:
                    # print_yellow_bright("Packet start: " + line.strip())
                    sip = m.group(1)
                    dip = m.group(3)
                    sport = m.group(2)
                    dport = m.group(4)
                    # print_yellow_bright("%s:%s -> %s:%s" % (sip,sport,dip,dport))
                    have_connection = True

                    self.server_port = dport

                    if sip.startswith("udp_"):
                        self.is_udp = True

            matched = False
            m = None

            if not matched:
                m = re_packet_content_client.search(line)
                if m:
                    # print_green_bright(line.strip())
                    # print_green(m.group(2))
                    this_packet_bytes.append(m.group(2))
                    this_packet_origin = 'client'
                    matched = True

            if not matched:
                m = re_packet_content_server.search(line)
                if m:
                    # print_red(m.group(2))
                    this_packet_bytes.append(m.group(2))
                    this_packet_origin = 'server'
                    matched = True

            if not matched:
                if this_packet_bytes:
                    # finalize packet

                    data = self.smcap_convert_lines_to_bytes(this_packet_bytes)
                    if this_packet_origin == 'client':
                        # print_green("# Converted: -->\n%s\n#<--" % (data,))
                        self.packets.append(data)
                        self.origins['client'].append(this_packet_index)
                    else:
                        # print_red("# Converted: -->\n%s\n#<--" % (data,))
                        self.packets.append(data)
                        self.origins['server'].append(this_packet_index)

                    this_packet_bytes = []
                    this_packet_origin = None
                    this_packet_index += 1

    def smcap_convert_lines_to_bytes(this, list_of_ords):
        bytes = b''

        for l in list_of_ords:
            for oord in l.split(" "):
                if oord:
                    bytes += binascii.unhexlify(oord)

        return bytes

    def list_smcap(self, args=None):

        fin = fileinput.input(files=[self.fnm, ])
        for line in fin:
            re_packet_start = re.compile(r'^\+\d+: ([^:]+):([^:]+)-([^:]+):([^:(]+)')

            sip = None
            dip = None
            sport = None
            dport = None
            have_connection = False

            if not have_connection:
                m = re_packet_start.search(line)
                if m:
                    # print_yellow_bright("Packet start: " + line.strip())
                    sip = m.group(1)
                    dip = m.group(3)
                    sport = m.group(2)
                    dport = m.group(4)

                    if sip.startswith("udp_"):
                        self.is_udp = True

                    fin.close()

                    n = sip.find("_")
                    if n >= 0 and n < len(sip) - 1:
                        sip = sip[n + 1:]

                    n = dip.find("_")
                    if n >= 0 and n < len(dip) - 1:
                        dip = dip[n + 1:]

                    if args:
                        if args == "sip":
                            print("%s" % (sip,), file=sys.stderr)
                            return sip
                        elif args == "dip":
                            print("%s" % (dip,), file=sys.stderr)
                            return dip
                        elif args == "sport":
                            print("%s" % (sport,), file=sys.stderr)
                            return sport
                        elif args == "dport":
                            print("%s" % (dport,), file=sys.stderr)
                            return dport
                        elif args == "proto":
                            if self.is_udp:
                                print("udp", file=sys.stderr)
                                return "udp"
                            else:
                                print("tcp", file=sys.stderr)
                                return "tcp"

                    else:
                        print_yellow(
                            "%s:%s -> %s:%s  (single connection per file in smcap files)" % (sip, sport, dip, dport))
                        return "%s:%s" % (sip, sport)

    def export_self(self, efile):

        ssource = self.export_script(None)
        out = ''

        with open(__file__) as f:
            lines = f.read().split('\n')

            for single_line in lines:
                out += single_line
                out += "\n"

                # print("export line: %s" % (single_line))
                if single_line == "# EMBEDDED DATA BEGIN":

                    out += "\n"
                    out += ssource
                    out += "\n"

                    import hashlib
                    out += "pplay_version = \"" + str(pplay_version) + "-" + hashlib.sha1(
                        ssource.encode('utf-8')).hexdigest() + "\"\n"

        with open(efile, "w") as o:
            o.write(out)
            # print_red("pack: using " + efile)

    def export_script(self, efile):

        if efile and os.path.isfile(efile):
            print_red_bright("refusing to overwrite already existing file!")
            return None

        c = "__pplay_packed_source__ = True\n\n\n\n"
        c += "class PPlayScript:\n\n"
        c += "    def __init__(self, pplay=None, args=None):\n"
        c += "        # access to pplay engine\n"
        c += "        self.pplay = pplay\n\n"
        c += "        self.packets = []\n"
        c += "        self.args = args\n"

        for p in self.packets:
            c += "        self.packets.append(%s)\n\n" % (repr(p),)

        c += "        self.origins = {}\n\n"
        c += "        self.server_port = %s\n" % (self.server_port,)
        c += "        self.custom_sport = %s\n" % (self.custom_sport,)

        for k in self.origins.keys():
            c += "        self.origins['%s']=%s\n" % (k, self.origins[k])

        c += "\n\n"

        if self.ssl_cert:
            with open(self.ssl_cert) as ca_f:
                c += "        self.ssl_cert=\"\"\"\n" + ca_f.read() + "\n\"\"\"\n"

        if self.ssl_key:
            with open(self.ssl_key) as key_f:
                c += "        self.ssl_key=\"\"\"\n" + key_f.read() + "\n\"\"\"\n"

        c += "\n\n"
        if self.ssl_ca_cert:
            with open(self.ssl_ca_cert) as ca_f:
                c += "        self.ssl_ca_cert=\"\"\"\n" + ca_f.read() + "\n\"\"\"\n"

        if self.ssl_ca_key:
            with open(self.ssl_ca_key) as key_f:
                c += "        self.ssl_ca_key=\"\"\"\n" + key_f.read() + "\n\"\"\"\n"

        c += "\n\n"
        c += """
    def before_send(self,role,index,data):
        # when None returned, no changes will be applied and packets[ origins[role][index] ] will be used
        return None

    def after_received(self,role,index,data):
        # return value is ignored: use it as data gathering for further processing
        return None
        """

        if not efile:

            return c
        else:
            f = open(efile, 'w')
            f.write(c.decode('utf-8'))
            f.close()

        return None

    # for spaghetti lovers
    def impersonate(self, who):

        if who == "client":
            self.impersonate_client()
        elif who == "server":
            self.impersonate_server()

    def send_aligned(self):

        if self.packet_index < len(self.origins[self.whoami]):
            return self.total_packet_index >= self.origins[self.whoami][self.packet_index]
        return False

    def send_issame(self):
        if self.packet_index < len(self.origins[self.whoami]):
            return self.packets[self.origins[self.whoami][self.packet_index]] == self.to_send
        return False

    def ask_to_send(self, xdata=None):

        data = None
        if xdata is None:
            data = self.to_send
        else:
            data = xdata

        aligned = ''
        if self.send_aligned():
            aligned = '(in-sync'
        else:
            aligned = '(off-sync'

        if not self.send_issame():
            if aligned:
                aligned += ", modified"
            else:
                aligned += "(modified"

        if aligned:
            aligned += ") "

        out = "# [%d/%d]: %s" % (self.packet_index + 1, len(self.origins[self.whoami]), aligned)
        if self.send_aligned():
            print_green_bright(out)
        else:
            print_yellow(out)

        out = ''
        if self.nohexdump:
            out = "# ... offer to send %dB of data (hexdump surpressed): " % (len(data),)
        else:
            out = hexdump(data)

        if self.send_aligned():
            print_green(out)
        # 
        # dont print hexdumps of unaligned data
        # else:
        #    print_yellow(out)

        if option_auto_send < 0 or option_auto_send >= 5:

            out = ''
            out += "#<--\n"
            out += "#--> SEND IT TO SOCKET? [ y=yes (default) | s=skip | c=CR | l=LF | x=CRLF ]\n"
            out += "#    For more commands or help please enter 'h'.\n"

            if self.send_aligned():
                print_green_bright(out)
            else:
                print_yellow(out)

    def ask_to_send_more(self):

        if not self.nostdin:
            print_yellow_bright("#--> SEND MORE INTO SOCKET? [ c=CR | l=LF | x=CRLF | N=new data]")
        # print_yellow_bright("#    Advanced: r=replace (vim 's' syntax: r/<orig>/<repl>/<count,0=all>)")

    def starttls(self):
        if have_ssl:
            self.use_ssl = True
            self.sock = self.prepare_socket(self.sock, self.whoami == 'server')
            self.sock_upgraded = self.sock

            return True
        else:
            return False

    def prepare_ssl_socket(self, s, server_side, on_sni=False):

        if not server_side:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

            if self.sslv > 0:
                sv = 3
                self.ssl_context.options |= ssl.OP_NO_SSLv2
                for v in [ssl.OP_NO_SSLv3, ssl.OP_NO_TLSv1, ssl.OP_NO_TLSv1_1, ssl.OP_NO_TLSv1_2]:
                    if sv == self.sslv:
                        sv = sv + 1
                        continue

                    self.ssl_context.options |= v
                    sv = sv + 1

                # disable tls1.3
                if self.sslv < 7 and ssl.HAS_TLSv1_3:
                    self.ssl_context.options |= ssl.OP_NO_TLSv1_3

            if self.ssl_cipher:
                self.ssl_context.set_ciphers(self.ssl_cipher)

            if self.ssl_alpn:
                self.ssl_context.set_alpn_protocols(self.ssl_alpn)

            return self.ssl_context.wrap_socket(s, server_hostname=self.ssl_sni, suppress_ragged_eofs=True)
        else:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            if self.sslv > 0:
                sv = 3
                self.ssl_context.options |= ssl.OP_NO_SSLv2
                for v in [ssl.OP_NO_SSLv3, ssl.OP_NO_TLSv1, ssl.OP_NO_TLSv1_1, ssl.OP_NO_TLSv1_2]:
                    if sv == self.sslv:
                        sv = sv + 1
                        continue

                    self.ssl_context.options |= v
                    sv = sv + 1

                # disable tls1.3
                if self.sslv < 7 and ssl.HAS_TLSv1_3:
                    self.ssl_context.options |= ssl.OP_NO_TLSv1_3

            if self.ssl_cipher:
                self.ssl_context.set_ciphers(self.ssl_cipher)

            if self.ssl_ecdh_curve:
                self.ssl_context.set_ecdh_curve(self.ssl_ecdh_curve)

            if self.ssl_cert and self.ssl_key:
                self.ssl_context.load_cert_chain(certfile=self.ssl_cert, keyfile=self.ssl_key)

            if not on_sni:
                self.ssl_context.sni_callback = self.imp_server_ssl_callback
                return self.ssl_context.wrap_socket(s, server_side=True)
            else:
                s.context = self.ssl_context
                return s

    def prepare_socket(self, s, server_side=False):
        if have_ssl and self.use_ssl:
            return self.prepare_ssl_socket(s, server_side)
        else:
            return s

    def impersonate_client(self):
        global option_socks, g_script_module

        if g_script_module and not self.scripter:
            self.scripter = g_script_module.PPlayScript(self, self.scripter_args)
            self.load_scripter_defaults()

        try:
            self.whoami = "client"

            s = None
            if self.is_udp:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                if option_socks:
                    # print_red_bright("SOCKS socket init") # DEBUG

                    s = socks.socksocket()
                    if len(option_socks) > 1:
                        s.set_proxy(socks.SOCKS5, option_socks[0], int(option_socks[1]))
                    else:
                        s.set_proxy(socks.SOCKS5, option_socks[0], int(1080))
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            ip = self.custom_ip
            port = int(self.server_port)

            t = ip.split(":")
            if len(t) > 1:
                ip = t[0]
                port = int(t[1])

            if port == 0:
                port = int(self.server_port)

            self.target = (ip, port)

            print_white_bright("IMPERSONATING CLIENT, connecting to %s:%s" % (ip, port))

            self.sock = s

            try:
                if self.custom_sport:
                    self.sock.bind(('', int(self.custom_sport)))

                self.sock.connect((ip, int(port)))
            except socket.error as e:
                print_white_bright(" === ")
                print_white_bright("   Connecting to %s:%s failed: %s" % (ip, port, e))
                print_white_bright(" === ")
                return

            try:
                self.sock = self.prepare_socket(self.sock, False)
                self.packet_loop()

            except socket.error as e:
                print_white_bright(" === ")
                print_white_bright("   Connection to %s:%s failed: %s" % (ip, port, e))
                print_white_bright(" === ")
                return


        except KeyboardInterrupt as e:
            print_white_bright("\nCtrl-C: bailing it out.")
            return

    def imp_server_ssl_callback(self, sock, sni, ctx):
        print_white("requested SNI: %s" % (sni,))
        if not sni:
            if self.ssl_sni:
                print_yellow("using default explicit SNI: " + self.ssl_sni)
                sni = self.ssl_sni
            else:
                sni = "server.pplay.cloud"
                print_yellow("using fallback SNI: " + sni)

        if not have_crypto:
            # no cryptography ... ok - either we have server cert provided, or we are doomed.

            if not self.ssl_cert or not self.ssl_key:
                print_red_bright("neither having cryptography (no CA signing), nor certificate pair")
                print_red_bright("this won't end up well.")
            return

        try:
            sslca_root = "/tmp/pplay-ca"
            SxyCA.init_directories(sslca_root)
            SxyCA.init_settings(cn=None, c=None)
            SxyCA.load_settings()

            if self.ssl_ca_cert and self.ssl_ca_key:
                ca_key = SxyCA.load_key(self.ssl_ca_key)
                ca_cert = SxyCA.load_certificate(self.ssl_ca_cert)

                prt_key = SxyCA.generate_rsa_key(2048)
                prt_csr = SxyCA.generate_csr(prt_key, "srv", sans_dns=[sni, ], sans_ip=None,
                                             custom_subj={"cn": sni})
                prt_cert = SxyCA.sign_csr(ca_key, prt_csr, "srv", cacert=ca_cert)

                tmp_key_file = \
                tempfile.mkstemp(dir=os.path.join(sslca_root, "certs/", "default/"), prefix="sni-key-")[1]
                g_delete_files.append(tmp_key_file)

                tmp_cert_file = \
                tempfile.mkstemp(dir=os.path.join(sslca_root, "certs/", "default/"), prefix="sni-cert-")[1]
                g_delete_files.append(tmp_cert_file)

                SxyCA.save_key(prt_key, os.path.basename(tmp_key_file))
                SxyCA.save_certificate(prt_cert, os.path.basename(tmp_cert_file))

                self.ssl_key = tmp_key_file
                self.ssl_cert = tmp_cert_file

                self.prepare_ssl_socket(sock, server_side=True, on_sni=True)

                print_green("spoofing cert for sni:%s finished" % (sni,))
            else:
                print_red("CA key or CA cert not specified, fallback to pre-set certificate")

        except Exception as e:
            print_red("error in SNI handler: " + str(e))
            print_red("fallback to pre-set certificate")
            raise e

    def impersonate_server(self):
        global g_script_module

        orig_use_ssl = self.use_ssl

        try:
            ip = "0.0.0.0"
            port = int(self.server_port)

            if self.custom_ip:

                t = self.custom_ip.split(":")
                if len(t) > 1:
                    ip = t[0]
                    port = int(t[1])

                elif len(t) == 1:
                    # assume it's port
                    port = int(t[0])

                # if specified port is 0, use original port in the capture
                if port == 0:
                    port = int(self.server_port)

                # print("custom IP:PORT %s:%s" % (ip,port) )

            self.whoami = "server"
            print_white_bright("IMPERSONATING SERVER, listening on %s:%s" % (ip, port,))

            server_address = (ip, int(port))

            if self.is_udp:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if not self.is_udp:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.bind(server_address)

            if not self.is_udp:
                s.listen(1)

            while True:
                print_white("waiting for new connection...")

                conn = None
                client_address = ["", ""]

                if not self.is_udp:
                    while True:
                        readable, writable, errored = select([s, ], [], [], 0.25)
                        if s in readable:
                            break
                        else:
                            # timeout
                            if self.detect_parent_death():
                                self.on_parent_death()

                    conn, client_address = s.accept()
                    self.target = client_address
                    print_white_bright("accepted client from %s:%s" % (client_address[0], client_address[1]))
                else:
                    conn = s
                    client_address = ["", ""]

                # flush stdin before real commands are inserted
                sys.stdin.flush()

                # use_ssl might get changed, ie with some STARTTLS operation
                self.use_ssl = orig_use_ssl
                conn = self.prepare_socket(conn, True)
                self.sock = conn

                try:
                    if g_script_module:
                        self.scripter = g_script_module.PPlayScript(self, self.scripter_args)
                        self.load_scripter_defaults()

                    self.packet_loop()
                except KeyboardInterrupt as e:
                    print_white_bright(
                        "\nCtrl-C: hit in client loop, exiting to accept loop. Hit Ctrl-C again to terminate.")
                    self.sock.close()
                except socket.error as e:
                    print_white_bright(
                        "\nConnection with %s:%s terminated: %s" % (client_address[0], client_address[1], e,))
                    if self.is_udp:
                        break

                # reset it in both cases when Ctrl-C received, or connection was closed
                self.packet_index = 0
                self.total_packet_index = 0

            # print_white("debug: end of loop.")

        except KeyboardInterrupt as e:
            print_white_bright("\nCtrl-C: bailing it out.")
            return
        except socket.error as e:
            print_white_bright("Server error: %s" % (e,))
            sys.exit(16)

    def read(self, blocking=True):

        # print_red_bright("DEBUG: read(): blocking %d" % blocking)

        if have_ssl and self.use_ssl:
            data = ''

            self.sock.setblocking(blocking)
            while True:
                try:
                    pen = self.sock.pending()
                    # print_red_bright("DEBUG: %dB pending in SSL buffer" % pen)
                    if pen == 0:
                        pen = 10240

                    data = self.sock.recv(pen)
                except ssl.SSLError as e:
                    # print_red_bright("DEBUG: read(): ssl error")
                    # Ignore the SSL equivalent of EWOULDBLOCK, but re-raise other errors

                    if e.errno != ssl.SSL_ERROR_WANT_READ:
                        raise
                    continue

                except SystemError as e:
                    print_red_bright("read(): system error: %s" % (str(e),))

                data_left = self.sock.pending()
                while data_left:
                    data += self.sock.recv(data_left)
                    data_left = self.sock.pending()
                break

            self.tstamp_last_read = time.time()
            self.sock.setblocking(True)
            return data
        else:
            self.tstamp_last_read = time.time()
            if not self.is_udp:
                self.sock.setblocking(True)
                return self.sock.recv(24096)
            else:
                data, client_address = self.sock.recvfrom(24096)
                self.target = client_address
                self.sock.setblocking(True)
                return data

    def write(self, data):

        if not data:
            return 0

        ll = len(data)
        l = 0

        if have_ssl and self.use_ssl:
            self.tstamp_last_write = time.time()
            while l < ll:
                r = self.sock.send(data[l:])
                l += r

                # print warning
                if r != ll:
                    print_red_bright("debug write: sent %d out of %d" % (l, ll))

            return l

        else:
            self.tstamp_last_write = time.time()
            if not self.is_udp:
                while l < ll:
                    r = self.sock.send(data[l:])
                    l += r

                    if r != ll:
                        print_red_bright("debug write: sent %d out of %d" % (l, ll))

                return l

            else:
                return self.sock.sendto(data, self.target)

    def load_to_send(self, role, role_index):
        who = self
        if self.scripter:
            who = self.scripter

        to_send_idx = who.origins[role][role_index]
        return who.packets[to_send_idx]

    def send_to_send(self):

        if self.to_send:
            self.packet_index += 1
            self.total_packet_index += 1

            total_data_len = len(self.to_send)
            total_written = 0

            while total_written != total_data_len:
                cnt = self.write(self.to_send)

                # not really clean debug, lots of data will be duplicated
                # if cnt > 200: cnt = 200

                data_len = len(self.to_send)

                if cnt == data_len:
                    print_green_bright("# ... %s [%d/%d]: has been sent (%d bytes)" % (
                        str_time(), self.packet_index, len(self.origins[self.whoami]), cnt))
                else:
                    print_green_bright("# ... %s [%d/%d]: has been sent (ONLY %d/%d bytes)" % (
                        str_time(), self.packet_index, len(self.origins[self.whoami]), cnt, data_len))
                    self.to_send = self.to_send[cnt:]

                total_written += cnt

            self.to_send = None

    def detect_parent_death(self):
        # mypid = os.getpid()
        # parpid = os.getppid()
        # print_red_bright("mypid %d, parent pid %d" % (mypid,parpid,))        

        return os.getppid() == 1

    def on_parent_death(self):
        sys.exit(-2)

    def select_wrapper(self, no_writes):

        inputs = [self.sock, sys.stdin]
        if self.nostdin:
            # print_red_bright("STDIN not used")
            inputs = [self.sock, ]

        outputs = [self.sock]
        if no_writes:
            outputs.remove(self.sock)

        if have_ssl and self.use_ssl:
            r = []
            w = []
            e = []

            if self.sock.pending(): r.append(self.sock)  # if there are bytes,

            if not no_writes:
                w.append(self.sock)  # FIXME: we assume we can always write without select

            rr, ww, ee = select(inputs, outputs, [], 0.2)
            if self.sock in rr:
                r.append(self.sock)
            if sys.stdin in rr:
                r.append(sys.stdin)

            if self.detect_parent_death():
                self.on_parent_death()

            return r, w, e

        else:

            r, w, e = select(inputs, outputs, [], 0.2)
            if self.detect_parent_death():
                self.on_parent_death()

            return r, w, e

    def is_eot(self):
        return self.total_packet_index >= len(self.packets)

    def packet_read(self):
        # print_red_bright("DEBUG: reading socket")

        d = self.read()

        # print_red_bright("DEBUG: read returned %d" % len(d))
        if not len(d):
            return len(d)

        expected_data = self.packets[self.total_packet_index]

        # wait for some time
        loopcount = 0
        len_expected_data = len(expected_data)
        len_d = len(str(d))
        t_start = time.time()

        while len_d < len_expected_data:
            # print_white("incomplete data: %d/%d" % (len_d,len_expected_data))
            loopcount += 1

            delta = time.time() - t_start
            if delta > 1:
                time.sleep(0.05)

            if delta > 10:
                break

            d += self.read()
            len_d = len(str(d))

        else:
            print_white("finished data: %d/%d" % (len_d, len_expected_data))

        # there are still some data to send/receive
        if self.total_packet_index < len(self.packets):
            # test if data are as we should expect
            aligned = False

            # if auto is enabled, we will not wait for user input when we received already some packet
            # user had to start pplay on the other side
            if option_auto_send:
                self.auto_send_now = time.time()

            # to print what we got and what we expect
            # print_white_bright(hexdump(d))
            # print_white_bright(hexdump(self.packets[self.total_packet_index]))

            scripter_flag = ""
            if self.scripter:
                scripter_flag = " (sending to script)"

            if d == self.packets[self.total_packet_index]:
                aligned = True
                self.total_packet_index += 1
                print_red_bright("# ... %s: received %dB OK%s" % (str_time(), len(d), scripter_flag))


            else:
                print_red_bright("# !!! /!\ DIFFERENT DATA /!\ !!!")
                smatch = difflib.SequenceMatcher(None, d, self.packets[self.total_packet_index],
                                                 autojunk=False)
                qr = smatch.ratio()
                if qr > 0.05:
                    print_red_bright(
                        "# !!! %s received %sB modified (%.1f%%)%s" % (str_time(), len(d), qr * 100, scripter_flag))
                    self.total_packet_index += 1
                else:
                    print_red_bright("# !!! %s received %sB of different data%s" % (str_time(), len(d), scripter_flag))

            if self.scripter:
                try:
                    self.scripter.after_received(self.whoami, self.packet_index, str(d))
                except AttributeError:
                    pass
                # print_red_bright("# received data processed")

            # this block is printed while in the normal packet loop (there are packets still to receive or send
            if aligned:
                if option_dump_received_correct:
                    print_red_bright("#-->")
                    print_red(hexdump(d))
                    print_red_bright("#<--")
            else:
                if option_dump_received_different:
                    print_red_bright("#-->")
                    print_red(hexdump(d))
                    print_red_bright("#<--")

        # this block means there is nothing to send/receive
        else:
            if option_dump_received_different:
                print_red_bright("#-->")
                print_red(hexdump(d))
                print_red_bright("#<--")

        # we have already data to send prepared!
        if self.to_send:
            #  print, but not block
            self.ask_to_send(self.to_send)
        else:
            self.ask_to_send_more()

        return len(d)

    def packet_write(self, cmd_hook=False):

        if self.packet_index >= len(self.origins[self.whoami]):
            print_yellow_bright("# [EOT]")
            self.ask_to_send_more()
            # if we have nothing to send, remove conn from write set
            self.to_send = None
            self.write_end = True
            return
        else:

            if not self.to_send:
                self.to_send = self.load_to_send(self.whoami, self.packet_index)

                # to_send_2 = None
                # if self.scripter:
                # try:
                # to_send_2 = self.scripter.before_send(self.whoami,self.packet_index,str(self.to_send))

                # except AttributeError:
                ## scripter doesn't have before_send implemented
                # pass

                # if to_send_2 != None:
                # print_yellow_bright("# data modified by script!")
                # self.to_send = to_send_2

                self.ask_to_send(self.to_send)

            else:

                if cmd_hook:
                    l = sys.stdin.readline()

                    # readline can return empty string
                    if len(l) > 0:
                        # print_white("# --> entered: '" + l + "'")
                        self.process_command(l.strip(), 'ysclxrihN')

                        # in auto mode, reset current state, since we wrote into the socket
                        if option_auto_send:
                            self.auto_send_now = time.time()
                            return

                # print_white_bright("debug: autosend = " + str(option_auto_send))

                # auto_send feature
                if option_auto_send > 0 and self.send_aligned():

                    now = time.time()
                    if self._last_countdown_print == 0:
                        self._last_countdown_print = now

                    delta = now - self._last_countdown_print
                    # print out the dot
                    if delta >= 1:

                        self.send_countdown = round(self.auto_send_now + option_auto_send - now)

                        # print dot only if there some few seconds to indicate
                        if option_auto_send >= 2:
                            # print(".",end='',file=sys.stderr)
                            # print(".",end='',file=sys.stdout)
                            if self.send_countdown > 0:
                                print("..%d" % (self.send_countdown,), end='\n', file=sys.stdout)
                                sys.stdout.flush()

                        self._last_countdown_print = now

                    if now - self.auto_send_now >= option_auto_send:

                        # indicate sending only when there are few seconds to indicate
                        if option_auto_send >= 2:
                            print_green_bright("  ... sending!")

                        been_sent = self.to_send
                        orig_index = self.packet_index

                        if self.scripter:
                            try:
                                to_send_2 = self.scripter.before_send(self.whoami, self.packet_index, str(self.to_send))

                            except AttributeError:
                                # scripter doesn't have before_send implemented
                                pass

                        self.send_to_send()
                        self.auto_send_now = now

                        if self.scripter:
                            try:
                                self.scripter.after_send(self.whoami, orig_index, str(been_sent))

                            except AttributeError:
                                # scripter doesn't have after_send implemented
                                pass

    def packet_loop(self):
        global option_auto_send

        running = 1
        self.write_end = False
        self.auto_send_now = time.time()
        eof_notified = False

        while running:
            # time.sleep(0.2)
            # print_red(".")

            if self.is_eot():

                # print_red_bright("DEBUG: is_eot returns true")

                if not eof_notified:
                    print_red_bright("### END OF TRANSMISSION ###")
                    eof_notified = True

                if self.exitoneot:
                    # print_red_bright("DEBUG: exitoneot true")

                    if self.whoami == "server":
                        if option_auto_send >= 0:
                            time.sleep(option_auto_send)
                        else:
                            time.sleep(0.5)

                        # FIXME: this blocks on client
                        if self.ssl_context:
                            # print_red_bright("DEBUG: unwrapping SSL")
                            self.sock.unwrap()

                    print_red("Exiting on EOT")

                    if not self.is_udp:
                        self.sock.shutdown(socket.SHUT_WR)
                    self.sock.close()
                    sys.exit(0)

            r, w, e = self.select_wrapper(self.write_end)

            # print_red_bright("DEBUG: sockets: r %s, w %s, e %s" % (str(r), str(w), str(e)))

            if self.sock in r and not self.send_aligned():

                l = self.packet_read()

                if l == 0:
                    print_red_bright("#--> connection closed by peer")
                    if self.exitoneot:
                        print_red("Exiting on EOT")
                        if not self.is_udp:
                            self.sock.shutdown(socket.SHUT_WR)
                        self.sock.close()
                        sys.exit(0)

                    break

            if self.sock in w:
                if not self.write_end:
                    self.packet_write(cmd_hook=(sys.stdin in r))

            if self.write_end and sys.stdin in r:
                l = sys.stdin.readline()
                if len(l) > 0:
                    self.process_command(l.strip(), 'yclxN')

                if self.to_send:
                    self.ask_to_send()
                else:
                    self.ask_to_send_more()

    def cmd_replace(self, command, data):
        # something like vim's replace:  r/something/smtelse/0

        if len(command) > 1:

            parts = command.split(command[1])
            # print_yellow(str(parts))
            if len(parts) == 4:
                return re.sub(parts[1], parts[2], str(data), int(parts[3]), flags=re.MULTILINE)
            else:
                print_yellow("Syntax error: please follow this pattern:")
                print_yellow("    r<delimiter><original><delimiter><replacement><delimiter><number_of_replacements>")
                print_yellow("Example:\n    r/GET/HEAD/1 ")
                print_yellow(
                    "Note:\n    Delimiter could be any character you choose. If number_of_replacements is zero, all occurences of original string are replaced.")
                return None

        return None

    def cmd_newdata(self, command, data):
        nd = ''
        nl = 1

        print_yellow_bright(
            "%% Enter new payload line by line (empty line commits). Lines will be sent out separated by CRLF.")
        l = sys.stdin.readline()

        while len(l) > 0:
            nd += l.strip() + "\r\n"
            nl += 1
            l = sys.stdin.readline()

        if nl > 1:
            print_yellow_bright("%% %d lines (%d bytes)" % (nl, len(nd)))
        else:
            print_yellow_bright("%% empty string - ignored")
        return nd

    def process_command(self, l, mask):
        global option_auto_send

        # print_yellow_bright("# thank you!")

        if l == '':
            l = 'y'

        if l[0] not in mask:
            print_yellow_bright("# Unknown command in this context.")
        else:
            if (l.startswith("y")):
                self.send_to_send()

                if self.packet_index == len(self.origins[self.whoami]):
                    print_green_bright("# %s [%d/%d]: that was our last one!!" % (
                        str_time(), self.packet_index, len(self.origins[self.whoami])))

            elif l.startswith('s'):
                self.packet_index += 1
                self.to_send = None
                print_green_bright(
                    "# %s [%d/%d]: has been SKIPPED" % (str_time(), self.packet_index, len(self.origins[self.whoami])))

            elif l.startswith('c'):
                self.to_send = None  # to reinit and ask again
                cnt = self.write("\n")
                print_green_bright("# %s custom '\\n' payload (%d bytes) inserted" % (str_time(), cnt,))

            elif l.startswith('l'):
                self.to_send = None  # to reinit and ask again
                cnt = self.write("\r")
                print_green_bright("# %s custom '\\r' payload (%d bytes) inserted" % (str_time(), cnt,))

            elif l.startswith('x'):
                self.to_send = None  # to reinit and ask again
                cnt = self.write("\r\n")
                print_green_bright("# %s custom '\\r\\n' payload (%d bytes) inserted" % (str_time(), cnt,))

            elif l.startswith('r') or l.startswith('N'):

                ret = None

                if l.startswith('r'):
                    ret = self.cmd_replace(l.strip(), self.to_send)
                elif l.startswith('N'):
                    ret = self.cmd_newdata(l.strip(), self.to_send)

                if ret:
                    self.to_send = ret
                    print_yellow_bright("# %s custom payload created (%d bytes)" % (str_time(), len(self.to_send),))
                    self.ask_to_send(self.to_send)
                else:
                    print_yellow_bright("# Custom payload not created")

            elif l.startswith('i'):
                option_auto_send = (-1 * option_auto_send)
                if option_auto_send > 0:
                    print_yellow_bright("# Toggle automatic send: enabled, interval %d" % (option_auto_send,))
                else:
                    print_yellow_bright("# Toggle automatic send: disabled")

            elif l.startswith('h'):
                self.print_help()

    def print_help(self):
        print_yellow_bright("#    More commands:")
        print_yellow_bright(
            "#    i  - interrupt or continue auto-send feature. Interval=%d." % (abs(option_auto_send),))
        print_yellow_bright("#    r  - replace (vim 's' syntax: r/<orig>/<repl>/<count,0=all>)")
        print_yellow_bright("#       - will try to match on all buffer lines")
        print_yellow_bright("#    N  - prepare brand new data. Multiline, empty line commits. ")


def main():
    global option_auto_send, g_script_module, have_colorama, option_socks

    parser = argparse.ArgumentParser(
        description=title,
        epilog=" - %s " % (copyright,))

    schemes_supported = "file,"
    if have_requests:
        schemes_supported += "http(s),"
    schemes_supported = schemes_supported[:-1]

    ds = parser.add_argument_group("Data Sources [%s]" % (schemes_supported,))
    group1 = ds.add_mutually_exclusive_group()
    if have_scapy:
        group1.add_argument('--pcap', nargs=1,
                            help='pcap where the traffic should be read (retransmissions not checked)')

    group1.add_argument('--smcap', nargs=1, help='textual capture taken by smithproxy')

    script_grp = group1.add_argument_group("Scripting options")
    script_grp.add_argument('--script', nargs=1,
                            help='load python script previously generated by --export command, OR use + to indicate script is embedded into source. See --pack option.')
    script_grp.add_argument('--script-args', nargs=1, help='pass string to the script args')

    ac = parser.add_argument_group("Actions")
    group2 = ac.add_mutually_exclusive_group()
    group2.add_argument('--client', nargs=1,
                        help='replay client-side of the CONNECTION, connect and send payload to specified IP address and port. Use IP:PORT or IP.')
    group2.add_argument('--server', nargs='?',
                        help='listen on port and replay server payload, accept incoming connections. Use IP:PORT or PORT')
    group2.add_argument('--list', action='store_true',
                        help='rather than act, show to us list of connections in the specified sniff file')
    group2.add_argument('--export', nargs=1,
                        help='take capture file and export it to python script according CONNECTION parameter')
    group2.add_argument('--pack', nargs=1, help='pack packet data into the script itself. Good for automation.')
    group2.add_argument('--smprint', nargs=1,
                        help='print properties of the connection. Args: sip,sport,dip,dport,proto')

    rc = parser.add_argument_group("Remotes")
    rcgroup = rc.add_mutually_exclusive_group()
    if have_paramiko:
        rcgroup.add_argument('--remote-ssh', nargs=1, help=""" Run itself on remote SSH server. 
        Arguments follow this IP:PORT or IP(with 22 as default SSH port) 
        Note: All local files related options are filtered out. 
        Remote server requires only pure python installed, as all smart stuff is done on the originating host.
        """)
        if have_socks:
            rcgroup.add_argument('--socks', nargs=1,
                                 help="""Client will connect via SOCKS proxy. Use IP:PORT, or IP (1080 is default port)""")

    ac_sniff = parser.add_argument_group("Sniffer file filters (mandatory unless --script is used)")
    ac_sniff.add_argument('--connection', nargs=1,
                          help='replay/export specified connection; use format <src_ip>:<sport>. IMPORTANT: it\'s SOURCE based to match unique flow!')

    prot = parser.add_argument_group("Protocol options")
    if have_ssl:
        prot.add_argument('--ssl', required=False, action='store_true',
                          help='toggle this flag to wrap payload to SSL (defaults to library ... default)')

    prot.add_argument('--tcp', required=False, action='store_true',
                      help='toggle to override L3 protocol from file and send payload in TCP')
    prot.add_argument('--udp', required=False, action='store_true',
                      help='toggle to override L3 protocol from file and send payload in UDP')
    prot.add_argument('--sport', required=False, nargs=1, help='Specify source port')

    if have_ssl:
        prot.add_argument('--ssl3', required=False, action='store_true',
                          help='ssl3 ... won\'t be supported by library most likely')
        prot.add_argument('--tls1', required=False, action='store_true', help='use tls 1.0')
        prot.add_argument('--tls1_1', required=False, action='store_true', help='use tls 1.1')
        prot.add_argument('--tls1_2', required=False, action='store_true', help='use tls 1.2')

        prot.add_argument('--tls1_3', required=False, action='store_true', help='use tls 1.3 (library claims support)')

    prot_ssl = parser.add_argument_group("SSL protocol options")
    if have_ssl:
        prot_ssl = parser.add_argument_group("SSL cipher support")
        prot_ssl.add_argument('--cert', required=False, nargs=1, help='certificate (PEM format) for --server mode')
        prot_ssl.add_argument('--key', required=False, nargs=1,
                              help='key of certificate (PEM format) for --server mode')

        if have_crypto:
            prot_ssl.add_argument('--cakey', required=False, nargs=1, help='use to self-sign server-side '
                                                                           'connections based on received SNI')
            prot_ssl.add_argument('--cacert', required=False, nargs=1, help='signing CA certificate to be used'
                                                                            'in conjunction with --ca-key')

        prot_ssl.add_argument('--cipher', required=False, nargs=1, help='specify ciphers based on openssl cipher list')
        prot_ssl.add_argument('--sni', required=False, nargs=1,
                              help='specify remote server name (SNI extension, client only)')
        prot_ssl.add_argument('--alpn', required=False, nargs=1,
                              help='specify comma-separated next-protocols for ALPN extension (client only)')
        prot_ssl.add_argument('--ecdh_curve', required=False, nargs=1, help='specify ECDH curve name')

    var = parser.add_argument_group("Various")

    auto_group = var.add_mutually_exclusive_group()
    auto_group.add_argument('--noauto', required=False, action='store_true',
                            help='toggle this to confirm each payload to be sent')
    auto_group.add_argument('--auto', nargs='?', required=False, type=float, default=5.0,
                            help='let %(prog)s to send payload automatically each AUTO seconds (default: %(default)s)')

    prot.add_argument('--version', required=False, action='store_true', help='just print version and terminate')
    var.add_argument('--exitoneot', required=False, action='store_true',
                     help='If there is nothing left to send and receive, terminate. Effective only in --client mode.')
    var.add_argument('--nostdin', required=False, action='store_true',
                     help='Don\'t read stdin at all. Good for external scripting, applies only with --auto')
    var.add_argument('--nohex', required=False, action='store_true', help='Don\'t show hexdumps for data to be sent.')
    var.add_argument('--nocolor', required=False, action='store_true', help='Don\'t use colorama.')

    var.add_argument('--verbose', required=False, action='store_true', help='Print out more output.')

    if have_paramiko:
        rem_ssh = parser.add_argument_group("Remote - SSH")
        rem_ssh.add_argument('--remote-ssh-user', nargs=1,
                             help='SSH user. You can use SSH agent, too (so avoiding this option).')
        rem_ssh.add_argument('--remote-ssh-password', nargs=1,
                             help='SSH password. You can use SSH agent, too (so avoiding this option).')

    args = parser.parse_args(sys.argv[1:])

    if have_colorama:
        if not args.nocolor:
            colorama.init(autoreset=False, strip=False)
        else:
            have_colorama = False

    if args.version:
        print_white_bright(title)
        print_white(copyright)
        print("", file=sys.stderr)
        print_white_bright(pplay_version)
        sys.exit(0)

    r = None
    if (have_scapy and args.pcap) or args.smcap:

        fnm = ""
        is_local = False

        if args.pcap:
            fnm = args.pcap[0]
        elif args.smcap:
            fnm = args.smcap[0]
        else:
            print_red_bright("it should not end up this way :/")
            sys.exit(255)

        if fnm.startswith("file://"):
            fnm = fnm[len("file://"):]
            is_local = True

        elif fnm.startswith("http://") or fnm.startswith("https://"):
            fnm = http_download_temp(fnm)
        else:
            is_local = True

        if fnm:
            if not os.path.isfile(fnm):
                print_red_bright("local file doesn't exist: " + fnm)
                sys.exit(3)

            r = Repeater(fnm, "")

    elif args.list:
        pass

    elif args.script or args.export:
        r = Repeater(None, "")

    elif have_paramiko and args.remote_ssh:
        # the same as script, but we won't init repeater
        pass
    else:
        print_yellow_bright(title)
        print_yellow_bright(copyright)
        print("")
        print_red("Colors support       : %d" % have_colorama)
        print_red("PCAP files support   : %d" % have_scapy)
        print_red("SSL support          : %d" % have_ssl)
        print_red("remote SSH support   : %d" % have_paramiko)
        print_red("remote files support : %d" % have_requests)
        print_red("Socks support        : %d" % have_socks)

        if have_ssl:
            print("")
            print_red("CA signing support   : %d" % have_crypto)


        print_red_bright("\nerror: nothing to do!")
        sys.exit(-1)

    if r is not None:
        if args.tcp:
            r.is_udp = False

        if args.udp:
            r.is_udp = True

        if args.ssl:
            if args.udp:
                print_red_bright("No DTLS support in python ssl wrappers, sorry.")
                sys.exit(-1)

            r.use_ssl = True

        if args.ssl3:
            r.sslv = 3
        if args.tls1:
            r.sslv = 4
        if args.tls1_1:
            r.sslv = 5
        if args.tls1_2:
            r.sslv = 6
        if args.tls1_3:
            r.sslv = 7

        if args.cert:
            r.ssl_cert = args.cert[0]

        if args.key:
            r.ssl_key = args.key[0]

        if args.cipher:
            r.ssl_cipher = ":".join(args.cipher)

        if args.sni:
            r.ssl_sni = args.sni[0]

        if args.alpn:
            r.ssl_alpn = args.alpn[0].split(',')

        if args.ecdh_curve:
            r.ssl_ecdh_curve = args.ecdh_curve[0]

        if args.cacert:
            r.ssl_ca_cert = args.cacert[0]

        if args.cakey:
            r.ssl_ca_key = args.cakey[0]

    if args.list:
        if args.smcap:
            r.list_smcap()
        elif have_scapy and args.pcap:
            r.list_pcap(args.verbose)

        sys.exit(0)

    elif args.smprint:
        if args.smcap:
            pr = None
            if args.smprint:
                pr = args.smprint[0]
                r.list_smcap(pr)
                sys.exit(0)

        sys.exit(-1)

    # content is controlled by script
    if args.script:

        if args.script_args:
            r.scripter_args = args.script_args[0]

        try:

            if args.script[0] != "+":
                # add current directory into PYTHONPATH
                sys.path.append(os.getcwd())

                # if there is path specified in the script filename, add it to PYTHONPATH too
                if os.path.dirname(args.script[0]) != '':
                    sys.path.append(os.path.dirname(args.script[0]))

                print_white_bright("Loading custom script: %s (pwd=%s)" % (args.script[0], os.getcwd()))

                mod_name = args.script[0]
                if mod_name.endswith(".py"):
                    mod_name = mod_name[0:-3]
                g_script_module = __import__(os.path.basename(mod_name), globals(), locals(), [], -1)

                r.scripter = g_script_module.PPlayScript(r, r.scripter_args)
                r.load_scripter_defaults()
            else:
                r.scripter = PPlayScript(r, r.scripter_args)
                r.load_scripter_defaults()

        except ImportError as e:
            print_red_bright("Error loading script file: %s" % (str(e),))
            # print_red(pprint.pformat(sys.))
            sys.exit(-2)
        except AttributeError as e:
            print_red_bright("Error loading script file: %s" % (str(e),))
            sys.exit(-2)

    if args.export or args.pack or args.client or args.server:
        if args.connection:
            l = args.connection[0].split(":")
            im_ip = None
            im_port = None

            if len(l) != 2:
                print_red_bright("error: connection syntax!")
                sys.exit(-1)

            im_ip = l[0]
            im_port = l[1]

            if args.smcap:
                r.read_smcap(im_ip, im_port)
            elif have_scapy and args.pcap:
                r.read_pcap(im_ip, im_port)

            if args.tcp:
                r.is_udp = False
            elif args.udp:
                r.is_udp = True


        elif args.smcap:
            # no --connection option setsockopt

            # okay, smcap holds only single connection
            # detect and read the connection

            ip_port = r.list_smcap().split(":")
            if len(ip_port) > 1:
                im_ip = ip_port[0]
                im_port = ip_port[1]
                r.read_smcap(im_ip, im_port)


        # we have to have data available, unless controlled by script
        elif not (args.script or args.export):
            print_white_bright("--connection argument has to be set for this option")
            sys.exit(-1)

        # cannot collide with script - those are in the exclusive argparse group
        if args.export:

            if args.cert:
                r.ssl_cert = args.cert[0]

            if args.key:
                r.ssl_key = args.key[0]

            if args.ca_cert:
                r.ssl_ca_cert = args.cacert[0]

            if args.ca_key:
                r.ssl_ca_key = args.cakey[0]

            export_file = args.export[0]
            if r.export_script(export_file):
                print_white_bright("Template python script has been exported to file %s" % (export_file,))
            sys.exit(0)

        elif args.pack:
            pack_file = args.pack[0]

            if args.cert:
                r.ssl_cert = args.cert[0]

            if args.key:
                r.ssl_key = args.key[0]

            if args.cacert:
                r.ssl_ca_cert = args.cacert[0]

            if args.cakey:
                r.ssl_ca_key = args.cakey[0]

            r.export_self(pack_file)
            print_white_bright("Exporting self to file %s" % (pack_file,))
            sys.exit(0)


        # ok regardless data controlled by script or capture file read
        elif args.client or args.server:

            if have_paramiko:
                if args.remote_ssh:

                    port = "22"
                    host = "127.0.0.1"
                    host_port = args.remote_ssh[0].split(":")

                    if len(host_port) > 0:
                        host = host_port[0]
                        if not host:
                            host = "127.0.0.1"

                    if len(args.remote_ssh) > 0:
                        port = host_port[1]

                    print_white("remote location: %s:%s" % (host, port,))

                    # this have_ is local only!
                    have_script = False
                    my_source = None
                    try:
                        if __pplay_packed_source__:
                            print_white_bright("remote-ssh[this host] - having embedded PPlayScript")
                            have_script = True

                            # it's not greatest way to get this script source, but as long as pplay is 
                            # single-source python script, it will work. Otherwise, we will need to do quine
                            my_source = open(__file__).read()

                    except NameError as e:
                        have_script = False
                        # print_red_bright("!!! this source is not produced by --pack, all required files must be available on your remote!")

                    if not have_script:

                        print_white_bright(
                            "remote-ssh[this host] - packing to tempfile (you need all arguments for --pack)")

                        if args.cert:
                            r.ssl_cert = args.cert[0]

                        if args.key:
                            r.ssl_key = args.key[0]

                        temp_file = tempfile.NamedTemporaryFile(prefix="pplay", suffix="packed")
                        r.export_self(temp_file.name)
                        print_white_bright("remote-ssh[this host] - done")
                        my_source = open(temp_file.name).read()

                        have_script = True

                    if my_source:

                        try:
                            paramiko.util.log_to_file('/dev/null')
                            from paramiko.ssh_exception import SSHException, AuthenticationException

                            client = paramiko.SSHClient()
                            client.load_system_host_keys()
                            # client.set_missing_host_key_policy(paramiko.WarningPolicy)
                            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                            if args.remote_ssh_user and args.remote_ssh_password:
                                client.connect(hostname=host, port=int(port), username=args.remote_ssh_user[0],
                                               password=args.remote_ssh_password[0], allow_agent=False,
                                               look_for_keys=False)
                                chan = client.get_transport().open_session(timeout=10)

                            elif args.remote_ssh_user:
                                client.connect(hostname=host, port=int(port), username=args.remote_ssh_user[0])
                                chan = client.get_transport().open_session(timeout=10)

                                paramiko.agent.AgentRequestHandler(chan)
                            else:
                                client.connect(hostname=host, port=int(port))
                                chan = client.get_transport().open_session(timeout=10)

                                paramiko.agent.AgentRequestHandler(chan)

                            cmd = "python -u - "
                            if have_script:
                                cmd += "--script +"

                            # iterate args and filter unwanted remote arguments, because of this we are not allowing abbreviated options :(

                            filter_next = False
                            for arg in sys.argv[1:]:
                                if filter_next:
                                    filter_next = False
                                    continue

                                if arg.startswith("--remote") or arg.startswith("--smcap") or arg.startswith("--pcap") \
                                        or arg.startswith("--key") or arg.startswith("--cert"):
                                    filter_next = True
                                    continue

                                cmd += " " + arg

                            # don't monitor stdin (it's always readable over SSH)
                            # exit on the end of replay transmission --remote-ssh is intended to one-shot tests anyway
                            cmd += " --nostdin"

                            # FIXME: not sure about this. Don't assume what user really wants to do
                            # cmd += " --exitoneot"

                            # print_red("sending cmd: " + cmd)

                            #
                            # chan.set_environment_variable(name="PPLAY_COLORAMA",value="1")
                            chan.set_combine_stderr(True)
                            chan.exec_command(cmd)
                            stdin = chan.makefile("wb", 10240)
                            stdout = chan.makefile("r", 10240)
                            # stderr = chan.makefile_stderr("r", 1024)

                            # write myself (worm-like!)
                            stdin.write(my_source)
                            stdin.flush()
                            # we must shutdown, so remote python knows the script is complete
                            chan.shutdown_write()

                            # print_red("remote-ssh[remote host] stdin flushed")

                            while not chan.exit_status_ready():
                                time.sleep(0.1)
                                if chan.recv_ready():
                                    d = chan.recv(10240)
                                    if len(d) > 0:
                                        sys.stdout.write(d)

                                r, w, e = select([sys.stdin, ], [], [], 0.1)
                                if sys.stdin in r:
                                    cmd = sys.stdin.readline()

                                    # print_red("cmd: " + cmd + "<<")
                                    # this currently doesn't work - stdin is closed by channel                                
                                    stdin.write(cmd)


                        except paramiko.AuthenticationException as e:
                            print_red_bright("authentication failed")

                        except paramiko.SSHException as e:
                            print_red_bright("ssh protocol error")

                        except KeyboardInterrupt as e:
                            print_red_bright("Ctrl-C: bailing, terminating remote-ssh.")

                        finally:
                            client.close()

                        sys.exit(0)
                    else:
                        print_red_bright("paramiko unavailable or --pack failed")

            if have_socks and args.socks:
                # print_red("Will use SOCKS") # DEBUG
                option_socks = args.socks[0].split(":")

            if args.ssl:
                if not have_ssl:
                    print_red_bright("error: SSL not available!")
                    sys.exit(-1)

                if args.server:
                    if not (
                            (args.key and args.cert)
                            or
                            (args.cakey and args.cacert)
                           ) and not args.script:

                        print_red_bright("error: SSL server requires: \n"
                                         "      --key and --cert for exact server certificate\n"
                                         "   -or- \n"
                                         "      --cakey and --cacert argument for generated certs by CA\n")
                        sys.exit(-1)

                r.use_ssl = True

            if args.noauto:
                option_auto_send = -1
            elif args.auto:
                option_auto_send = args.auto

                if args.nostdin:
                    print_red_bright("stdin will be unmonitored")
                    r.nostdin = True

            else:
                # option_auto_send = 5
                pass

            if args.nohex:
                r.nohexdump = True

            if args.client:

                if args.sport:
                    r.custom_sport = args.sport[0]

                if len(args.client) > 0:
                    r.custom_ip = args.client[0]

                if args.exitoneot:
                    r.exitoneot = True

                r.impersonate('client')

            elif args.server:

                if args.exitoneot:
                    r.exitoneot = True

                if len(args.server) > 0:
                    # arg type is '?' so no list there, just string
                    r.custom_ip = args.server
                else:
                    r.custom_ip = None

                r.impersonate('server')

    else:
        print_white_bright(
            "No-op! You wanted probably to set either --client <target_server_ip> or --server arguments ... Hmm?")

    # parser.print_help()


def cleanup():
    global g_delete_files
    for f in g_delete_files:
        try:
            # print_white("unlink tempfile - %s" % (f,))
            os.unlink(f)
        except OSError as e:
            pass


import atexit

if __name__ == "__main__":
    atexit.register(cleanup)
    main()
