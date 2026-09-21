# RMG PMO gate skills

Claude plugin marketplace for the Roularta Media Group PMO process. Four skills,
one per gate, each producing the same three things: a requirements checklist, the
official PMO deck filled in, and a report of what is missing or inconsistent.

| Skill | Gate | Approver |
|-------|------|----------|
| `rmg-project-pitch` | Phase 0 DISCOVER — Project Pitch | PPM / CIO / Project Owner |
| `rmg-pid` | Phase 1 INITIATE — PID | PMO Board / CEO |
| `rmg-plan-to-execute` | Phase 2 ANALYSE — Plan to Execute | Steerco / PMO Board / CEO if deviation > 10% vs the PID |
| `rmg-project-closing` | Phase 4/5 GO LIVE - CLOSE — Closing document | Steerco / CIO |

## Install

```
/plugin marketplace add <your-github-user>/rmg-pmo-marketplace
/plugin install rmg-pmo@rmg-pmo
```

The repo is private, so anyone installing needs read access to it and a GitHub
account signed in to their machine.

To pick up changes later:

```
/plugin marketplace update rmg-pmo
```

## How the four gates connect

Each project gets one append-only context file, `project-context.md`, in its own
folder. Every skill reads the whole file and writes only its own phase. Approved
figures are frozen in `### Committed at INIT` and `### Committed at BUILD` blocks.

That is what makes the cross-gate checks possible:

- the **PID** must give a verdict on every assumption the **pitch** raised, and
  flags scope that grew since the pitch
- the **PTE** measures its build figures against what the **PID** committed and
  states whether the 10% rule puts it in front of the CEO
- the **Closing** document builds its deliverables table from what the PID and
  PTE committed, not from memory, and compares spend against the PID baseline

## Layout

```
.claude-plugin/marketplace.json     marketplace manifest
plugins/rmg-pmo/
  .claude-plugin/plugin.json        plugin manifest
  skills/<skill>/SKILL.md           one folder per gate
  skills/<skill>/fieldmap.json      which field goes in which template cell
  skills/<skill>/evals.json         test prompts, including an incomplete case
  templates/*.pptx                  master copies of the official PMO templates
  scripts/fill_template.py          the fill engine, shared by all four skills
  assets/context-template.md        skeleton for a new project context file
  references/context-file.md        the context file spec
docs/pmo-process.md                 how the four gates actually work
docs/decisions/                     what was decided, and what is still assumed
docs/team-input/                    corrections from the people who run the process
```

## Changing a skill

1. Edit under `plugins/rmg-pmo/`, on a branch.
2. Re-run the eval prompts in `skills/<skill>/evals.json`, including the
   deliberately incomplete case — the gap report is the part most likely to break.
3. Append to `docs/decisions/` with what changed and what prompted it. An entry
   that is not confirmed by the PMO is marked `Status: assumed`.
4. Bump the version in **both** manifests, add a `CHANGELOG.md` entry, and merge.

Editing a template in `templates/` affects every project that has not yet been
approved. Check `docs/decisions/` for the cell coordinates a fieldmap depends on
before changing a template's structure — the fieldmaps address cells by position.

## What is still unconfirmed

Listed in full in `docs/decisions/`. The two that matter most:

- **The 10% deviation rule is not measurable as written.** The PID commits a
  range, the PTE commits a point; the same figures can read as +6.9% or +23.9%.
  The skill reports every reading and escalates the ambiguity rather than picking
  one. Needs a ruling from the Head of PMO.
- **The Closing document's "Committed Resources / INIT" column** is assumed to
  mean the PID figures, not the PTE's.

## Live project data

Per-project folders are deliberately **not** in this repo — see `.gitignore`.
They hold real budgets, names and board decisions. They live in the Cowork
folder next to the generated decks.
