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

## Visualization Design

- Soil moisture will be plotted from the SME2 grid (EASE-Grid 2.0
  projection, 200 m posting).
- *Decision pending (v0.1 Sprint 2 planning)*: plotting stack
  (matplotlib alone or with cartopy for projection-aware maps).

## Testing

- Unit tests accompany code changes (see global project rules).
- Pure-Python code is tested with pytest (`tests/`, configured in
  `pyproject.toml`); run `.venv/bin/pytest` from the project root. Any
  future CMake components build and test in a `build/` directory.
- `tests/test_read_sme2.py` smoke-tests the ability to read the sample
  SME2 product (imports, group structure, non-empty soil moisture,
  plausible lat/lon coordinates).

## Open Decisions

Open decisions above are resolved during sprint planning (`/roadmap`
workflow) and recorded in `docs/roadmap.md` under **Clarified decisions**
and in the corresponding `docs/plan/` document. This design document is
updated as decisions are made.
