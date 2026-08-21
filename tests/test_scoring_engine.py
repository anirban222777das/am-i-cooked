import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from scoring_engine import calculate_cooked_score, get_cooked_level
from api.schemas import SituationAnalysis

def _mock_analysis(urgency, preparation, consequences, recoverability, key_factors=["mock"]):
    return SituationAnalysis(
        category="academic",
        urgency=urgency,
        preparation=preparation,
        consequences=consequences,
        recoverability=recoverability,
        time_remaining="mock",
        key_factors=key_factors,
        explicit_facts=[],
        uncertainties=[],
        confidence=1.0,
        interpretation_notes=""
    )

def test_insufficient_context():
    res = calculate_cooked_score(_mock_analysis(0, 0, 0, 0, key_factors=[]))
    assert res["status"] == "needs_more_context"
    
def test_case_1_high_severity():
    # Exam tomorrow, prep 0, consequences high, recoverability low
    analysis = _mock_analysis(10, 0, 10, 0)
    res = calculate_cooked_score(analysis)
    assert res["status"] == "success"
    assert res["cooked_score"] == 100
    assert res["cooked_level"] == "CHARCOAL ☠️"

def test_case_2_high_recoverability():
    # Exam next month, prep 0, consequences 10, recoverability high
    analysis = _mock_analysis(2, 0, 10, 10)
    res = calculate_cooked_score(analysis)
    assert res["status"] == "success"
    assert res["cooked_score"] == 38 # (6 + 40 + 30) * 0.5 = 76 * 0.5 = 38
    assert res["cooked_level"] == "SLIGHTLY COOKED 🟡"

def test_case_3_high_prep():
    # Exam tomorrow, prep 9, consequences 10, recoverability 2
    analysis = _mock_analysis(10, 9, 10, 2)
    res = calculate_cooked_score(analysis)
    assert res["status"] == "success"
    # Raw: (30) + (4) + (30) = 64
    # Mult: 1.0 - 0.1 = 0.9
    # Final = 58
    assert res["cooked_score"] == 58
    assert res["cooked_level"] == "GETTING COOKED 🟠"

def test_case_4_not_cooked():
    # Prep 10, urgency 1, consequences 1, recoverability 10
    analysis = _mock_analysis(1, 10, 1, 10)
    res = calculate_cooked_score(analysis)
    assert res["status"] == "success"
    # Raw: 3 + 0 + 3 = 6
    # Mult: 0.5
    # Final: 3
    assert res["cooked_score"] == 3
    assert res["cooked_level"] == "NOT COOKED 🟢"

def test_boundary_values():
    assert get_cooked_level(0) == "NOT COOKED 🟢"
    assert get_cooked_level(20) == "NOT COOKED 🟢"
    assert get_cooked_level(21) == "SLIGHTLY COOKED 🟡"
    assert get_cooked_level(40) == "SLIGHTLY COOKED 🟡"
    assert get_cooked_level(41) == "GETTING COOKED 🟠"
    assert get_cooked_level(60) == "GETTING COOKED 🟠"
    assert get_cooked_level(61) == "VERY COOKED 🔴"
    assert get_cooked_level(80) == "VERY COOKED 🔴"
    assert get_cooked_level(81) == "ABSOLUTELY COOKED 💀"
    assert get_cooked_level(95) == "ABSOLUTELY COOKED 💀"
    assert get_cooked_level(96) == "CHARCOAL ☠️"
    assert get_cooked_level(100) == "CHARCOAL ☠️"
