


from models import EpistemicClaim
from engine import InvertedPyramidEngine

def test_contradiction_override():
    claim = EpistemicClaim("Klaim uji coba founder")
    claim.add_evidence("Bukti 1", is_contradiction=False)
    claim.add_evidence("Kontra Bukti 1", is_contradiction=True)
    
    claim.evaluate_epistemic_status()
    assert claim.status == "CONTRADICTED" or claim.status == "INCONCLUSIVE"
    assert claim.confidence_score <= 0.5

def test_engine_compile_method():
    engine = InvertedPyramidEngine()
    res = engine.compile_synthesis()
    assert "APEX_CORE" in res
    assert "SOURCE_LAYER" in res
