# WorkBuddy adapter — how to install DeepReview

WorkBuddy (Tencent) does not publish a skills directory the way Claude Code or
Codex do; skills are created through WorkBuddy's own **Create Skills** flow,
which generates a `skill.yml` plus implementation files from a natural-language
description. Two ways to bring DeepReview in:

## Option A — Create Skills flow (recommended)

1. Open WorkBuddy and start a new task with the Create Skills entry point.
2. When asked to describe the skill, paste the `description` block below.
3. After WorkBuddy generates the `skill.yml`, replace/merge its `instructions`
   (or system-prompt) field with the full text of [`SKILL.md`](../SKILL.md),
   and attach this repository's `assets/` and `references/` files as skill
   resources.
4. Install, then test in a **fresh** conversation with:
   `深度调研：非降解性分子胶` (or any topic).

## Option B — paste-in description

Use this as the Create Skills description:

```yaml
name: deep-review
description: >
  Conduct deep field-survey reviews on any research topic — historical
  evolution, landmark papers, current landscape (BOTH academic research AND
  industrial / drug-development perspectives), hot research fronts, and
  high-value open problems — with verified citations and a documented search
  strategy. Renders bilingual (EN/ZH) reports in one of three templates:
  Nature Protocols-style HTML (default), journal-manuscript DOCX, or Markdown.
  Trigger words: 深度调研, 深度综述, deep review, deep dive, landscape report,
  field survey.
source_instructions_file: SKILL.md   # attach the repo's SKILL.md content
resources:
  - references/section_guide.md
  - references/search_playbook.md
  - references/qc_checklist.md
  - assets/nature_review_template.html
  - assets/deepreview_build.py
  - assets/palettes.py
  - assets/build_manuscript_template.py
  - assets/manuscript_template.docx
  - assets/review_skeleton.md
input: topic or research question (+ optional language / template / quick-pass flag)
output: bilingual report under deep_review_<topic>_<YYYYMMDD>/final/ plus
        evidence_log.md, references.bib, figures/
limits: never write prose before the evidence log row exists; never deliver
        without the scripted QC gates passing; volatile industrial numbers need
        two independent sources.
```

Field names may differ slightly across WorkBuddy versions — keep the *content*
of each field and map it to whatever the Create Skills dialog asks for.
