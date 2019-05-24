import cryptography
import os
import jwt
from jwt.algorithms import Algorithm
from jwt.api_jws import PyJWS
from jwt.exceptions import (
    DecodeError, InvalidAlgorithmError, InvalidSignatureError,
    InvalidTokenError
)
from jwt.utils import base64url_decode, force_bytes, force_unicode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key, load_ssh_public_key
)

def encode_rs512(payload):
	rsa_priv_file = open(os.path.expanduser('~/.ssh/id_rsa'), 'r')
	priv_rsakey = load_pem_private_key(force_bytes(rsa_priv_file.read()), password=None, backend=default_backend())
	return jwt.encode(payload, priv_rsakey, algorithm='RS512')

def decode_rs512(payload):
	rsa_pub_file = open(os.path.expanduser('~/.ssh/id_rsa.pub'), 'r')
	pub_rsakey = load_ssh_public_key(force_bytes(rsa_pub_file.read()), backend=default_backend())
	return PyJWS().decode(payload, pub_rsakey)