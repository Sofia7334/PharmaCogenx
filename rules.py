def evaluate_rule(profile, rule):
    """Evaluate a structured profile against one documented rule."""

    if not profile:
        return {
            "status":"insufficient_data",
            "message":"Required profile data is missing."
        }