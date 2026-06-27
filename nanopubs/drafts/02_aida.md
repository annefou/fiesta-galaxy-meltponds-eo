# 02 — AIDA Sentence

> The atomic, declarative answer to the PICO question. Ends with a full stop.
> `Relates to this nanopublication` = the **PICO URI** (step 01).

## Form fields (`docs/forrt-form-fields.md` § AIDA sentence)

`AIDA sentence` (required, ends with full stop) · `Select related topics/tags` (optional) · `Relates to this nanopublication` (required) · `Supported by datasets` (optional, repeatable) · `Supported by other publications` (optional, repeatable)

---

### Enter your AIDA sentence here (ending with a full stop)

```
The off-the-shelf Galaxy bioimage-analysis workflow, reused without modification from cell-nuclei counting, detects supraglacial melt water on Sentinel-2 imagery of the Greenland ice sheet and recovers about 88 percent of the area of independently mapped supraglacial lakes for the same location and melt season.
```

> Atomic check: one empirical finding (the reused workflow detects melt water and
> recovers ~88% of mapped lake area). The over-counting / precision caveat is NOT
> in the AIDA — it belongs in the Outcome's *limitations*.

### Select related topics/tags (dropdown, optional)

```
remote sensing; image segmentation; glaciology
```
*(pick whatever the platform vocabulary actually offers that is closest)*

### Relates to this nanopublication (required)

```
<paste PICO URI from PUBLISHED.md step 01 after publishing>
```

### Supported by datasets (optional, repeatable)

- Glen et al. (2024), supraglacial meltwater-feature outlines (ground truth): `https://doi.org/10.5281/zenodo.11645884`
- Sentinel-2 L2A scene S2A_22WEV_20190723 (input), AWS Open Data: `https://registry.opendata.aws/sentinel-2-l2a-cogs/`

### Supported by other publications (optional, repeatable)

- Williamson et al. (2018), NDWIice supraglacial-lake method: `https://doi.org/10.5194/tc-12-3045-2018`

> ⚠️ **Platform bug note** (`docs/forrt-form-fields.md` § AIDA): populating *both*
> "Supported by datasets" AND "Supported by other publications" has previously made
> Science Live fail at publish. If it errors, either (a) move Williamson 2018 into
> *datasets* and leave *publications* empty, or (b) publish this AIDA via Nanodash
> (URI becomes `w3id.org/np/…`). The sibling cellprofiler-eo chain did populate both
> successfully, so try as-is first.
