# 07 — Research Software (optional layer)

> Published **after** the six-step core chain. Describes the reusable artefact this
> work produced: the **importable Galaxy melt-pond workflow** (`workflows/
> meltpond_mapping_sentinel2.ga`) — others can import it into any Galaxy and point
> the same threshold → label → count → measure chain at their own Sentinel-2 (or
> other single-band) imagery. `Research Project` back-links to the **Claim URI**
> (step 03). (Same layer the sibling cellprofiler-eo chain published.)

## Form fields (`docs/forrt-form-fields.md` § Research Software)

`URI of published software` (required, full URL) · `Software Title` · `Repository URL` · `Research Project` (optional) · `License` (optional) · `Related Datasets` (optional, repeatable) · `Related Publications` (optional, repeatable)

---

### URI of published software (required) — Zenodo concept DOI

```
https://doi.org/10.5281/zenodo.20943752
```

### Software Title

```
FIESTA — Galaxy melt-pond mapping workflow (off-the-shelf bioimage tools on Sentinel-2)
```

### Repository URL

```
https://github.com/annefou/fiesta-galaxy-meltponds-eo
```

### Research Project (optional) — back-link to the Claim URI (step 03)

```
<paste Claim URI from PUBLISHED.md step 03 after publishing>
```

### License (optional)

```
https://spdx.org/licenses/MIT.html
```

### Related Datasets (optional, repeatable — one URL each)

- Sentinel-2 L2A (input imagery), AWS Open Data: `https://registry.opendata.aws/sentinel-2-l2a-cogs/`
- Glen et al. (2024) lake outlines (validation): `https://doi.org/10.5281/zenodo.11645884`

### Related Publications (optional, repeatable — one URL each)

- The FORRT Outcome this software implements: `<paste Outcome URI from PUBLISHED.md step 05 after publishing>`
- Reused Galaxy training material / method: `https://gxy.io/GTN:T00181`
- Reused image-analysis software (scikit-image): `https://doi.org/10.7717/peerj.453`
- Supraglacial-water detection method (Williamson 2018): `https://doi.org/10.5194/tc-12-3045-2018`
