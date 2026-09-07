# Search Playbook — Deep Review

Tool routing and copy-paste query patterns per source. Examples use the molecular-glue motivating case; substitute the topic du jour. Record every query verbatim in `evidence_log.md` — they ship in the report's Methods section.

Run order for a standard pass: PubMed (corpus) → OpenAlex (landmarks + trend) → citation chaining → industry track (parallelizable) → gap-filling round after synthesis clustering.

---

## 1. PubMed — primary academic corpus

E-utilities REST (no key needed for light use; `api_key` if rate-limited):

```bash
# Search
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=100&sort=relevance&term=(%22molecular+glue%22%5BTitle%2FAbstract%5D)+AND+(stabilizer%5BTitle%2FAbstract%5D+OR+non-degradative%5BTitle%2FAbstract%5D)+NOT+(PROTAC%5BTitle%2FAbstract%5D+OR+degrader%5BTitle%2FAbstract%5D)"

# Fetch details for a PMID list (usetimestamp for access-date logging)
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=PMID1,PMID2"
```

Patterns:
* Title/Abstract field tags `[…]` beat bare keywords; combine concept OR-blocks with AND.
* Use `NOT` blocks to enforce the Section-1 term boundary (e.g. exclude PROTAC/degrader for a non-degrader review) — and record that this was done.
* Date fence: `AND 2023:2026[dp]` for fronts; remove it for landmarks.
* Local alternative: `pubmed-database` / `biopython` (Bio.Entrez) skills wrap the same API — fine to use.
* `bgpt-paper-search` adds structured methods/results fields when mechanism-level detail is needed.

## 2. OpenAlex — landmarks & trend data

```bash
# Works matching the topic, sorted by citations (landmark discovery)
curl -s "https://api.openalex.org/works?filter=title_and_abstract.search:molecular%20glue&sort=cited_by_count:desc&per-page=25" | jq '.results[] | {year, cited_by_count, doi, title: .title}'

# Per-year counts for the trend figure (this is THE trend chart's data source)
curl -s "https://api.openalex.org/works?filter=title_and_abstract.search:molecular%20glue&group_by=publication_year" | jq '.group_by[] | {year: .key, count: .count}'
```

Patterns:
* Landmark thresholds by age: ≥ 100 citations (< 3 y), ≥ 250 (3–7 y), ≥ 500 (> 7 y) — soften for small fields (use within-field percentile instead: top 5%).
* `group_by=publication_year` gives real trend numbers — chart those, never sketch a trend.
* Forward chaining: `filter=cites:W<openalex_id>` on a landmark. Backward: `referenced_works` of the field's best review.
* Include a polite mailto: `&mailto=you@lab.org` in the query string.

## 3. ClinicalTrials.gov — pipeline ground truth (biomed)

```bash
# API v2
curl -s "https://clinicaltrials.gov/api/v2/studies?query.intr=molecular+glue&pageSize=100&countTotal=true" | jq '.totalCount'
# Filter fields to what the pipeline table needs
curl -s "https://clinicaltrials.gov/api/v2/studies?query.intr=%22molecular+glue%22&fields=NCTId,BriefTitle,OverallStatus,Phase,LeadSponsorName,Condition" 
```

Patterns:
* Company pipeline pages overstate; the registry is the arbiter for "has a trial, what phase".
* A program with a company page but no registry entry is preclinical — say exactly that, with "per company disclosure" attribution.
* Check `OverallStatus` and `LastUpdatePostDate` — a terminated trial is itself a finding worth a sentence.

## 4. FDA / regulators — approvals & status (biomed)

* openFDA: `curl -s "https://api.fda.gov/drug/label.json?search=molecular+glue"` ; Drugs@FDA for approval letters and first-approval dates.
* EMA / NMPA via site search when US-only would skew the story (common for China-centered fields — search 药监局 and company CDE filings in Chinese).

## 5. Patents — IP landscape (biomed & chemistry)

* Google Patents via WebFetch: `https://patents.google.com/?q=%22molecular+glue%22+stabilizer&oq=...` — read result pages for assignee/family signals.
* USPTO PatentsView API for counts by assignee: quick way to name who controls foundational IP without legal analysis (report facts, not legal opinions).

## 6. Companies, deals, funding — web layer

Tools: WebSearch, `research-lookup`, `perplexity-search` (has API plumbing locally). Query patterns (run EN + ZH for China-relevant fields):

* `"<topic>" pipeline site:company.com OR press release` — program names and stages
* `"<topic>" partnership OR "license agreement" OR acquisition 2025..2026` — deals
* `"<topic>" biotech Series OR financing` — funding
* Chinese: `"<术语>" 管线 OR 授权 OR 融资 2026`

Rules:
* Deal values and dates: two independent sources (company PR + trade press counts as two; two aggregators quoting one PR do not).
* Company self-description ("first", "only", "leading") is marketing — quote with attribution or drop.
* Log every URL + access date; confidence B for PR-with-specifics, C otherwise.

## 7. Non-biomed adaptation

Academic track unchanged (arXiv replaces/extends PubMed where the field lives there: `http://export.arxiv.org/api/query?search_query=ti:"<term>"`). Industry track becomes: vendors & products, open-source vs commercial adoption, notable deployments, hiring/growth signals — same two-source rule, same evidence table.

## 8. Subagent fan-out (when the runtime supports it)

Dispatch two parallel agents with the scope card:

* Agent A (academic): returns evidence rows (claim/source/URL/date/confidence) meeting ≥ 20 core refs, plus OpenAlex year-counts JSON and top-cited list.
* Agent B (industry): returns evidence rows meeting ≥ 8 pipeline/company entries with registry verification where applicable.

Agents return rows, not prose — synthesis is done once, centrally, against both row-sets (prevents dueling narratives).

## 9. Citation verification (mandatory, before render)

```bash
# Resolve PMIDs → confirm they exist and titles match what you claim
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=PMID1,PMID2"
# DOIs
curl -sI "https://doi.org/<DOI>" | head -1   # expect 302 to the right publisher
```

Every in-text `[n]` must map to a verified row here before the report ships.
