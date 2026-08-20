# NISAR Data Exploration

## Version 0.1

### Sprint 1: Python Setup
- Set up a Python virtual environment (venv) and a `pyproject.toml` project file
- Be ready to read netCDF4 files in python
- We will be reading and plotting soil moisture from the NISAR file NISAR_L3_PR_SME2_028_005_A_020_4005_DHDH_A_20260813T125218_20260813T125253_P05023_N_F_J_001.h5

**Clarified decisions:**
- Environment: venv + `pyproject.toml` (project file is TOML, not YAML)
- Reader stack: xarray with the netCDF4 engine
- Plotting deps installed now (ahead of Sprint 2): matplotlib + cartopy (SME2 is on EASE-Grid 2.0)
- Verification: pytest smoke test that opens the sample SME2 `.h5` and asserts expected groups/datasets exist

**Detailed Plan:** See `docs/plan/v0.1-sprint1-python-setup.md`

**GitHub Issue:** [#1](https://github.com/captainkirk99/nisar_play/issues/1)

### Sprint 2: Data Exploration
- Read the NISAR file
- Plot the soil moisture data
- Plot the lat/lon bounds of the data
