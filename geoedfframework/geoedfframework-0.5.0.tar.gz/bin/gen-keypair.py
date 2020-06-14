#!/usr/bin/env python3

# this script is used to generate a public-private key pair for use in
# encrypting sensitive args to be transferred from the submit host to the execution machine

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

import os
import sys

arg_count = len(sys.argv)

# validation, we need the job directory as an argument
if arg_count < 1:
    raise Exception("Incorrect number of arguments provided")

job_dir = str(sys.argv[1])

curr_dir = os.getcwd()

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend())

public_key = private_key.public_key()

# Storing the keys
# store to both working dir (so can be transferred back) and job dir
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())

# save to curr dir and job dir
private_key_path = '%s/private.pem' % curr_dir
with open(private_key_path, 'wb') as f:
    f.write(pem)

private_key_path = '%s/private.pem' % job_dir
with open(private_key_path, 'wb') as f:
    f.write(pem)

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)

public_key_path = '%s/public.pem' % curr_dir
with open(public_key_path, 'wb') as f:
    f.write(pem)

public_key_path = '%s/public.pem' % job_dir
with open(public_key_path, 'wb') as f:
    f.write(pem)
