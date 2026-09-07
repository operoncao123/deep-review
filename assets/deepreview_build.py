#!/usr/bin/env python3
"""deepreview_build — generic build core for Deep Review workspaces.

Topic-agnostic extraction of the patterns that proved themselves in the
DR-PROT-001 (proteasome) build. A workspace's build_report.py keeps only its
REG registry (key -> PMID/URL), its content fragments, and its REVIEW_ID /
VERSION / dates — everything below is reusable as-is:

    from deepreview_build import (
        build_number_map, substitute_citations, references_rows,
        inject_colgroups, year_counts, meta_tokens, apply_meta, qc_report)

Design rules enforced here (see ../references/qc_checklist.md):
* in-text [n] citations link DIRECTLY to the source record — PubMed/DOI URL
  taken from the registry entry, external and `target="_blank" rel="noopener"`;
  the reference table repeats the same URL (reader clicks once, lands on PubMed);
* document meta (version, dates, counts) is INJECTED from one constants block
  via {{DR_*}} / {{NREFS}} / {{NPMID}} / {{NURLREF}} / {{TREND_*}} tokens —
  prose never hardcodes numbers the build can compute;
* trend charts read data/*.json, use a CONTINUOUS annual axis, and trim
  pre-field strays (10-year-window rule);
* booktabs colgroups pin pure-number index columns to their floor width;
* qc_report checks bare [n], external target/rel, internal anchor resolution
  (a stray href="#ref-n" now FAILS — reference rows no longer carry ids),
  and leftover tokens — and returns False so callers can sys.exit(1).
"""
import json, os, re, sys, html

TOK = re.compile(r"⟦([A-Za-z0-9_,\s]+)⟧")
META_RE = re.compile(r"\{\{([A-Z_]+)\}\}")

# ---------------- citations ----------------
def build_number_map(frag, registry):
    """⟦key⟧ tokens -> 1-based numbers by order of first appearance."""
    order = []
    for m in TOK.finditer(frag):
        for k in [x.strip() for x in m.group(1).split(",") if x.strip()]:
            if k not in registry:
                sys.exit(f"ERROR: unknown cite key: {k}")
            if k not in order:
                order.append(k)
    return {k: i + 1 for i, k in enumerate(order)}

def substitute_citations(frag, nummap, registry):
    """⟦key⟧ tokens -> [n] anchors opening the source record directly.

    One external link per number: registry[key]["url"] (PubMed for kind=pmid,
    DOI/registry URL otherwise), always target="_blank" rel="noopener".
    Renamed from substitute_internal (which emitted #ref-n page anchors);
    workspaces upgrading to this builder change one import + call site."""
    def rep(m):
        keys = [x.strip() for x in m.group(1).split(",") if x.strip()]
        out = []
        for k in keys:
            u = html.escape(registry[k]["url"], quote=True)
            out.append(f'[<a href="{u}" target="_blank" rel="noopener">{nummap[k]}</a>]')
        return "".join(out)
    return TOK.sub(rep, frag)

def references_rows(nummap, registry, render_ref):
    """render_ref(n, registry[key]) -> HTML for the citation cell."""
    return "".join(
        f'<tr><td class="lbl">{n}</td><td>{render_ref(n, registry[k])}</td></tr>'
        for k, n in sorted(nummap.items(), key=lambda kv: kv[1]))

# ---------------- bib keys ----------------
_BIB_STOP = {"the", "a", "an", "of", "and", "in", "for", "on", "by", "is", "are",
             "to", "from", "with", "at", "as", "its", "via", "into", "that", "this"}

def bib_key(first_author, year, title, fallback):
    """firstauthorYYYYkeyword per qc_checklist; deduplicate via dedup_bib_keys."""
    a = re.sub(r"[^A-Za-z]", "", (first_author or "").split()[0] if first_author else "").lower() or "anon"
    kw = "work"
    for w in re.split(r"[\s\-–—/()]+", (title or "").lower()):
        w = re.sub(r"[^a-z]", "", w)
        if len(w) >= 4 and w not in _BIB_STOP:
            kw = w
            break
    return f"{a}{year}{kw}" if year and a != "anon" else fallback

