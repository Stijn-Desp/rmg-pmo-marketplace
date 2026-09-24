---
name: rmg-plan-to-execute
description: >
  Prepares everything needed for the RMG PMO Plan to Execute gate (phase 2 -
  ANALYSE): the requirements checklist, a prefilled PROJECT PLAN TO EXECUTE deck
  from the official PMO template, the deviation check against what the PID
  committed, and a report of what is missing or inconsistent. Use this whenever
  someone mentions PTE, Plan to Execute, plan van uitvoering, the ANALYSE phase,
  the conclusion of the analysis, the final business case or final EA
  recommendation, the build budget or build planning, moving from analysis to
  build, or asks whether the deviation versus the PID needs CEO approval.
---

# RMG Plan to Execute (phase 2 - ANALYSE)

Approver: **Steerco / PMO Board / CEO if the deviation is more than 10% versus
the initial request in the PID**. Key output: **approved Project Plan to
Execute**. Next phase: BUILD, steered through the Steerco.

Produce three things, in this order, every time:

**A. Requirements brief** - the fixed checklist below.
**B. Prepared deck** - the official template filled in, with a visible marker
wherever a field could not be filled.
**C. Gap report** - short and prioritised, at the very top of the reply, with the
deviation verdict at the top of it.

## Step 1 - Find the project and its context file

Ask for `PRJ00xxx.NAME` if not given. The context file is
`<project folder>/project-context.md`.

Put it in, in order of preference: a folder the user has connected to this
session that already holds this project or a `projects/` directory; a connected
folder the user names; or, if no folder is connected, this session's own
workspace - in which case deliver the context file to the chat alongside the deck
and tell the user to keep it, because the next gate reads it.

Never require a particular folder name, and never invent a location - ask if it
is ambiguous.

Read the **whole** file. The `### Committed at INIT` block from phase 1 is a
required input to this gate.

If there is no context file in this session - a new session, or the project
folder is not connected - ask the user to attach it or paste it before going
further. Do not reconstruct an earlier phase's figures from memory: the whole
point of the cross-gate checks is that they compare against what was actually
committed. If there is no PID section, or that block is empty,
say so plainly: the deviation check cannot be run and that is itself a finding -
do not substitute the PTE's own numbers as the baseline.

## Step 2 - Requirements brief

Every item is a hard gate:

| # | Item | Owner | Realistic lead time |
|---|------|-------|--------------------|
| 1 | Finale business requirements | Project Owner | TBD |
| 2 | Finale business case opgesteld | Business Controlling | TBD |
| 3 | Finale EA aanbeveling uitgevoerd | Enterprise Architecture | TBD |
| 4 | IT Resources/Timing afgetoetst | IT | TBD |
| 5 | PTE gecheckt met Project Sponsor | Project Manager | TBD |
| 6 | PTE gecheckt met Head of PMO | Project Manager | TBD |
| 7 | PTE gevalideerd op PMO board | Head of PMO | TBD |

Lead times are not documented. Print `TBD` - do not estimate. Report each item
as **Y**, **N** or **not stated**; "not stated" is a gap.

Also check, from the phase's key activities: was the **Steerco installed** during
ANALYSE? The PTE names the Steerco as an approver, so a project reaching this
gate without one is blocked.

## Step 3 - The deviation check

This is the most important thing this skill does. Build this table from the
context file and the new figures:

| Measure | PID (committed at INIT) | PTE | Deviation | > 10%? |
|---------|------------------------|-----|-----------|--------|
| Total spend (internal kEUR + external kEUR) | | | | |
| Internal MD | | | | |
| External kEUR | | | | |
| Build estimate (PID range) vs total BUILD | | | | |

The rule in the template says CEO / PMO Board approval is needed if the
deviation is more than 10% versus the initial request in the PID, without saying
deviation of what. This skill measures it on **total project spend** and reports
MD separately. That reading is recorded as *assumed* in `decisions/` - if the
user says otherwise, follow them and note that the decision log needs updating.

**When the PID committed a range** (the build estimate normally is one, e.g.
"180-240 MD internal plus 60-90 kEUR external"), the verdict can flip depending on
which point of the range you measure against, so measure against **all three** and
show them. Report the verdict on the top of the range, because that is the largest
figure the PMO Board actually approved, and name the midpoint result underneath.
If the two readings disagree about whether the 10% threshold is crossed, say so
explicitly and let the Head of PMO decide - do not pick the reading that avoids
the escalation.

