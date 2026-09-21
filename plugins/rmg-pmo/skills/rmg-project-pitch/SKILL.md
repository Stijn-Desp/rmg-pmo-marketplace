---
name: rmg-project-pitch
description: >
  Prepares the RMG PMO Project Pitch (phase 0 - DISCOVER): the requirements
  checklist, a prefilled PROJECT PITCH deck from the official PMO template, and
  a report of what is still missing. Use this whenever someone mentions a project
  pitch, pitching a project or an idea to the PMO, the DISCOVER phase, getting
  something on the roadmap, screening an opportunity, or asks what is needed
  before the pitch - including when they only ask for the deck or only for the
  checklist.
---

# RMG Project Pitch (phase 0 - DISCOVER)

Approver: **PPM / CIO / Project Owner**. Key output: **approved Project Pitch**.
Next gate: the PID at the end of INITIATE.

Purpose of the phase, per the template: discover and screen opportunities or
threats, and make a first test of whether this becomes a project on the roadmap.
The pitch is deliberately thin - resist the urge to turn it into a PID.

Produce three things, in this order, every time:

**A. Requirements brief** - the checklist below.
**B. Prepared deck** - the official template filled in, with a visible marker
wherever a field could not be filled.
**C. Gap report** - short and prioritised, at the very top of the reply.

## Step 1 - Find the project and its context file

A pitch usually has no PRJ number yet. Ask for a short project name; use
`PRJ-TBD.NAME` as the folder name until a number is assigned, and note in the
context file that the number is still to be assigned.

The context file is `<PMO folder>/projects/<name>/project-context.md`, where
`<PMO folder>` is the folder holding `Context/Templates/` (normally
`RMG Skills`). Create the folder and seed the file from
`assets/context-template.md` at the plugin root if it does not exist. If you cannot reach that
folder, ask where the project should live rather than inventing a location.

## Step 2 - Requirements brief

There is no separate tool checklist for this gate - the template's own content
is the requirement. All five are hard gates:

| # | Item | Owner |
|---|------|-------|
| 1 | Short description of the project (purpose / context) | Project Owner |
| 2 | Assumptions to be investigated | Project Owner |
| 3 | Strategic fit with the Roularta strategy | Project Owner |
| 4 | Estimated project size / complexity | Project Manager |
| 5 | Proposed Project Sponsor and proposed Project Manager | Project Owner / Head of PMO |

## Step 3 - Collect the content

`fieldmap.json` (next to this SKILL.md) is the authoritative field list, with a label and an
owner per field.

Take what you can from the user's message and any attachments, then ask for the
rest **in one batch**, offering a draft wherever you can write one. Never fill a
field by inference: a plausible sponsor name or a plausible strategic-fit
paragraph is worse than a gap, because it will not get corrected.

Keep it high level. Size / complexity at this stage is a range and a rationale
("roughly 200-300 MD, three systems touched, two external parties"), not a
budget table.

**A small project is under 30 MD** [source: Stijn, 18/09/2026]. The thresholds
for medium and large are not established - ask, do not offer a bracket you made
up. Offering an invented scale is how a wrong number gets confirmed by accident.

## Step 4 - Consistency checks

- **Strategic fit must name a strategic objective**, not just assert that the
  project is useful. If the user's input only says why the project is a good
  idea, flag it: this is the field the pitch is actually judged on.
- **Assumptions must be testable and numbered.** They are the carry-forward to
  the PID, which has to come back with a verdict on each one. An assumption
  phrased as an opinion ("users will like it") is a gap - ask what would be
  measured to test it.
- **Description and assumptions must not contradict each other**: anything stated
  as fact in the description but listed as an assumption below is a
  contradiction. Flag it and ask which it is.
- **Size / complexity must be consistent with the description**: a description
  spanning several systems and countries with a "small" estimate gets flagged.
- **Sponsor and Project Manager**: both must be named people, not roles or
  "TBD". A pitch with no sponsor has nobody to approve the PID.

## Step 5 - Write the context file

Fill the phase 0 section: fields, the numbered assumptions table, open gaps.
When the user confirms the pitch was approved, record the date and approver. Add
`[source: ...]` to each new fact and append a change-log row.

## Step 6 - Build the deck

```bash
python3 "$PLUGIN/scripts/fill_template.py" \
  --map "$PLUGIN/skills/rmg-project-pitch/fieldmap.json" \
  --values "<project folder>/pitch-values.json" \
  --out "<project folder>/<NAME> - PITCH - <yyyy-mm-dd>.pptx"
```

where `$PLUGIN` is this plugin's root folder - the directory two levels above
this SKILL.md, also available as `${CLAUDE_PLUGIN_ROOT}` where that is set. The
official template is named in `fieldmap.json` and resolved relative to it, so
there is no template path to get wrong. Never edit the template in `templates/`
- it is the master copy shared by every project.

`pitch-values.json` has the shape `{"cells": {...}}`. Keep it next to the deck.

Leave out any field you do not have. The script writes
`(MISSING: label -- owner: X -- needed by: Y)` into the cell, which is what makes
an unfinished deck obviously unfinished. Never pass a guess to avoid a marker.

Check the script's JSON report. `missing` is the backbone of the gap report.
`warnings` and `overflow` must be empty - the template's boxes are a fixed
height and do not autofit, so overflowing text is drawn over the box below.
`shrunk` entries are fine but tell you the text is long for the box: if the
font dropped below about 10pt, shorten the text instead of shipping it small.

## Step 7 - Reply

Gap report first:

```
## Blocking (pitch cannot be submitted)
- item -- owner -- needed by

## Needed for the next step (PID)
- item -- owner -- needed by

## Worth confirming
- item -- why it is uncertain
```

Under "needed for the next step", name what the PID will demand that the pitch
does not: a documented business case, an EA pre-check, IT resources and timing
tested, and a verdict on each assumption listed here. That is the value of doing
the pitch properly.

If nothing is missing, say so explicitly. Then one line naming the deck and its
folder. Do not summarise the deck's contents.
