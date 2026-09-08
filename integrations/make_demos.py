#!/usr/bin/env python3
"""Generate standalone figure-wrapper HTMLs from the mutagenesis EN/ZH reports,
with the CSS :root panel swapped to any palettes.py panel."""
import importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FINAL = ("/Users/operoncao/Nutstore Files/我的坚果云/Postdoc/agent/Review/"
         "ultra-mutagenesis system application/deep_review_in_vivo_mutagenesis_20260906/final")
REPORTS = {"EN": os.path.join(FINAL, "in_vivo_mutagenesis_systems_EN.html"),
           "ZH": os.path.join(FINAL, "in_vivo_mutagenesis_systems_ZH.html")}
OUTDIR = os.path.join(REPO, "demo")

spec = importlib.util.spec_from_file_location(
    "palettes", os.path.join(REPO, "assets", "palettes.py"))
palettes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(palettes)

OPEN = re.compile(r'<(div|ol|table)\b[^>]*class="[^"]*(figblock|fig(?![-\w])|venn-wrap|'
                  r'pathway|matrix|table-wrap|m2x2|tl(?![-\w]))[^"]*"')

def container_at(body, i):
    best = None
    for m in OPEN.finditer(body):
        if m.start() > i:
            break
        tag = m.group(1)
        depth, j = 1, m.end()
        while depth:
            nxt = re.search(rf'<{tag}\b|</{tag}>', body[j:])
            if not nxt:
                break
            depth += -1 if nxt.group(0)[1] == "/" else 1
            j += nxt.end()
        if depth == 0 and m.start() <= i < j:
            w = j - m.start()
            if best is None or w < best[0]:
                best = (w, m.start(), j)
    return None if best is None else body[best[1]:best[2]]

def extract(body, anchor):
    pos = 0
    while True:
        i = body.find(anchor, pos)
        if i < 0:
            raise SystemExit(f"anchor never in container: {anchor[:40]!r}")
        got = container_at(body, i)
        if got and len(got) > 200:
            return got
        pos = i + 1

def head_styles(t, panel_name):
    s = t[t.index("<head>"):t.index("</head>")]
    s = s[s.index("<style>"):]
    if panel_name:
        css = palettes.css_vars(palettes.PANELS[panel_name])
        s = re.sub(r":root\{.*?\}", f":root{{{css}}}", s, count=1, flags=re.S)
    # hide the live palette switcher widget in all captures
    s += ("<style>.palette-bar,#pal-switch,.pal-switch{display:none!important}"
          ";svg{overflow:visible!important}</style>")
    return s

def body_inner(t):
    b = re.sub(r"^<body[^>]*>", "", t[t.index("<body"):])
    return b[:b.rindex("</body>")]

# anchors per figure (present in both languages where applicable)
FIGS = [
    ("01_overview",  "HERO",      None),
    ("02_mechanism", "FIG",       "Mechanistic panorama|机制全景"),
    ("03_trend",     "FIG",       "Annual publication trend|发文趋势"),
    ("04_timeline",  "ANCHOR",    '<ol class="tl"'),
    ("05_pipeline",  "ANCHOR",    "Industrial platforms|产业平台"),
    ("06_matrix",    "ANCHOR",    'class="matrix"'),
]

def lang_body(t):
    return body_inner(t)

def save(name, styles, block):
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8">' + styles +
            '</head><body style="margin:0;padding:60px;background:#fff">' +
            block + "</body></html>")
    path = os.path.join(OUTDIR, name + ".html")
    open(path, "w").write(html)
    return path

def main(panel, only=None):
    os.makedirs(OUTDIR, exist_ok=True)
    made = []
    for lang, path in REPORTS.items():
        t = open(path).read()
        H = head_styles(t, panel)
        B = body_inner(t)
        for stem, kind, anchor in FIGS:
            name = f"{lang}_{stem}"
            if only and not any(name.startswith(o) for o in only):
                continue
            if kind == "HERO":
                block = B
                Hx = H + "<style>section,footer,nav,.toc{display:none!important}</style>"
            else:
                a = anchor
                if "|" in a:
                    for cand in a.split("|"):
                        if cand in B:
                            a = cand
                            break
                block = extract(B, a)
                Hx = H
            if kind == "FIG":
                block = block.replace(
                    'x="36" y="26" font-size="10" text-anchor="end"',
                    'x="58" y="26" font-size="10" text-anchor="end"')
            made.append(save(name, Hx, block))
    return made

if __name__ == "__main__":
    panel = sys.argv[1] if len(sys.argv) > 1 else "nejm"
    only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    for p in main(panel, only):
        print(p)
