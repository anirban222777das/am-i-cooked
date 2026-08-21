import json
import os
from pydantic import ValidationError
from mlx_lm import load, generate
from api.schemas import SituationAnalysis

# Use project-relative path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "qwen3-4b")

# Global instances to avoid reloading
_model = None
_tokenizer = None

SYSTEM_PROMPT = """You are an objective context extraction engine for a humor app called 'Am I Cooked?'. Your job is to analyze the user's situation and extract only the contextual information necessary for determining how bad (cooked) their situation is.

RULES:
- Only use information provided by the user.
- Never invent facts.
- Do not predict future events or make legal/medical conclusions.
- If information is unknown, use the `uncertainties` list.
- If the user provides contradictory statements, identify the contradiction in `uncertainties`.
- Treat emojis and slang as contextual signals (e.g., 💀 often implies high severity or urgency).
- Return ONLY the required JSON structured output. Do not output explanations outside the schema.

SARCASM HANDLING:
Distinguish literal statements from sarcasm. 
Example User: "Yeah I'm totally prepared. Haven't opened the book once."
Correct Interpretation: The first sentence is sarcastic. The user's preparation is very low (0).
You may use the `interpretation_notes` field to explain this: "The phrase 'totally prepared' conflicts with 'haven't opened the book once'; the latter provides stronger evidence of preparation."

JSON SCHEMA REQUIREMENTS:
- needs_more_context: boolean (set to true ONLY IF the user says something extremely short/vague like "bro 💀" or "help" and there is not enough context to judge their situation)
- category: one of [academic, career, financial, relationship, coding, deadline, personal, other]
- urgency: integer 0-10 (how soon it matters)
- preparation: integer 0-10 (how prepared they are. 0 = not prepared at all, 10 = fully prepared)
- consequences: integer 0-10 (how bad it is based ONLY on provided facts)
- recoverability: integer 0-10 (how easily they can recover. 0 = permanent ruin, 10 = easily fixed)
- time_remaining: string (e.g. 'tomorrow', 'unknown')
- key_factors: list of concise strings representing the most critical factors
- explicit_facts: list of undeniable facts directly stated by the user
- uncertainties: list of things that are unclear or contradictory
- confidence: float 0.0-1.0 (how confident you are in this extraction)
- interpretation_notes: string (optional short explanation of slang/sarcasm, leave blank if literal)

Output ONLY valid JSON."""

def _load_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        try:
            _model, _tokenizer = load(MODEL_PATH)
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {MODEL_PATH}. Did you download it? Error: {e}")

def extract_context(text: str) -> SituationAnalysis:
    """
    Sends raw text to the local Qwen3 4B model and returns a validated SituationAnalysis object.
    Raises ValueError if extraction fails or output is invalid.
    """
    _load_model()
    
    prompt = f"{SYSTEM_PROMPT}\n\nUser Text: {text}\nJSON Output:\n"
    messages = [{"role": "user", "content": prompt}]
    
    formatted_prompt = _tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    output = generate(_model, _tokenizer, prompt=formatted_prompt, max_tokens=400)
    
    clean_out = output.strip()
    if clean_out.startswith("```json"):
        clean_out = clean_out[7:-3]
    elif clean_out.startswith("```"):
        clean_out = clean_out[3:-3]
        
    try:
        data = json.loads(clean_out)
        return SituationAnalysis(**data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from LLM output: {e}\nRaw output: {clean_out}")
    except ValidationError as e:
        raise ValueError(f"LLM output failed schema validation: {e}\nRaw output: {clean_out}")
