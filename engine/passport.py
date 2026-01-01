from datetime import datetime

from engine.interpreter import map_skill_narrative, map_fit_band


def generate_cif_report(
    skill_scores,
    narratives,
    fit_bands,
    context="Education"
):
    """
    Generate a CIF Report Card from evaluated skill scores
    """

    skills_output = []

    for skill_id, score in skill_scores.items():
        narrative_def = narratives.get(skill_id)
        if not narrative_def:
            continue

        band = map_skill_narrative(
            score_normalized=score / 5,
            bands=narrative_def["bands"]
        )

        skills_output.append({
            "skill_id": skill_id,
            "display_name": narrative_def.get(
                "display_name",
                skill_id.replace("SK_", "").replace("_", " ").title()
            ),
            "score": round(score / 5, 3),
            "band": band["label"],
            "strength": band["strength"],
            "growth_edge": band["growth"]
        })

    cif_score_value = round(
        sum([s["score"] for s in skills_output]) / len(skills_output) * 100,
        1
    ) if skills_output else 0

    cif_band = map_fit_band(
        cif_score_value / 100,
        fit_bands["cif_score"]
    )

    return {
        "cif_id": f"CIF-{context.upper()}-{datetime.utcnow().strftime('%Y%m%d%H%M')}",
        "context": context,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "cif_score": {
            "value": cif_score_value,
            "band": cif_band["label"],
            "interpretation": cif_band["description"]
        },
        "skills_snapshot": skills_output,
        "validation_metadata": {
            "skills_evaluated": len(skills_output),
            "confidence_level": "medium"
        }
    }
