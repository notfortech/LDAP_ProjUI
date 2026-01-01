def map_skill_narrative(score_normalized, bands):
    for band in bands:
        if band["min"] <= score_normalized <= band["max"]:
            return band
    return bands[-1]


def map_fit_band(score_normalized, bands):
    for band in bands:
        if band["min"] <= score_normalized <= band["max"]:
            return band
    return bands[-1]
