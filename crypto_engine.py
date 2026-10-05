import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

KEYS_DIR = "keys"
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "icam_private.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "icam_public.pem")

class ICAMCryptoEngine:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self._ensure_keys()

    def _ensure_keys(self):
        os.makedirs(KEYS_DIR, exist_ok=True)
        try:
            if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
                with open(PRIVATE_KEY_PATH, "rb") as f:
                    self.private_key = serialization.load_pem_private_key(f.read(), password=None)
                with open(PUBLIC_KEY_PATH, "rb") as f:
                    self.public_key = serialization.load_pem_public_key(f.read())
            else:
                self.generate_keypair()
        except Exception:
            # Fallback jika berkas PEM terdeteksi korup/MalformedFraming
            self.generate_keypair()

    def generate_keypair(self):
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

        pem_private = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pem_public = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(pem_private)
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(pem_public)

    def sign_content(self, data: bytes) -> bytes:
        if not self.private_key:
            self.generate_keypair()
        return self.private_key.sign(data)

    def verify_signature(self, signature: bytes, data: bytes) -> bool:
        if not self.public_key:
            return False
        try:
            self.public_key.verify(signature, data)
            return True
        except Exception:
            return False
