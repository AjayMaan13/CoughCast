# CLAUDE.md — rules for AI assistants in this repo

CoughCast: wheeze and cough detection from audio, research prototype. The owner (Ajay) builds it to learn signal processing and to show the work in interviews. He must be able to explain every line.

## Never

- Never run git commands that change history or the remote: no `git add`, `git commit`, `git push`, `git reset`, `git checkout`, `git rebase`, `git stash`, and no `gh`. Read-only git (`git status`, `git diff`, `git log`) is fine.
- Never write a number into README.md, docs/, or any text meant for people. Use `[ ]` blanks. Numbers come from files in `results/`, and Ajay copies them in himself.
- Never download datasets. Write the script; Ajay runs it.
- Never delete or modify anything in `data/`.
- Never install packages outside the project's virtual environment.
- Never add features, files, or abstractions that weren't asked for.

## Always

- Read the current phase in `coughcast-build-plan.md` before starting work.
- Make one small change per request. Say which files you changed.
- Write a test for every function that does maths or splits data. Use synthetic data in tests, never real recordings.
- Run `pytest -q` after a change and show the output.
- Keep functions short (aim under 30 lines). Prefer plain functions to classes.
- Fix every random seed (`random`, `numpy`, `torch`) at 0 unless told otherwise.
- Fit scalers, thresholds, and hyperparameters on train or validation data only. Test data is used once per model.
- Split by patient (ICBHI), by fold (ESC-50), or by recording (COUGHVID). Never random rows when a group exists.
- When explaining, be short and concrete. If asked "why", give the reason in plain words first, then the detail.

## Not in scope unless the plan's Stretch section is reached

Docker, databases, cloud, experiment trackers, config frameworks, CI, ONNX, pretrained audio models, Grad-CAM, mobile apps.

## Machine

MacBook Air M1, 8 GB RAM. Use `mps` if available, else CPU. Keep models small. Cache features to `.npz` instead of recomputing. Use `num_workers=0` if data loading hangs.

## Honesty

This is a research prototype, not a medical device. Never describe results as clinical, diagnostic, or pediatric. Synthetic nights and simulated weeks are always labelled as such.
