---
name: deep-review
description: Conduct deep field-survey reviews on any research topic — historical evolution, landmark papers, current landscape (BOTH academic research AND industrial / drug-development perspectives), hot research fronts, and high-value open problems — with verified citations and a documented search strategy. Renders bilingual (EN/ZH) reports in one of three templates Nature Protocols-style HTML (default), journal-manuscript DOCX, or Markdown. Use when the user asks for 深度调研, 深度综述, deep review, deep dive, landscape report, state-of-the-field report, field survey, or a comprehensive review covering literature plus industry pipeline (e.g. "non-degradable molecular glue 深度调研"). Not for single-experiment protocol reports (use nature-protocols-report instead).
metadata:
    skill-author: operoncao
---

# Deep Review

A domain-agnostic deep-survey engine: **history → landmark works → dual-track landscape (academic + industry) → research fronts → open problems → outlook**, executed with an evidence-first workflow and rendered as a polished bilingual report.

Three commitments, in priority order:

1. **Evidence before prose.** No sentence is written before its supporting source exists in the evidence log. This is the anti-hallucination backbone of the whole skill.
2. **Dual-track coverage.** Academic literature and industrial development are separate research tracks with separate sources, minimums, and quality rules — never a token "industry outlook" paragraph.
3. **Reproducibility.** Every search query, database, and access date is recorded and shipped in the report's Methods appendix.

## Scope Model

* **Core skeleton** is domain-agnostic (works for molecular glue, RNA editing, solid-state batteries, LLM agents…). The "industry track" generalizes to *practitioner/commercial landscape* for non-biomed topics.
* **Biomed / drug-development extension** (auto-enabled for therapeutic, target, modality, or disease topics) adds: ClinicalTrials.gov trials, FDA approvals, patents, company pipelines, BD deals. See `references/search_playbook.md`.
* Term disambiguation is mandatory for emerging fields: section 1 of every report draws the boundary against adjacent concepts (e.g. non-degrader molecular glue vs PROTAC/degrader molecular glue) before anything else is discussed.

## Workflow

### Phase 0 — Scope & workspace

1. Create the workspace next to the user's files: `deep_review_<topic>_<YYYYMMDD>/` containing `evidence_log.md`, `figures/`, `final/`, `references.bib`.
2. Fill a scope card at the top of `evidence_log.md`: topic; term boundaries (concept vs adjacent concepts); time window; dual-track emphasis; template choice; languages. If any of these is genuinely ambiguous, ask once, with options; otherwise state assumptions and proceed.
3. Pick the template now (see Templates) — it determines figure formats downstream.

### Phase 1 — Research (populate the evidence log)

`evidence_log.md` is a table; one row per fact:

```markdown
| # | claim (one fact) | section | source (journal/company/registry) | URL | accessed | confidence |
|---|---|---|---|---|---|---|
| 12 | Compound X showed Y in Z model | 4 Mechanisms | Nature 2023 | https://doi.org/... | 2026-09-03 | A |
```

Confidence: **A** = primary literature / registry / regulatory filing; **B** = secondary but reputable (review, company PR with specifics); **C** = press/analyst commentary — usable only with attribution, never for numbers.

**Academic track** (target ≥ 20 core references, 30–60 typical):

* PubMed E-utilities for the primary corpus; OpenAlex for bibliometrics — citation-sorted identification of landmark papers and per-year publication counts for the trend figure.
* Backward chaining (references of the 3–5 top reviews) + forward chaining (who cites the landmarks) via OpenAlex.
* `bgpt-paper-search` optional when structured experimental detail is needed.

**Industry track** (drug topics: ≥ 8 pipeline/company entries; general topics: equivalent practitioner coverage):

* ClinicalTrials.gov API (trial counts, phases, sponsors), FDA/approvals, patents (Google Patents / USPTO), company pipelines and deals via WebSearch / `research-lookup` / `perplexity-search`.
* **Two-source rule:** pipeline phase, deal value, launch date — any volatile industrial number needs two independent sources or an explicit "single-source, unconfirmed" flag in the report.

