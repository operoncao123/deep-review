# Section Guide — Deep Review

Per-section content requirements for the 11-section skeleton. Lengths assume the standard pass (30–60 references, 8–12 sections); halve them for a quick pass. Figures refer to the nature-html component classes; DOCX/Markdown use equivalents.

---

## Abstract

* 150–250 words, 2–3 paragraphs: (1) what the field is and why now; (2) 3–5 headline findings with numbers where available; (3) what the reader gets from each track.
* Must contain at least one finding from the academic track and one from the industrial track.
* Ends with the evidence cutoff: "Evidence current as of YYYY-MM-DD."

## 1. Scope & Definitions

**Purpose:** fix the terminology before anything else. Emerging fields have unstable vocabulary; readers from adjacent fields will misread the report without this.

Must contain:
* A crisp definition of the core concept, with 1–2 authoritative citations.
* **Boundary table or Venn** against the 2–3 nearest adjacent concepts — what is in, what is out, and the single clearest discriminator for each pair. Example for non-degrader molecular glue: outcome (stabilize/activate/inhibit a function) vs degradation (PROTAC, CELMoD/degrader glues); the discriminators are "ubiquitin–proteasome dependence" and "covalent ternary complex with an E3 ligase".
* Inclusion criteria for what literature/companies count (mechanism class, time window, language).
* A short glossary if ≥ 5 field-specific acronyms appear in the report.

Visual: Venn (two circles + explicit lens path) or a 2-column "in / out" booktabs table.

## 2. Historical Timeline

* 5–9 milestones from origin to present. Each milestone = year + one-line event + why it mattered (conceptual pivot, enabling technology, clinical/validation inflection).
* Distinguish three milestone types in the visual (e.g. concept / tool / validation) with pill tags — don't present a flat list.
* Cite the primary source for each milestone, not a review's retelling.

Visual: **vertical-spine timeline** — `ol.tl` with one `<li class="lcd|pc|deg">` per milestone; the li class colours the spine dot, the year sits in a mono left rail, pill + title share one line, the "why" sentence sits below. Do NOT use a card grid (5-across mini-cards cram long text and read as a flat wall). For DOCX: convert to a 4-column booktabs table (Year / Type / Milestone / Why it mattered).

## 3. Landmark Works

* 6–15 entries selected by citation percentile within field age (see search_playbook thresholds), plus qualitative musts (first demonstration, mechanism resolution, clinical first).
* **Per entry: why it mattered** — the door it opened, not a restated abstract. One to three sentences.
* Include patents or registry entries here when they, not papers, were the inflection (common in industry-heavy subfields).
* Mark entry type with pills (paper / patent / trial / approval).

Visual: booktabs table — # / work (linked) / year / type / why it mattered.

## 4. Mechanisms & Paradigms

* How the field's core objects work; competing frameworks presented side by side with their evidence status (established / emerging / contested).
* Name the key experimental readouts that distinguish the frameworks — this is what an experimental reader needs.
* If the field is pre-mechanistic, say so and describe the phenomenology levels instead; do not invent a mechanism narrative.

Visual: `pathway` diagram (two parallel rows converging on shared outcome reads well for dual-track fields); `def` box for formal definitions.

## 5. Academic Landscape

* Who: 5–12 leading groups (institution, one-line platform contribution, representative linked reference). Order by contribution, not alphabetically.
* What toolkit exists: assays, databases, computational methods — with the canonical citation for each.
* Activity metrics: per-year publication counts (real numbers from OpenAlex — see search_playbook), split by sub-theme if the trend has branches.
* Where it's concentrated: geography/funding signals only if you have data; skip vibes.

Visual: publication-trend chart (real data, never sketched; state the query behind it in Methods). **Continuous annual axis** — one bar per year from field origin to present; never mix 5-year sampling with annual sampling at uniform bar pitch (it distorts where growth phases sit). Trim pre-field strays (OpenAlex misindexes ancient titles) with the 10-year-window rule (`year_counts` in `assets/deepreview_build.py`); take the headline total from the API `meta.count`, not the group_by sum. Mark a partial current year with lighter fill + `*`. Value labels only on years where they don't collide.

## 6. Industrial Landscape *(biomed extension; see below for schema)*

* Company-by-company or program-by-program pipeline table.
* Deals & financing: partnerships, M&A, notable rounds — each with value, date, both parties, source. Two-source rule on values.
* IP posture: patent families/thickets if identifiable; who controls foundational IP.
* For non-biomed topics this section becomes the practitioner/commercial landscape (vendors, adopters, open-source vs commercial split).

