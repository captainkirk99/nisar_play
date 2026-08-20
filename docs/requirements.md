# Requirements — NISAR Data Exploration

## Purpose

Explore NISAR (NASA-ISRO SAR) data products in Python, starting with the
Level 3 Soil Moisture (SME2) sample file in `data/`.

## Functional Requirements

- **R1**: The project shall provide a reproducible Python environment
  (virtual environment plus a project definition file).
- **R2**: The project shall be able to read NISAR HDF5/netCDF4 product
  files, specifically the SME2 sample file:
  `data/NISAR_L3_PR_SME2_028_005_A_020_4005_DHDH_A_20260813T125218_20260813T125253_P05023_N_F_J_001.h5`
- **R3**: The project shall plot the soil moisture data from the SME2 file.
- **R4**: The project shall plot the lat/lon bounds of the SME2 data.

## Non-Functional Requirements

- **N1**: Code changes shall be covered by unit tests, run from a `build`
  directory where applicable, or via pytest for pure-Python code.
- **N2**: Documentation (`README.md`, `docs/design.md`, this file) shall be
  kept up to date with all changes.
- **N3**: The environment shall be reproducible from the project definition
  file alone (no undocumented dependencies).

## Constraints

- NISAR products are HDF5 files internally structured as CF/netCDF-compliant
  data; the reading approach must handle this format.
- SME2 data is posted on the EASE-Grid 2.0 projection; plotting must account
  for this when georeferencing.

## Traceability

Requirements map to roadmap items in `docs/roadmap.md`:

| Requirement | Roadmap item |
|-------------|--------------|
| R1, R2 | v0.1 Sprint 1: Python Setup |
| R3, R4 | v0.1 Sprint 2: Data Exploration |
| N2 | v0.1 Sprint 3: Documentation Site |
| N1 | v0.1 Sprint 4: Add CI |