Worked example: PID build estimate 180-240 MD internal + 60-90 kEUR external
= 223.8-308.4 kEUR at 910 EUR/MD. A PTE landing on 329.8 kEUR is **+6.9% versus
the top of the range** but **+23.9% versus the midpoint** - one reading needs only
the Steerco, the other needs the CEO. That case must be handed to the Head of PMO,
not resolved silently.

State the verdict in one line, first thing in the gap report:

> Deviation +18% on total spend (PID 85 kEUR -> PTE 100 kEUR): **CEO / PMO Board
> approval required** on top of Steerco approval.

or

> Deviation +4% on total spend: Steerco approval is sufficient.

If the PID baseline is missing, write: **deviation cannot be established -
baseline missing from the PID**. Never report a deviation of 0% when the baseline
is simply absent.

## Step 4 - Collect the content

`fieldmap.json` (next to this SKILL.md) is the authoritative field list, with a label and an owner
per field.

Carry forward description, strategic fit and general objective from the PID
rather than asking again - but show the user what you carried forward, because
the analysis may have changed them. Ask for the genuinely new material in one
batch: the conclusion of the analysis, the final scope, the build resources, the
build milestones, the updated benefits, the current risks.

Resource figures: ask for **man-days per team** (IT, Cycles, PMO, other RMG) and
the external MD and kEUR. Do not compute kEUR or totals - `fill_template.py`
derives them from the rate in the context file.

## Step 5 - Consistency checks

**Against the PID**
- The deviation table above.
- Scope: list every difference between the PID's in/out of scope and the PTE's
  final scope. Scope that grew without the budget growing, or a budget that grew
  without the scope changing, both get flagged.
- Benefits: if the business case KPI moved versus the PID, say by how much. A
  benefit that shrank while the cost grew is the finding the Steerco most needs.
- Recurring cost after go live: flag any change versus the PID.
- Organization: flag every change of Sponsor, Product Manager, Product Owner or
  Project Manager since the PID.
- Risks: any PID risk that has disappeared from the PTE without being resolved is
  a gap - it either materialised, was mitigated, or was forgotten. Say which.
- Build milestones: compare against the high-level build milestones in the PID.
  Flag slippage of the go-live date.

**Inside the PTE**
- The conclusion of the analysis must cover all four parts the template asks for:
  the essence of the analyses performed, the additional certainties and insights
  gained, the architectural impact together with Enterprise Architecture, and the
  remaining uncertainties with how they will be handled during BUILD. Name any
  part that is missing - a conclusion missing the remaining uncertainties is the
  most common weak spot.
- Final scope: in and out both filled. "Final" means no open questions left in
  it; flag any hedging language.
- Every quantitative benefit is a KPI with a number and a baseline, validated by
  Controlling.
- Build milestones: every row has a start and an end date, dates chronological,
  and the go-live date present.
- Risks: at least one, each with probability, impact and mitigation.
- Every internal resource must be committed by the person **and** their manager.
  Planning built on uncommitted people is the classic slippage cause and the
  template says so explicitly.
- Steerco and stakeholder group listed for the BUILD phase.

## Step 6 - Write the context file

Update the phase 2 section: gate checklist with evidence, the deviation table,
fields, open gaps. When the user confirms the PTE was approved, fill
`### Committed at BUILD` and freeze it. Do not touch the phase 1 section - append
a change-log row instead.

## Step 7 - Build the deck

```bash
python3 "$PLUGIN/scripts/fill_template.py" \
  --map "$PLUGIN/skills/rmg-plan-to-execute/fieldmap.json" \
  --values "<project folder>/pte-values.json" \
  --out "<project folder>/PRJ00xxx.NAME - PTE - <yyyy-mm-dd>.pptx"
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

`pte-values.json` has the shape `{"meta": {"internal_md_rate_eur": 910},
"cells": {...}, "tables": {...}}`. Keep it next to the deck.

Leave out any field you do not have; the script writes
`(MISSING: label -- owner: X -- needed by: Y)` into the cell. Never pass a guess
to avoid a marker.

Check the script's JSON report. `missing` is the backbone of the gap report.
`warnings` and `overflow` must be empty - the template's boxes are a fixed
height and do not autofit, so overflowing text is drawn over the box below.
`shrunk` entries are fine but tell you the text is long for the box: if the
font dropped below about 10pt, shorten the text instead of shipping it small.

## Step 8 - Reply

Deviation verdict first, then:

```
## Blocking (PTE cannot go to the Steerco / PMO Board)
- item -- owner -- needed by

## Needed for the next step (BUILD and the first Steerco)
- item -- owner -- needed by

## Worth confirming
- item -- why it is uncertain
```

If nothing is missing, say so explicitly. Then one line naming the deck and its
folder. Do not summarise the deck's contents.
