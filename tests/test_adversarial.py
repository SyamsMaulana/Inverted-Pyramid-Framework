


import pytest
from models import EpistemicClaim, EvidenceObject, FORBIDDEN_EPISTEMIC_STATUSES
from engine import InvertedPyramidEngine
from crypto_engine import ICAMCryptoEngine

@pytest.fixture
def crypto():
    engine = ICAMCryptoEngine()
    engine.generate_keypair()
    return engine

@pytest.fixture
def pyramid_engine(crypto):
    return InvertedPyramidEngine(crypto_engine=crypto)

# Test 01: Claim tanpa bukti independen -> HANYA PROVISIONAL (Tidak ke APEX)
def test_01_self_attestation_yields_provisional(pyramid_engine):
    claim = EpistemicClaim("Bumi berbentuk kubus.", author_agent="Agent_A")
    claim.add_evidence("Bukti internal A", provider_agent="Agent_A")
    pyramid_engine.process_claim(claim)
    
    assert claim.status == "PROVISIONAL"
    assert len(pyramid_engine.apex_core) == 0

# Test 02: Forged Signature -> Status REJECTED
def test_02_invalid_signature_rejection(pyramid_engine):
    claim = EpistemicClaim("Transfer dana berhasil.", author_agent="Agent_A")
    claim.signature_hex = "deadbeef" * 8  # Forged Signature Fake Hex
    pyramid_engine.process_claim(claim)
    
    assert claim.authenticity_status in ["SIGNED_INVALID", "SIGNED_CORRUPTED"]
    assert claim.status == "REJECTED"
    assert len(pyramid_engine.supporting_body) == 0

# Test 03: Valid Signature -> Authenticity Status SIGNED_VALID
def test_03_valid_signature_pass(crypto, pyramid_engine):
    claim = EpistemicClaim("Klaim tervalidasi kunci.", author_agent="Agent_A")
    sig = crypto.sign_content(claim.statement.encode('utf-8'))
    claim.signature_hex = sig.hex()
    pyramid_engine.process_claim(claim)
    
    assert claim.authenticity_status == "SIGNED_VALID"

# Test 04: Contradiction Ratio -> Ditolak dari APEX (INCONCLUSIVE / CONTRADICTED)
def test_04_contradiction_blocks_apex(pyramid_engine):
    claim = EpistemicClaim("Metode X efisien 50%.", author_agent="Agent_A")
    claim.add_evidence("Bukti mendukung 1", provider_agent="Agent_B")
    claim.add_evidence("Bukti menolak 1", is_contradiction=True, provider_agent="Agent_C")
    pyramid_engine.process_claim(claim)
    
    assert claim.status in ["INCONCLUSIVE", "CONTRADICTED"]
    assert len(pyramid_engine.apex_core) == 0

# Test 05: Spam Evidence tanpa keberagaman sumber -> Tetap Dibatasi Skornya
def test_05_spam_evidence_capped_score():
    claim = EpistemicClaim("Spam Claim", author_agent="Agent_A")
    for i in range(50):
        claim.add_evidence(f"Spam text {i}", provider_agent="Agent_A")
    claim.evaluate_epistemic_status()
    
    assert claim.status == "PROVISIONAL"
    assert claim.confidence_score <= 0.5

# Test 06: Independent Evidence -> Dipromosikan ke SUPPORTED
def test_06_independent_evidence_promotes_supported(pyramid_engine):
    claim = EpistemicClaim("Eksperimen fisika A berhasil.", author_agent="Lab_Author")
    claim.add_evidence("Hasil verifikasi eksternal", provider_agent="Independent_Lab_B")
    pyramid_engine.process_claim(claim)
    
    assert claim.status == "SUPPORTED"
    assert len(pyramid_engine.apex_core) == 1

# Test 07: Hard Invariant Protection -> Mencegah Forbidden Status
def test_07_forbidden_status_raises_error():
    claim = EpistemicClaim("Claim dengan status terlarang", author_agent="Agent_A")
    claim.status = "VERIFIED_AL_HAQQ"
    
    with pytest.raises(ValueError):
        claim.supporting_evidence.append(EvidenceObject("Text", "Agent_B"))
        claim.evaluate_epistemic_status()

# Test 08: Missing Engine Flag Check
def test_08_signature_without_engine():
    engine_no_crypto = InvertedPyramidEngine(crypto_engine=None)
    claim = EpistemicClaim("Claim dengan signature tanpa engine", author_agent="Agent_A")
    claim.signature_hex = "abcd1234"
    engine_no_crypto.process_claim(claim)
    
    assert claim.authenticity_status == "UNVERIFIED_NO_ENGINE"

# Test 09: EvidenceObject Structured Representation Check
def test_09_evidence_object_structure():
    ev = EvidenceObject(content="Data bukti", provider_agent="Agent_X", source_uri="https://ref.org/1")
    assert ev.content_hash is not None
    assert ev.received_at is not None
    assert ev.independence_status == "UNKNOWN"

# Test 10: ICAM Blind Test -> Penetapan status bebas dari identitas Founder
def test_10_icam_blind_test(pyramid_engine):
    payload = "Efisiensi sistem komputasi terbukti 15%."
    
    claim_founder = EpistemicClaim(payload, author_agent="ICAM/Syams Maulana")
    claim_founder.add_evidence("Bukti eksternal", provider_agent="Verificator_X")
    
    claim_anon = EpistemicClaim(payload, author_agent="Anonymous_Agent_99")
    claim_anon.add_evidence("Bukti eksternal", provider_agent="Verificator_X")
    
    pyramid_engine.process_claim(claim_founder)
    pyramid_engine.process_claim(claim_anon)
    
    # Invariant: Kedua status dan confidence score WAJIB IDENTIK 100%
    assert claim_founder.status == claim_anon.status
    assert claim_founder.confidence_score == claim_anon.confidence_score

