# 01 — PICO Research Question (question-rooted chains, comparative)

> Use this draft instead of `01_quote.md` if your chain is question-rooted with a clear comparator (X vs Y). For descriptive/scoping question-rooted chains, use `01_pcc.md`. See `docs/chain-decision-tree.md`.
>
> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **After choosing the chain shape, delete the two step-1 alternates you aren't using.** Once you've decided this chain is question-rooted-comparative and keep `01_pico.md`, run:
> ```bash
> rm nanopubs/drafts/01_quote.md nanopubs/drafts/01_pcc.md
> ```

**Form heading:** *"PICO Research Question — Define a research question using the PICO framework (Population, Intervention, Comparator, Outcome)"*

## Field-by-field draft

<!-- field: pico -->
### Short ID used as URI suffix (text input, required)

Slug becomes part of the nanopub URI. Use kebab-case.

```
meltpond-offtheshelf-bioimage-pico
```

<!-- field: label -->
### Label for the research question (text input, required)

10-200 characters. Length-bounded.

```
Can an off-the-shelf bioimage-analysis workflow count supraglacial melt ponds on Sentinel-2 imagery?
```

<!-- field: description -->
### Description of the research question (textarea, required)

One coherent sentence/paragraph that names P, I, C, O inline.

```
In Sentinel-2 optical imagery of the Greenland ice-sheet ablation zone containing supraglacial melt ponds (Population), does the standard off-the-shelf Galaxy bioimage-analysis workflow — water-index thresholding, connected-component labelling, and object counting and measurement — reused without modification from a cell-nuclei-counting tutorial (Intervention), compared with an independently published, purpose-built supraglacial-lake mapping product and with alternative thresholding choices (Comparator), detect and quantify the melt ponds with detection agreement and total melt-water area comparable to the published mapping (Outcome)?
```

<!-- field: type -->
### Question Type (dropdown, required)

- [ ] causation research question - (Does factor X cause outcome Y?)
- [ ] descriptive research question - (What are the characteristics of X?)
- [x] effectiveness research question - (Does approach X work better than Y?)
- [ ] experience research question - (How do people experience phenomenon X?)
- [ ] prediction research question - (What outcomes can we expect from X?)

<!-- field: populationDescription -->
### Description of the population (textarea, required)

Who/what is being studied. Discipline-level concept — not implementation. See `docs/pico-study-outcome-levels.md`.

```
Supraglacial meltwater features in Sentinel-2 Level-2A optical imagery of the south-west Greenland ice-sheet ablation zone (Russell–Leverett / Isunnguata Sermia margin) — a 10 km × 10 km, 10 m-resolution chip of scene S2A_22WEV_20190723, acquired 2019-07-23.
```

<!-- field: interventionGroupDescription -->
### Description of the intervention group (textarea, required)

The intervention or exposure being examined. Discipline-level concept.

```
The generic, deployed Galaxy "imgteam" bioimage-analysis workflow — a normalised-difference water index computed from two bands, median denoising, thresholding, connected-component labelling, and per-object counting and area measurement — reused without modification from the Galaxy Training Network tutorial "Introduction to Image Analysis using Galaxy" (gxy.io/GTN:T00181), which uses the same tool chain to count stained cell nuclei.
```

<!-- field: comparatorGroupDescription -->
### Description of the comparator group (textarea, required)

The comparison or control condition. Discipline-level concept.

```
An independently produced, purpose-built supraglacial-lake mapping dataset for the same area and melt season (Glen et al. 2024, Sentinel-2 lake outlines, nearest acquisition 2019-07-25), and alternative thresholding choices on the same imagery (automatic Otsu; the more permissive Moussavi et al. 2020 water-index threshold).
```

<!-- field: outcomeGroupDescription -->
### Description of the outcome group (textarea, required)

What outcomes are being measured. The kind of measurement, not the value.

```
Detection agreement against the published lake outlines (precision, recall, F1 and intersection-over-union), the number of detected melt ponds, and the total melt-water area (km²).
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 01.
