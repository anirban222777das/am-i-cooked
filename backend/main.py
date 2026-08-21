from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from api.schemas import PredictRequest, PredictResponse
from humor_engine.humor import generate_humor
from llm_engine import extract_context
from scoring_engine import calculate_cooked_score

app = FastAPI(
    title="Am I Cooked? 💀",
    description="A humorous ML API to tell you how screwed you are.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "cooked_level_model.joblib")
CATEGORY_PATH = os.path.join(BASE_DIR, "models", "category_model.joblib")

level_model = None
category_model = None
embedder = None

@app.on_event("startup")
def load_models():
    global level_model, category_model, embedder
    try:
        level_model = joblib.load(MODEL_PATH)
        category_model = joblib.load(CATEGORY_PATH)
        print("Loading embedder... (this might take a few seconds on first run)")
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not load models. Did you train them? Error: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "models_loaded": level_model is not None and embedder is not None}

@app.get("/model-info")
def model_info():
    if level_model is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    return {
        "level_model": str(level_model),
        "category_model": str(category_model),
        "embedder": "all-MiniLM-L6-v2"
    }

def calculate_score(probs, level):
    ev = sum(i * p for i, p in enumerate(probs))
    score = (ev / 5.0) * 100
    return min(100, max(0, int(score)))

@app.post("/predict/baseline", response_model=PredictResponse)
def predict_baseline(request: PredictRequest):
    if level_model is None or embedder is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # 1. Embed the text semantically
    embedding = embedder.encode([request.text])
    
    # 2. Predict Category
    category_pred = category_model.predict(embedding)[0]
    
    # 3. Predict Level
    probs = level_model.predict_proba(embedding)[0]
    level_pred = int(level_model.predict(embedding)[0])
    confidence = float(probs[level_pred])
    
    # 4. Score Calculation
    score = calculate_score(probs, level_pred)
    
    # 5. Humor Engine
    verdict, recs, level_name = generate_humor(level_pred, category_pred)
    
    # Simple semantic reasoning (mocked for speed)
    reasons = []
    if level_pred >= 4:
        reasons.append("Extreme severity detected in the semantics of the text.")
    if "tomorrow" in request.text.lower() or "hours" in request.text.lower() or "due" in request.text.lower():
        reasons.append("High urgency detected (time constraint)")
    if not reasons:
        reasons.append(f"Model identified patterns of a Level {level_pred} situation")
    
    return PredictResponse(
        cooked_score=score,
        cooked_level=level_name,
        level_int=level_pred,
        confidence=round(confidence, 2),
        category=category_pred,
        reasons=reasons,
        verdict=verdict,
        recommendations=recs
    )

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # 1. Extract context using LLM
    try:
        analysis = extract_context(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    # 2. Calculate score
    score_result = calculate_cooked_score(analysis)
    
    # 3. Handle insufficient context
    if score_result.get("status") == "needs_more_context":
        return PredictResponse(
            needs_more_context=True,
            verdict="Whoa there. I need a little more context before I can cook you properly. 💀",
            recommendations=[
                "Tell me what happened specifically.",
                "Include when it happened (e.g. 'tomorrow', 'next week').",
                "Explain the consequences."
            ]
        )
        
    # 4. Generate Humor
    category_title = analysis.category.title()
    verdict, recs, _ = generate_humor(score_result["level_int"], category_title)
    
    # 5. Return Response
    return PredictResponse(
        cooked_score=score_result["cooked_score"],
        cooked_level=score_result["cooked_level"],
        level_int=score_result["level_int"],
        confidence=analysis.confidence,
        category=analysis.category,
        urgency=analysis.urgency,
        preparation=analysis.preparation,
        consequences=analysis.consequences,
        recoverability=analysis.recoverability,
        key_factors=analysis.key_factors,
        reasons=analysis.key_factors, # backward compatibility
        verdict=verdict,
        recommendations=recs
    )
