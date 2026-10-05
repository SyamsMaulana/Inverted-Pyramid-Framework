import hashlib
import hmac
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional, List

class IntegrityStatus(Enum):
    INTACT = "INTEGRITY_INTACT"
    TAMPERED = "INTEGRITY_MUTATED"

class AuthenticityStatus(Enum):
    AUTHENTIC = "SIGNATURE_VALID"
    INVALID_SIGNATURE = "SIGNATURE_UNVERIFIED"

class AlHaqqProtocol:
    def __init__(self, author: str = "Syams Maulana (ICAM)", secret_key: str = "AL_HAQQ_SECRET_KEY"):
        self.author = author
        self.secret_key = secret_key.encode('utf-8')
        self.audit_chain: List[Dict[str, Any]] = []

    def compute_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _sign_hash(self, content_hash: str) -> str:
        """Menghasilkan HMAC-SHA256 Signature tanpa dependency eksternal."""
        return hmac.new(self.secret_key, content_hash.encode('utf-8'), hashlib.sha256).hexdigest()

    def sign_and_embed(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        content_hash = self.compute_hash(content)
        signature_hex = self._sign_hash(content_hash)
        
        payload = {
            "author": self.author,
            "timestamp_utc": timestamp,
            "content_hash": content_hash,
            "digital_signature_hex": signature_hex,
            "metadata": metadata or {},
            "raw_content": content
        }
        self._append_audit_log("SIGN_AND_EMBED", content_hash, payload)
        return payload

    def verify_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raw_content = payload.get("raw_content", "")
        claimed_hash = payload.get("content_hash", "")
        signature_hex = payload.get("digital_signature_hex", "")

        computed_hash = self.compute_hash(raw_content)
        integrity = IntegrityStatus.INTACT if computed_hash == claimed_hash else IntegrityStatus.TAMPERED

        expected_sig = self._sign_hash(claimed_hash)
        authenticity = AuthenticityStatus.AUTHENTIC if hmac.compare_digest(expected_sig, signature_hex) else AuthenticityStatus.INVALID_SIGNATURE

        verification_result = {
            "integrity": integrity.value,
            "authenticity": authenticity.value,
            "is_valid": (integrity == IntegrityStatus.INTACT and authenticity == AuthenticityStatus.AUTHENTIC)
        }
        self._append_audit_log("VERIFY_PAYLOAD", computed_hash, verification_result)
        return verification_result

    def _append_audit_log(self, action: str, target_hash: str, details: Any):
        prev_log_hash = self.audit_chain[-1]["log_hash"] if self.audit_chain else "GENESIS_NODE"
        log_entry = {
            "index": len(self.audit_chain),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "target_hash": target_hash,
            "prev_log_hash": prev_log_hash,
            "details": details
        }
        log_entry["log_hash"] = self.compute_hash(json.dumps(log_entry, sort_keys=True))
        self.audit_chain.append(log_entry)
