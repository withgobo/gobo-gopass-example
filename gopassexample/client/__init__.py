import json
import os
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime

from cryptography.hazmat.primitives import hashes, hmac, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY_SIZE = 16
BLOCK_SIZE = 16


class GoPass:
    def __init__(self, shared_secret: str):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(shared_secret.encode())
        key = digest.finalize()
        self.encryption_key, self.signing_key = key[:KEY_SIZE], key[KEY_SIZE:]

    def encrypt(self, msg: str) -> bytes:
        iv = os.urandom(BLOCK_SIZE)

        padder = padding.PKCS7(BLOCK_SIZE * 8).padder()
        encoded_padded_msg = padder.update(msg.encode())
        encoded_padded_msg += padder.finalize()

        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(encoded_padded_msg)
        ct += encryptor.finalize()
        return iv + ct

    # NOTE: not used
    def decrypt(self, encrypted_msg: bytes) -> str:
        iv, ct = encrypted_msg[:BLOCK_SIZE], encrypted_msg[BLOCK_SIZE:]

        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_encoded_msg = decryptor.update(ct)
        padded_encoded_msg += decryptor.finalize()

        unpadder = padding.PKCS7(BLOCK_SIZE * 8).unpadder()
        encoded_msg = unpadder.update(padded_encoded_msg)
        encoded_msg += unpadder.finalize()
        return encoded_msg.decode()

    def sign(self, encrypted_msg: bytes) -> bytes:
        h = hmac.HMAC(self.signing_key, hashes.SHA256())
        h.update(encrypted_msg)
        return h.finalize()

    def generate_token(self, obj: dict) -> str:
        obj = obj or {}
        obj["timestamp"] = datetime.utcnow().isoformat()
        encrypted_msg = self.encrypt(json.dumps(obj, default=str))
        signature = self.sign(encrypted_msg)
        return urlsafe_b64encode(encrypted_msg + signature).decode()

    # NOTE: not used
    def parse_token(self, token: str) -> dict:
        encoded_token = urlsafe_b64decode(token)

        encrypted_msg, signature = (
            encoded_token[: -hashes.SHA256.digest_size],
            encoded_token[-hashes.SHA256.digest_size :],
        )

        assert signature == self.sign(encrypted_msg)

        message = self.decrypt(encrypted_msg)
        return json.loads(message)

    def generate_url(self, obj: dict, domain: str, ssl: bool = True) -> str:
        token = self.generate_token(obj)
        proto = "https" if ssl else "http"
        return f"{proto}://{domain}/account/login/gopass/{token}"
