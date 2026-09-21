# Decisions — RMG PMO gate skills

## 2026-09-07 — Scope: four gate skills, one per milestone
Decision: build `rmg-project-pitch`, `rmg-pid`, `rmg-plan-to-execute`,
`rmg-project-closing`. A Steerco skill is deliberately left for later even
though `Context/Templates/Template Steerco.pptx` exists.
Source: Stijn, session 2026-09-07.
Status: confirmed

## 2026-09-07 — One context file per project, append-only
Decision: each project gets `projects/PRJ00xxx.NAME/project-context.md` with a
section per phase. Skills add their phase and never rewrite an earlier one, so
the PTE deviation check and the Closing doc can read what the PID committed.
Source: Stijn, session 2026-09-07.
Status: confirmed

## 2026-09-07 — Output language
Decision: field labels stay as in the official templates (mixed EN/NL);
everything the skills write into them is English.
Source: Stijn, session 2026-09-07.
Status: confirmed

## 2026-09-07 — Dutch guidance text is replaced, not kept
Decision: when a template cell contains guidance text ("Beschrijf welk probleem
of opportuniteit..."), the skill overwrites it with the content, or with a
visible `(MISSING: ... -- owner: ... -- needed by: ...)` marker when the input is
not available. The guidance never survives into a board deck.
Source: Stijn, session 2026-09-07.
Status: confirmed

## 2026-09-07 — Figures are typed in per project, arithmetic is computed
Decision: MD estimates, external cost and business case figures are supplied by
the project manager per run; no Excel or JIRA integration for now. kEUR per team
(MD x internal rate / 1000), the internal RMG totals, the phase totals and the
Closing committed-vs-spend differences are computed by `fill_template.py` so the
deck cannot contain arithmetic that disagrees with itself.
Source: Stijn, session 2026-09-07.
Status: confirmed

## 2026-09-07 — Internal MD rate 910 EUR (2026)
Decision: 910 EUR / MD for profiles inside IT DEV, Cycles and PMO. Held in the
context file per project as `internal_md_rate_eur` so a rate change does not
retro-edit approved decks.
Source: note on the PROJECT RESOURCES slide of the PID and PTE templates.
Status: confirmed

## 2026-09-07 — "Totaal INTERN RMG": MD includes other RMG, kEUR does not
Decision: the internal MD total sums IT DEV + Cycles + PMO + other RMG; the
internal kEUR total sums only the three billable lines, because the template
note says other internal effort is mapped but not charged to the project (the
template itself prints "x" in that kEUR cell).
Source: inferred from the template note; not confirmed by PMO.
Status: assumed

## 2026-09-07 — Rows 7 and 9 of the resources table are spacers
Decision: external resources are written on the "Totaal Externe Resources" row
itself; the blank rows above and below it are treated as layout spacers.
Source: inferred from the template structure.
Status: assumed

## 2026-09-07 — The 10% deviation rule is measured on total project spend
Decision: the PTE skill flags "CEO / PMO Board approval required" when the total
BUILD spend (internal kEUR + external kEUR) deviates more than 10% from what the
PID committed. It also reports the MD deviation separately.
Source: the "Goedkeurder" row of the PTE template says "CEO, indien deviatie >
10% tov initial request in PID" but does not say deviation of what.
Status: assumed -- needs confirmation from Head of PMO

## 2026-09-07 — Closing "Committed Resources / INIT" = the PID figures
Decision: the Closing doc's committed column is filled from the PID, not the PTE.
The skill also shows the PTE figure next to it in the gap report when the two
differ, so the reader sees which baseline is being used.
Source: the column header says "INIT", which is phase 1.
Status: assumed -- needs confirmation from Head of PMO

## 2026-09-07 — Pitch and Closing have no separate gate checklist
Decision: only PID and PTE have tool checklists (screenshots in
`Context/Requirements per phase/`). The Pitch and Closing skills check what
their own template requires, plus for Closing the IT Service Desk arrangements
listed in the template's key activities. No invented checklist.
Source: Stijn chose "leave those two gate-light", session 2026-09-07.
Status: confirmed

## 2026-09-07 — Deviation against a range: report all three readings
Decision: the PID build estimate is normally a range. The PTE skill measures the
deviation against the top of the range (the largest figure the PMO Board
approved) and also reports the midpoint. Where the two readings disagree about
whether 10% is crossed, the skill says so and hands the call to the Head of PMO
rather than picking the reading that avoids escalation.
Source: found while testing PRJ00214.SELFSERVICE end to end — build estimate
180-240 MD + 60-90 kEUR gave +6.9% on the top of the range but +23.9% on the
midpoint for the same PTE figures.
Status: assumed -- needs confirmation from Head of PMO

## 2026-09-07 — Observation: the 10% rule is not measurable as written
Observation, not a change: "deviatie > 10% tov initial request in PID" cannot be
applied unambiguously while the PID commits a range and the PTE commits a point.
The skills encode a reading and flag the ambiguity every time it matters. Worth
raising with the PMO — either the PID should commit a single figure, or the rule
should name which point of the range it means.
Status: open -- to raise

## 2026-09-18 — Template boxes are fixed height; the engine shrinks to fit
Decision: the official templates use fixed-height table rows with no autofit, so
text that does not fit is silently drawn over the box below it. `fill_template.py`
now estimates the fit, reduces the font in 0.5pt steps down to 9pt, and reports
each reduction under `shrunk`. If it still does not fit at 9pt it reports
`overflow`, which must be treated as an error and the text shortened.
Source: found on the first real pitch (Uitbreiding eindredactie met AI) — the
description and assumptions overran their boxes and overlapped the next heading.
Affects: all four skills, `assets/fill_template.py`.
Status: confirmed

## 2026-09-18 — Empty template cells are written at 12pt
Decision: cells that are empty in the template carry no run to copy formatting
from, and the inherited default is much larger than the deck's body text. The
engine now writes those at 12pt, so a filled box and a MISSING marker on the same
slide render at the same size.
Source: same test — the markers rendered visibly larger than the filled boxes.
Affects: all four skills, `assets/fill_template.py`.
Status: confirmed

## 2026-09-18 — A small project is under 30 MD
Decision: at RMG, "small" in the pitch's estimated project size / complexity
means under 30 MD. The thresholds for medium and large are not established; the
pitch skill must ask rather than offer a bracket it invented.
Source: Stijn, correcting a draft during the Uitbreiding eindredactie met AI
pitch, session 2026-09-18. Recorded in `team-input/2026-09-18-stijn-corrections.md`.
Affects: skills/rmg-project-pitch/SKILL.md
Status: confirmed (small); medium and large thresholds still unknown

## 2026-09-21 — Packaged as a Claude plugin marketplace
Decision: the four skills ship as one plugin, `rmg-pmo`, in a private GitHub
marketplace repo. One plugin rather than four, because they are one process and
share the fill engine, the templates and the context-file spec. The fill engine,
the four official templates, the context-file spec and the context template are
now single copies at the plugin root instead of one copy per skill.
Each skill's `fieldmap.json` names its template and the engine resolves it
relative to the fieldmap, so no template path is passed on the command line.
Source: Stijn, session 2026-09-21.
Affects: everything under `plugins/rmg-pmo/`.
Status: confirmed

## 2026-09-21 — Overflow: grow the row when there is room, shrink before that
Decision: when text does not fit a template cell the engine now, in order:
shrinks the font to a 9pt floor; if that is not enough, grows the row provided
there is genuinely free space between that table and whatever sits below it on
the slide; and only reports a real `overflow` when neither works. This replaced a
check that treated every stacked box the same and flagged cases where the row
would simply have grown into empty space.
Source: found when the relocated plugin refilled the PRJ00214.SELFSERVICE decks —
two fields written before the overflow check existed were flagged, and inspecting
the geometry showed both had room below them. Verified by rendering the closing
deck.
Affects: `plugins/rmg-pmo/scripts/fill_template.py`.
Status: confirmed

## 2026-09-21 — The Cowork `skills/` folder is retired
Decision: `skills/` in the Cowork folder is superseded by the repo. It was moved
to `_superseded-skills/` so nobody edits a copy that is no longer distributed.
The repo under `rmg-pmo-marketplace/` is the only source of truth for skill
content; the Cowork folder keeps `projects/` (live project data, git-ignored) and
`Context/Templates/` (where the PMO's own master templates arrive).
Status: confirmed
