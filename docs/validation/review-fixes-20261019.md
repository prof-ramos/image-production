# Focused PR review fixes — 19 October 2026

The two findings against `5990fc9` were reproduced before changing production code:

- A stored `{"criteria": {}}` review allowed another variant's review to approve the run.
- Invalid stored reviews/history were accepted by CLI commands; a null history could also raise an unstructured exception.
- With umask `022`, the manifest temporary existed with mode `0644` before writing completed and before chmod.

Loading now applies the existing review validator to stored reviews and history, including required criteria for the run. Missing history remains supported; null history and null historical entries are rejected. Pending current reviews remain supported. Manifest bytes are unchanged on these failures, and CLI failures use JSON stderr and exit code 2.

The manifest temporary is now opened exclusively with mode `0600` before any content is written. Existing confinement checks, atomic replacement, final mode and temporary cleanup remain in place.

## Verification

Sequential offline checks on macOS ARM64, Python 3.12.15, Pillow 12.3.0:

```sh
uv run --offline --with-requirements requirements-dev.txt python -m unittest discover -s tests -v
```

24 tests passed (1.679 seconds in the recorded run). The three added tests cover the two-variant approval reproduction, six corrupt stored-review/history cases across verify/status/review, and real temporary permissions at creation under umask `022`. All new regression cases were observed failing before their fixes.

The official Skill Creator `quick_validate.py` reported `Skill is valid!`; `git diff --check` passed. The existing resume-without-original-source and confinement tests also passed.

These checks use tiny synthetic fixtures. No integrated image generation or functional/visual homologation was performed. The pending cases in issue #2 remain pending; this patch does not approve image artifacts or request a merge.
