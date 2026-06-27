# 06 — CiTO Citation

> Closes the core chain. `Identifier for the citing creative work` = the
> **Outcome URI** (step 05). This is a **question-rooted** chain with no original
> paper to confirm/dispute, so the citations **credit** the reused method/software,
> name the detection method, and cite the validation data source (same pattern as
> the sibling cellprofiler-eo chain).

## Form fields (`docs/forrt-form-fields.md` § Citation with CiTO)

`Identifier for the citing creative work` (required) · `List citations` (repeatable, ≥1), each with `Citation Type` (dropdown) + `DOI or other URL`

---

### Identifier for the citing creative work (required)

```
<paste Outcome URI from PUBLISHED.md step 05 after publishing>
```

### List citations

#### Citation 1 — the reused Galaxy training material / method

- **Citation Type:** `credits`
- **DOI or other URL:** `https://gxy.io/GTN:T00181`

> The replication input: the Galaxy Training Network tutorial *"Introduction to
> Image Analysis using Galaxy"* (counts cell nuclei), reused unchanged on melt
> ponds. Cited by its stable PURL — `credits` is the CiTO type for a directly
> reused tutorial (`replicates` is not offered by the platform).

#### Citation 2 — the reused image-analysis software

- **Citation Type:** `credits`
- **DOI or other URL:** `https://doi.org/10.7717/peerj.453`

> scikit-image, the library the Galaxy `imgteam` tools wrap to do the
> thresholding / labelling / measurement.

#### Citation 3 — the supraglacial-water detection method

- **Citation Type:** `usesMethodIn`
- **DOI or other URL:** `https://doi.org/10.5194/tc-12-3045-2018`

> Williamson et al. (2018) — the NDWIice index and the 0.25 threshold used to turn
> the bands into a water mask.

#### Citation 4 — the validation data source (ground truth)

- **Citation Type:** `citesAsDataSource`
- **DOI or other URL:** `https://doi.org/10.5281/zenodo.11645884`

> Glen et al. (2024) — the independently published Sentinel-2 lake outlines the
> detection was benchmarked against.
