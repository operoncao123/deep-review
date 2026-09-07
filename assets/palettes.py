#!/usr/bin/env python3
"""DR-PROT-001 colour panels — top-journal derived, fresh & muted.

Every deliverable (HTML reports, matplotlib figures, DOCX accents) takes its
colours from ONE panel. Switch the active panel:

    export DEEPREVIEW_PANEL = nature | nejm | lancet | science | jama
                            | graphite | solar | forest | orchid | rose   (default: nature)

or edit ACTIVE below. The HTML reports additionally ship a live switcher
(bottom-right dots); print/PDF export uses whichever panel is selected.
"""

def _mix(hex_color: str, white: float) -> str:
    """Blend a hex colour toward white; white=0 -> unchanged, 1 -> white."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r = round(r + (255 - r) * white)
    g = round(g + (255 - g) * white)
    b = round(b + (255 - b) * white)
    return f"#{r:02X}{g:02X}{b:02X}"

def _deep(hex_color: str, k: float = 0.82) -> str:
    """Darken toward ink for pill/label text that must keep contrast."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"#{round(r*k):02X}{round(g*k):02X}{round(b*k):02X}"

# base hue sets, derived from the ggsci top-journal palettes (softened where
# the house colour is harsh — e.g. Lancet red #ED0000 -> #C43425), plus five
# contrast panels that leave the blue-teal family entirely (graphite..rose)
_HUES = {
    "nature":  dict(accent="#3C5488", sea="#00A087", warm="#D2703F",
                    sand="#B08C3E", slate="#7E6BA8", sage="#6E9464", ink="#212730"),
    "nejm":    dict(accent="#0072B5", sea="#20854E", warm="#BC3C29",
                    sand="#E18727", slate="#7876B1", sage="#79AF97", ink="#1F2933"),
    "lancet":  dict(accent="#00468B", sea="#0099B4", warm="#C43425",
                    sand="#A67C2E", slate="#925E9F", sage="#4E9B60", ink="#1E252C"),
    "science": dict(accent="#3B4992", sea="#008B45", warm="#C93A32",
                    sand="#B08C3E", slate="#631879", sage="#5B9E60", ink="#232733"),
    "jama":    dict(accent="#374E55", sea="#00A1D5", warm="#B24745",
                    sand="#C08A3E", slate="#7A6C9B", sage="#79AF97", ink="#242B2E"),
    # --- contrast panels: deliberately different hue personalities ---
    "graphite": dict(accent="#5E6A75", sea="#3E7C8F", warm="#B4433A",
                     sand="#A08A5A", slate="#7A6A9B", sage="#7E9968", ink="#212427"),
    "solar":    dict(accent="#B4622E", sea="#2E7E6B", warm="#3E6E8E",
                     sand="#C9A227", slate="#6B5B95", sage="#7FA05A", ink="#2A2521"),
    "forest":   dict(accent="#2F6B4F", sea="#3D7EA6", warm="#C06A38",
                     sand="#A8902E", slate="#705E8F", sage="#96A651", ink="#22282A"),
    "orchid":   dict(accent="#6E4E9E", sea="#2E8B8B", warm="#C2564B",
                     sand="#A8783E", slate="#4E6FA3", sage="#6E9B7C", ink="#26222E"),
    "rose":     dict(accent="#A64D6D", sea="#35877B", warm="#C8742E",
                     sand="#B08C3E", slate="#6E5B8E", sage="#7C9A6D", ink="#2B2226"),
}

_LABELS = {
    "nature": "Nature · 蓝青", "nejm": "NEJM · 蓝红", "lancet": "Lancet · 深蓝",
    "science": "Science · 蓝紫", "jama": "JAMA · 灰绿",
    "graphite": "Graphite · 朱砂", "solar": "Solar · 暖陶", "forest": "Forest · 松绿",
    "orchid": "Orchid · 紫罗兰", "rose": "Rose · 浆果",
}

def build_panel(name: str) -> dict:
    h = _HUES[name]
    a, sea, warm = h["accent"], h["sea"], h["warm"]
    sand, slate, sage = h["sand"], h["slate"], h["sage"]
    ink = h["ink"]
    p = {
        "name": name, "label": _LABELS[name],
        # text
        "ink": ink, "ink-soft": _mix(ink, 0.28), "ink-faint": _mix(ink, 0.55),
        # rules
        "rule": _mix(a, 0.18), "rule-thin": _mix(a, 0.58), "rule-hair": _mix(a, 0.82),
        # core hues
        "accent": a, "accent-deep": _deep(a, 0.72),
        "sea": sea, "warm": warm, "sand": sand, "slate": slate, "sage": sage,
        # surfaces (paper carries a whisper of the accent hue)
        "paper": _mix(a, 0.978),
        "bg-soft": _mix(a, 0.95), "bg-shared": _mix(sea, 0.94),
        "bg-deg": _mix(a, 0.90), "tint-accent-bd": _mix(a, 0.62),
        "bg-lcd": _mix(sand, 0.90), "bg-lcd-bd": _mix(sand, 0.66),
        # pills (five category tags)
        "pill-deg-bg": _mix(a, 0.90), "pill-deg-fg": _deep(a, 0.80), "pill-deg-bd": _mix(a, 0.62),
        "pill-a-bg": _mix(sea, 0.90), "pill-a-fg": _deep(sea, 0.80), "pill-a-bd": _mix(sea, 0.62),
        "pill-lcd-bg": _mix(sand, 0.90), "pill-lcd-fg": _deep(sand, 0.80), "pill-lcd-bd": _mix(sand, 0.62),
        "pill-ko-bg": _mix(slate, 0.90), "pill-ko-fg": _deep(slate, 0.80), "pill-ko-bd": _mix(slate, 0.62),
        "pill-pc-bg": _mix(sage, 0.90), "pill-pc-fg": _deep(sage, 0.80), "pill-pc-bd": _mix(sage, 0.62),
        # venn: classic two-hue duo (accent vs warm)
        "v1-stroke": a, "v1-fill": _mix(a, 0.85),
        "v2-stroke": warm, "v2-fill": _mix(warm, 0.86),
        # figures
        "fig-bar": _mix(a, 0.72), "fig-bar-partial": _mix(a, 0.90),
        "fig-line": sea, "fig-band": _mix(a, 0.93),
    }
    return p

PANELS = {name: build_panel(name) for name in _HUES}
ACTIVE = __import__("os").environ.get("DEEPREVIEW_PANEL", "nature").lower()
if ACTIVE not in PANELS:
    ACTIVE = "nature"
P = PANELS[ACTIVE]

def css_vars(panel: dict) -> str:
    """Serialize a panel as CSS custom properties for :root."""
    keys = [k for k in panel if k not in ("name", "label")]
    return ";".join(f"--{k}:{panel[k]}" for k in sorted(keys)) + ";"

# JS object literal for the in-HTML live switcher (same values, same names)
def js_panels() -> str:
    import json
    out = {}
    for name, p in PANELS.items():
        out[name] = {"label": p["label"],
                     **{k: p[k] for k in p if k not in ("name", "label")}}
    return json.dumps(out, ensure_ascii=False)

if __name__ == "__main__":
    for name, p in PANELS.items():
        print(f"{name:8s} {p['label']}: accent={p['accent']} sea={p['sea']} warm={p['warm']}")
    print("active:", ACTIVE, "->", P["label"])
