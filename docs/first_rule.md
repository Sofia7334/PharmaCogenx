# PharmaCogenx — First Rule Specification

## 1. Rule Identification
- Rule ID: PGX-001
- Gene: HLA-B
- Medication: Abacavir
- Source guideline: FDA Table of Pharmacogenetic Associations
- Guideline publication/update date: Verify the current table date

## 2. Required Input
- Required genetic information: HLA-B*57:01 test result
- Accepted input format: Structured positive or negative test result
- Required phenotype or interpretation: HLA-B*57:01 positive or negative

## 3. Rule Conditions
- Condition to evaluate: Whether the HLA-B*57:01 allele is present
- Expected result when the condition matches: For a positive result, report the FDA-listed increased hypersensitivity risk and avoidance recommendation
- Behavior when the condition does not match: For a negative result, report that this specific positive-result rule was not triggered; do not imply that all hypersensitivity risk is absent
- Behavior when required information is missing: Return an insufficient-data status

## 4. Output
- Interpretation: Display the test result and applicable rule outcome
- Explanation: The FDA identifies an association between HLA-B*57:01 positivity and increased abacavir hypersensitivity risk
- Evidence source: FDA Table of Pharmacogenetic Associations
- Relevant limitations: Educational prototype only; not a clinical decision-making tool. A negative result does not establish that abacavir is appropriate for a particular person.

## 5. Testing Plan
- Test case 1: Positive HLA-B*57:01 result
- Test case 2: Negative HLA-B*57:01 result
- Test case 3: Missing test result
- Test case 4: Invalid or unsupported test result