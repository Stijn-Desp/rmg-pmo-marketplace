# RMG PMO process — the four gates

Distilled from the official templates in `Context/Templates/` and the phase
checklists in `Context/Requirements per phase/`. Everything marked **(assumed)**
still needs confirmation — see `decisions/2026-09-pmo-gate-skills.md`.

## Phase model

The phase ribbon on every template cover slide reads:

`0 DISCOVER → 1 INITIATE → 2 ANALYSE → 3 BUILD → 4 GO LIVE (- NAZORG) → 5 OPERATIONS`

Four of the six phases end in a document gate. BUILD has no document gate of its
own; it is steered through the recurring Steerco (see `Context/Templates/Template
Steerco.pptx`, no skill built yet).

| # | Phase | Gate document | Key output | Approver (from the template) |
|---|-------|---------------|-----------|------------------------------|
| 0 | DISCOVER | Project Pitch | Approved Project Pitch | PPM / CIO / Project Owner |
| 1 | INITIATE | PID | Approved PID | PMO Board / CEO |
| 2 | ANALYSE | Plan to Execute (PTE) | Approved Project Plan to Execute | Steerco / PMO Board / CEO **if deviation > 10% vs the initial request in the PID** |
| 3 | BUILD | (Steerco reporting) | — | Steerco |
| 4/5 | GO LIVE - CLOSE | Closing document | Closing document | Steerco / CIO |

## Phase 0 — DISCOVER → Project Pitch

**Purpose (template):** discover and screen opportunities or threats; a first test
of whether this becomes a project on the roadmap.

**Key activities:** high-level description of the context; test against Roularta's
strategic objectives; high-level estimate of complexity and size.

**Document content:** short description (purpose / context), assumptions to be
investigated, strategic fit, estimated project size / complexity, proposed
Project Sponsor and proposed Project Manager.

No separate tool checklist is known for this gate. **(assumed: the template's own
content is the whole requirement.)**

The *assumptions to be investigated* are the important carry-forward: the PID has
to come back and say what happened to each of them.

## Phase 1 — INITIATE → PID

**Purpose (template):** create support for the project, so the work needed to
reach a given project result is understood *before* the spend is committed.

**Key activities:** start a limited project team (kick off); test a number of
assumptions; work out objectives and expected benefits; business case with
assistance / validation via Controlling; resources with assistance / validation
via IT; architectural check; map feasibility and risks; plan deliverables;
stakeholders; further project approach; monitor & control.

**Gate checklist** (from `Context/Requirements per phase/PID.png`, all mandatory):

1. Business req. gedefinieerd
2. Business case gedocumenteerd en up to date
3. EA pre-check
4. IT Resources/timing afgetoetst
5. PID gecheckt met Project Sponsor
6. PID gecheckt met Head of PMO
7. PID gevalideerd op PMO board

**Document content:** project description / strategic fit; general objective
(SMART) + integration in organization + follow-up KPIs; scope in/out with
geography (BE / NL / BENE); expected benefits (quantitative-financial,
recurring cost after go live, qualitative); project resources (build estimate as
a range + a detailed ANALYSIS table); planning (analysis milestones + high-level
build milestones); organization (sponsor, product manager, product owner, project
manager, Steerco, project team, stakeholder group); DPIA & EA impact; main risks;
approval box.

**Resources rules from the template note:**
- Internal MD price **2026: 910 € / MD** for profiles inside IT DEV, Cycles and
  PMO (the people who do time registration in JIRA).
- Effort of other internal project resources must also be mapped but is **not
  charged financially** to the project — it goes under "other RMG".
- **Every internal resource requested must be committed in advance by the person
  themselves and by their manager**, in particular for building the planning.

**DPIA is required when:** automated evaluation / profiling of an individual's
personal aspects; processing of sensitive data (biometric, data collected from
third parties, health, income, behaviour, preferences and interests, location or
movements, private activities, sensor data, telephony/internet or other
communication data); systematic monitoring of public spaces; matching or merging
of datasets containing personal data. Contact for questions or help: **Peter Thiers**.

## Phase 2 — ANALYSE → Plan to Execute

**Purpose (template):** acquire detailed insight leading to a well-founded,
supported and efficient realisation.

**Key activities:** restart the (adjusted) project team — kick off; **install the
Steerco**; business and functional analysis; architectural check; determine final
scope; determine the plan of execution / methodology; determine concrete
deliverables and timing; refine project budget / required means; sharpen the
business case and KPIs; proof of concept; monitor & control.

**Gate checklist** (from `Context/Requirements per phase/PTE.png`, all mandatory):

1. Finale business requirements
2. Finale business case opgesteld
3. Finale EA aanbeveling uitgevoerd
4. IT Resources/Timing afgetoetst
5. PTE gecheckt met Project Sponsor
6. PTE gecheckt met Head of PMO
7. PTE gevalideerd op PMO board

**Document content:** description / strategic fit; general objective + final
scope; overall conclusion of the analysis; expected benefits; project resources
(BUILD table); high-level build planning; organization for BUILD; main risks;
approval box.

The conclusion of the analysis must cover four things per the template: the
essence of the analyses performed (analysis documents as annex); which additional
certainties and insights were gained and how they contribute to the success of
the project result; the architectural impact (together with Enterprise
Architecture); the remaining uncertainties and how they will be handled during
BUILD.

**The 10% rule:** the approver row says CEO / PMO Board approval is needed *if the
deviation is more than 10% versus the initial request in the PID*. This is the
single most important automated check in the PTE skill. **(assumed: the deviation
is measured on the total committed project spend — internal kEUR + external kEUR
— rather than on MD or on the build estimate alone.)**

## Phase 4/5 — GO LIVE - CLOSE → Closing document

**Purpose (template):** validate the delivered project result and anchor it in the
operational organization.

**Key activities:** are the necessary arrangements made with the IT Service Desk —
incident flow, contact persons internal/external, SLA available; follow up the
(first) operational results of the project implementation; confirmation that the
project delivers the desired result — closing meeting; adjust where needed,
aftercare; communication to the organization; approach for the post-project review.

**Document content:** evaluation of initial objectives / deliverables (deliverable,
realised Y/N + date, comment) + realisation of quantitative and qualitative
benefits; evaluation of project resources (committed at INIT vs spend vs
difference); validation of the project result by Business, I.T., EA and other
stakeholders; how the result is integrated in the organization + follow-up KPIs.

The "Committed Resources / INIT" column means the figures **as approved in the
PID**, not the later PTE figures. That is why the context file freezes the PID
numbers. **(assumed — worth confirming with Head of PMO.)**

No separate tool checklist is known for this gate. **(assumed: the template's own
content plus the IT Service Desk arrangements listed under key activities are the
requirement.)**

## Naming and storage

- Projects are identified as `PRJ00xxx.NAME` (from the template cover slides).
- Per-project working folder: `projects/PRJ00xxx.NAME/` inside this folder,
  holding `project-context.md` and the generated decks.
- Generated decks: `PRJ00xxx.NAME - <GATE> - <yyyy-mm-dd>.pptx`.
