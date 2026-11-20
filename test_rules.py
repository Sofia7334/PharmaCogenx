
# Import the evaluator and FDA data loader for testing.
from rules import evaluate_rule
from fda_data import load_fda_associations


# Build a mock genetic profile for the Abacavir example.
def make_profile(result="positive"):
    """Return a mock HLA-B*57:01 genetic result."""

    # Keep the gene and allele consistent with FDA rule FDA.1.1.
    return {
        "gene": "HLA-B",
        "allele": "HLA-B*57:01",
        "result": result,
    }


# Use the authentic FDA source record instead of duplicating its data.
def make_rule():
    """Return the FDA association for Abacavir and HLA-B*57:01."""

    # Load the original associations from the FDA workbook.
    associations = load_fda_associations()

    # Retrieve the first record in Section 1 by its stable identifier.
    return next(
        record
        for record in associations
        if record["rule_id"] == "FDA.1.1"
    )


# Test that an empty profile is rejected.
def test_missing_profile():
    result = evaluate_rule({}, make_rule())
    assert result["status"] == "insufficient_data"


# Test that a missing rule is handled explicitly.
def test_missing_rule():
    result = evaluate_rule(make_profile(), {})
    assert result["status"] == "no_rule"


# Test that a positive genetic result triggers the FDA association.
def test_positive_result():
    result = evaluate_rule(make_profile("positive"), make_rule())
    assert result["status"] == "matched"
    assert result["rule_id"] == "FDA.1.1"
    assert result["medication"] == "Abacavir"


# Test that a negative result does not trigger the positive-result condition.
def test_negative_result():
    result = evaluate_rule(make_profile("negative"), make_rule())
    assert result["status"] == "rule_not_triggered"


# Test that unsupported result values are rejected.
def test_invalid_result():
    result = evaluate_rule(make_profile("unknown"), make_rule())
    assert result["status"] == "invalid_input"


# Test that a different gene does not match the association.
def test_gene_mismatch():
    profile = make_profile()
    profile["gene"] = "OTHER"

    result = evaluate_rule(profile, make_rule())
    assert result["status"] == "no_match"


# Test that missing genetic information is rejected.
def test_missing_genetic_field():
    profile = {"gene": "HLA-B", "allele": "HLA-B*57:01"}

    result = evaluate_rule(profile, make_rule())
    assert result["status"] == "insufficient_data"


# Test that all 147 FDA association records load successfully.
def test_fda_record_count():
    associations = load_fda_associations()
    assert len(associations) == 147


# Test that each FDA section starts with the expected identifier and drug.
def test_fda_section_identifiers():
    associations = load_fda_associations()

    # Index the first record from each section for straightforward checks.
    first_records = {
        record["source_section"]: record
        for record in associations
        if record["source_entry"] == 1
    }

    assert first_records[1]["rule_id"] == "FDA.1.1"
    assert first_records[1]["drug"] == "Abacavir"

    assert first_records[2]["rule_id"] == "FDA.2.1"
    assert first_records[2]["drug"] == "Aficamten"

    assert first_records[3]["rule_id"] == "FDA.3.1"
    assert first_records[3]["drug"] == "Amitriptyline"


# Test that the original Abacavir description and Excel row are preserved.
def test_abacavir_description_is_preserved():
    associations = load_fda_associations()

    # Locate the source record using its stable identifier.
    abacavir = next(
        record
        for record in associations
        if record["rule_id"] == "FDA.1.1"
    )

    assert "Do not use abacavir" in abacavir["description"]
    assert abacavir["source_excel_row"] == 3
