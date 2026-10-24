# Published nanopub chain — URI registry

This file is the canonical registry of published nanopub URIs for this replication. Update it as you publish each step.

**Chain shape:** question-rooted, method-reuse (PICO anchor — no upstream paper to
confirm/dispute; we reuse the GTN tutorial `gxy.io/GTN:T00181` cross-discipline).
Published 2026-10-24 on `https://platform.sciencelive4all.org` through the chain
wizard, from `nanopubs/chain-draft.json` (built from `drafts/`). Outcome repository:
release v0.1.0, version DOI [10.5281/zenodo.20943837](https://doi.org/10.5281/zenodo.20943837).

## Chain

| Step | Template | URI | Published |
|---|---|---|---|
| 01 | PICO Research Question | https://w3id.org/sciencelive/np/RAr8yNJMJ5_mHhXz726OUO7CAZskPKfeFs2TGROHIlvTo | 2026-10-24 |
| 02 | AIDA Sentence | https://w3id.org/sciencelive/np/RAzrEtOaQXSVKoX2ee6IHQAPBGvdhC_3AloLvxCkz1wDg | 2026-10-24 |
| 03 | FORRT Claim | https://w3id.org/sciencelive/np/RA4U43eT7l8C72nVwVQFAKajzMb9LBQQmWBKSl_CtmyPg | 2026-10-24 |
| 04 | FORRT Replication Study | https://w3id.org/sciencelive/np/RA_gj6eWwBKH2gMv-wufc48XbkhnK7hoNjdJOM1WaMHVA | 2026-10-24 |
| 05 | FORRT Replication Outcome | https://w3id.org/sciencelive/np/RAWPGEnaMCG_wvmHo7d-1i3-LgWeU9GykotMQpDLBk7y0 | 2026-10-24 |
| 06 | CiTO Citation | https://w3id.org/sciencelive/np/RAMfb27eg4pBtsPq5HkD0UniVimeunT0xyi1S4uMd1VdQ | 2026-10-24 |

## Optional layers

| Step | Template | URI | Published |
|---|---|---|---|
| 07 | Research Software | not applicable (the repo reuses existing tools; it is not a reusable software product) | |

## Format

URIs from Science Live are of the form `https://w3id.org/sciencelive/np/RA…`. URIs from Nanodash (used as a fallback when the Science Live UI hits a bug) are of the form `https://w3id.org/np/RA…`. Both are valid and citable.

If a URI is not in the Science Live namespace, view it via the Science Live viewer by wrapping the URI:

```
https://platform.sciencelive4all.org/np/?uri=<full-URI>
```

## Cross-references

- Drafts: `nanopubs/drafts/`
- Form structure: `docs/forrt-form-fields.md`
- Chain shape decision: `docs/chain-decision-tree.md`
