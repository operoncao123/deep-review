#!/usr/bin/env python3
"""Render the inline figure blocks of a built Deep Review HTML report to
300-dpi PNGs for the DOCX manuscript. Usage:
    python3 render_figures.py <final_report.html> <figures_dir> <spec.json>
spec.json: {"<out_name>": {"anchor": "<substring uniquely locating the block>",
                            "kind": "figblock|pathway|tablewrap"}}
figblock/tablewrap = smallest enclosing .figblock/.table-wrap container;
pathway = the .pathway div itself.
"""
import importlib.util, json, os, re, subprocess, sys

spec = importlib.util.spec_from_file_location(
    "palettes", "/Users/operoncao/Nutstore Files/我的坚果云/Postdoc/agent/skills/deep-review/assets/palettes.py")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
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

def main():
    html_path, figdir, spec_path = sys.argv[1], sys.argv[2], sys.argv[3]
    t = open(html_path).read()
    head = t[t.index("<head>"):t.index("</head>")]
    head = head[head.index("<style>"):]
    head += ("<style>.palette-bar,.pal-dots,#pal-switch,.dr-switch{display:none!important}"
             "svg{overflow:visible!important}</style>")
    B = re.sub(r"^<body[^>]*>", "", t[t.index("<body"):])
    B = B[:B.rindex("</body>")]
    os.makedirs(figdir, exist_ok=True)
    jobs = json.load(open(spec_path))
    for out_name, job in jobs.items():
        i = B.index(job["anchor"])
        if job["kind"] == "pathway":
            s = t  # unused
            # the .pathway div itself: balanced div scan from its open tag
            m = re.compile(r'<div class="pathway"[^>]*>').search(B, i - 200)
            start = m.start()
            depth, j = 1, m.end()
            while depth:
                nxt = re.search(r"<div\b|</div>", B[j:])
                depth += -1 if nxt.group(0) == "</div>" else 1
                j += nxt.end()
            block = B[start:j]
        else:
            block = container_at(B, i)
        wrap = (f'<!DOCTYPE html><html><head><meta charset="utf-8">{head}</head>'
                f'<body style="margin:0;padding:60px;background:#fff">{block}</body></html>')
        wp = os.path.join(figdir, out_name + ".html")
        open(wp, "w").write(wrap)
        png = os.path.join(figdir, out_name + ".raw.png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=3", "--window-size=1500,3200",
                        "--virtual-time-budget=8000", f"--screenshot={png}",
                        "file://" + os.path.abspath(wp)],
                       check=True, capture_output=True)
        from PIL import Image, ImageChops
        im = Image.open(png).convert("RGB")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        b = ImageChops.difference(im, bg).getbbox()
        b = (max(0, b[0] - 12), max(0, b[1] - 12), min(im.width, b[2] + 12), min(im.height, b[3] + 12))
        im.crop(b).save(os.path.join(figdir, out_name + ".png"), optimize=True)
        os.remove(wp); os.remove(png)
        print(out_name, Image.open(os.path.join(figdir, out_name + ".png")).size)

if __name__ == "__main__":
    main()
