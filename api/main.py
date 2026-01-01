from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import json

from engine.question_engine import get_questions
from engine.question_engine import evaluate_weighted_signals

app = FastAPI()

# -------------------- CORS (FIXED) --------------------
# IMPORTANT:
# Do NOT use allow_origins=["*"] with allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- LOAD DATA --------------------
with open("data/core/signals.json", "r", encoding="utf-8") as f:
    SIGNALS = json.load(f)

with open("data/core/skills.json", "r", encoding="utf-8") as f:
    SKILLS = json.load(f)

with open("data/core/questions.json", "r", encoding="utf-8") as f:
    QUESTIONS_DATA = json.load(f)

# -------------------- MAPS --------------------
# Used by scoring engine
SIGNAL_MAP = {
    s["signal_id"]: {
        "question_ids": s["question_ids"],
        "weights": s["weights"]
    }
    for s in SIGNALS
}

# Used for UI descriptions
SIGNAL_META = {
    s["signal_id"]: s["description"]
    for s in SIGNALS
}

# Scale mapping
SCALE_WEIGHTS = {
    "A": 1.0,
    "B": 0.75,
    "C": 0.5,
    "D": 0.25
}

# -------------------- SKILL INFERENCE --------------------
def infer_skills(signal_scores, skills):
    inferred = []

    for skill in skills:
        total = 0
        weight_sum = 0

        for src in skill["derived_from"]:
            sig_id = src["signal_id"]
            weight = src["weight"]

            if sig_id in signal_scores:
                total += signal_scores[sig_id] * weight
                weight_sum += weight

        if weight_sum > 0:
            value = round(total / weight_sum, 2)

            inferred.append({
                "skill_id": skill["skill_id"],
                "description": skill["description"],
                "value": value,
                "confidence_level": skill["confidence_level"],
                "stability_index": skill["stability_index"],
                "band": (
                    "Emerging" if value < 0.25 else
                    "Developing" if value < 0.5 else
                    "Proficient" if value < 0.75 else
                    "Strong"
                )
            })

    return inferred

# -------------------- ROUTES --------------------
@app.get("/questions")
def get_questions_api(
    context: str = Query(default="education"),
    limit: int = Query(default=3, ge=1, le=20)
):
    """
    Returns flattened questions + scale
    """
    situations = QUESTIONS_DATA["situations"]
    all_questions = []

    for s in situations:
        for q in s["questions"]:
            q_copy = q.copy()
            q_copy["situation_title"] = s["title"]
            q_copy["background"] = s["background"]
            q_copy["context"] = ["education"]
            all_questions.append(q_copy)

    selected = get_questions(all_questions, context=context, limit=limit)

    return {
        "scale": QUESTIONS_DATA["scale"],
        "questions": selected
    }

@app.post("/evaluate")
async def evaluate_demo(request: Request):
    payload = await request.json()
    responses = payload.get("responses", {})

    # 1. Compute signal scores
    signal_scores = evaluate_weighted_signals(
        responses=responses,
        signal_definitions=SIGNAL_MAP,
        scale_weights=SCALE_WEIGHTS
    )

    # 2. Enrich signals for UI
    enriched_signals = [
        {
            "description": SIGNAL_META[sig_id],
            "score": round(score, 2),
            "band": (
                "Emerging" if score < 0.25 else
                "Developing" if score < 0.5 else
                "Proficient" if score < 0.75 else
                "Strong"
            )
        }
        for sig_id, score in signal_scores.items()
    ]

    # 3. CIF score
    cif_value = round(
        sum(signal_scores.values()) / len(signal_scores), 2
    ) if signal_scores else 0

    # 4. Infer skills
    inferred_skills = infer_skills(signal_scores, SKILLS)

    return {
        "cif_score": {
            "value": cif_value,
            "band": (
                "Emerging" if cif_value < 0.25 else
                "Developing" if cif_value < 0.5 else
                "Proficient" if cif_value < 0.75 else
                "Strong"
            )
        },
        "signals": enriched_signals,
        "skills": inferred_skills
    }
