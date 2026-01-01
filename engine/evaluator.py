import json

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def evaluate_signals(responses: dict, signals: list):
    """
    Returns normalized signal scores (0–5 scale)
    """
    signal_scores = {}

    for signal in signals:
        total = 0.0
        weight_sum = 0.0

        for q in signal["questions"]:
            qid = q["id"]
            w = q["weight"]

            if qid in responses:
                total += responses[qid] * w
                weight_sum += w

        if weight_sum > 0:
            signal_scores[signal["signal_id"]] = round(total / weight_sum, 2)
        else:
            signal_scores[signal["signal_id"]] = 0.0

    return signal_scores

def compute_skills(signal_scores, skill_defs):
    skill_scores = {}

    for skill in skill_defs:
        total = 0
        weight_sum = 0

        for src in skill["derived_from"]:
            score = signal_scores.get(src["signal_id"], 0)
            total += score * src["weight"]
            weight_sum += src["weight"]

        skill_scores[skill["skill_id"]] = round(total / weight_sum, 3)

    return skill_scores

def compute_roles(skill_scores, role_defs):
    role_scores = {}

    for role in role_defs:
        total = 0
        weight_sum = 0

        for sk in role["skills"]:
            score = skill_scores.get(sk["skill_id"], 0)
            total += score * sk["weight"]
            weight_sum += sk["weight"]

        role_scores[role["role_id"]] = round(total / weight_sum, 3)

    return role_scores
