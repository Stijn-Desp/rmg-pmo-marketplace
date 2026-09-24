---
name: rmg-pid
description: >
  Prepares everything needed for the RMG PMO PID gate (phase 1 - INITIATE):
  the requirements checklist, a prefilled PROJECT INITIATION DOCUMENT deck from
  the official PMO template, and a report of what is still missing or
  inconsistent. Use this whenever someone mentions PID, Project Initiation
  Document, the INITIATE phase, going to the PMO Board or PMO board validation,
  what is needed before the PID, EA pre-check, or the analysis-phase resource
  estimate - including when they only ask for the deck, only for the checklist,
  or only to add one section to an existing PID.
---

# RMG PID (phase 1 - INITIATE)

Approver: **PMO Board / CEO**. Key output: **approved PID**. Next gate: the Plan
to Execute at the end of ANALYSE.

Produce three things, in this order, every time:

**A. Requirements brief** - the fixed checklist below, with what is present and
what is not.
**B. Prepared deck** - the official template filled in, with a visible marker
wherever a field could not be filled.
**C. Gap report** - short and prioritised, at the very top of the reply.

## Step 1 - Find the project and its context file

Ask for the PRJ number and name if not given (`PRJ00xxx.NAME`).

The context file is `<project folder>/project-context.md`.

Put it in, in order of preference: a folder the user has connected to this
session that already holds this project or a `projects/` directory; a connected
folder the user names; or, if no folder is connected, this session's own
workspace - in which case deliver the context file to the chat alongside the deck
and tell the user to keep it, because the next gate reads it.

Never require a particular folder name, and never invent a location - ask if it
is ambiguous. If the project folder does not exist, create it and seed the
context file from `assets/context-template.md` at the plugin root. If you cannot reach that folder,
say so and ask where the project lives - do not invent a location.

Read the **whole** context file, not just the PID section. Phase 0 is an input
to this gate.

If there is no context file in this session - a new session, or the project
folder is not connected - ask the user to attach it or paste it before going
further. Do not reconstruct an earlier phase's figures from memory: the whole
point of the cross-gate checks is that they compare against what was actually
committed.

## Step 2 - Requirements brief

Every item is a hard gate: without it the PID does not go to the PMO Board.

| # | Item | Owner | Realistic lead time |
|---|------|-------|--------------------|
| 1 | Business req. gedefinieerd | Project Owner | TBD |
| 2 | Business case gedocumenteerd en up to date | Business Controlling | TBD |
| 3 | EA pre-check | Enterprise Architecture | TBD |
| 4 | IT Resources/timing afgetoetst | IT | TBD |
| 5 | PID gecheckt met Project Sponsor | Project Manager | TBD |
| 6 | PID gecheckt met Head of PMO | Project Manager | TBD |
| 7 | PID gevalideerd op PMO board | Head of PMO | TBD |

Lead times are not documented yet. Print `TBD` - do not estimate them. If the
user states one, record it in the context file and mention that it should be
added to `decisions/`.

Report each item as **Y**, **N**, or **not stated**. "Not stated" is a gap, not
a pass.

## Step 3 - Collect the content

`fieldmap.json` (next to this SKILL.md) is the authoritative field list: every key under `cells`
and `tables` has a `label` and an `owner`. Work from it rather than from memory.

Take what you can from the context file, the user's message and any attachments.
Then ask for the rest **in one batch**, with a proposed draft for anything you
can draft (a SMART objective from a rough goal, a risk from something the user
mentioned in passing). Reacting to a draft is easier than answering a blank
question. Never fill a field by inference - a plausible sponsor name or a
plausible KPI is worse than a gap, because it will not get corrected.

Resource figures: ask for **man-days per team** (IT DEV, Cycles, PMO, other RMG)
and for the external MD and kEUR. Do not compute kEUR or totals yourself -
`fill_template.py` does that from the rate in the context file (910 EUR/MD for
2026), so the deck's arithmetic is always internally consistent.

## Step 4 - Consistency checks

Run all of these and report every failure in the gap report.

**Against phase 0 (the pitch)**
- Each *assumption to be investigated* from the pitch must have a verdict in the
  PID (confirmed / rejected / still open). List any assumption with no verdict.
- Scope: if the PID's in-scope is wider than the pitch's description, say so
  explicitly - silent scope growth between pitch and PID is a known failure mode.
- The pitch's proposed Sponsor and Project Manager versus the PID's organization
  table: flag any change.
