#!/usr/bin/env python3
"""Build manuscript_template.docx for the deep-review skill.

Journal-manuscript style: A4, 2.5 cm margins, monochrome, Times New Roman 12 pt
(SimSun for CJK), double-spaced body, numbered sections, hanging-indent
references. Regenerate with:  python3 build_manuscript_template.py
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

INK = RGBColor(0x00, 0x00, 0x00)

def set_cjk(style_or_run, cjk_font="SimSun"):
    """Force an East-Asian font so ZH reports don't fall back randomly."""
    rpr = style_or_run.element.get_or_add_rPr() if hasattr(style_or_run, "element") else style_or_run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), cjk_font)

def style_font(st, name="Times New Roman", size=12, bold=False, italic=False):
    st.font.name = name
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.italic = italic
    st.font.color.rgb = INK
    set_cjk(st)

def add_style(doc, name, base="Normal", **kw):
    st = doc.styles.add_style(name, 1)  # 1 = paragraph style
    st.base_style = doc.styles[base]
    style_font(st, **kw)
    return st

def booktabs(table):
    """Top/bottom rules + hairline header underline; no vertical borders."""
    tbl = table._tbl
    tblpr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge, sz in (("top", "12"), ("bottom", "12"), ("insideH", "0"), ("insideV", "0"), ("left", "0"), ("right", "0")):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)      # 12 = 1.5pt thick, 0 = none
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblpr.append(borders)

doc = Document()

# Page & default style
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)  # A4
for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sec, m, Cm(2.5))

normal = doc.styles["Normal"]
style_font(normal, size=12)
pf = normal.paragraph_format
pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
pf.space_after = Pt(0)

# Style sheet
title = add_style(doc, "ReviewTitle", size=16, bold=True)
title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(12)

subtitle = add_style(doc, "ReviewSubtitle", size=12, italic=True)
subtitle.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_after = Pt(24)

meta = add_style(doc, "MetaLine", size=10)
meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
meta.paragraph_format.space_after = Pt(24)

h1 = add_style(doc, "SectionHeading", size=14, bold=True)
h1.paragraph_format.space_before = Pt(18)
h1.paragraph_format.space_after = Pt(6)
h1.paragraph_format.keep_with_next = True

h2 = add_style(doc, "SubsectionHeading", size=12, bold=True, italic=True)
h2.paragraph_format.space_before = Pt(12)
h2.paragraph_format.space_after = Pt(6)
h2.paragraph_format.keep_with_next = True

abstract = add_style(doc, "AbstractBlock", size=12)
abstract.paragraph_format.left_indent = Cm(1.0)
abstract.paragraph_format.right_indent = Cm(1.0)
abstract.paragraph_format.space_after = Pt(18)

caption = add_style(doc, "TableCaption", size=10, bold=True)
caption.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
caption.paragraph_format.space_before = Pt(10)
caption.paragraph_format.keep_with_next = True

tnote = add_style(doc, "TableNote", size=9)
tnote.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
tnote.paragraph_format.space_after = Pt(10)

figcap = add_style(doc, "FigCaption", size=10, bold=True)
figcap.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
figcap.paragraph_format.space_before = Pt(12)
figcap.paragraph_format.keep_with_next = True

figpara = add_style(doc, "FigurePara", size=12)
figpara.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
figpara.paragraph_format.space_after = Pt(12)
figpara.paragraph_format.keep_with_next = True  # figure never splits from its caption

# Booktabs rows carry no separators — paragraph spacing is the only row boundary.
# Table typography conventions: Arial at ONE uniform size (9 pt) for every table
# (per-table sizes read as inconsistent pages); serif body, sans tables.
tabletext = add_style(doc, "TableText", size=9)
style_font(tabletext, name="Arial", size=9)
tabletext.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
tabletext.paragraph_format.space_before = Pt(5)
tabletext.paragraph_format.space_after = Pt(5)

refstyle = add_style(doc, "ReferenceEntry", size=12)
refstyle.paragraph_format.first_line_indent = Cm(-1.0)  # hanging indent
refstyle.paragraph_format.left_indent = Cm(1.0)
refstyle.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
refstyle.paragraph_format.space_after = Pt(6)

keyp = add_style(doc, "KeyPoint", size=12, italic=True)
keyp.paragraph_format.left_indent = Cm(1.0)
keyp.paragraph_format.space_before = Pt(6)
keyp.paragraph_format.space_after = Pt(6)

