




import hashlib
import datetime

class EpistemicClaim:
    def __init__(self, statement: str, author_agent: str = "ICAM/Syams Maulana"):
        self.statement = statement
        self.timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        
        # 1. Integrity Layer
        self.content_hash = hashlib.sha256(statement.encode('utf-8')).hexdigest()
        self.integrity_status = "HASH_MATCH"
        
        # 2. Authenticity Layer (Kriptografi Nyata)
        self.attribution_mark = f"ICAM Attribution Mark [{author_agent}]"
        self.signature_hex = None
        self.authenticity_status = "UNVERIFIED"
        
        # 3. Provenance Layer (Sesuai Konsep W3C PROV)
        self.provenance = {
            "entity_id": f"urn:claim:{self.content_hash[:10]}",
            "activity": "CLAIM_GENERATION",
            "agent": author_agent,
            "was_derived_from": []
        }
        
        # 4. Evidence Layer
        self.supporting_evidence = []
        self.contradicting_evidence = []
        
        # 5. Epistemic Status
        self.status = "UNVERIFIED"
        self.confidence_score = 0.0

    def add_evidence(self, evidence_text: str, is_contradiction: bool = False):
        """Menambahkan bukti pendukung atau kontra-bukti."""
        if is_contradiction:
            self.contradicting_evidence.append(evidence_text)
        else:
            self.supporting_evidence.append(evidence_text)
            
    def evaluate_epistemic_status(self):
        """
        P3 Engine Rules: Tidak boleh status SUPPORTED tanpa pemeriksaan kontra-bukti.
        External evidence must override founder metadata.
        """
        supp_count = len(self.supporting_evidence)
        contra_count = len(self.contradicting_evidence)
        
        if contra_count > 0 and contra_count >= supp_count:
            self.status = "CONTRADICTED"
            self.confidence_score = 0.0
        elif supp_count > 0 and contra_count == 0:
            self.status = "SUPPORTED"
            # Skor bertambah seiring jumlah bukti independen
            self.confidence_score = min(0.5 + (supp_count * 0.15), 0.95)
        elif supp_count > 0 and contra_count > 0:
            self.status = "INCONCLUSIVE"
            self.confidence_score = 0.5
        else:
            self.status = "UNVERIFIED"
            self.confidence_score = 0.1
