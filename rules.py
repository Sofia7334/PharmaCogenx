
def evaluate_rule(profile, rule):
    """Evaluate a structured profile against a documented rule."""

    if not isinstance(profile, dict) or not profile:
        return {
            "status": "insufficient_data",
            "message": "Required profile data is missing or invalid."
        }

    if not isinstance(rule, dict) or not rule:
        return {
            "status": "no_rule",
            "message": "No applicable rule is available."
        }

    required_profile_fields = {"gene", "allele", "result"}
    required_rule_fields = {
        "rule_id", "gene", "allele", "medication"
    }

    if not required_profile_fields.issubset(profile):
        return {
            "status": "insufficient_data",
            "message": "Required genetic information is missing."
        }

    if not required_rule_fields.issubset(rule):
        return {
            "status": "invalid_rule",
            "message": "The rule specification is incomplete."
        }

    if not all(
        isinstance(profile[field], str) and profile[field].strip()
        for field in required_profile_fields
    ):
        return {
            "status": "invalid_input",
            "message": "Genetic input values must be nonempty strings."
        }

    if not all(
        isinstance(rule[field], str) and rule[field].strip()
        for field in required_rule_fields
    ):
        return {
            "status": "invalid_rule",
            "message": "Rule fields must be nonempty strings."
        }

    if (
        profile["gene"] != rule["gene"]
        or profile["allele"] != rule["allele"]
    ):
        return {
            "status": "no_match",
            "message": "The genetic profile does not match this rule."
        }

    result = profile["result"].strip().lower()

    if result not in {"positive", "negative"}:
        return {
            "status": "invalid_input",
            "message": "Result must be positive or negative."
        }

    if result == "positive":
        return {
            "status": "matched",
            "rule_id": rule["rule_id"],
            "medication": rule["medication"],
            "result": "positive",
            "interpretation": (
                "HLA-B*57:01 positive: the FDA-listed "
                "abacavir avoidance recommendation applies."
            ),
            "evidence_source": rule.get(
                "evidence_source", "FDA Table of Pharmacogenetic Associations"
            )
        }

    return {
        "status": "rule_not_triggered",
        "rule_id": rule["rule_id"],
        "medication": rule["medication"],
        "result": "negative",
        "interpretation": (
            "The HLA-B*57:01 positive-result rule was not triggered. "
            "This does not establish that abacavir is appropriate "
            "or eliminate all risk of hypersensitivity."
        ),
        "evidence_source": rule.get(
            "evidence_source", "FDA Table of Pharmacogenetic Associations"
        )
    }
