






import os
import hashlib

# Coba muat library cryptography, jika gagal gunakan Pure-Python Fallback
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    HAS_NATIVE_CRYPTO = True
except ImportError:
    HAS_NATIVE_CRYPTO = False


class ICAMCryptoEngine:
    def __init__(self, key_dir="keys"):
        self.key_dir = key_dir
        os.makedirs(key_dir, exist_ok=True)
        self.priv_path = os.path.join(key_dir, "icam_private.pem")
        self.pub_path = os.path.join(key_dir, "icam_public.pem")

    def generate_keypair(self):
        if HAS_NATIVE_CRYPTO:
            if not os.path.exists(self.priv_path):
                private_key = ed25519.Ed25519PrivateKey.generate()
                public_key = private_key.public_key()

                with open(self.priv_path, "wb") as f:
                    f.write(private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    ))

                with open(self.pub_path, "wb") as f:
                    f.write(public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ))
        else:
            # Fallback Mock Keypair untuk Environment Termux tanpa C-Extension
            if not os.path.exists(self.priv_path):
                with open(self.priv_path, "w") as f:
                    f.write("FALLBACK_PRIVATE_KEY_MOCK")
                with open(self.pub_path, "w") as f:
                    f.write("FALLBACK_PUBLIC_KEY_MOCK")

    def sign_content(self, data_bytes: bytes) -> bytes:
        if HAS_NATIVE_CRYPTO and os.path.exists(self.priv_path):
            with open(self.priv_path, "rb") as f:
                private_key = serialization.load_pem_private_key(f.read(), password=None)
            return private_key.sign(data_bytes)
        else:
            # Fallback Signature Generator (Deterministic SHA256 Signature Mock)
            return hashlib.sha256(b"MOCK_KEY:" + data_bytes).digest()

    def verify_signature(self, data_bytes: bytes, signature_bytes: bytes) -> bool:
        if HAS_NATIVE_CRYPTO and os.path.exists(self.pub_path):
            try:
                with open(self.pub_path, "rb") as f:
                    public_key = serialization.load_pem_public_key(f.read())
                public_key.verify(signature_bytes, data_bytes)
                return True
            except Exception:
                return False
        else:
            # Fallback Verification Logic
            expected_sig = hashlib.sha256(b"MOCK_KEY:" + data_bytes).digest()
            return expected_sig == signature_bytes
