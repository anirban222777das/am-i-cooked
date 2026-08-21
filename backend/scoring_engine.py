from api.schemas import SituationAnalysis
import math

def calculate_cooked_score(analysis: SituationAnalysis) -> dict:
    """
    Deterministically calculates a 0-100 cooked score based on the extracted situation context.
    
    Weights:
    - Urgency (W=3.0): Immediate problems are inherently worse.
    - Preparation Deficit (W=4.0): The core of being "cooked" is not being prepared. (10 - preparation)
    - Consequences (W=3.0): The objective fallout of failure.
    
    Recoverability (0-10) acts as a dampening multiplier. A highly recoverable situation
    reduces the raw score by up to 50% (multiplier = 1.0 - (recoverability * 0.05)).
    """
    
    # Check for insufficient information
    if getattr(analysis, 'needs_more_context', False):
        return {"status": "needs_more_context"}
        
    if not analysis.key_factors and not analysis.explicit_facts:
        return {"status": "needs_more_context"}
        
    if analysis.urgency == 0 and analysis.preparation == 0 and analysis.consequences == 0 and analysis.recoverability == 0:
        return {"status": "needs_more_context"}

    # Base features
    urgency = analysis.urgency
    preparation = analysis.preparation
    consequences = analysis.consequences
    recoverability = analysis.recoverability
    
    # Derived feature
    preparation_deficit = 10 - preparation
    
    # Weighted raw score (Max = 30 + 40 + 30 = 100)
    raw_score = (urgency * 3.0) + (preparation_deficit * 4.0) + (consequences * 3.0)
    
    # Recoverability dampening (0 -> 1.0, 10 -> 0.5)
    multiplier = 1.0 - (recoverability * 0.05)
    
    final_score = raw_score * multiplier
    
    # Ensure bounds
    clamped_score = max(0, min(100, int(round(final_score))))
    
    return {
        "status": "success",
        "cooked_score": clamped_score,
        "cooked_level": get_cooked_level(clamped_score),
        "level_int": score_to_level_int(clamped_score)
    }

def score_to_level_int(score: int) -> int:
    if score <= 20:
        return 0
    elif score <= 40:
        return 1
    elif score <= 60:
        return 2
    elif score <= 80:
        return 3
    elif score <= 95:
        return 4
    else:
        return 5

def get_cooked_level(score: int) -> str:
    if score <= 20:
        return "NOT COOKED 🟢"
    elif score <= 40:
        return "SLIGHTLY COOKED 🟡"
    elif score <= 60:
        return "GETTING COOKED 🟠"
    elif score <= 80:
        return "VERY COOKED 🔴"
    elif score <= 95:
        return "ABSOLUTELY COOKED 💀"
    else:
        return "CHARCOAL ☠️"
