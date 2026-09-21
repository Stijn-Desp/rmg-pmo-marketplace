---
name: rmg-project-closing
description: >
  Prepares everything needed for the RMG PMO project closing (phase 4/5 - GO LIVE
  / CLOSE): the requirements checklist, a prefilled PROJECT CLOSING DOC deck from
  the official PMO template, the committed-versus-spend comparison against the
  PID, and a report of what is missing or unresolved. Use this whenever someone
  mentions closing a project, the closing document or closing doc, the closing
  meeting, nazorg, go live and close, handover to the IT Service Desk, the
  post-project review, or asks what is needed to close a project or whether the
  promised benefits were realised.
---

# RMG Project Closing (phase 4/5 - GO LIVE - CLOSE)

Approver: **Steerco / CIO**. Key output: **closing document**. Purpose of the
phase, per the template: validate the delivered project result and anchor it in
the operational organization.

Produce three things, in this order, every time:

**A. Requirements brief** - the checklist below.
**B. Prepared deck** - the official template filled in, with a visible marker
wherever a field could not be filled.
**C. Gap report** - short and prioritised, at the very top of the reply.

## Step 1 - Find the project and its context file

Ask for `PRJ00xxx.NAME` if not given. The context file is
`<PMO folder>/projects/PRJ00xxx.NAME/project-context.md`, where `<PMO folder>` is
the folder holding `Context/Templates/` (normally `RMG Skills`).

Read the **whole** file. This gate is almost entirely a comparison against
earlier phases: the PID's `### Committed at INIT` block, the PTE's final scope
and deliverables, and the benefit KPIs promised in both. If those sections are
missing, say so - the closing document cannot honestly evaluate against a
baseline that was never recorded, and that is a finding rather than something to
work around.

## Step 2 - Requirements brief

There is no separate tool checklist for this gate. The requirement is the
template's own content plus the arrangements listed under the phase's key
activities. All hard gates:

| # | Item | Owner |
|---|------|-------|
| 1 | Every PID/PTE deliverable evaluated, realised Y/N + date | Project Manager |
| 2 | Realisation of the quantitative / financial benefits vs the business case | Business Controlling |
| 3 | Realisation of the qualitative benefits | Project Owner |
| 4 | Committed resources (from the PID) vs actual spend | PMO / Project Manager |
| 5 | IT Service Desk: incident flow agreed | Project Manager / IT Service Desk |
| 6 | IT Service Desk: contact persons internal and external | Project Manager |
| 7 | IT Service Desk: SLA available | Project Manager |
| 8 | Validation of the project result by Business, I.T., EA and other stakeholders | Project Sponsor |
| 9 | Integration in the organization + follow-up KPIs with an owner | Project Owner |
| 10 | Closing meeting held - confirmation the project delivers the desired result | Project Sponsor |
| 11 | Communication to the organization | Project Manager |
| 12 | Approach for the post-project review agreed | Head of PMO |

Items 5 to 7 are the ones most often skipped and are what turn a delivered
project into a supported one. Report each as **Y**, **N** or **not stated**.

## Step 3 - Collect the content

`fieldmap.json` (next to this SKILL.md) is the authoritative field list, with a label and an owner
per field.

Build the deliverables table from the PID and PTE, not from the user's memory:
take the milestones and objectives recorded in the context file and ask for a
realised Y/N + date and a comment per line. A deliverable the project quietly
dropped only shows up if the list is derived from what was committed.

Resource figures: the **committed** column comes from the PID's frozen block; ask
only for the actual spend (internal MD, external EUR, other expenses). Do not
compute the differences - `fill_template.py` derives them.

## Step 4 - Consistency checks

**Against the PID and PTE**
- Every deliverable and milestone recorded in the PID or PTE must appear in the
  deliverables table. List any that do not - each is either delivered, descoped
  with a decision behind it, or silently dropped.
- Every benefit KPI promised in the PID or PTE must have a realisation
  statement. "Too early to measure" is an acceptable answer; a blank is not -
  record when it will be measured and who measures it.
- Committed versus spend: report the difference and the percentage per line. Any
  line beyond 10% needs an explanation in the comment column; flag a deviation
  with an empty comment.
- The PID's build figure is normally a **range**. The committed column needs one
  number: use the top of the range, and state in the comment column which point of
  the range was used. Never present a range-derived figure as if it had been an
  exact commitment.
- If the PID and PTE committed figures differ, name both in the gap report and
  state which one is used as the baseline. This skill uses the **PID** figures,
  because the template's column header says INIT - recorded as *assumed* in
  `decisions/`. If the user says the PTE is the baseline, follow them and note
  that the decision log needs updating.
- Recurring cost after go live: compare what actually recurs against what the
  PID and PTE predicted, and confirm someone owns that budget now.
- Any risk still open at closing must be named, with who carries it into
  operations.

**Inside the closing document**
- The four validators (Business, I.T., EA, other stakeholders) must be named
  people. An unvalidated result cannot be closed.
- Integration in the organization must name the operational owner and the
  IT Service Desk arrangements, not just say "handed over".
- Every follow-up KPI must have an owner and a measurement date after closing.
  A KPI with no owner is not follow-up, it is a wish.
- Scope delivered versus the PTE's final scope: state any difference explicitly.

## Step 5 - Write the context file

Fill the phase 4/5 section: fields, the realisation-versus-promised table, open
gaps, and what carries into operations. Do not edit the phase 1, 2 or 3 sections
- append a change-log row instead.

Anything learned here that should change how earlier gates are run (a benefit
type that never gets measured, a resource line that is always wrong) belongs in
`decisions/` as an observation. Record it; do not quietly fix the process.

## Step 6 - Build the deck

```bash
python3 "$PLUGIN/scripts/fill_template.py" \
  --map "$PLUGIN/skills/rmg-project-closing/fieldmap.json" \
  --values "<project folder>/closing-values.json" \
  --out "<project folder>/PRJ00xxx.NAME - CLOSING - <yyyy-mm-dd>.pptx"
```

where `$PLUGIN` is this plugin's root folder - the directory two levels above
this SKILL.md, also available as `${CLAUDE_PLUGIN_ROOT}` where that is set. The
official template is named in `fieldmap.json` and resolved relative to it, so
there is no template path to get wrong. Never edit the template in `templates/`
- it is the master copy shared by every project.

`closing-values.json` has the shape `{"cells": {...}, "tables": {...}}`. Keep it
next to the deck.

Leave out any field you do not have; the script writes
`(MISSING: label -- owner: X -- needed by: Y)` into the cell. Never pass a guess
to avoid a marker.

Check the script's JSON report. `missing` is the backbone of the gap report.
`warnings` and `overflow` must be empty - the template's boxes are a fixed
height and do not autofit, so overflowing text is drawn over the box below.
`shrunk` entries are fine but tell you the text is long for the box: if the
font dropped below about 10pt, shorten the text instead of shipping it small.

## Step 7 - Reply

Gap report first:

```
## Blocking (project cannot be closed)
- item -- owner -- needed by

## Needed for the next step (operations and the post-project review)
- item -- owner -- needed by

## Worth confirming
- item -- why it is uncertain
```

Under "needed for the next step", put what operations inherits: the follow-up
KPIs and their owners, the open risks, the recurring cost and its budget owner,
and the post-project review date.

If nothing is missing, say so explicitly. Then one line naming the deck and its
folder. Do not summarise the deck's contents.
