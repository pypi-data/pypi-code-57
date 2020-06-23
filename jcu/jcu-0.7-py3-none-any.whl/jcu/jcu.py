import argparse
import base64
import binascii
import json
#
# from Crypto.Hash import SHA512, SHA
# from Crypto.PublicKey import RSA
# from Crypto.Signature import PKCS1_v1_5

parser = argparse.ArgumentParser()
parser.add_argument("-ip", dest="ip", help="ip", default="192.168.2.251", required=False)
args = parser.parse_args()
ip = args.ip
print(ip)
#
# class JenkinsUpdateCenter:
#     def __init__(self):
#         self.updateCenterVersion = "1"
#         self.core = None
#         self.warnings = None
#         self.plugins = None
#         self.id = "default"
#         self.connectionCheckUrl = None
#         self._private_key = None
#         self._cert = [None]
#
#     @staticmethod
#     def _sha1_digest(body):
#         digest = base64.b64encode(SHA.new(body).digest()).decode("utf-8")
#         return digest
#
#     @staticmethod
#     def _sha512_digest(body):
#         digest = binascii.hexlify(SHA512.new(body).digest()).decode("utf-8")
#         return digest
#
#     def _sign(self, body, algo="SHA-1"):
#         signer = PKCS1_v1_5.new(self._private_key)
#         if algo == "SHA-1":
#             digest = SHA.new()
#         else:
#             digest = SHA512.new()
#         digest.update(body)
#         try:
#             signature = signer.sign(digest)
#         except Exception as err:
#             raise Exception("Could not make sign. " + str(err))
#         return signature
#
#     def _sha1_signature(self, body):
#         signature = base64.b64encode(self._sign(body, "SHA-1")).decode("utf-8")
#         return signature
#
#     def _sha512_signature(self, body):
#         signature = binascii.hexlify(self._sign(body, "SHA-512")).decode("utf-8")
#         return signature
#
#     def load_private(self, key_path):
#         try:
#             with open(key_path, "r") as fd:
#                 self._private_key = RSA.importKey(fd.read())
#         except Exception as err:
#             raise Exception("Could not load private key " + key_path + ". " + str(err))
#
#     def load_public(self, key_path):
#         try:
#             with open(key_path, "rb") as fd:
#                 self._cert = base64.b64encode(fd.read()).decode("utf-8")
#         except Exception as err:
#             raise Exception("Could not load public key " + key_path + ". " + str(err))
#
#     def out(self, fd):
#         output = {"updateCenterVersion": self.updateCenterVersion}
#         if self.core is not None:
#             output["core"] = self.core
#         if self.warnings is not None:
#             output["warnings"] = self.warnings
#         if self.plugins is not None:
#             output["plugins"] = self.plugins
#         output["id"] = self.id
#         if self.connectionCheckUrl is not None:
#             output["connectionCheckUrl"] = self.connectionCheckUrl
#         payload = (json.dumps(output, separators=(",", ":"), sort_keys=True, ensure_ascii=False).encode("utf-8"))
#         output["signature"] = {"certificates": [self._cert]}
#         output["signature"]["correct_digest"] = self._sha1_digest(payload)
#         output["signature"]["correct_digest512"] = self._sha512_digest(payload)
#         output["signature"]["correct_signature"] = self._sha1_signature(payload)
#         output["signature"]["correct_signature512"] = self._sha512_signature(payload)
#         try:
#             fd.write("updateCenter.post(\n" + json.dumps(output, separators=(",", ":"), sort_keys=True) + "\n);")
#         except Exception as err:
#             raise Exception("Could not write output. " + str(err))
#
#
# def main():
#     www_root = "/YUM/jenkins/"
#     original_update_center_json = "update-center.json"
#     www_url = f"http://{ip}:81/jenkins"
#     private_key = "update-center.key"
#     public_key = "update-center.der"
#
#     # Load original update center
#     with open(www_root + original_update_center_json, "r", encoding="utf-8") as fd:
#         original = json.loads(fd.read().replace("updateCenter.post(\n", "").replace("\n);", ""))
#
#     uc = JenkinsUpdateCenter()
#     uc.load_private(private_key)
#     uc.load_public(public_key)
#     uc.plugins = json.loads(
#         json.dumps(original["plugins"])
#             .replace("http://updates.jenkins-ci.org/download/plugins/", www_url + "/plugins/")
#             .replace("https://plugins.jenkins.io", www_url)
#             .replace("https://jenkins.io", www_url)
#     )
#     uc.warnings = original["warnings"]
#     uc.core = json.loads(
#         json.dumps(original["core"])
#             .replace("http://updates.jenkins-ci.org/download/war/", www_url + "/war/")
#             .replace("https://plugins.jenkins.io", www_url)
#             .replace("https://jenkins.io", www_url)
#     )
#     with open(www_root + "/update-center.json", "w") as fd:
#         uc.out(fd)
#
#
# if __name__ == '__main__':
#     main()
