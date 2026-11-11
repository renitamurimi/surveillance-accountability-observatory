# Surveillance Accountability Observatory — Accountability Gap Explorer

A five-case, manually annotated Streamlit proof of concept. Select a legal case, read its three accountability questions, and expand the supporting evidence to see extracted values, source quotations, and page references.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publish

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, `documents.csv`, `evidence.csv`, and `insights.csv` into its root.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/), select **Create app**, and choose your repository, branch, and `app.py` entry point.
3. Deploy and check all five cases and their evidence links.

## Data sources

- `documents.csv`: one row per source legal document (five records).
- `evidence.csv`: manually annotated source excerpts (36 records; `E-004B` is an additional Schmidt legal-issues record).
- `insights.csv`: three evidence-linked accountability questions per case (15 records).

## Pre-publication checks

- **Insight 2.2:** Its interpretation is cut off in the supplied Word document. The application displays the original truncated text with a warning. Finish the interpretation in `insights.csv` before sharing publicly.
- **Schmidt insights:** The Word document had placeholders instead of IDs. These were linked to existing evidence as follows: 1.1 → E-002, E-005; 1.2 → E-001; 1.3 → E-003, E-005. Review these mappings.
- Verify that all source URLs and case statuses remain current before publishing.

## Interpretive limits

Allegations in complaints are not judicial findings. A missing reference to a safeguard does not prove the safeguard was absent. The app does not use AI to generate findings, and it does not automatically refresh source documents or case statuses.
