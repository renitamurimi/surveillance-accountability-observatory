
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SGEL | Accountability Gap Explorer",
    page_icon="🔎",
    layout="wide"
)

BASE = Path(__file__).parent

@st.cache_data
def load_data():
    return (
        pd.read_csv(BASE / "documents.csv", keep_default_na=False),
        pd.read_csv(BASE / "evidence.csv", keep_default_na=False),
        pd.read_csv(BASE / "insights.csv", keep_default_na=False)
    )

docs, evidence, insights = load_data()

st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.hero {
    padding: 1.4rem 1.6rem;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    margin-bottom: 1.2rem;
}
.eyebrow {
    font-size: .8rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #64748b;
}
.hero h1 {
    margin: .35rem 0;
    font-size: 2.1rem;
}
.muted {
    color: #64748b;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="eyebrow">
        Surveillance Governance Evidence Lab (SGEL) · Proof of Concept
    </div>
    <h1>Accountability Gap Explorer</h1>
    <p>
        An evidence-linked tool for examining surveillance governance.
        Explore accountability questions and trace them to excerpts
        from primary legal documents.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("Legal cases", len(docs))
c2.metric("Evidence records", len(evidence))
c3.metric("Accountability insights", len(insights))


with st.expander("About SGEL and the Accountability Gap Explorer"):
    st.markdown("""
### Surveillance Governance Evidence Lab (SGEL)

The Surveillance Governance Evidence Lab (SGEL) is a
public-interest research initiative developing evidence-based
tools to examine the governance and accountability of
surveillance technologies.

Its first tool, the **Accountability Gap Explorer (AGE)**,
connects questions about surveillance practices to evidence
from primary legal documents.

SGEL aims to support journalists, civil society organizations,
researchers, and policymakers investigating surveillance
governance.

#### How SGEL differs from existing initiatives

SGEL complements resources such as the Electronic Frontier
Foundation's Atlas of Surveillance and other surveillance
transparency initiatives.

Rather than primarily cataloging surveillance deployments,
SGEL organizes evidence around specific accountability
questions concerning data retention, information sharing,
legal authorization, and oversight.

Its emphasis is on connecting documented evidence to
questions that may require further investigation.

#### Methodology

This proof of concept examines five legal cases, using
one manually reviewed primary legal document per case.

Seven standardized evidence fields are used:

- Technology
- Vendor
- Surveillance Purpose
- Retention Period
- Data Sharing
- Legal Issues
- Oversight

The prototype contains **36 evidence records and
15 accountability insights**, linked to supporting
source evidence.

#### Future development

SGEL plans to extend the Accountability Gap Explorer
into an investigative workflow that helps users:

1. Examine documented surveillance practices.
2. Identify unresolved governance questions.
3. Determine what additional evidence may be needed.
4. Explore suggested investigative next steps.
5. Generate downloadable, source-linked investigative briefs.

These investigative workflow and downloadable briefing
features are planned developments and are not included
in the current prototype.

#### Interpretive limitations

Accountability questions are not findings of misconduct
or legal violations.

SGEL distinguishes allegations from judicial findings
and identifies unresolved governance questions.

**Missing documentation is not proof that a safeguard
does not exist.**

All evidence in this prototype was manually reviewed.
No AI-based extraction was used.
    """)


case_names = docs["case_name"].tolist()
case = st.selectbox("Select a legal case", case_names)

doc = docs.loc[docs.case_name == case].iloc[0]
subset = insights.loc[insights.doc_id == doc.doc_id]
case_evidence = evidence.loc[evidence.doc_id == doc.doc_id]

st.caption(
    f"{doc.doc_id} · {doc.state} · "
    f"{doc.doc_type} · {doc.document_date}"
)

st.markdown(f"**Source status:** {doc.evidence_status}")

if doc.source_url and str(doc.source_url).startswith(
    ("http://", "https://")
):
    st.link_button(
        "Open primary source document",
        doc.source_url
    )


st.subheader("Accountability questions")

for _, ins in subset.iterrows():
    with st.expander(
        f"{ins.insight_id} · {ins.title}",
        expanded=True
    ):
        st.markdown(
            f"**Accountability question**  \n{ins.question}"
        )

        st.markdown("**Interpretation**")
        st.write(ins.interpretation)

        if ins.review_note:
            st.warning(ins.review_note)

        ids = [
            v.strip()
            for v in ins.evidence_ids.split(",")
            if v.strip()
        ]

        st.caption(
            "Supporting evidence: " + ", ".join(ids)
        )

        for eid in ids:
            matches = case_evidence.loc[
                case_evidence.evidence_id == eid
            ]

            if matches.empty:
                st.error(
                    f"Missing evidence record: {eid}"
                )
                continue

            ev = matches.iloc[0]

            with st.expander(
                f"{eid} · "
                f"{ev.field_name.replace('_', ' ').title()}"
            ):
                st.markdown("**Extracted value**")
                st.write(ev.extracted_val)

                st.markdown("**Source excerpt**")
                st.info(
                    ev.evidence_excerpt
                    or "No excerpt recorded in source worksheet."
                )

                loc = []

                if str(ev.source_page).strip():
                    loc.append(
                        "Page: " + str(ev.source_page)
                    )

                if str(ev.source_para).strip():
                    loc.append(
                        "Paragraph: " + str(ev.source_para)
                    )

                st.caption(
                    " · ".join(loc)
                    if loc
                    else "Source pinpoint not specified"
                )

                st.caption(
                    "Evidence status: "
                    + str(ev.evidence_status)
                    + " | Verification: "
                    + str(ev.verification_status)
                )


st.subheader("Seven evidence fields")

fields = [
    "tech",
    "vendor",
    "surveillance_purpose",
    "retention_period",
    "data_sharing",
    "legal_issues",
    "oversight"
]

labels = {
    "tech": "Technology",
    "vendor": "Vendor",
    "surveillance_purpose": "Surveillance purpose",
    "retention_period": "Retention period",
    "data_sharing": "Data sharing",
    "legal_issues": "Legal issues",
    "oversight": "Oversight"
}

for field in fields:
    vals = case_evidence.loc[
        case_evidence.field_name == field
    ]

    with st.expander(
        f"{labels[field]} "
        f"({len(vals)} record{'s' if len(vals) != 1 else ''})"
    ):
        if vals.empty:
            st.write("Not recorded")

        for _, v in vals.iterrows():
            st.markdown(
                f"**{v.evidence_id}** — {v.extracted_val}"
            )
            st.caption(
                f"Source page: "
                f"{v.source_page or 'not specified'}"
            )


st.divider()

st.markdown("**Methodology and limitations**")

st.caption(
    "This is a manually annotated five-document proof "
    "of concept, not a comprehensive database of "
    "surveillance practices. Complaints contain allegations, "
    "not adjudicated findings. Judicial opinions may include "
    "findings, holdings, and unresolved issues. An unmentioned "
    "safeguard is not presumed absent. Evidence status and "
    "source references should be consulted before drawing "
    "conclusions. Source dates and case statuses may change; "
    "this prototype does not automatically update litigation "
    "outcomes."
)

