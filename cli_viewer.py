import sys
from models import EpistemicClaim, EvidenceObject
from engine import InvertedPyramidEngine

def print_header():
    print("=" * 65)
    print("   INVERTED PYRAMID FRAMEWORK — EPISTEMIC CLI VIEWER v0.1")
    print("=" * 65)

def inspect_claim_demo():
    print_header()
    statement = input("\nMasukkan Klaim/Pernyataan yang ingin diuji: ")
    if not statement.strip():
        statement = "Klaim Uji Coba Default Engine"

    author = input("Masukkan ID Pembuat Klaim [default: ICAM/Syams Maulana]: ")
    if not author.strip():
        author = "ICAM/Syams Maulana"

    claim = EpistemicClaim(statement=statement, author_agent=author)
    
    print("\n--- MENAMBAHKAN BUKTI ---")
    ev_content = input("Masukkan konten bukti pendukung: ")
    if ev_content.strip():
        ev_agent = input("Masukkan ID Penyedia Bukti: ")
        claim.add_evidence(
            EvidenceObject(
                content=ev_content,
                provider_agent=ev_agent if ev_agent.strip() else "EXTERNAL_AGENT",
                independence_status="POLICY_VERIFIED" if ev_agent != author else "UNKNOWN"
            )
        )

    engine = InvertedPyramidEngine()
    engine.process_claim(claim)
    
    print("\n" + "=" * 65)
    print("                 EPISTEMIC EVALUATION RESULT")
    print("=" * 65)
    print(f"Statement    : {claim.statement}")
    print(f"Hash SHA256  : {claim.content_hash}")
    print(f"Author Agent : {claim.provenance['agent']}")
    print(f"Status State : {claim.status}")
    print(f"Conf. Score  : {claim.confidence_score}")
    print(f"Authenticity : {claim.authenticity_status}")
    print("=" * 65)

if __name__ == "__main__":
    inspect_claim_demo()
