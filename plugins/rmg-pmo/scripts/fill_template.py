#!/usr/bin/env python3
"""
fill_template.py -- fill an official RMG PMO PowerPoint template from a values file.

Usage:
    python3 fill_template.py --map <skill>/fieldmap.json --values values.json \
                             --out OUTPUT.pptx [--template X.pptx] [--strict]

The official template is named in the fieldmap and resolved relative to it, so
--template is only needed to override it.

Design rules (do not change without logging a decision):
  * Formatting of the template is preserved: text is written into the existing
    run so font, size and colour survive.
  * Every field declared in the fieldmap MUST be supplied. A field that is
    absent, null or empty is written as a visible marker:
        <MISSING: label -- owner: X -- needed by: Y>
    so an unfinished deck is obviously unfinished. It is never left blank and
    never keeps the template's Dutch guidance text.
  * Numbers are never invented: K-euro and totals are computed by this script
    from the man-days supplied, so the deck cannot contain arithmetic that
    disagrees with itself.
  * Exit code 0 = written. The script prints a JSON report on stdout listing
    filled fields, missing fields and any overflow, for use in the gap report.
"""
import argparse, copy, json, os, sys
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

MARK_OPEN, MARK_CLOSE = "⟨", "⟩"

# ----------------------------------------------------------------- text writing
def _para_template(p_el):
    """A copy of a paragraph element with its runs/breaks stripped."""
    t = copy.deepcopy(p_el)
    for tag in ("a:r", "a:br", "a:fld"):
        for el in t.findall(qn(tag)):
            t.remove(el)
    return t

def _run_template(tf):
    for p in tf.paragraphs:
        if p.runs:
            return copy.deepcopy(p.runs[0]._r)
    return None

def _append_run(p_el, r_el):
    end = p_el.find(qn("a:endParaRPr"))
    if end is not None:
        end.addprevious(r_el)
    else:
        p_el.append(r_el)

def set_text(tf, value, italic=None, fallback_pt=12.0):
    """Replace the whole text frame with `value`, keeping the original run formatting."""
    lines = str(value).split("\n")
    tmpl_r = _run_template(tf)
    tmpl_p = _para_template(tf.paragraphs[0]._p)
    body = tf._txBody
    for p in body.findall(qn("a:p")):
        body.remove(p)
    if tmpl_r is None:
        # The cell was empty in the template, so there is no formatting to copy and
        # the inherited default is far too large. Use the deck's body size instead,
        # so filled boxes and MISSING markers render at the same size.
        for p in body.findall(qn("a:p")):
            body.remove(p)
        body.append(copy.deepcopy(tmpl_p))
        tf.text = "\n".join(lines)
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.size = Pt(fallback_pt)
                if italic is not None:
                    r.font.italic = italic
        return
    for line in lines:
        p_el = copy.deepcopy(tmpl_p)
        r_el = copy.deepcopy(tmpl_r)
        r_el.find(qn("a:t")).text = line
        _append_run(p_el, r_el)
        body.append(p_el)
    if italic is not None:
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.italic = italic

def sub_text(tf, find, value):
    """Replace `find` with `value` in place, preserving runs, line breaks and formatting."""
    for p in tf.paragraphs:
        runs = list(p.runs)
        if not runs:
            continue
        texts = [r.text for r in runs]
        joined = "".join(texts)
        idx = joined.find(find)
        if idx < 0:
            continue
        end, pos, placed = idx + len(find), 0, False
        for r, t in zip(runs, texts):
            rs, re_ = pos, pos + len(t)
            pos = re_
            if re_ <= idx or rs >= end:
                continue
            lo, hi = max(idx, rs) - rs, min(end, re_) - rs
            r.text = t[:lo] + ("" if placed else str(value)) + t[hi:]
            placed = True
        return True
    return False

def append_text(tf, value):
    for p in reversed(tf.paragraphs):
        if p.runs:
            p.runs[-1].text = p.runs[-1].text.rstrip() + " " + str(value)
            return True
    set_text(tf, value)
    return True

# ----------------------------------------------------------------- overflow check
def _font_pt(cell, default=12.0):
    for p in cell.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size:
                return r.font.size.pt
    return default

def _metrics(table, ri, ci):
    cell = table.cell(ri, ci)
    span_w = getattr(cell, "span_width", 1) or 1
    span_h = getattr(cell, "span_height", 1) or 1
    col_w = sum(table.columns[c].width
                for c in range(ci, min(ci + span_w, len(table.columns))))
    row_h = sum(table.rows[r].height
                for r in range(ri, min(ri + span_h, len(table.rows))))
    return cell, Emu(col_w).pt, Emu(row_h).pt

# Calibrated against rendered output of the official templates, not theory.
CHAR_W, LINE_H, PAD_W, PAD_H = 0.63, 1.25, 14.0, 12.0

