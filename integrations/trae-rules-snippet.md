# DeepReview — TRAE rules snippet

Paste the block below into `.trae/rules/project_rules.md` (project level) or the
user-rules editor (global), then make sure the skill folder itself is installed
at `~/.trae/skills/deep-review/` (run `./integrations/install.sh trae`).

TRAE builds that support Agent Skills discover the folder automatically; the
rules entry below guarantees routing even on builds that only honour rules.

```markdown
## DeepReview skill (深度调研 / deep field survey)

When the user asks for a 深度调研, 深度综述, deep review, deep dive,
landscape report, state-of-the-field report, field survey, or a comprehensive
literature + industry-pipeline review of any topic:

1. Read `~/.trae/skills/deep-review/SKILL.md` and follow it exactly.
2. Load its companion files from the same folder as needed:
   `references/section_guide.md`, `references/search_playbook.md`,
   `references/qc_checklist.md`, `assets/nature_review_template.html`,
   `assets/deepreview_build.py`, `assets/palettes.py`.
3. Non-negotiables of the skill: evidence log before prose; dual-track research
   (academic + industrial) with coverage minimums; 11-section skeleton;
   in-text `[n]` citations linking directly to PubMed/DOI records; scripted QC
   gates (exit non-zero on FAIL) before delivery.
```
