<!--
Deep Review — Markdown skeleton (universal fallback template).
Fills the same 11-section skeleton as the HTML/DOCX templates.
Citations: [n] numbered in order of first appearance; one entry per reference
in §11, each ending with PMID or DOI link. Export references.bib alongside.
-->

# {{Review Title — Deep Review}}

> {{Italic subtitle framing scope and dual-track coverage}}

| Review ID | Version | Date | Field | Evidence cutoff |
|---|---|---|---|---|
| {{DR-001}} | {{v1.0}} | {{YYYY-MM-DD}} | {{field}} | {{YYYY-MM-DD}} |

## Abstract

{{Problem, scope, 3–5 headline findings (≥1 per track), evidence cutoff date.}}

**Contents:** 1 Scope · 2 Timeline · 3 Landmarks · 4 Mechanisms · 5 Academic landscape · 6 Industrial landscape · 7 Fronts · 8 Open problems · 9 Outlook · 10 Methods · 11 References

## 1. Scope & Definitions

{{Definition + boundary vs 2–3 adjacent concepts (a small in/out table reads well); inclusion criteria; glossary if ≥5 acronyms.}}

## 2. Historical Timeline

{{5–9 milestones — YYYY · event · why it mattered · primary citation [n].}}

## 3. Landmark Works

{{6–15 works with why each mattered (table: # / work+link / year / type / why).}}

## 4. Mechanisms & Paradigms

{{Competing frameworks, evidence status, distinguishing readouts.}}

## 5. Academic Landscape

### 5.1 Groups & toolkit
{{5–12 groups by contribution; assays/databases/methods with canonical citations.}}

### 5.2 Activity trend
{{Interpretation of per-year counts (real OpenAlex data; query in §10). Embed chart: `figures/trend.png`}}

## 6. Industrial Landscape

### 6.1 Pipeline
| Company | Program | Target / modality | Stage | Indication | Source |
|---|---|---|---|---|---|
| {{…}} | {{…}} | {{…}} | {{…}} | {{…}} | {{NCT/disclosure + access date}} |

### 6.2 Deals & financing
{{Value, date, parties, source; two-source rule.}}

### 6.3 IP posture
{{Facts only.}}

## 7. Research Fronts

{{3–6 directions, last 2–3 years, momentum evidence, preprints flagged.}}

## 8. Open Problems

{{5–10 problems; rank by importance × tractability; top-right = highest-value work; say the ranking is this report's assessment.}}

## 9. Outlook

### 9.1 For academic readers
{{…}}

### 9.2 For industrial readers
{{…}}

## 10. Methods: Search Strategy

PRISMA-lite: identified {{N}} → dedup {{N}} → core corpus {{N}} → cited {{N}}.

| Database | Query (verbatim) | Run date | Results |
|---|---|---|---|
| PubMed | `{{query}}` | {{YYYY-MM-DD}} | {{N}} |
| OpenAlex | `{{filter}}` | {{YYYY-MM-DD}} | {{N}} |

Declared limitations: {{language bias / cutoff / databases not searched / single-source facts}}.

## 11. References

1. {{Author}} {{Title}}. {{Journal}}. {{Year}};{{Vol}}:{{Pages}}. [PMID: {{XXXXXXXX}}](https://pubmed.ncbi.nlm.nih.gov/{{XXXXXXXX}}/)
2. {{Author}} {{Title}}. {{Journal}}. {{Year}}. [doi:{{…}}](https://doi.org/{{…}})

---

*{{DR-001 · v1.0 · YYYY-MM-DD · 中文版 | English}}*
