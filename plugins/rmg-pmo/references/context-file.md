# The project context file

One file per project, at `<PMO folder>/projects/PRJ00xxx.NAME/project-context.md`.
All four gate skills read it and write to it. It is the reason the gates can check
each other instead of each starting from a blank page.

## Rules

1. **Append-only per phase.** Never edit or delete a section belonging to a phase
   that is already approved. If a fact changes after approval, add it to the
   current phase's section and to the change log — do not rewrite history. The
   deviation checks depend on the old numbers still being there.
2. **Frozen blocks.** `### Committed at <PHASE>` blocks are written once, when the
   gate is approved, and never touched again. The PTE reads the PID's block; the
   Closing doc reads the PID's block (and reports the PTE's alongside it).
3. **Every fact carries its source.** `[source: Steerco 12/09/26]`,
   `[source: Stijn]`, `[assumed]`. A fact with no source is treated as assumed
   and shows up under "Worth confirming" in the gap report.
4. **Unknown means unknown.** Write `TBD — owner: <role>` rather than a plausible
   value. Nothing in this file may be inferred: approval chains, thresholds,
   names, lead times and figures come from the user or from an earlier phase.
5. **Dates as dd/mm/yyyy**, money in kEUR unless the template says otherwise,
   effort in MD.

## Skeleton

```markdown
# PRJ00xxx.NAME — project context

- PRJ number:
- Project name:
- Project Owner:
- Project Sponsor:
- Project Manager:
- Current phase:
- internal_md_rate_eur: 910   (year: 2026)
- Last updated:

## Phase 0 — DISCOVER / Project Pitch
Status: not started | draft | submitted | approved dd/mm/yyyy | rejected
Approver: PPM / CIO / Project Owner
Deck:

### Fields
(one bullet per fieldmap key that this gate uses)

### Assumptions to be investigated
| # | Assumption | Raised | Resolved in |
|---|------------|--------|-------------|

### Open gaps at gate
### Remarks

## Phase 1 — INITIATE / PID
Status:
Approver: PMO Board / CEO
Deck:

### Gate checklist
| # | Item | Y/N | Evidence / date | Owner |
|---|------|-----|-----------------|-------|
| 1 | Business req. gedefinieerd | | | |
| 2 | Business case gedocumenteerd en up to date | | | |
| 3 | EA pre-check | | | |
| 4 | IT Resources/timing afgetoetst | | | |
| 5 | PID gecheckt met Project Sponsor | | | |
| 6 | PID gecheckt met Head of PMO | | | |
| 7 | PID gevalideerd op PMO board | | | |

### Fields
### Assumption resolution (from the pitch)
| # | Pitch assumption | Verdict | Evidence |

### Committed at INIT  (FROZEN once approved)
- analysis internal MD:
- analysis internal kEUR:
- analysis external MD / kEUR:
- analysis total MD / kEUR:
- build estimate (range):
- recurring cost after go live:
- benefit KPI(s):
- scope in / out:
- resource commitments confirmed by person + manager: Y/N per resource

### Open gaps at gate
### Remarks

## Phase 2 — ANALYSE / Plan to Execute
Status:
Approver: Steerco / PMO Board / CEO if deviation > 10% vs the PID
Deck:

### Gate checklist
| # | Item | Y/N | Evidence / date | Owner |
|---|------|-----|-----------------|-------|
| 1 | Finale business requirements | | | |
| 2 | Finale business case opgesteld | | | |
| 3 | Finale EA aanbeveling uitgevoerd | | | |
| 4 | IT Resources/Timing afgetoetst | | | |
| 5 | PTE gecheckt met Project Sponsor | | | |
| 6 | PTE gecheckt met Head of PMO | | | |
| 7 | PTE gevalideerd op PMO board | | | |

### Deviation vs PID
| Measure | PID | PTE | Deviation | > 10%? |

### Fields
### Committed at BUILD  (FROZEN once approved)

### Open gaps at gate
### Remarks

## Phase 3 — BUILD
(no gate document; Steerco reporting. Keep scope changes, budget changes and
milestone slippage here so the Closing doc can explain the deviations.)

## Phase 4/5 — GO LIVE - CLOSE / Closing document
Status:
Approver: Steerco / CIO
Deck:

### Fields
### Realisation vs what was promised
| Promised in | KPI / deliverable | Realised | Evidence |

### Open gaps at gate
### Remarks

## Change log
| Date | Phase | What changed | Source |
```
