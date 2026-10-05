




import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class ICAMCryptoEngine:
    def __init__(self, key_dir="keys"):
        self.key_dir = key_dir
        os.makedirs(key_dir, exist_ok=True)
        self.priv_path = os.path.join(key_dir, "icam_private.pem")
        self.pub_path = os.path.join(key_dir, "icam_public.pem")

    def generate_keypair(self):
        """Menghasilkan pasangan Public & Private Key baru jika belum ada."""
        if not os.path.exists(self.priv_path):
            private_key = ed25519.Ed25519PrivateKey.generate()
            public_key = private_key.public_key()

            # Simpan Private Key
            with open(self.priv_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            # Simpan Public Key
            with open(self.pub_path, "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
            print("[Crypto] Keypair baru berhasil dibuat.")
        else:
            print("[Crypto] Keypair sudah ada. Menggunakan kunci eksis.")

    def sign_content(self, data_bytes: bytes) -> bytes:
        """Menandatangani data menggunakan Private Key."""
        with open(self.priv_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        return private_key.sign(data_bytes)

    def verify_signature(self, data_bytes: bytes, signature_bytes: bytes) -> bool:
        """Memverifikasi signature menggunakan Public Key."""
        try:
            with open(self.pub_path, "rb") as f:
                public_key = serialization.load_pem_public_key(f.read())
            public_key.verify(signature_bytes, data_bytes)
            return True
        except Exception:
            return False
