# 03 — FORRT Claim

> Links the AIDA to a FORRT claim genre. `Search for an AIDA sentence` = the
> **AIDA URI** (step 02).

## Form fields (`docs/forrt-form-fields.md` § FORRT Claim)

`Short URI suffix as claim ID` · `Label of the claim` · `Search for an AIDA sentence` (required) · `Type of FORRT claim` (dropdown, 7 options) · `Source URI` (optional)

---

### Short URI suffix as claim ID

```
meltpond-offtheshelf-detection
```

### Label of the claim (descriptive title, not a sentence)

```
Off-the-shelf bioimage tools detect supraglacial melt ponds on Sentinel-2 (cross-discipline reuse)
```

### Search for an AIDA sentence (required)

```
<paste AIDA URI from PUBLISHED.md step 02 after publishing>
```

### Type of FORRT claim (dropdown)

```
model performance
```

> **Rationale / choice for Anne.** The claim asserts a *detection-accuracy* result
> (recovers ~88 % of mapped lake area; precision/recall/IoU against an independent
> reference), so `model performance` (accuracy / F1 / evaluation metrics) is the
> right genre — see `docs/claim-type-vocabulary.md`.
>
> Note this **differs from the sibling cellprofiler-eo chain**, which used
> `descriptive pattern` *because it deliberately did not benchmark against a
> reference catalog*. We do have a quantitative benchmark (Glen et al. 2024), which
> is exactly what makes `model performance` appropriate here. If you'd rather frame
> the headline as feasibility-of-transfer rather than accuracy, switch to
> `descriptive pattern` to match the family — your call.

### Source URI (optional, full URL form)

```
https://doi.org/10.5281/zenodo.20943752
```
