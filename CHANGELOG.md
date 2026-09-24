# Changelog

## 0.1.1 — 2026-09-24

Fixes the skills failing in a session that has no connection to the PMO folder.
Nothing was missing from the plugin — the instructions sent Claude to the wrong
place to look for it.

- The skills now locate the plugin with a discovery command and state that the
  engine runs in the session's own shell. The installed plugin lives in the
  session workspace; the shell that reaches a user's connected folders cannot
  see it, which is why the deck could not be generated.
- The context file no longer has to live in a folder called `RMG Skills`. It goes
  in whichever folder is connected, or in the session itself, in which case the
  skill delivers it to the chat and says to keep it.
- The three later gates now stop and ask for the context file when it is absent,
  instead of proceeding without the baseline they are supposed to check against.

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
