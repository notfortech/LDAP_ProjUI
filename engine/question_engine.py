# engine/question_engine.py

def get_questions(questions_list, context="education", limit=5):
    """
    Select questions based on context and optional limit
    """
    filtered = []

    for q in questions_list:
        contexts = q.get("context", ["education"])
        if context in contexts:
            filtered.append(q)

    return filtered[:limit]


def evaluate_weighted_signals(
    responses: dict,
    signal_definitions: dict,
    scale_weights: dict
):
    """
    responses: { "SIT_01_Q1": "B", "SIT_02_Q3": "A" }

    signal_definitions:
    {
        "SIG_BOUNDARY_ASSERTION": {
            "question_ids": [...],
            "weights": [...],
            "description": "..."
        }
    }
    """

    signal_scores = {}

    for signal_id, meta in signal_definitions.items():
        total = 0.0
        weight_sum = 0.0

        for qid, weight in zip(meta["question_ids"], meta["weights"]):
            if qid not in responses:
                continue

            selected_option = responses[qid]

            if selected_option not in scale_weights:
                raise ValueError(
                    f"Invalid option '{selected_option}' for question '{qid}'"
                )

            score = scale_weights[selected_option]
            total += score * weight
            weight_sum += weight

        if weight_sum > 0:
            signal_scores[signal_id] = round(total / weight_sum, 2)

    return signal_scores
