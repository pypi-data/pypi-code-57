import base64
import hashlib
import logging
import os
import shutil
import tempfile
import zipfile

import pyaes
import fire


MODULE_TEMPLATE = os.path.join(os.path.dirname(__file__), "module_template.txt")
KEY_SIZE = 16
MAX_LINE_LENGTH = 80

template = None

logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def _chunks(data, chunk_size):
    return (data[i:i + chunk_size] for i in range(0, len(data), chunk_size))


def encrypt_module(module_path, output_path, key):
    encryptor = pyaes.AESModeOfOperationCTR(key)
    with open(module_path, "r") as module_file:
        module_content = module_file.read()
    encrypted_module = base64.b64encode(encryptor.encrypt(module_content))
    encrypted_module = os.linesep + os.linesep.join(_chunks(encrypted_module, MAX_LINE_LENGTH))
    code_hash = hashlib.sha256(module_content).hexdigest()

    global template
    if template is None:
        with open(MODULE_TEMPLATE, "r") as template_file:
            template = template_file.read()

    with open(output_path, "w") as output_file:
        output_file.write(
            template.format(
                module_name=__name__,
                encryped_code=encrypted_module,
                code_hash=code_hash
            )
        )
    logger.debug("Encrypted file {} with into {}".format(module_path, output_path))


def load_module_content(encrypted_module, key, code_hash):
    decryptor = pyaes.AESModeOfOperationCTR(key)
    decrypted_module = decryptor.decrypt(
        base64.b64decode(encrypted_module.strip().replace(os.linesep, ""))
    )
    if hashlib.sha256(decrypted_module).hexdigest() != code_hash:
        raise ValueError("Decrypted code hash mismatch! Key made be wrong")
    return decrypted_module


def encrypt_wheel(wheel_path, output_dir, key):
    unzipped_dir = tempfile.mkdtemp()
    encrypted_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(wheel_path, "r") as wheel_file:
        wheel_file.extractall(unzipped_dir)

    logger.info("Encrypting wheel {}".format(wheel_path))
    for root, _, files in os.walk(unzipped_dir):
        encrypted_path = os.path.join(encrypted_dir, (os.path.relpath(root, unzipped_dir)))
        if not os.path.exists(encrypted_path):
            os.makedirs(encrypted_path)
        for file_name in files:
            source_file = os.path.join(root, file_name)
            destionation_file = os.path.join(encrypted_path, file_name)
            if file_name.endswith(".py"):
                encrypt_module(source_file, destionation_file, key)
            else:
                shutil.copy2(source_file, destionation_file)
                logger.debug("Copying {} to {}".format(source_file, destionation_file))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, os.path.basename(wheel_path))
    shutil.make_archive(output_path, "zip", root_dir=encrypted_dir)
    os.rename(output_path + ".zip", output_path)


def private(*paths, **kwargs):
    key = kwargs.pop("key", None)
    output = kwargs.pop("output", "output")

    for argument in kwargs.keys():
        if argument not in ["key", "output"]:
            logger.warning('Unknown argument "{}"'.format(argument))
            return

    if key is None:
        key = os.urandom(KEY_SIZE)
    else:
        if type(key) is not str:
            key = str(key)
        try:
            key = key.decode("hex")
        except TypeError:
            logger.warning("The key must be hexadecimal string!")
            return
        if len(key) != KEY_SIZE:
            logger.warning("The key must be of length {}, current length is {}".format(KEY_SIZE, len(key)))
            return

    if not os.path.exists(output):
        os.makedirs(output)

    logger.info("Using key {}".format(key.encode("hex")))
    with open(os.path.join(output, "key.txt"), "w") as key_file:
        key_file.write(key.encode("hex"))

    for path in paths:
        if not os.path.exists(path):
            logger.warning("Path {} does not exists, skipping".format(path))
            continue
        _, extension = os.path.splitext(path)
        if extension == ".whl":
            encrypt_wheel(path, output, key)
        elif extension == ".py":
            encrypt_module(path, output, key)
        else:
            logging.warning("Path {} must have extension .whl or .py, skipping".format(path))


def main():
    fire.Fire(private)


if __name__ == '__main__':
    main()
