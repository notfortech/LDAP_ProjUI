from engine.evaluator import (
    load_json,
    evaluate_signals,
    compute_skills,
    compute_roles
)

# Load schemas
signals = load_json("data/signals.json")
skills = load_json("data/skills.json")
roles = load_json("data/roles.json")

# Dummy survey responses (1–5 scale)
responses = {
    "Q1": 4,
    "Q2": 3,
    "Q3": 5,
    "Q4": 4,
    "Q5": 3,
    "Q6": 4
}

# Run engine
signal_scores = evaluate_signals(responses, signals)
skill_scores = compute_skills(signal_scores, skills)
role_scores = compute_roles(skill_scores, roles)

print("\n=== SIGNAL SCORES ===")
for k, v in signal_scores.items():
    print(f"{k}: {v}")

print("\n=== SKILL SCORES ===")
for k, v in skill_scores.items():
    print(f"{k}: {v}")

print("\n=== ROLE FIT ===")
for k, v in role_scores.items():
    print(f"{k}: {v}")
