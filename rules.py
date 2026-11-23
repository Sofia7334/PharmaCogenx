
"""Evaluate mock genetic results against documented FDA associations."""


def evaluate_rule(profile, rule):
    """Evaluate a profile against one FDA association."""

    # Reject missing or incorrectly structured profile data.
    if not isinstance(profile, dict) or not profile:
        return {
            "status": "insufficient_data",
            "message": "Required profile data is missing or invalid.",
        }

    # Reject a missing or incorrectly structured FDA association.
    if not isinstance(rule, dict) or not rule:
        return {
            "status": "no_rule",
            "message": "No applicable rule is available.",
        }

    # Require the genetic information needed for evaluation.
    required_profile_fields = {"gene", "allele", "result"}
    if not required_profile_fields.issubset(profile):
        return {
            "status": "insufficient_data",
            "message": "Required genetic information is missing.",
        }

    # Require fields provided by the FDA data loader.
    required_rule_fields = {
        "rule_id",
        "gene",
        "affected_subgroups",
        "drug",
        "description",
    }
    if not required_rule_fields.issubset(rule):
        return {
            "status": "invalid_rule",
            "message": "The FDA association is missing required fields.",
        }

    # Ensure all supplied genetic values are nonempty strings.
    if not all(
        isinstance(profile[field], str) and profile[field].strip()
        for field in required_profile_fields
    ):
        return {
            "status": "invalid_input",
            "message": "Genetic input values must be nonempty strings.",
        }

    # Ensure essential FDA association fields contain valid strings.
    if not all(
        isinstance(rule[field], str) and rule[field].strip()
        for field in required_rule_fields
    ):
        return {
            "status": "invalid_rule",
            "message": "FDA association fields must be nonempty strings.",
        }

    # Accept only positive or negative results in this prototype.
    result = profile["result"].strip().lower()
    if result not in {"positive", "negative"}:
        return {
            "status": "invalid_input",
            "message": "Result must be positive or negative.",
        }

    # Check whether the profile's gene matches the FDA association.
    if profile["gene"].strip().upper() != rule["gene"].strip().upper():
        return {
            "status": "no_match",
            "message": "The genetic profile does not match this association.",
        }

    # Normalize the allele and subgroup for the HLA-B*57:01 prototype.
    allele = profile["allele"].strip().upper()
    subgroup = rule["affected_subgroups"].strip().upper()

    # Remove the HLA-B prefix to compare with the FDA subgroup notation.
    allele_designation = allele.removeprefix("HLA-B")

    # Stop if the allele designation does not appear in the subgroup.
    if allele_designation not in subgroup:
        return {
            "status": "no_match",
            "message": "The allele does not match this FDA association.",
        }

    # Return the original FDA description for a positive result.
    if result == "positive":
        return {
            "status": "matched",
            "rule_id": rule["rule_id"],
            "medication": rule["drug"],
            "result": result,
            "interpretation": rule["description"],
            "evidence_source": rule.get(
                "source", "FDA Table of Pharmacogenetic Associations"
            ),
            "educational_notice": (
                "Educational demonstration only. This output is not a "
                "clinical decision or a substitute for professional advice."
            ),
        }

    # Explain that a negative result does not establish medication safety.
    return {
        "status": "rule_not_triggered",
        "rule_id": rule["rule_id"],
        "medication": rule["drug"],
        "result": result,
        "interpretation": (
            "The positive-result condition for this association was not "
            "triggered. This does not establish that the medication is "
            "appropriate or eliminate all relevant risks."
        ),
        "evidence_source": rule.get(
            "source", "FDA Table of Pharmacogenetic Associations"
        ),
        "educational_notice": (
            "Educational demonstration only. This output is not a "
            "clinical decision or a substitute for professional advice."
        ),
    }