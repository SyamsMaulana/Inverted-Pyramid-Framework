







from models import EpistemicClaim
from crypto_engine import ICAMCryptoEngine

class InvertedPyramidEngine:
    def __init__(self, crypto_engine: ICAMCryptoEngine = None):
        self.crypto_engine = crypto_engine
        self.apex_core = []       # Core Conclusions + Confidence Score
        self.supporting_body = [] # Reasoning, Evidence, Contradictions
        self.source_layer = []     # Raw Data, Provenance, Timestamps

    def process_claim(self, claim: EpistemicClaim):
        """
        P3 Mandatory Crypto Gate & Pyramid Routing:
        Memverifikasi tanda tangan digital sebelum routing klaim.
        """
        # 1. Mandatory Crypto Verification Gate
        if claim.signature_hex and self.crypto_engine:
            try:
                sig_bytes = bytes.fromhex(claim.signature_hex)
                raw_bytes = claim.statement.encode('utf-8')
                is_valid = self.crypto_engine.verify_signature(raw_bytes, sig_bytes)
                
                if is_valid:
                    claim.authenticity_status = "SIGNED_VALID"
                else:
                    claim.authenticity_status = "SIGNED_INVALID"
                    claim.status = "REJECTED"
            except Exception:
                claim.authenticity_status = "SIGNED_CORRUPTED"
                claim.status = "REJECTED"
        elif claim.signature_hex and not self.crypto_engine:
            # Peringatan: Terdapat signature tapi tidak ada crypto engine penyedia verifikasi
            claim.authenticity_status = "UNVERIFIED_NO_ENGINE"

        # 2. Evaluasi Epistemik State Machine jika belum REJECTED
        if claim.status != "REJECTED":
            claim.evaluate_epistemic_status()

        # 3. Populasi Source Layer (Akar Data Selalu Dicatat)
        self.source_layer.append({
            "entity": claim.provenance["entity_id"],
            "hash": claim.content_hash,
            "agent": claim.provenance["agent"],
            "timestamp": claim.timestamp,
            "signature": claim.signature_hex,
            "authenticity": claim.authenticity_status,
            "status": claim.status
        })

        # 4. Routing Penolakan (Jika REJECTED -> HENTIKAN PROMOSI)
        if claim.status == "REJECTED":
            return

        # 5. Populasi Supporting Body
        self.supporting_body.append({
            "statement": claim.statement,
            "supporting_evidence": claim.supporting_evidence,
            "contradicting_evidence": claim.contradicting_evidence,
            "status": claim.status
        })

        # 6. Populasi Apex Core (Hanya jika lolos ambang bukti/SUPPORTED)
        if claim.status == "SUPPORTED":
            self.apex_core.append({
                "core_conclusion": claim.statement,
                "confidence_score": claim.confidence_score,
                "authenticity": claim.authenticity_status
            })

    def compile_synthesis(self) -> dict:
        return {
            "APEX_CORE": self.apex_core,
            "SUPPORTING_BODY": self.supporting_body,
            "SOURCE_LAYER": self.source_layer
        }
