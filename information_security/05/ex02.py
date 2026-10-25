"""
Confidentiality - symmetric encryption
Encrypt and decrypt a string with AES-256-GCM and a password.

Usage:
  Encrypt: python ex02.py encrypt "your message" "your password"
  Decrypt: python ex02.py decrypt "<base64-ciphertext>" "your password"

Key derivation: PBKDF2-HMAC-SHA256 with a random 16-byte salt (100 000 iterations)
Encryption:     AES-256-GCM with a random 12-byte nonce (provides confidentiality + integrity)

Wire format (base64-encoded):  salt(16) | nonce(12) | ciphertext+tag
"""

import os
import sys
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,          # 256 bits
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode())


def encrypt(plaintext: str, password: str) -> str:
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(salt + nonce + ciphertext).decode()


def decrypt(token: str, password: str) -> str:
    data = base64.b64decode(token)
    salt, nonce, ciphertext = data[:16], data[16:28], data[28:]
    key = derive_key(password, salt)
    return AESGCM(key).decrypt(nonce, ciphertext, None).decode()


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("encrypt", "decrypt"):
        print(__doc__)
        sys.exit(1)

    mode, text, password = sys.argv[1], sys.argv[2], sys.argv[3]

    if mode == "encrypt":
        print(encrypt(text, password))
    else:
        try:
            print(decrypt(text, password))
        except Exception:
            print("Decryption failed — wrong password or corrupted ciphertext.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
