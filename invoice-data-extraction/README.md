# Invoice Data Extraction – Prompt Engineering Task

## Objective
Design a structured prompt that extracts invoice data and returns strictly valid JSON.

## Approach
- Defined a strict JSON schema
- Enforced null handling for missing fields
- Normalized date formats to ISO (YYYY-MM-DD)
- Converted currency values to numeric format
- Handled multiple tax entries by summing them
- Added currency inference rules

## Edge Cases Considered
- Missing invoice fields
- Different date formats
- Multiple tax lines
- Currency symbols without codes
- Duplicate totals
- Multi-page invoices

## Files
- prompt.txt → Main extraction prompt
- schema.json → Defined JSON schema
- sample_invoice.txt → Example invoice input
- expected_output.json → Expected structured result