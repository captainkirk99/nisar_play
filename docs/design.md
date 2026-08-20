# Design — NISAR Data Exploration

## Overview

A small Python project for reading and visualizing NISAR data products.
The initial focus is the Level 3 Soil Moisture (SME2) sample file in
`data/`. See `docs/requirements.md` for requirements and `docs/roadmap.md`
for the sprint plan.

## Repository Layout

```
nisar_play/
├── data/            # NISAR sample products (HDF5 + metadata sidecars)
├── docs/
│   ├── design.md        # this document
│   ├── requirements.md  # project requirements
│   ├── roadmap.md       # version/sprint roadmap
│   └── plan/            # per-sprint detailed plans
├── src/
│   └── nisar_play/  # Python package (installed editable via pip)
├── tests/           # pytest test suite
└── README.md
```

## Environment

- Python >= 3.12 virtual environment (`.venv/`, untracked) with the project
  defined in `pyproject.toml` (setuptools backend, `src/` layout).
- Dependencies: `xarray`, `netCDF4`, `matplotlib`, `cartopy`; dev extra:
  `pytest`.
- Install with `python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"`.

## Data Access Design

- NISAR products are HDF5 files structured to be CF/netCDF-compliant.
  Radar/geophysical layers live in nested groups (e.g.
  `/science/LSAR/SME2/...`).
- Reader stack: **xarray with the netCDF4 engine**, opening a specific HDF5
  group via the `group=` argument (e.g. `group="/science/LSAR/SME2/grids"`).
  The lower-level `netCDF4.Dataset` API is used where raw group traversal
  is needed (e.g. structure checks in tests).
- Key SME2 datasets in the `grids` group: `soilMoisture`,
  `soilMoistureUncertainty`, `retrievalQualityFlag`, `latitude`,
  `longitude`, `xCoordinates`/`yCoordinates` (EASE-Grid 2.0).
- Background reference: `.windsurf/skills/nisar-instruments-data/SKILL.md`.

- Reader module: `src/nisar_play/sme2.py` — opens the `grids` group,
  loads a quality-masked soil moisture grid (fill values NaN; pixels whose
  `retrievalQualityFlag` least significant bit marks the retrieval "not
  recommended" are masked), and computes the granule's lat/lon bounds.

## Visualization Design

- Plotting stack: **matplotlib + cartopy** (projection-aware GeoAxes).
- SME2 grids are posted on EASE-Grid 2.0 (EPSG:6933) but ship 1-D
  `latitude`/`longitude` coordinate arrays, so layers are drawn in
  geographic coordinates via `transform=ccrs.PlateCarree()`.
- Plotting module: `src/nisar_play/plots.py` — two figures:
  - Soil moisture map: `pcolormesh` on a cartopy GeoAxes with coastlines,
    state borders, gridline labels, and a units-labeled colorbar.
  - Footprint overview map: the granule's lat/lon bounding box drawn on a
    padded regional map with coastlines.
- Figures are saved as PNGs (default `output/`, untracked) and can also be
  shown interactively. `bbox_inches="tight"` is avoided when saving — it
  collapses the cartopy GeoAxes, leaving only the colorbar.
- CLI: `plot-sme2` (console script, `src/nisar_play/cli.py`; also
  `python -m nisar_play`) produces both figures; the SME2 file path
  defaults to the sample file in `data/`.
- Cartopy downloads Natural Earth background shapefiles (coastlines,
  borders) on first use and caches them locally; NISAR data itself is
  never downloaded — it is read from local files.

## Testing

- Unit tests accompany code changes (see global project rules).
- Pure-Python code is tested with pytest (`tests/`, configured in
  `pyproject.toml`); run `.venv/bin/pytest` from the project root. Any
  future CMake components build and test in a `build/` directory.
- `tests/test_read_sme2.py` smoke-tests the ability to read the sample
  SME2 product (imports, group structure, non-empty soil moisture,
  plausible lat/lon coordinates).
- `tests/test_plots_sme2.py` tests the Sprint 2 capabilities: reader
  functions (quality masking, coordinates, bounds), plot smoke tests on
  the Agg backend (non-trivial PNG written; no image comparisons), and a
  CLI smoke test producing both PNGs.

## Documentation Toolchain

- Docstrings follow the **NumPy convention** (Parameters / Returns /
  Raises sections) throughout `src/nisar_play/`.
- The documentation site is built with **MkDocs + Material theme +
  mkdocstrings** (`mkdocs.yml`): an auto-generated API reference
  (`docs/api/*.md`) plus the narrative pages in `docs/` (index,
  requirements, design, roadmap, sprint plans).
- `mkdocs build --strict` is the docs regression check; local output goes
  to `site/` (untracked).
- Publishing: `.github/workflows/docs.yml` builds the site and deploys it
  to **GitHub Pages** on pushes to `main`
  (https://captainkirk99.github.io/nisar_play/). GitHub Pages must be
  enabled with "GitHub Actions" as the source in the repository settings.

## Open Decisions

Open decisions above are resolved during sprint planning (`/roadmap`
workflow) and recorded in `docs/roadmap.md` under **Clarified decisions**
and in the corresponding `docs/plan/` document. This design document is
updated as decisions are made.