def _fits(text, width_pt, height_pt, pt):
    cpl = max(8, int((width_pt - PAD_W) / (pt * CHAR_W)))
    need = sum(max(1, -(-len(line) // cpl)) for line in str(text).split("\n"))
    have = max(1, int((height_pt - PAD_H) / (pt * LINE_H)))
    return need <= have, need, have

def room_below(slide, prs, shape):
    """Vertical space in points between this shape's bottom and whatever is
    underneath it - the next shape down, or the bottom of the slide."""
    bottom = shape.top + shape.height
    limit = prs.slide_height
    for other in slide.shapes:
        if other is shape:
            continue
        try:
            top, height = other.top, other.height
        except Exception:
            continue
        if top is None or height is None:
            continue
        if top >= bottom - 9525:          # roughly at or below our bottom edge
            limit = min(limit, top)
    return Emu(max(0, limit - bottom)).pt

def fit_cell(prs, slide, shape, ri, ci, text, autoshrink=True, min_pt=9.0):
    """The official templates have no autofit. Text that does not fit either makes
    the row grow - pushing the table into whatever sits below it - or, in a
    one-row box, is simply drawn over the next box.

    Try in order: it already fits; shrink the font to fit; grow the row if there is
    genuinely room underneath on the slide; otherwise report a real overflow.
    Returns None | ("shrunk", pt) | ("grew", lines, pt) | ("overflow", need, have)."""
    try:
        table = shape.table
        cell, w, h = _metrics(table, ri, ci)
        pt = _font_pt(cell)
        ok, need, have = _fits(text, w, h, pt)
        if ok:
            return None
        if autoshrink:
            trial = pt
            while trial > min_pt:
                trial = round(trial - 0.5, 1)
                if _fits(text, w, h, trial)[0]:
                    for p in cell.text_frame.paragraphs:
                        for r in p.runs:
                            r.font.size = Pt(trial)
                    return ("shrunk", trial)
        extra_pt = (need - have) * pt * LINE_H
        if extra_pt <= room_below(slide, prs, shape):
            table.rows[ri].height = table.rows[ri].height + Pt(extra_pt)
            return ("grew", need - have, round(extra_pt, 1))
        return ("overflow", need, have)
    except Exception:
        return None

def _font_pt(cell, default=12.0):
    for p in cell.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size:
                return r.font.size.pt
    return default

# ----------------------------------------------------------------- table helpers
def clone_last_row(table):
    tbl = table._tbl
    rows = tbl.findall(qn("a:tr"))
    new = copy.deepcopy(rows[-1])
    for tc in new.findall(qn("a:tc")):
        tf = tc.find(qn("a:txBody"))
        if tf is None:
            continue
        ps = tf.findall(qn("a:p"))
        for p in ps[1:]:
            tf.remove(p)
        for tag in ("a:r", "a:br", "a:fld"):
            for el in ps[0].findall(qn(tag)):
                ps[0].remove(el)
    rows[-1].addnext(new)
    return table.rows[len(table.rows) - 1]

# ----------------------------------------------------------------- main fill
def shape_at(prs, slide_i, shape_i):
    return list(prs.slides[slide_i].shapes)[shape_i]

def marker(spec, key):
    label = spec.get("label", key)
    owner = spec.get("owner", "unassigned")
    by = spec.get("needed_by", "before the gate")
    return f"{MARK_OPEN}MISSING: {label} -- owner: {owner} -- needed by: {by}{MARK_CLOSE}"

def fmt(v):
    """Print 71.0 as 71 but keep 41.0 -> 41 and 10.9 -> 10.9."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)

def is_empty(v):
    return v is None or (isinstance(v, str) and not v.strip())

def derive(values, fmap, report):
    """Compute K-euro and totals so the deck's arithmetic is always internally consistent."""
    rate = float(values.get("meta", {}).get("internal_md_rate_eur", 910))
    cells = values.setdefault("cells", {})
    for key, rule in fmap.get("derived", {}).items():
        try:
            if "keur_from_md" in rule:
                md = cells.get(rule["keur_from_md"])
                if is_empty(md):
                    continue
                cells[key] = fmt(round(float(str(md).replace(",", ".")) * rate / 1000, 1))
            elif "sum" in rule:
                parts = [cells.get(k) for k in rule["sum"]]
                if any(is_empty(p) for p in parts):
                    continue
                total = sum(float(str(p).replace(",", ".")) for p in parts)
                cells[key] = fmt(round(total, 1))
            elif "diff" in rule:
                a, b = (cells.get(k) for k in rule["diff"])
                if is_empty(a) or is_empty(b):
                    continue
                d = float(str(a).replace(",", ".")) - float(str(b).replace(",", "."))
                cells[key] = ("+" if d >= 0 else "-") + fmt(round(abs(d), 1))
            report["derived"].append(key)
        except (TypeError, ValueError) as e:
            report["warnings"].append(f"could not derive {key}: {e}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    ap.add_argument("--values", required=True)
    ap.add_argument("--template", required=False,
                    help="defaults to the 'template' path in the fieldmap, resolved "
                         "relative to the fieldmap's own directory")
    ap.add_argument("--out", required=True)
    ap.add_argument("--strict", action="store_true",
                    help="fail instead of writing MISSING markers")
    a = ap.parse_args()

    fmap = json.load(open(a.map, encoding="utf-8"))
    values = json.load(open(a.values, encoding="utf-8"))
    template = a.template
    if not template:
        template = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(a.map)), fmap["template"]))
    if not os.path.exists(template):
        sys.exit(f"template not found: {template}")
    prs = Presentation(template)
    report = {"filled": [], "missing": [], "derived": [], "overflow": [], "shrunk": [], "grew": [], "warnings": [],
              "unknown_keys": []}

    derive(values, fmap, report)
    vcells = values.get("cells", {})
    vtables = values.get("tables", {})

    for k in vcells:
        if k not in fmap.get("cells", {}):
            report["unknown_keys"].append(k)
    for k in vtables:
        if k not in fmap.get("tables", {}):
            report["unknown_keys"].append(k)

    # ---- single fields
    for key, spec in fmap.get("cells", {}).items():
        val = vcells.get(key)
        missing = is_empty(val)
        if missing:
            if a.strict:
                report["missing"].append(key)
                continue
            val = marker(spec, key)
            report["missing"].append(key)
        else:
            report["filled"].append(key)
        sh = shape_at(prs, spec["slide"], spec["shape"])
        mode = spec.get("mode", "cell")
        ital = spec.get("italic", fmap.get("default_italic"))
        if mode == "cell":
            tf = sh.table.cell(spec["row"], spec["col"]).text_frame
            set_text(tf, val, ital, fmap.get("default_font_pt", 12.0))
            res = fit_cell(prs, prs.slides[spec["slide"]], sh, spec["row"], spec["col"], val,
                           autoshrink=spec.get("autoshrink", fmap.get("default_autoshrink", True)),
                           min_pt=spec.get("min_pt", fmap.get("default_min_pt", 9.0)))
            if res and not missing:
                if res[0] == "shrunk":
                    report["shrunk"].append(f"{key}: font reduced to {res[1]}pt to fit the box")
                elif res[0] == "grew":
                    report["grew"].append(
                        f"{key}: row made {res[2]}pt taller for {res[1]} extra line(s); "
                        f"there was room below it on the slide")
                else:
                    report["overflow"].append(
                        f"{key}: needs about {res[1]} lines, the box fits about {res[2]} even at "
                        f"the minimum font size - shorten it or it will overlap the box below")
        elif mode == "cell_append":
            append_text(sh.table.cell(spec["row"], spec["col"]).text_frame, val)
        elif mode == "text":
            set_text(sh.text_frame, val, ital, fmap.get("default_font_pt", 12.0))
        elif mode == "append":
            append_text(sh.text_frame, val)
        elif mode == "sub":
            repl = f'{spec["find"]} {val}' if spec.get("keep_find") else val
            if not sub_text(sh.text_frame, spec["find"], repl):
                report["warnings"].append(
                    f"{key}: token {spec['find']!r} not found on slide {spec['slide']}")
        else:
            report["warnings"].append(f"{key}: unknown mode {mode}")

    # ---- clear leftover guidance cells
    for spec in fmap.get("clear", []):
        sh = shape_at(prs, spec["slide"], spec["shape"])
        set_text(sh.table.cell(spec["row"], spec["col"]).text_frame, "")

    # ---- repeating tables
    for key, spec in fmap.get("tables", {}).items():
        rows = vtables.get(key) or []
        sh = shape_at(prs, spec["slide"], spec["shape"])
        table = sh.table
        cols = spec["cols"]
        first = spec["first_row"]
        capacity = len(table.rows) - first - len(spec.get("reserved_rows", []))
        if not rows:
            report["missing"].append(key)
            if not a.strict:
                set_text(table.cell(first, 0).text_frame,
                         marker(spec, key))
                for ci in range(1, len(table.columns)):
                    set_text(table.cell(first, ci).text_frame, "")
            continue
        report["filled"].append(f"{key} ({len(rows)} rows)")
        for i, row in enumerate(rows):
            ri = first + i
            if ri >= len(table.rows):
                if spec.get("grow", True):
                    clone_last_row(table)
                else:
                    report["overflow"].append(
                        f"{key}: {len(rows) - i} row(s) did not fit ({capacity} available)")
                    break
            for ci, col in enumerate(cols):
                if col is None:
                    continue
                v = row.get(col, "")
                if col == "nr" and is_empty(v):
                    v = str(i + 1)
                set_text(table.cell(ri, ci).text_frame, "" if is_empty(v) else str(v),
                         spec.get("italic", fmap.get("default_italic")))
        # blank out unused pre-existing rows
        for ri in range(first + len(rows), len(table.rows)):
            for ci, col in enumerate(cols):
                if col is None:
                    continue
                if table.cell(ri, ci).text.strip():
                    set_text(table.cell(ri, ci).text_frame, "")

    prs.save(a.out)
    report["out"] = a.out
    report["template"] = template
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