def dedup_bib_keys(keys_in_order):
    """Same firstauthor+year+keyword -> trailing a, b, c… (first duplicate gets 'a')."""
    seen, out = {}, []
    for k in keys_in_order:
        if k in seen:
            out.append(k + chr(ord("a") + seen[k] - 1))
            seen[k] += 1
        else:
            seen[k] = 1
            out.append(k)
    return out

# ---------------- trend data ----------------
def year_counts(json_path, min_decade_works=50):
    """OpenAlex group_by JSON -> (dense [(year, n)], total).

    Leading strays are trimmed: the series starts at the first year whose
    following 10-year window holds ≥ min_decade_works works — isolated
    misindexed hits (a topic word matching an 1836 title) would otherwise
    stretch the chart across empty centuries. Total prefers the API's
    meta.count over the group_by sum (they differ when records lack years)."""
    d = json.load(open(json_path))
    by_year = {int(g["key"]): g["count"] for g in d["group_by"]}
    years = sorted(by_year)
    start = years[0]
    for y in years:
        if sum(by_year.get(w, 0) for w in range(y, y + 10)) >= min_decade_works:
            start = y
            break
    total = (d.get("meta") or {}).get("count") or sum(by_year.values())
    return [(y, by_year.get(y, 0)) for y in range(start, years[-1] + 1)], total

# ---------------- meta tokens ----------------
def meta_tokens(review_id, version, run_date, cutoff, nummap, registry,
                series=None, total=None):
    npmid = sum(1 for k in nummap if registry[k].get("kind") == "pmid")
    out = {
        "DR_ID": review_id, "DR_VERSION": version, "DR_DATE": run_date,
        "DR_CUTOFF": cutoff, "NREFS": str(len(nummap)), "NPMID": str(npmid),
        "NURLREF": str(len(nummap) - npmid),
    }
    if series:
        out["TREND_TOTAL"] = f"{(total or 0):,}"
        out["TREND_PARTIAL"] = f"{series[-1][1]:,}"
    return out

def apply_meta(frag, tokens):
    return META_RE.sub(lambda m: tokens.get(m.group(1), m.group(0)), frag)

# ---------------- booktabs colgroups ----------------
def _strip_tags(x):
    return re.sub(r"<[^>]+>", "", x)

def _disp_w(piece):
    """Display width: CJK glyphs are ~2x a latin char at the same font size."""
    return sum(2.1 if ord(ch) > 0x2E80 else 1.0 for ch in piece)

_NUM_RE = re.compile(r"^[\d,\.–\-%]+$")

def _tokens(x):
    out = []
    for w in _strip_tags(x).replace("/", "/ ").replace("(", " (").split():
        if re.match(r"^\d{4}[-/]\d{2}([-/]\d{2,4})?$", w):
            out.append(_disp_w(w))  # keep dates (2026-09-03) on one line
            continue
        for piece in w.split("-"):
            if piece and "⟦" not in piece:
                W = min(_disp_w(piece), 28)  # long code/URL strings may wrap anywhere
                if piece.upper() == piece and any(ch.isalpha() for ch in piece):
                    W *= 1.18  # ALL-CAPS tokens render wide
                out.append(W)
    return out