**Parallelize when possible:** dispatch two subagents (academic track / industry track) with the scope card; each returns evidence rows, not prose. Merge and deduplicate by URL/DOI, then **write the merged rows back into `evidence_log.md`** — the log is the audit spine; leaving placeholder rows while the real evidence lives in side files breaks commitment #1.

Stop research when: coverage minimums met AND the last 10 results add no new claim (saturation), or ~60% of the time budget is spent.

### Phase 2 — Synthesis

1. Cluster evidence rows into the 11-section skeleton (below). Gaps discovered here send you back to Phase 1 for one targeted round, not more.
2. Make **3–5 figures**, data-driven wherever possible: per-year publication trend (real OpenAlex counts — never sketched by eye, **continuous annual axis — no 5-year subsampling at uniform pitch**, that distorts the curve; trim pre-field strays with the 10-year-window rule in `assets/deepreview_build.py: year_counts`), historical timeline (vertical-spine `ol.tl` component, not a card grid), mechanism/paradigm diagram, open-problem 2×2 (importance × tractability — **top-LEFT is the priority quadrant**: field-defining × tractable; never label a rightward arrow "tractability" when the right column is "needs breakthrough"). HTML templates use plain SVG/CSS components; DOCX embeds 300-dpi grayscale-safe matplotlib PNGs.
3. Number references in order of first appearance; build the citation→PMID/DOI map; export `references.bib` (keys `firstauthorYYYYkeyword`, deduplicated with a/b suffixes).
4. **Single source of truth for meta:** version, run date, evidence cutoff, review ID, and all computed counts (total refs, PMID count, trend totals) live in ONE constants block in the build script and are injected into every deliverable via tokens (`{{DR_VERSION}}`, `{{NPMID}}`, `{{TREND_TOTAL}}`…). Prose never hardcodes numbers the build can compute — hand-written counts are the #1 drift source.

### Phase 3 — Render & verify

1. Copy the chosen template from `assets/`, fill it section by section from the evidence log — every load-bearing claim in the report must trace to a log row. `assets/deepreview_build.py` carries the reusable mechanics (numbering, citation links, colgroups, meta tokens, QC); the workspace keeps only the registry, fragments, and constants.
2. Bilingual default → two files with identical structure, named by topic: `<topic_keywords>_EN.html` / `<topic_keywords>_ZH.html` (DOCX/Markdown same convention). Never `report_en.html`.
3. **Citation linking (HTML):** in-text `[n]` link DIRECTLY to the source record — one external anchor per number pointing at the PubMed/DOI URL from the registry (`target="_blank" rel="noopener"`); clicking a citation opens PubMed, it never scrolls to the reference list. Ranges expanded; letter suffixes linked; strip anchors → zero bare `[n]`.
4. Run the delivery gates in `references/qc_checklist.md`. Hard gates: (a) citation verification — every PMID/DOI resolves (E-utilities / doi.org) and no unlinked `[n]` remains; (b) coverage minimums with the search-strategy appendix present; (c) QC scripts exit non-zero on any FAIL (print-only gates are not gates).

## Report Skeleton

| # | Section | Must contain | Typical visual |
|---|---|---|---|
| — | Abstract | Problem, scope, 3–5 headline findings, date-of-evidence | — |
| 1 | Scope & Definitions | Term boundary vs adjacent concepts; inclusion criteria | Venn (adjacent concepts) |
| 2 | Historical Timeline | Origins → conceptual pivots → enabling technologies | Vertical-spine timeline (`ol.tl`) |
| 3 | Landmark Works | Classic papers/patents; **why each mattered**, not a list | Booktabs table with linked PMIDs |
| 4 | Mechanisms & Paradigms | How the field's core objects work; competing frameworks | Pathway diagram |
| 5 | Academic Landscape | Leading groups/platforms; methodological toolkit; activity metrics | Publication-trend chart (continuous axis) |
| 6 | Industrial Landscape | Companies, pipeline/trials, deals, patents, IP tensions | Pipeline table (booktabs + pills) |
| 7 | Research Fronts | Last 2–3 years' hot directions, with evidence of momentum | — |
| 8 | Open Problems | Bottlenecks ranked by importance × tractability | 2×2 matrix (priority = top-LEFT) |
| 9 | Outlook | Separate implications for academic vs industrial readers | Keypoint callouts |
| 10 | Methods: Search Strategy | Databases, query strings, dates, result counts, limitations | PRISMA-lite counts |
| 11 | References | Numbered, clickable PMID/DOI | `bk` table |

