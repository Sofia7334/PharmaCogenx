
"""Load pharmacogenetic associations from the FDA source workbook."""

from pathlib import Path

from openpyxl import load_workbook


# Define the location of the original FDA workbook relative to this file.
DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "2026-11-19_PharmaCogenx_FDAPharmacogeneticAssociationsTable.xlsx"
)


def load_fda_associations(file_path=DATA_FILE):
    """Load all FDA association records while preserving source information."""

    # Open the source workbook without modifying its contents.
    workbook = load_workbook(file_path, read_only=True, data_only=True)

    # Collect normalized records from all three FDA sections.
    associations = []

    try:
        # Process each worksheet independently to preserve section provenance.
        for sheet in workbook.worksheets:
            # Extract the section number from worksheet names such as "Section 1".
            section_number = int(sheet.title.split()[-1])

            # Read rows after the title and column-header rows.
            data_entry_number = 0

            for excel_row, row in enumerate(
                sheet.iter_rows(min_row=3, values_only=True),
                start=3,
            ):
                # Skip blank rows that do not contain a drug name.
                if not row or row[0] is None or not str(row[0]).strip():
                    continue

                # Increment the identifier's entry number only for actual records.
                data_entry_number += 1

                # Preserve the four original FDA columns without rewriting their text.
                drug, gene, affected_subgroups, description = row[:4]

                # Store each association with its stable, section-based identifier.
                association = {
                    "rule_id": (
                        f"FDA.{section_number}.{data_entry_number}"
                    ),
                    "source": "FDA Table of Pharmacogenetic Associations",
                    "source_section": section_number,
                    "source_entry": data_entry_number,
                    "source_excel_row": excel_row,
                    "drug": drug,
                    "gene": gene,
                    "affected_subgroups": affected_subgroups,
                    "description": description,
                }

                # Add the normalized association to the results.
                associations.append(association)

    finally:
        # Always close the workbook, including if parsing raises an error.
        workbook.close()

    # Return all associations in worksheet order.
    return associations