import os
import sys

# --------------------------------------------------
# Ensure project root in path
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# Imports (engine only)
# --------------------------------------------------
from engine.loader import load_json
from engine.question_engine import get_questions, evaluate_responses
from engine.evaluator import compute_skills
from engine.passport import generate_cif_report

# --------------------------------------------------
# Load core schemas
# --------------------------------------------------
questions = load_json("data/core/questions.json")
skills = load_json("data/core/skills.json")
skill_narratives = load_json("data/core/skill_narratives.json")
fit_bands = load_json("data/display/fit_bands.json")

# --------------------------------------------------
# Step 1: Render questions (demo)
# --------------------------------------------------

question_signal_map = {
    q["question_id"]: q["signal_id"]
    for q in questions["questions"]
}

selected_questions = get_questions(
    questions,
    context="education",
    limit=3
)

selected_question_ids = [q["question_id"] for q in selected_questions]

print("\n=== QUESTIONS ===")
for q in selected_questions:
    print(f"\n{q['text']}")

    scale = questions.get("scale", {})
    print("\nResponse scale:")
    for k, v in scale.get("labels", {}).items():
        print(f"{k}: {v}")


# --------------------------------------------------
# Step 2: Simulated user responses
# --------------------------------------------------
responses = {
    "Q_BOUNDARY_1": 1,
    "Q_EMOTION_1": 1,
    "Q_JUDGMENT_1": 0
}

# --------------------------------------------------
# Step 3: Signal evaluation
# --------------------------------------------------
signal_scores = evaluate_responses(
    selected_question_ids,
    responses,
    question_signal_map
)

# --------------------------------------------------
# Step 4: Skill computation
# --------------------------------------------------
skill_scores = compute_skills(signal_scores, skills)

# --------------------------------------------------
# Step 5: Generate CIF report
# --------------------------------------------------
cif_report = generate_cif_report(
    skill_scores=skill_scores,
    narratives=skill_narratives,
    fit_bands=fit_bands,
    context="Education"
)

# --------------------------------------------------
# Output
# --------------------------------------------------
print("\n=== CIF REPORT ===")
print(cif_report)