Visual: pipeline table (booktabs + phase pills); optionally a `m2x2` positioning matrix (e.g. platform vs targeted, early vs late stage).

### Pipeline table schema (drug topics)

| Column | Content | Rule |
|---|---|---|
| Company | — | Group subsidiaries under parent |
| Program / code name | — | As the company names it |
| Target / modality | e.g. "CYPA–BCL2L1 stabilizer" | Mechanism-level, not marketing-level |
| Stage | Discovery / preclinical / Ph I / Ph II / Ph III / approved | Pill-tagged; registry-verified where a trial exists |
| Indication | — | If disclosed |
| Status & date | e.g. "active, NCT…, updated 2026-08" | Source + access date mandatory |
| Source | NCT / PR / filing | Two-source rule for stage claims |

## 7. Research Fronts

* 3–6 directions active in the last 2–3 years. Per direction: what's new, who's driving it (labs and/or companies), 2–4 linked recent references, and honest momentum evidence (publication acceleration, trial starts, funding).
* Preprints allowed and encouraged here — flagged as preprint.

## 8. Open Problems

* 5–10 problems, each: statement, why it matters (rate-limiting for what), current best attempt + its limitation.
* Rank visually in a 2×2: x = tractability, y = importance. **The TOP-LEFT quadrant (field-defining × near-term tractable) is the "urgent and high-value" answer** — make it explicit in prose and give that cell the accent fill.
* Axis labelling: the x dimension runs "more tractable" (left) → "needs breakthrough" (right). Never draw a rightward arrowhead labelled "tractability" — it then points at *low* tractability, a self-contradiction. Use a plain rule with an end caption on each side.

Visual: `matrix` 4-quadrant or `m2x2`.

## 9. Outlook

* Two explicitly labeled subsections: **for academic readers** (what to work on, which problems unlock others) and **for industrial readers** (where the white space is, which claims are over-hyped).
* 3–5 year horizon. Bold claims allowed but each tied to an evidence row or marked as this report's assessment ("we assess that…").

Visual: `keypoint` callouts, one per track.

## 10. Methods: Search Strategy

* Databases searched with query strings verbatim, date run, result counts.
* PRISMA-lite counts: identified → after dedup → core corpus (reviews excluded) → cited in report.
* Inclusion/exclusion criteria from Section 1 restated mechanically.
* Declared limitations: language bias, cutoff date, databases not searched, single-source facts.

## 11. References

* Numbered in order of first appearance; Vancouver/Nature style.
* Every entry ends with clickable PMID (preferred) or DOI, `target="_blank" rel="noopener"`.
* HTML: in-text `[n]` link **directly to the source record** — one external anchor per number pointing at the PubMed/DOI URL from the registry (`target="_blank" rel="noopener"`; ranges expanded, letter suffixes linked, no bare `[n]` after stripping anchors). Do NOT route in-text numbers through `#ref-n` page anchors: the reader clicking a citation wants the PubMed record, not a scroll to the reference list. The full citation stays one glance away in section 11.
* The `#` column is an index, not content: pin it to ~5% width (the colgroup injector's numeric-column rule does this automatically) — a wide index column visually detaches numbers from citations.
* `references.bib` exported alongside — keys `firstauthorYYYYkeyword` (`bib_key` + `dedup_bib_keys` in `assets/deepreview_build.py`).

---

## Cross-cutting writing rules

* Prose synthesizes across sources; never annotated-list style.
* Numbers with sources always ("~40 clinical programs (ClinicalTrials.gov, accessed 2026-09-03)").
* Contested claims: present both sides with their evidence status; the Venn/2×2 does not settle arguments by fiat.
* No emoji, no marketing adjectives ("revolutionary", "game-changing") — in any template. Decorative symbols (★, ◆) count as emoji for this rule; emphasis comes from fill/border/typography.
* **Meta single-source:** version, dates, review ID and every computed count (refs total, PMID count, trend totals) are injected via build tokens, never typed into prose by hand. Same rule for README and the evidence log — if a number appears in three places, two of them will drift.
* Tables: give columns breathing room (≥ 16 px inter-column padding in HTML); index/number columns pinned narrow; the longest unbreakable token per column determines its floor (calibrate to print width, not screen).
