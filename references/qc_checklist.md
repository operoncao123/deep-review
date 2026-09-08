# QC Checklist — Deep Review Delivery Gates

Run top to bottom before handing over any report. **Bold gates are hard blockers** — a report failing them does not ship. Anything a script can check must be checked by the build script (`assets/deepreview_build.py`), which exits non-zero on FAIL; a printed "PASS" you typed yourself is not a gate.

## A. Evidence integrity

* [ ] **Every load-bearing claim in the report traces to an `evidence_log.md` row** (spot-check each section's first and last claim at minimum)
* [ ] **Merged evidence rows are written back into `evidence_log.md`** — placeholder rows with the real evidence in side files is a hard fail
* [ ] **Every PMID/DOI verified to resolve** (esummary / doi.org 302) and titles match the claims they support
* [ ] **Two-source rule enforced** on all volatile industrial numbers (phases, deal values, dates) — or explicitly flagged "single-source, unconfirmed"
* [ ] No confidence-C source backs a number anywhere in the report
* [ ] Every evidence row carries URL + access date
* [ ] Registry keys that ended up uncited are reported by the build and pruned (or the citation restored)

## B. Coverage

* [ ] ≥ 20 core academic references (quick pass: ≥ 10); typical 30–60
* [ ] ≥ 8 industry entries for drug topics (quick pass: ≥ 4); non-biomed: equivalent practitioner coverage
* [ ] ≥ 3 databases searched, each with query strings recorded
* [ ] Both tracks appear in the Abstract with at least one concrete finding each
* [ ] No section rests on < 3 evidence rows — researched further or cut with a stated reason
* [ ] Term-boundary (Section 1) explicitly excludes the adjacent concept, and search NOT-blocks reflect it

## C. Figures & tables

* [ ] 3–5 figures present; trend chart uses real OpenAlex counts on a **continuous annual axis** (query recorded in Methods; pre-field strays trimmed; partial year marked with lighter fill + `*`)
* [ ] 2×2 matrix: priority quadrant top-LEFT (importance × tractable); no arrowhead labelled "tractability" pointing at the "needs breakthrough" side
* [ ] Timeline: vertical-spine component (year rail + type-coloured dots), not a card grid
* [ ] Every table has `Table N.` caption + footnote note (HTML/DOCX equivalents)
* [ ] Pipeline table rows carry stage + source + access date
* [ ] Numeric index columns (`#`, year) pinned narrow; ≥ 16 px inter-column padding in HTML tables
* [ ] Venn uses panel-derived two-hue duo with explicit lens (HTML); no corner cell pure black
* [ ] DOCX figures: 300 dpi, grayscale-legible, **caption below the figure for every figure without exception**
* [ ] DOCX tables: word-fit audit passes — final column width ≥ longest unbreakable token; slash compounds made breakable with zero-width spaces (Word/LibreOffice never break at "/")
* [ ] HTML tables: `<wbr>` after "/" in text nodes (Chrome never breaks slash compounds either — without it they overprint the next column); `overflow-wrap:break-word` on td as last-resort valve
* [ ] Figure code contains no hardcoded hex colours — everything derives from the active panel
* [ ] **Every `table.bk` has a `<thead>`** — glossary/short tables included; the DOCX builder needs it for the header row and repeat-on-split
* [ ] Timeline CSS intact in the shipped template: `.tl-body{display:block;…}` (inline span margins do NOT indent block children — without this the why-paragraph escapes full-width and collides with the year rail and spine), why-paragraph `margin-top` 8–9px, `li` padding-bottom 24–26px
* [ ] DOCX table cell paragraphs carry `space_before = space_after = Pt(5)` (booktabs rows have no separators; spacing is the only row boundary); long timeline tables use `cantSplit` rows + repeating header
* [ ] **DOCX typography uniform across pages**: Arial at ONE size (9 pt) for every table, and Arial for the body too (one family throughout) — per-table font sizes read as inconsistent pages; header row centred, bold, min height 0.8 cm (`trHeight atLeast`) with 2/4 pt spacing; body cells: narrow label-like columns (≤ ~26 chars) centred, long prose columns left; no bold in body cells (header only)
* [ ] **Figures never split from their captions**: the figure paragraph style carries `keep_with_next` (caption below figure); verify in the rendered PDF that every image and its caption share a page
* [ ] Venn labels fit INSIDE their regions: intersection text within the lens at every line's height, region labels clear of the circle strokes (widen the lens by moving centres closer before shrinking text)
* [ ] Pathway/flow figures: parallel lanes use symmetric styling (same fill logic per role); colour carries emphasis, not `bold` — no bold text inside figures

## D. Citations & linking (HTML)

* [ ] **In-text `[n]` link directly to the source record**: one external anchor per number pointing at the registry's PubMed/DOI URL (`target="_blank" rel="noopener"`) — clicking a citation opens PubMed, it never scrolls to the reference list; ranges expanded
* [ ] **Strip all `<a>…</a>` from body → zero bare `[n]` patterns remain**
* [ ] **No `href="#ref-n"` citation anchors remain** (reference rows carry no ids; the build's unresolved-anchor check FAILS on any stray one)
* [ ] Reference table: numbered, Vancouver/Nature style, every entry ends in clickable PMID/DOI ↗ with `target="_blank" rel="noopener"`
* [ ] No anchor contains an emoji; no decorative symbols (★) anywhere
* [ ] `references.bib` exported, keys `firstauthorYYYYkeyword` (dedup a/b suffixes), count matches reference table

## E. Structure & polish (all templates)

* [ ] 8–12 numbered sections (or merges justified in Methods); sub-sections numbered 1.1 / 1.2
* [ ] Title block complete: Review ID / version / date / field / evidence cutoff
* [ ] **Meta consistency: version, dates, and every computed count are token-injected from one constants block** — identical in HTML, DOCX, guide, README, evidence log (this gate fails if any number was typed by hand)
* [ ] Methods section lists every database, query verbatim, run date, PRISMA-lite counts
* [ ] Evidence cutoff date appears in meta-grid and Abstract
* [ ] Bilingual (when requested): two files, identical structure and numbering, topic-based names (`<topic>_EN.html` / `<topic_keywords>_ZH.html`), footer marks language
* [ ] Print button + `@media print` intact (HTML); figures don't split across pages (DOCX)
* [ ] Palette switcher (if shipped): styles in `<head>`, widget div right after `<body>`, label localized
* [ ] Gene names / code names in mono (HTML) or consistent styling (DOCX/MD)
* [ ] No emoji, no marketing adjectives, no decorative gradients

## E2. Prose style (de-AI) — hard gate

* [ ] **Zero em-dashes in rendered output of every deliverable**: no `—` (EN) and no `——` (ZH) in body prose, table cells, captions, figure in-chart titles, reference strings, page `<title>`, or placeholders. Check the BUILT artifacts, not the source: `grep '—' final/*.html` must only hit `<head>` CSS comments; every text page of the exported PDF must be clean. Rewrite as colon / semicolon / comma appositive / sentence split; en-dash `–` remains only in numeric ranges and compound pairs
* [ ] AI-cliché scan clean: EN — delve / crucial / pivotal (except "pivotal trial") / metaphorical landscape / "not only…but also" / rule-of-three padding; ZH — 值得注意的是 / 综上所述 / 总而言之 / 不可否认 / 翻译腔 / 无依据定性断言. (References: humanizer-zh, ai-flavor-remover, qu-ai-wei, shuorenhua on GitHub)
* [ ] Sentence-level grammar pass done in BOTH languages; fragments are stylistic, not ungrammatical; bilingual fragments stay factually symmetric

## F. Workspace handoff

* [ ] Workspace folder delivered: `final/` outputs + `evidence_log.md` (merged rows included) + `references.bib` (+ `figures/`)
* [ ] Version bumped correctly — in the constants block, and the README's deliverable list (file names, page counts) regenerated or verified against the actual files
* [ ] One-paragraph summary message to the user: headline findings + file paths + evidence cutoff + known gaps