# ---- Skeleton content ----
doc.add_paragraph("{{Review Title — Deep Review}}", style="ReviewTitle")
doc.add_paragraph("{{Italic subtitle framing scope and dual-track coverage}}", style="ReviewSubtitle")
doc.add_paragraph("{{Review ID}} · {{v1.0}} · {{YYYY-MM-DD}} · Field: {{field}} · Evidence cutoff: {{YYYY-MM-DD}}", style="MetaLine")

doc.add_paragraph("{{Abstract — problem, scope, 3–5 headline findings (≥1 per track), evidence cutoff date.}}", style="AbstractBlock")

sections = [
    ("1  {{Scope & Definitions}}", ["{{Definition + boundary vs adjacent concepts; inclusion criteria; glossary.}}"]),
    ("2  {{Historical Timeline}}", ["{{5–9 milestones, each with year, event, why it mattered, primary citation.}}"]),
    ("3  {{Landmark Works}}", ["{{6–15 works; why each mattered, not restated abstracts.}}"]),
    ("4  {{Mechanisms & Paradigms}}", ["{{Competing frameworks + the readouts that distinguish them.}}"]),
    ("5  {{Academic Landscape}}", [
        "5.1  {{Groups & toolkit}}",
        "5.2  {{Activity trend — real OpenAlex counts; embed matplotlib PNG, 300 dpi, grayscale-safe, captioned}}",
    ]),
    ("6  {{Industrial Landscape}}", [
        "6.1  {{Pipeline table — see below}}",
        "6.2  {{Deals & financing (two-source rule)}}",
        "6.3  {{IP posture — facts only}}",
    ]),
    ("7  {{Research Fronts}}", ["{{3–6 directions from the last 2–3 years with momentum evidence; preprints flagged.}}"]),
    ("8  {{Open Problems}}", ["{{5–10 problems ranked by importance × tractability; state this ranking is the report's assessment.}}"]),
    ("9  {{Outlook}}", [
        "9.1  {{For academic readers}}",
        "9.2  {{For industrial readers}}",
    ]),
    ("10  {{Methods: Search Strategy}}", ["{{Databases, verbatim queries, run dates, PRISMA-lite counts, declared limitations.}}"]),
    ("11  {{References}}", ["{{Numbered, Vancouver/Nature style, hanging indent, one per line:}}",
                            "{{Author}} {{Title}}. {{Journal}}. {{Year}};{{Vol}}:{{Pages}}. PMID: {{XXXXXXXX}} (or doi:{{…}})"]),
]
for head, paras in sections:
    doc.add_paragraph(head, style="SectionHeading")
    for p in paras:
        style = "SubsectionHeading" if p[0].isdigit() else "Normal"
        doc.add_paragraph(p, style=style)

# Pipeline table example
doc.add_paragraph("{{Table 1. Pipeline landscape}}", style="TableCaption")
doc.add_paragraph("{{Stage = registry status where available; source + access date mandatory; two-source rule on volatile numbers.}}", style="TableNote")
tbl = doc.add_table(rows=3, cols=6)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
booktabs(tbl)
hdr = ["Company", "Program", "Target / modality", "Stage", "Indication", "Source"]
def set_row_height(row, cm):
    """Minimum row height (atLeast) — keeps a header row from looking cramped."""
    trpr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), str(int(cm * 567))); h.set(qn("w:hRule"), "atLeast")
    trpr.append(h)

for i, h in enumerate(hdr):
    cell = tbl.rows[0].cells[i]
    cell.paragraphs[0].style = doc.styles["TableText"]
    run = cell.paragraphs[0].add_run(h)
    run.bold = True
    pf = cell.paragraphs[0].paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER      # header row always centred
    pf.space_before = Pt(2); pf.space_after = Pt(4)
set_row_height(tbl.rows[0], 0.8)                  # generous header height
for r in range(1, 3):
    for c, val in enumerate(["{{company}}", "{{program}}", "{{target}}", "{{stage}}", "{{indication}}", "{{NCT / disclosure + date}}"]):
        cell = tbl.rows[r].cells[c]
        cell.paragraphs[0].style = doc.styles["TableText"]
        cell.paragraphs[0].add_run(val)
        # centre narrow label-like columns, left-align long prose columns
        cell.paragraphs[0].paragraph_format.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER if len(val) <= 26 else WD_ALIGN_PARAGRAPH.LEFT)

doc.save("manuscript_template.docx")
print("manuscript_template.docx written")