def inject_colgroups(frag, table_class="bk"):
    """Content-aware column widths for every booktabs table.

    Pure-number index columns ('#', years) are pinned to their floor width —
    an index is not content and must not steal width from text columns.
    Remaining columns share the pool by sqrt-damped content weight, floored so
    the longest unbreakable token never breaks (calibrated to the ~670px PRINT
    content width, narrower than screen; 16px inter-column padding included)."""
    def fix(m):
        block = m.group(0)
        if "<colgroup" in block:
            return block
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", block, re.S)
        header_cells, body_rows = None, []
        for r_ in rows:
            if "<th" in r_ and header_cells is None:
                header_cells = re.findall(r"<th[^>]*>(.*?)</th>", r_, re.S)
            elif "<td" in r_:
                body_rows.append(re.findall(r"<td[^>]*>(.*?)</td>", r_, re.S))
        ncols = len(header_cells) if header_cells else (max(map(len, body_rows)) if body_rows else 0)
        if ncols == 0:
            return block
        col_len = [[] for _ in range(ncols)]
        col_tok = [[] for _ in range(ncols)]
        col_txt = [[] for _ in range(ncols)]
        if header_cells:
            for i, hcel in enumerate(header_cells[:ncols]):
                t = _strip_tags(hcel).strip()
                col_len[i].append(len(t))
                col_tok[i].extend(len(p) for p in t.split())
        for cells in body_rows:
            for ci, cel in enumerate(cells[:ncols]):
                t = _strip_tags(cel)
                col_len[ci].append(min(len(" ".join(t.split())), 220))
                col_tok[ci].extend(_tokens(cel))
                col_txt[ci].append(" ".join(t.split()))
        pinned = {}
        for ci in range(ncols):
            cells, toks = col_txt[ci], col_tok[ci]
            if cells and all(_NUM_RE.match(t) for t in cells) and toks and max(toks) <= 4:
                pinned[ci] = max(4.2, 1.42 * max(toks) + 2.8)
        weights = [max(3.0, max(v) ** 0.5) for v in col_len]
        floors = [max(4.5, 1.42 * max(toks) + 3.2) if toks else 5.0 for toks in col_tok]
        sf = sum(floors)
        if sf > 100.0:
            floors = [f * 100.0 / sf for f in floors]
        pool = 100.0 - sum(pinned.values())
        widths = dict(pinned)
        free = [i for i in range(ncols) if i not in pinned]
        tot = sum(weights[i] for i in free)
        for i in free:
            widths[i] = pool * weights[i] / tot if tot > 0 else pool / max(1, len(free))
        fixed = set(pinned)
        for _ in range(ncols):
            under = [i for i in free if i not in fixed and widths[i] < floors[i] - 1e-6]
            if not under:
                break
            for i in under:
                fixed.add(i)
                widths[i] = floors[i]
            pool = 100.0 - sum(widths[i] for i in fixed)
            fpool = sum(weights[i] for i in free if i not in fixed)
            if fpool <= 0 or pool <= 0:
                break
            for i in free:
                if i not in fixed:
                    widths[i] = pool * weights[i] / fpool
        cg = "<colgroup>" + "".join(f'<col style="width:{widths[i]:.1f}%">' for i in range(ncols)) + "</colgroup>"
        block = re.sub(r'(<th[^>]*?)\s+style="width:[^"]*"', r"\1", block)
        # <wbr> after "/" in TEXT NODES only: Chrome never breaks slash compounds
        # on its own, and floors assume they are breakable. Attribute values
        # (href="…/…") are untouched — the pattern only spans tag-free text.
        # (Keep `overflow-wrap:break-word` on td in the template as the last-resort
        # valve for tokens that still don't fit.)
        block = re.sub(r">([^<>]+)<", lambda m: ">" + m.group(1).replace("/", "/<wbr>") + "<", block)
        return block.replace(f'<table class="{table_class}">',
                             f'<table class="{table_class}">' + cg, 1)
    return re.sub(rf'<table class="{table_class}">.*?</table>', fix, frag, flags=re.S)

# ---------------- QC ----------------
def qc_report(path, label=None):
    """Hard gates for a rendered HTML report. Returns True/False — callers
    should sys.exit(1) on False so CI and pipelines catch failures."""
    t = open(path).read()
    body = t[t.index("<body>"):]
    stripped = re.sub(r"<a\b[^>]*>.*?</a>", "", body, flags=re.S)
    bare = re.findall(r"\[\d+\]", stripped)
    ext = re.findall(r'<a\s[^>]*href="http[^"]*"[^>]*>', body)
    no_target = [a for a in ext if 'target="_blank"' not in a]
    no_rel = [a for a in ext if 'rel="noopener"' not in a]
    ids = set(re.findall(r'id="([^"]+)"', body))
    unresolved = set(re.findall(r'href="#([^"]+)"', body)) - ids
    leftover = re.findall(r"\{\{[A-Z_]+\}\}|⟦", body)
    ok = not (bare or no_target or no_rel or unresolved or leftover)
    print(f"QC {label or os.path.basename(path)}: bare[n]={len(bare)}, "
          f"ext missing target={len(no_target)}, missing noopener={len(no_rel)}, "
          f"unresolved internal anchors={len(unresolved)} {sorted(unresolved)[:4]}, "
          f"leftover tokens={len(leftover)} -> {'PASS' if ok else 'FAIL'}")
    return ok
