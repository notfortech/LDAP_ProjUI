def map_fit_band(score, bands):
    for band in bands:
        if band["min"] <= score <= band["max"]:
            return band
    return None

def map_skill_narrative(score, bands):
    for band in bands:
        if band["min"] <= score <= band["max"]:
            return band
    return None
