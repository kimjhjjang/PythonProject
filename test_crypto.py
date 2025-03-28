import base64
import logging

import src.util.crypto as crypto
from src.util import setup_logging

setup_logging('test_crypto')

# Example Usage
# This corresponds to Base64.encode2String(this.pwd) in Java
key = 'q6O8Vgq21bdelnCz'

aes = crypto.AES(key)

# plain_text is 'connectionInfoId' + groupId'
plaintext = "2340005063G1000000001"

token = aes.encrypt_to_base64(plaintext)
logging.info("Encrypted Token (Base64): {}".format(token))

if token == "fpxOG+Azkz3ukekTeRjsfG33mnkwWL4lcbOespCKRu8=":
    logging.info('####### successfully encrypted #######')


# Decrypt the Base64 token to verify
encrypted_bytes = base64.b64decode(token)
decrypted = aes.decrypt(encrypted_bytes)
logging.info("Decrypted Token: {}".format( decrypted))

if plaintext == decrypted:
    logging.info('####### successfully decrypted #######')
