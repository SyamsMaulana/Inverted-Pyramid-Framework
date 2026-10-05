




from models import EpistemicClaim

class InvertedPyramidEngine:
    def __init__(self):
        self.apex_core = []      # Core Conclusions + Confidence Score
        self.supporting_body = [] # Reasoning, Evidence, Contradictions
        self.source_layer = []    # Raw Data, Provenance, Timestamps (Mengganti BASE_ARCHIVE)

    def process_claim(self, claim: EpistemicClaim):
        """Proses pembagian klaim ke dalam struktur piramida terbalik."""
        # Evaluasi status klaim terlebih dahulu
        claim.evaluate_epistemic_status()
        
        # 1. Populasi Source Layer (Akar Data)
        self.source_layer.append({
            "entity": claim.provenance["entity_id"],
            "hash": claim.content_hash,
            "agent": claim.provenance["agent"],
            "timestamp": claim.timestamp,
            "signature": claim.signature_hex
        })
        
        # 2. Populasi Supporting Body (Penalaran & Bukti)
        self.supporting_body.append({
            "statement": claim.statement,
            "supporting_evidence": claim.supporting_evidence,
            "contradicting_evidence": claim.contradicting_evidence,
            "status": claim.status
        })
        
        # 3. Populasi Apex Core (Hanya jika lolos ambang bukti/SUPPORTED)
        if claim.status == "SUPPORTED":
            self.apex_core.append({
                "core_conclusion": claim.statement,
                "confidence_score": claim.confidence_score,
                "authenticity": claim.authenticity_status
            })

    def compile_synthesis(self) -> dict:
        """
        Memperbaiki bug 'self' pada v1.0.0.
        Menghasilkan output sintetis terstruktur.
        """
        return {
            "APEX_CORE": self.apex_core,
            "SUPPORTING_BODY": self.supporting_body,
            "SOURCE_LAYER": self.source_layer
        }