8–12 sections, 30–60 references, single-run 1–2 h. Merge sections only when the topic genuinely lacks material (e.g. no industry presence → fold section 6 into 7 with a one-line justification in Methods).

## Templates

| Template | File | Use when | Notes |
|---|---|---|---|
| **nature-html** (default) | `assets/nature_review_template.html` | Default; screen reading, print/PDF export | Full aesthetic rules inherited from the Nature Protocols system; includes TOC + linked citations |
| **manuscript-docx** | `assets/manuscript_template.docx` | Journal-submission style, collaborators who edit in Word | Monochrome, double-spaced body, numbered sections, hanging-indent references; regenerate via `assets/build_manuscript_template.py` |
| **markdown** | `assets/review_skeleton.md` | Version-controlled base, feeding other pipelines | Universal fallback |

Selection: default nature-html; switch on explicit user request ("用 DOCX", "manuscript 格式", "要 markdown"). All templates share the same 11-section skeleton and citation rules.

Adding templates (LaTeX via `venue-templates`, summary slide deck, …): copy the pattern — one self-contained file in `assets/`, one row here, skeleton and QC gates unchanged.

## Prose Style & Typography (de-AI)

The report must read as professional academic writing, not as machine-generated prose. Rules below are hard gates; community references: [humanizer-zh](https://github.com/op7418/humanizer-zh), [ai-flavor-remover](https://github.com/hylarucoder/ai-flavor-remover), [qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei), [shuorenhua](https://github.com/MrGeDiao/shuorenhua).

1. **No em-dashes in rendered content.** Zero `—` (EN) and zero `——` (ZH) anywhere a reader can see: body prose, table cells, captions/notes, figure in-chart titles, reference strings, page `<title>`, placeholders. Em-dash density is the most recognizable AI-writing marker. Rewrite as a colon, semicolon, comma appositive, or split sentences. The en-dash `–` stays for numeric ranges (1978–2026) and compound pairs (ubiquitin–proteasome). CSS/Python comments may keep them (never rendered). Scan rendered output, not source: grep the built HTML text and extracted PDF text; both must return zero.
2. **Academic register, no AI clichés.** EN ban-list: *delve, crucial, pivotal* (except the term of art *pivotal trial*), *landscape* as metaphor outside section names, *"not only … but also"*, rule-of-three padding, throat-clearing openers. ZH ban-list: 值得注意的是、综上所述、总而言之、不可否认、翻译腔、无依据的定性断言、空洞排比. Terse house voice is fine; fragments must still be grammatical. Prefer concrete numbers and named entities over adjectives.
3. **Every `table.bk` carries a `<thead>`, no exceptions** — glossary/short tables too. The DOCX builder derives its header row and repeat-on-split behavior from `thead`; a headerless table renders as an unlabeled wall of rows in both HTML and DOCX.
4. **Table breathing room (booktabs rows have no separators).** DOCX: every body-cell paragraph gets `space_before = space_after = Pt(5)` (see `assets/build_manuscript_template.py` TableText); long milestone-style tables use `cantSplit` rows with a repeating header. HTML `table.bk` keeps `td` padding ≥ 11px vertical.
5. **Timeline (`ol.tl`) geometry is load-bearing.** `.tl-body` MUST be `display:block`: as an inline span its `margin-left` does not indent block children, so the why-paragraph escapes to full width and collides with the year rail and the spine line. Why-paragraph spacing: `margin-top` 8–9px; `li` padding-bottom 24–26px so each milestone reads as one unit.
6. **Bilingual parity.** Every content edit is applied to the EN and ZH fragments symmetrically — same facts, same structure, natural phrasing in each language (do not translate strings that are house conventions, e.g. pill labels).
7. **DOCX table & figure typography.** One font family for the whole manuscript: Arial (body 12 pt double-spaced, tables 9 pt — per-table font sizes or mixed serif/sans read as inconsistent pages); centred bold header row with ≥0.8 cm height; narrow columns centred, prose columns left; no bold in body cells; 5 pt cell spacing as the only row boundary. Figures: `keep_with_next` on the figure paragraph so an image is never separated from its caption by a page break; pathway lanes styled symmetrically (colour carries emphasis, never bold); venn labels must sit fully inside their regions — widen the lens (move circle centres closer) before shrinking text.
8. **Colour diversity.** Ten panels ship in `assets/palettes.py` spanning distinct hue families (journal blues/teals plus graphite/solar/forest/orchid/rose). Offer the user a panel choice at kickoff; don't default every report to the same family. All panel colours derive automatically — never hardcode hexes.

## Quality Gates (summary — full list in `references/qc_checklist.md`)

* **Citations:** PMID/DOI of every reference verified to resolve; in-text `[n]` each open the source record directly (PubMed/DOI URL, `target="_blank" rel="noopener"`; strip anchors → zero bare `[n]`; no `href="#ref-n"` page anchors remain).
* **Coverage:** ≥ 20 core academic refs; ≥ 8 industry entries (drug topics); ≥ 3 databases; both tracks represented in Abstract.
* **Industrial facts:** two-source rule enforced; every row in the pipeline table carries source + access date.
* **Freshness:** evidence cutoff date printed in title-block meta and Methods; nothing older than the run for volatile facts.
* **Meta consistency:** version / dates / all computed counts injected from one constants block; identical across HTML, DOCX, README, and the evidence log. Registry keys never-cited are reported and pruned.
* **Balance check:** no section built on < 3 evidence rows — either research more or cut the section honestly.
* **Style gate:** zero em-dashes (`—`/`——`) in rendered text of every deliverable; every `table.bk` has a `<thead>`; DOCX table cell spacing ≥ 5pt before/after; AI-cliché scan clean (ban-list in Prose Style above).

## Variations

* **Single language:** one file, drop the language tag in the footer.
* **Update mode:** point at an existing `deep_review_<topic>_*/` workspace; refresh the industry track and academic track for the period since the old evidence cutoff; keep stable reference numbering where possible; bump version (v1.0 → v1.1) **in the build script's constants block only** — tokens propagate it everywhere.
* **Quick pass:** halve minimums (≥ 10 refs, ≥ 4 industry entries), compress skeleton to Scope / Timeline / Landscape / Open Problems — state "quick pass" in the report header.
* **Non-biomed topics:** industry track becomes practitioner/commercial landscape via general web sources; registry/patent tools simply don't fire.
* **Different accent (HTML only):** pick a palette panel via `DEEPREVIEW_PANEL` (`assets/palettes.py`: nature / nejm / lancet / science / jama; paper tint, pills, figure fills and the venn duo derive automatically — no hardcoded hexes in figures) or add a row to `_HUES`. The canonical live switcher (`palettes.switcher_html()`: label + 2×5 deepened-swatch grid, choice persisted in localStorage) ships with every report; styles go in `<head>`, the widget div right after `<body>` (never inside `<head>`), label localized to the document language.

## Resources

* `references/section_guide.md` — per-section content requirements, figure specs, biomed-extension details, pipeline-table schema
* `references/search_playbook.md` — database-by-database query patterns with copy-paste API examples
* `references/qc_checklist.md` — full pre-delivery checklist
* `assets/nature_review_template.html` — default render target (review-adapted, self-contained; vertical-spine timeline, content-aware colgroups, palette-panel CSS variables)
* `assets/deepreview_build.py` — generic build core: ⟦key⟧ numbering, direct-to-PubMed citation-link substitution, references rows, colgroup injection, trend-data loading with stray trimming, meta-token injection, QC gates with exit codes
* `assets/palettes.py` — top-journal palette panels (nature/nejm/lancet/science/jama); all hues and derived tints for HTML, SVG and matplotlib share one source
* `assets/manuscript_template.docx` + `assets/build_manuscript_template.py` — Word manuscript template and its generator
* `assets/review_skeleton.md` — Markdown fallback
