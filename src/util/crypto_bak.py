import hashlib
import os

from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


password = "12345"


def encrypt_password(plain_text):

    # Salt는 랜덤으로 생성 (Jasypt에서 SaltGenerator로 설정)
    salt = os.urandom(8)  # DES는 8바이트 Salt 필요

    # PBKDF2를 사용하여 키를 생성
    key = PBKDF2("CloudEncKeyForUplus", salt, dkLen=8, count=1000, hmac_hash_module=hashlib.md5)

    # DES 암호화 객체 생성
    cipher = DES.new(key, DES.MODE_CBC)

    # 평문을 패딩 처리하여 암호화
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), DES.block_size))

    # 암호문, Salt, IV를 base64로 인코딩하여 반환
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    salt_b64 = b64encode(salt).decode('utf-8')

    return f'ENC({salt_b64}:{iv}:{ct})'


def decrypt_password(encrypted_text):

    # 암호문에서 Salt, IV, 암호문 분리
    salt_b64, iv_b64, ct_b64 = encrypted_text[4:-1].split(':')
    salt = b64decode(salt_b64)
    iv = b64decode(iv_b64)
    ct = b64decode(ct_b64)

    # PBKDF2를 사용하여 키를 생성
    key = PBKDF2("CloudEncKeyForUplus", salt, dkLen=8, count=1000, hmac_hash_module=hashlib.md5)

    # DES 복호화 객체 생성
    cipher = DES.new(key, DES.MODE_CBC, iv)

    # 복호화
    decrypted = unpad(cipher.decrypt(ct), DES.block_size)

    return decrypted.decode('utf-8')


def encrypt(plain_text):

    # 비밀번호를 사용해 256비트 키 생성 (SHA-256)
    key = hashlib.sha256(password.encode()).digest()

    # AES 암호화 객체 생성
    cipher = AES.new(key, AES.MODE_CBC)

    # 평문 패딩 처리
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))

    # 암호문과 IV (초기화 벡터)를 base64로 인코딩하여 반환
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return f'ENC({iv}:{ct})'


def decrypt(encrypted_text):

    # 암호문에서 IV와 암호문 부분을 분리
    iv, ct = encrypted_text[4:-1].split(':')
    iv = b64decode(iv)
    ct = b64decode(ct)

    # 비밀번호를 사용해 256비트 키 생성 (SHA-256)
    key = hashlib.sha256(password.encode()).digest()

    # AES 복호화 객체 생성
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 복호화
    decrypted = unpad(cipher.decrypt(ct), AES.block_size)

    return decrypted.decode('utf-8')
