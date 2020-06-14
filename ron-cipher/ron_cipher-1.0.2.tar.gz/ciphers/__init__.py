from ciphers.caeser_cipher import CaeserCipher
from ciphers.vigenere_cipher import VigenereCipher
import argparse

VERSION = "1.0.2"


def caeser_cipher(args):  # pragma: no cover
    caeser = CaeserCipher(rotation=args.rotation)

    if args.action == "encrypt":
        print(caeser.encrypt(plain_text=args.input))
    else:
        print(caeser.decrypt(encrypted=args.input))


def vigenere_cipher(args):  # pragma: no cover
    vigenere = VigenereCipher(secret=args.secret)

    if args.action == "encrypt":
        print(vigenere.encrypt(plain_text=args.input))
    else:
        print(vigenere.decrypt(encrypted=args.input))


def parse_args():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Determine which cipher, rotation, input string"
    )
    subparsers = parser.add_subparsers(dest="cipher")

    caeser = subparsers.add_parser("caeser", help="Use the Caeser Cipher")
    caeser.add_argument(
        "-r",
        "--rotation",
        help="Set the rotation for the cipher",
        type=int,
        action="store",
        nargs="?",
        const=5,
    )
    caeser.add_argument(
        "-i",
        "--input",
        help="Set the input string for the cipher",
        type=str,
        action="store",
        required=True,
    )
    caeser.add_argument(
        "-a",
        "--action",
        help="Set the action for the cipher",
        choices=["encrypt", "decrypt"],
        action="store",
        required=True,
    )

    vigenere = subparsers.add_parser(
        "vigenere", help="Use the Vigenere Cipher"
    )
    vigenere.add_argument(
        "-s",
        "--secret",
        help="Set the secret for the cipher",
        action="store",
        type=str,
        nargs="?",
        const="secret",
    )
    vigenere.add_argument(
        "-i",
        "--input",
        help="Set the input string for the cipher",
        action="store",
        required=True,
    )
    vigenere.add_argument(
        "-a",
        "--action",
        help="Set the action for the cipher",
        choices=["encrypt", "decrypt"],
        action="store",
        required=True,
    )

    return parser.parse_args()


operations = {"caeser": caeser_cipher, "vigenere": vigenere_cipher}


def main():  # pragma: no cover
    args = parse_args()
    operations[args.cipher](args)
