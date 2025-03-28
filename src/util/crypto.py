from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64


class AES:

    def __init__(self, key: str):

        key = base64.b64encode(key.encode()).decode()
        # Decode Base64 key and store it
        self.key = base64.b64decode(key)
        # Ensure the key length is 16, 24, or 32 bytes for AES
        if len(self.key) not in {16, 24, 32}:
            raise ValueError("Invalid AES key length. Key must be 16, 24, or 32 bytes.")


    def encrypt(self, plaintext: str) -> bytes:
        # Pad the plaintext to be a multiple of the AES block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        # Create AES cipher in ECB mode
        cipher = Cipher(algorithms.AES(self.key), modes.ECB())
        encryptor = cipher.encryptor()

        # Encrypt the padded plaintext
        return encryptor.update(padded_data) + encryptor.finalize()


    def decrypt(self, ciphertext: bytes) -> str:
        # Create AES cipher in ECB mode
        cipher = Cipher(algorithms.AES(self.key), modes.ECB())
        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding from the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

        return decrypted.decode()


    def encrypt_to_base64(self, plaintext: str) -> str:
        """
        Encrypts the given plaintext and encodes the result to Base64.
        This mimics Java's `encryptToBase64` functionality.
        """
        encrypted_bytes = self.encrypt(plaintext)  # Encrypt the plaintext
        # Convert encrypted bytes to Base64 encoded string
        return base64.b64encode(encrypted_bytes).decode()

