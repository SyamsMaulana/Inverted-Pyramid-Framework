



from crypto_engine import ICAMCryptoEngine
from models import EpistemicClaim
from engine import InvertedPyramidEngine

def run_alhaqq_v2_demo():
    print("=== AL-HAQQ PROTOCOL v2.0 SYSTEM DEMO ===")
    
    # 1. Inisialisasi Kriptografi
    crypto = ICAMCryptoEngine()
    crypto.generate_keypair()
    
    # 2. Buat Klaim Baru oleh Syams Maulana
    claim_text = "Metode ekstraksi rempah lokal meningkatkan rendemen cita rasa hingga 30%."
    claim = EpistemicClaim(statement=claim_text, author_agent="ICAM/Syams Maulana")
    
    # 3. Penandatanganan Digital Nyata
    raw_bytes = claim.statement.encode('utf-8')
    sig = crypto.sign_content(raw_bytes)
    claim.signature_hex = sig.hex()
    
    # 4. Verifikasi Signature
    is_valid = crypto.verify_signature(raw_bytes, sig)
    claim.authenticity_status = "SIGNED_VALID" if is_valid else "SIGNED_INVALID"
    
    # 5. Uji Engine Contradiction & Evidence
    claim.add_evidence("Jurnal Kuliner 2025: Ekstraksi suhu rendah meningkatkan rendemen rasa.", is_contradiction=False)
    
    # Simulasi Pengujian Kontra-Bukti (Uncomment untuk menguji mekanisme pembatalan):
    # claim.add_evidence("Uji lab independen: Tidak ada kenaikan signifikan pada senyawa rasa.", is_contradiction=True)
    
    # 6. Eksekusi Inverted Pyramid Engine
    engine = InvertedPyramidEngine()
    engine.process_claim(claim)
    
    synthesis = engine.compile_synthesis()
    
    # 7. Output Hasil Audit Eksplisit
    print("\n[HASIL SINTESIS ARCHITECTURE v2]")
    print(f"Status Klaim       : {claim.status}")
    print(f"Confidence Score   : {claim.confidence_score}")
    print(f"Authenticity Status: {claim.authenticity_status}")
    print(f"Signature Verification: {'PASSED' if is_valid else 'FAILED'}")
    print("\n[APEX CORE]:", synthesis["APEX_CORE"])
    print("[SOURCE LAYER]:", synthesis["SOURCE_LAYER"])

if __name__ == "__main__":
    run_alhaqq_v2_demo()
