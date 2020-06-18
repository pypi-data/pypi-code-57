import random
import json
import os
import requests
from umbral import config, keys, signing, pre, params, curve, kfrags
from umbral.curve import SECP256K1

config.set_default_curve(SECP256K1)

def produce(data, attribute, supertype_id, secret_access_key):
    sk = keys.UmbralPrivateKey.from_bytes(bytes.fromhex(secret_access_key))
    signing_key = keys.UmbralPrivateKey.from_bytes(bytes.fromhex(os.environ.get('SUPERTYPE_SIGNING_KEY')))

    pk = sk.get_pubkey()
    pk_hex = pk.to_bytes().hex()
    ciphertext, capsule = pre.encrypt(pk, bytes(data.get('data'), encoding='utf8'))
    ciphertext_hex = ciphertext.hex()
    capsule_hex = capsule.to_bytes().hex()
    capsule_params_curve_nid = capsule.params.curve.curve_nid
    verifying_key = signing_key.get_pubkey().to_bytes().hex()

    url = 'https://z1lwetrbfe.execute-api.us-east-1.amazonaws.com/default/produce'
    values = {
        'capsule_hex': capsule_hex,
        'supertype_id': supertype_id,
        'capsule_params_curve_nid': capsule_params_curve_nid,
        'ciphertext': ciphertext_hex,
        'pk': pk_hex,
        'attribute': attribute,
        'verifying_key': verifying_key
    }
    
    x = requests.post(url, json = values)
    return x 

def consume(supertype_id, attribute, date, secret_access_key):
    sk = keys.UmbralPrivateKey.from_bytes(bytes.fromhex(secret_access_key))
    pk_hex = sk.get_pubkey().to_bytes().hex()

    url = 'https://z1lwetrbfe.execute-api.us-east-1.amazonaws.com/default/consume'
    values = {
        'nuid': supertype_id,
        'pk': pk_hex,
        'attribute': attribute,
        'date': date,
    }

    x = requests.post(url, json = values)
    if (x.text == 'No entries found'):
        print('NOTHING TO SHOW')
        return 'Nothing to show'

    response = x.json()

    capsule = pre.Capsule.from_bytes(bytes.fromhex(response.get('capsuleHex')), pre.UmbralParameters(pre.Curve(response.get('capsuleParamsCurveNid'))))
    received_kfrags = response.get('connections')
    for i in range(len(received_kfrags)):
        received_kfrags[i] = kfrags.KFrag.from_bytes(bytes.fromhex(received_kfrags[i]))
    producer_verifying_key = (keys.UmbralPublicKey.from_hex(response.get('verifyingKey')))
    prodcuer_pk = keys.UmbralPublicKey.from_bytes(bytes.fromhex(response.get('vendor')))
    receiver_pk = keys.UmbralPublicKey.from_bytes(bytes.fromhex(pk_hex))
    received_kfrags = random.sample(received_kfrags, 10)
    capsule.set_correctness_keys(delegating=prodcuer_pk,
        receiving=receiver_pk,
        verifying=producer_verifying_key
    )

    cfrags = list()
    for kfrag in received_kfrags:
        cfrag = pre.reencrypt(kfrag=kfrag, capsule=capsule)
        cfrags.append(cfrag)

    capsule.set_correctness_keys(delegating=prodcuer_pk,
        receiving=receiver_pk,
        verifying=producer_verifying_key
    )
    for cfrag in cfrags:
        capsule.attach_cfrag(cfrag)

    cleartext = pre.decrypt(ciphertext=bytes.fromhex(response.get('ciphertext')), capsule=capsule, decrypting_key=sk)

    return cleartext.decode('utf-8')