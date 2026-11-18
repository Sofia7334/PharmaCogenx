from rules import evaluate_rule

# Define a reusable mock profile for the abacavir example.
def make_profile(result="positive"):
    return {
        "gene": "HLA-B",
        "allele": "HLA-B*57:01",
        "result": result
    }

# Define a reusable rule using the project's proposed identifier format.
def make_rule():
    return {
        "rule_id": "FDA.1.3",
        "gene": "HLA-B",
        "allele": "HLA-B*57:01",
        "medication": "Abacavir",
        "evidence_source": "FDA Table of Pharmacogenetic Associations"
    }

# Verify that an empty profile is rejected.
def test_missing_profile():
    result = evaluate_rule({}, make_rule())

    assert result["status"] == "insufficient_data"

# Verify that a missing rule is handled explicitly.
def test_missing_rule():
    result = evaluate_rule(make_profile(), {})

    assert result["status"] == "no_rule"

# Verify that a positive result triggers the documented rule.
def test_positive_result():
    result = evaluate_rule(make_profile("positive"), make_rule())

    assert result["status"] == "matched"
    assert result["rule_id"] == "FDA.1.3"
    assert result["medication"] == "Abacavir"

# Verify that a negative result does not trigger the positive-result rule.
def test_negative_result():
    result = evaluate_rule(make_profile("negative"), make_rule())

    assert result["status"] == "rule_not_triggered"

# Verify that a result outside the accepted values is rejected.
def test_invalid_result():
    result = evaluate_rule(make_profile("unknown"), make_rule())

    assert result["status"] == "invalid_input"

# Verify that a different gene does not match this rule.
def test_gene_mismatch():
    profile = make_profile()
    profile["gene"] = "OTHER"

    result = evaluate_rule(profile, make_rule())

    assert result["status"] == "no_match"

# Verify that incomplete genetic information is rejected.
def test_missing_genetic_field():
    profile = {"gene": "HLA-B", "allele": "HLA-B*57:01"}

    result = evaluate_rule(profile, make_rule())

    assert result["status"] == "insufficient_data"
