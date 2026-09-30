# Resume workstream — 2026-10-01 IST

Roadmap: [#2](https://github.com/utkarshmankad/um-resume-as-a-code/issues/2). Sprint: [#3](https://github.com/utkarshmankad/um-resume-as-a-code/issues/3).

## Inspected state

- Default branch `main`, commit `33445878ebcb8fd5a99e84280307ab0d41b2bf88`.
- [PR #1](https://github.com/utkarshmankad/um-resume-as-a-code/pull/1) already merged 2026-09-28. No duplicate or reversal.
- README documents PRs to main, then manual Build Resume publication after PDF review. No AGENTS.md; no rulesets returned by repository API. No open backlog or PRs before this run.
- [Main CI #36488581340](https://github.com/utkarshmankad/um-resume-as-a-code/actions/runs/36488581340) succeeded. Build, PDF validation, render and artifact upload passed; publish was skipped. Artifact `10999599936` expires 2026-12-27.
- Downloaded that exact main artifact; rendered and inspected both pages. Two A4 pages, readable CM-Super typography, no clipping/overlap, Fynd starts page two, Oracle ends April 2026. This is technical visual inspection, not owner approval of publication or factual claims.
- PR #1 comments/reviews contain no final owner PDF approval. Stale PR description says leave open for PDF review. Do not infer publication approval from its merged state.
- Nine historical releases remain; latest historical release `v19-5-26-TP`. No canonical `latest` release found. No GitHub workflow-dispatch/release-creation connector is exposed.

## Sprint checklist

- [x] Add exact normalized Core Competencies guard before compilation/PDF validation.
- [x] Six local regressions: approved source, harmless rewrap, deleted skill, renamed skill, reordered skill, summary wording change.
- [x] Preserve every .tex/style file; no resume content or layout changes.
- [x] Shell syntax and diff whitespace checks.
- [ ] New draft PR CI build and review bundle verified (update issue #3 with exact run).
- [ ] Review and merge the validation-only PR through normal repo flow after checks.

Local compiler is Tectonic 0.17.0, pypdf 6.10.0. A fresh local compile is blocked by HTTP 403 fetching `https://relay.fullyjustified.net/default_bundle_v33.tar.index.gz`; no cached bundle. Do not claim a fresh local PDF build passed. CI runs the documented build with the new source guards and tests.

## Next action and boundaries

Check draft PR CI, inspect its review artifact, and update #3. Validation-only merge may proceed after CI/review rules; do not edit career content. Obtain owner approval of the exact canonical PDF before publication. Then use the authorized manual workflow with `publish=true`, verify SHA and download, and finalize release notes. Historical cleanup remains deferred until acceptance. Announcement draft: [LAUNCH_DRAFT.md](LAUNCH_DRAFT.md); community rules/duplicate checks and verified release must precede posting.
