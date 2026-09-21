# Changelog

## 0.1.0 — 2026-09-21

First packaged release. Four gate skills: `rmg-project-pitch`, `rmg-pid`,
`rmg-plan-to-execute`, `rmg-project-closing`.

- Fill engine shared at `plugins/rmg-pmo/scripts/fill_template.py` (was duplicated
  per skill). Templates, the context-file spec and the context template are also
  single copies at the plugin root.
- The template is named in each skill's `fieldmap.json` and resolved relative to
  it, so no template path is passed on the command line.
- Known-assumed rules are listed in `docs/decisions/`. The 10% PTE deviation rule
  and the Closing baseline question are both still unconfirmed by the PMO.
