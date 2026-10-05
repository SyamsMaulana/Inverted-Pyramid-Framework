





import hashlib
import datetime
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class EvidenceObject:
    content: str
    provider_agent: str
    source_uri: Optional[str] = None
    
    content_hash: Optional[str] = None
    created_at: Optional[str] = None
    received_at: Optional[str] = None
    
    evidence_type: str = "PRIMARY"       # PRIMARY | SECONDARY | TERTIARY | ANECDOTAL
    provenance_type: str = "DIRECT"      # DIRECT | DERIVED | TRANSLATED | SYNTHESIZED
    
    signature: Optional[str] = None
    public_key_id: Optional[str] = None
    
    signature_status: str = "UNSIGNED"   # UNSIGNED | VALID | INVALID
    source_status: str = "UNVERIFIED"   # UNVERIFIED | DECLARED | VERIFIED_EXTERNAL
    
    # Status Independensi (Bukan Boolean Sederhana):
    # Valid values: UNKNOWN | DISJOINT_IDENTITY | DECLARED_INDEPENDENCE | POLICY_VERIFIED
    independence_status: str = "UNKNOWN"
    derived_from: Optional[str] = None

    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        if not self.received_at:
            self.received_at = datetime.datetime.now(datetime.timezone.utc).isoformat()


class EpistemicClaim:
    def __init__(self, statement: str, author_agent: str = "ICAM/Syams Maulana"):
        self.statement = statement
        self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # 1. Integrity Layer
        self.content_hash = hashlib.sha256(statement.encode('utf-8')).hexdigest()
        self.integrity_status = "HASH_MATCH"
        
        # 2. Authenticity Layer
        self.attribution_mark = f"ICAM Attribution Mark [{author_agent}]"
        self.signature_hex = None
        self.authenticity_status = "UNVERIFIED"
        
        # 3. Provenance Layer (W3C PROV Compliant)
        self.provenance = {
            "entity_id": f"urn:claim:{self.content_hash[:10]}",
            "activity": "CLAIM_GENERATION",
            "agent": author_agent,
            "was_derived_from": []
        }
        
        # 4. Evidence Layer (Mendukung Objek Bukti Baru & String Legacy)
        self.supporting_evidence: List[EvidenceObject] = []
        self.contradicting_evidence: List[EvidenceObject] = []
        
        # 5. Epistemic Status
        self.status = "UNVERIFIED"
        self.confidence_score = 0.0

    def add_evidence(self, evidence, is_contradiction: bool = False, provider_agent: str = "UNKNOWN"):
        """
        Menambahkan bukti. Mendukung masukan berupa objek EvidenceObject 
        maupun string (untuk kompatibilitas skrip lama).
        """
        if isinstance(evidence, str):
            evidence_obj = EvidenceObject(
                content=evidence,
                provider_agent=provider_agent,
                independence_status="DECLARED_INDEPENDENCE" if provider_agent != self.provenance["agent"] else "UNKNOWN"
            )
        else:
            evidence_obj = evidence
            
        if is_contradiction:
            self.contradicting_evidence.append(evidence_obj)
        else:
            self.supporting_evidence.append(evidence_obj)
            
    def evaluate_epistemic_status(self):
        """
        P1 Engine Rules: Evaluasi berdasarkan Objek Bukti terstruktur.
        """
        supp_count = len(self.supporting_evidence)
        contra_count = len(self.contradicting_evidence)
        
        if contra_count > 0 and contra_count >= supp_count:
            self.status = "CONTRADICTED"
            self.confidence_score = 0.0
        elif supp_count > 0 and contra_count == 0:
            # Peningkatan status dasar ke PROVISIONAL / SUPPORTED
            self.status = "SUPPORTED"
            self.confidence_score = min(0.5 + (supp_count * 0.15), 0.85)
        elif supp_count > 0 and contra_count > 0:
            self.status = "INCONCLUSIVE"
            self.confidence_score = 0.4
        else:
            self.status = "UNVERIFIED"
            self.confidence_score = 0.0
