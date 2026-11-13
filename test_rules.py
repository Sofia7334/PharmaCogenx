
from rules import evaluate_rule

def test_missing_profile():
    result = evaluate_rule({}, {"rule_id": "TEST-001"})
    assert result["status"] == "insufficient_data"

def test_missing_rule():
    result = evaluate_rule({"gene": "TEST"}, {})
    assert result["status"] == "no_rule"

def test_rule_not_implemented():
    profile = {"gene": "TEST"}
    rule = {"rule_id": "TEST-001"}
    result = evaluate_rule(profile, rule)

    assert result["status"] == "not_implemented"