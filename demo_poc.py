import json
from dataclasses import asdict
from models import EpistemicClaim, EvidenceObject
from engine import InvertedPyramidEngine
from crypto_engine import ICAMCryptoEngine

def custom_serializer(obj):
    if isinstance(obj, EvidenceObject):
        return asdict(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def run_real_world_poc():
    crypto = ICAMCryptoEngine()
    crypto.generate_keypair()
    pyramid = InvertedPyramidEngine(crypto_engine=crypto)

    print("=== EXECUTING REAL-WORLD PROOF OF CONCEPT ===")

    # Klaim 1: Proposal Dapur Inspirasi Tidore
    claim1 = EpistemicClaim(
        statement="Transformasi bahan pangan lokal Tidore meningkatkan nilai tambah ekonomi komunitas maritime.",
        author_agent="ICAM/Syams Maulana"
    )
    claim1.add_evidence(
        EvidenceObject(
            content="Laporan Studi Lapangan Dinas Ketahanan Pangan Maluku Utara 2026",
            provider_agent="Dinas_Ketahanan_Pangan_Malut",
            independence_status="POLICY_VERIFIED"
        )
    )
    sig1 = crypto.sign_content(claim1.statement.encode('utf-8'))
    claim1.signature_hex = sig1.hex()
    pyramid.process_claim(claim1)

    # Klaim 2: Klaim Terkontradiksi / Unverified
    claim2 = EpistemicClaim(
        statement="Penggunaan metode X 100% menjamin keberhasilan tanpa risiko.",
        author_agent="External_Contributor"
    )
    claim2.add_evidence("Klaim sepihak tanpa data pendukung", provider_agent="External_Contributor")
    claim2.add_evidence("Laporan kegagalan pengujian lapangan BSN", is_contradiction=True, provider_agent="BSN_Auditor")
    pyramid.process_claim(claim2)

    # Output Sintesis Pyramid
    synthesis = pyramid.compile_synthesis()
    print(json.dumps(synthesis, indent=2, default=custom_serializer))

if __name__ == "__main__":
    run_real_world_poc()