- The pitch's estimated size / complexity versus the PID's analysis + build
  figures: flag an order-of-magnitude mismatch.

**Inside the PID**
- General objective: check it is genuinely SMART. Name the missing letters
  (measurable without a number, no time frame, and so on).
- Every benefit claimed in "quantitative / financial benefits" must be a KPI with
  a number and a baseline. A benefit with no number is a gap.
- Every follow-up KPI must have an owner after go live.
- Recurring cost after go live must be answered, including "none" - a blank here
  reads as not checked.
- Scope: both in-scope and out-of-scope must be filled, and the geography
  (BE / NL / BENE) must be set and consistent with the per-row geography.
- Milestones: analysis milestones present; at least high-level build milestones
  present; every row has a start and an end date; dates chronological; the
  analysis milestones must include reaching the PTE, because that is this
  project's next gate.
- Risks: at least one risk, each with probability, impact and a mitigation. A
  risk with no mitigation is a gap.
- DPIA: must be answered yes or no with a reason. If the project description
  mentions personal data, profiling, sensitive data, monitoring of public spaces
  or the merging of datasets with personal data, and the DPIA answer is "no" or
  missing, flag it as blocking and point at Peter Thiers.
  `dpia-triggers.md` (next to this SKILL.md) has the full list of triggers.
- EA impact must be the conclusion of the pre-architectural checklist, not a
  promise to do one.
- Every internal resource in the project team must be confirmed as committed by
  the person **and** their manager. Any resource without that double commitment
  is a gap - the template says so explicitly and planning built on uncommitted
  people is the classic slippage cause.
- Organization: Sponsor, Product Manager, Product Owner and Project Manager must
  all be named. Steerco and stakeholder group must be listed.

## Step 5 - Write the context file

Update the phase 1 section: the gate checklist with evidence, the fields, the
assumption resolution table, the open gaps. When the user confirms the PID was
approved, fill `### Committed at INIT` and treat it as frozen from then on - the
PTE deviation check and the Closing document both read it.

Append a change-log row for anything you changed. Add `[source: ...]` to each new
fact.

## Step 6 - Build the deck

```bash
python3 "$PLUGIN/scripts/fill_template.py" \
  --map "$PLUGIN/skills/rmg-pid/fieldmap.json" \
  --values "<project folder>/pid-values.json" \
  --out "<project folder>/PRJ00xxx.NAME - PID - <yyyy-mm-dd>.pptx"
```

where `$PLUGIN` is this plugin's root folder. Find it first, in **this session's
own shell** (the Bash tool):

```bash
PLUGIN=$(dirname "$(dirname "$(find ~/.claude/plugins -name fill_template.py -path '*rmg-pmo*' | head -1)")")
```

The installed plugin lives in this session's workspace. A shell that reaches the
user's connected folders on their computer cannot see it, so run the fill in the
session's own shell and copy the finished deck to the project folder afterwards.
If that command returns nothing, say the plugin files cannot be found and stop -
never rebuild the official template by hand.

The template is named in `fieldmap.json` and resolved relative to it, so there is
no template path to pass. Never edit the template in `templates/` - it is the
master copy shared by every project.

`pid-values.json` has the shape `{"meta": {"internal_md_rate_eur": 910},
"cells": {...}, "tables": {...}}`. Keep it next to the deck - it is how the next
revision is produced without retyping everything.

Leave out any field you do not have. The script writes
`(MISSING: label -- owner: X -- needed by: Y)` into the cell, which is what makes
an unfinished deck obviously unfinished on screen. Never pass a guess to avoid a
marker, and never hand-edit the template in another way.

Check the script's JSON report. `missing` is the backbone of the gap report.
`warnings` and `overflow` must be empty - the template's boxes are a fixed
height and do not autofit, so overflowing text is drawn over the box below.
`shrunk` entries are fine but tell you the text is long for the box: if the
font dropped below about 10pt, shorten the text instead of shipping it small.

## Step 7 - Reply

Gap report first, in this format:

```
## Blocking (PID cannot go to the PMO Board)
- item -- owner -- needed by

## Needed for the next step (Plan to Execute)
- item -- owner -- needed by

## Worth confirming
- item -- why it is uncertain
```

If nothing is missing, say so explicitly. Silence reads as "not checked".

Then one line naming the deck and the folder it is in, and the checklist table.
Do not summarise the deck's contents - the user can open it.
