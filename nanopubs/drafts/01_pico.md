# 01 — PICO Research Question (chain anchor)

> **Question-rooted chain** (no upstream paper sentence is being tested — we reuse
> a Galaxy Training Network tutorial method cross-discipline). PICO over PCC
> because the question has clear comparators (a purpose-built lake-mapping product;
> alternative thresholds). See `docs/chain-decision-tree.md`.
> Same shape as the sibling `fiesta-galaxy-cellprofiler-eo` chain.

## Form fields (`docs/forrt-form-fields.md` § PICO Research Question)

`Short ID` · `Research Question Title` (10–200 chars) · `Complete Research Question` · `Question Type` (radio: Causation/Descriptive/Effectiveness/Experience/Prediction) · `Population (P)` · `Intervention (I)` · `Comparison (C)` · `Outcome (O)`

---

### Short ID (used as URI suffix)

```
meltpond-offtheshelf-bioimage-pico
```

### Research Question Title (10–200 characters)

```
Can an off-the-shelf bioimage-analysis workflow count supraglacial melt ponds on Sentinel-2 imagery?
```

### Complete Research Question

```
In Sentinel-2 optical imagery of the Greenland ice-sheet ablation zone containing
supraglacial melt ponds (Population), does the standard off-the-shelf Galaxy
bioimage-analysis workflow — water-index thresholding, connected-component
labelling, and object counting and measurement — reused without modification from
a cell-nuclei-counting tutorial (Intervention), compared with an independently
published, purpose-built supraglacial-lake mapping product and with alternative
thresholding choices (Comparator), detect and quantify the melt ponds with
detection agreement and total melt-water area comparable to the published mapping
(Outcome)?
```

### Question Type (radio)

```
Effectiveness
```

### Population (P)

```
Supraglacial meltwater features in Sentinel-2 Level-2A optical imagery of the
south-west Greenland ice-sheet ablation zone (Russell–Leverett / Isunnguata Sermia
margin) — a 10 km × 10 km, 10 m-resolution chip of scene S2A_22WEV_20190723,
acquired 2019-07-23.
```

### Intervention (I)

```
The generic, deployed Galaxy "imgteam" bioimage-analysis workflow — a
normalised-difference water index computed from two bands, median denoising,
thresholding, connected-component labelling, and per-object counting and area
measurement — reused without modification from the Galaxy Training Network
tutorial "Introduction to Image Analysis using Galaxy" (gxy.io/GTN:T00181), which
uses the same tool chain to count stained cell nuclei.
```

### Comparison (C)

```
An independently produced, purpose-built supraglacial-lake mapping dataset for the
same area and melt season (Glen et al. 2024, Sentinel-2 lake outlines, nearest
acquisition 2019-07-25), and alternative thresholding choices on the same imagery
(automatic Otsu; the more permissive Moussavi et al. 2020 water-index threshold).
```

### Outcome (O)

```
Detection agreement against the published lake outlines (precision, recall, F1 and
intersection-over-union), the number of detected melt ponds, and the total
melt-water area (km²).
```
