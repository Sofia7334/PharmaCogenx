
"""Run the PharmaCogenx educational pharmacogenomics prototype."""

# Import the FDA data loader and rule evaluator.
from fda_data import load_fda_associations
from rules import evaluate_rule


def main():
    """Collect a mock result and display its educational interpretation."""

    # Load the original FDA associations from the source workbook.
    associations = load_fda_associations()

    # Select the documented Abacavir and HLA-B*57:01 association.
    rule = next(
        association
        for association in associations
        if association["rule_id"] == "FDA.1.1"
    )

    # Introduce the prototype and explain the mock input.
    print("=" * 60)
    print("PharmaCogenx — Educational Pharmacogenomics Simulator")
    print("=" * 60)
    print("Demonstration association: Abacavir and HLA-B*57:01")
    print("Enter a mock result to evaluate the documented FDA association.")
    print("Accepted results: positive or negative")

    # Ask the user for a mock result and normalize capitalization.
    result = input("\nMock genetic result: ").strip().lower()

    # Build the mock profile for the selected FDA association.
    profile = {
        "gene": "HLA-B",
        "allele": "HLA-B*57:01",
        "result": result,
    }

    # Evaluate the mock profile against the authentic FDA source record.
    interpretation = evaluate_rule(profile, rule)

    # Display the evaluation status.
    print("\n" + "-" * 60)
    print("Evaluation result")
    print("-" * 60)
    print(f"Status: {interpretation['status']}")

    # Display the association details when a rule was evaluated.
    if "rule_id" in interpretation:
        print(f"Rule ID: {interpretation['rule_id']}")
        print(f"Medication: {interpretation['medication']}")
        print(f"Genetic result: {interpretation['result']}")

    # Display the interpretation or validation message.
    print(
        interpretation.get(
            "interpretation",
            interpretation.get("message", "No interpretation available."),
        )
    )

    # Identify the source of the association.
    if "evidence_source" in interpretation:
        print(f"Source: {interpretation['evidence_source']}")

    # Clearly label the output as educational rather than clinical advice.
    if "educational_notice" in interpretation:
        print(f"\nNOTICE: {interpretation['educational_notice']}")

    print("-" * 60)


# Run the demonstration only when this file is executed directly.
if __name__ == "__main__":
    main()
