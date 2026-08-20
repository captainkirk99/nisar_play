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
- Read the NISAR SME2 file via reusable reader functions in `src/nisar_play/`
- Plot the soil moisture data on a projection-aware (cartopy) map with
  coastlines/gridlines, masking invalid/flagged retrievals
- Plot the lat/lon bounds of the data as a footprint overview map showing
  the granule's bounding box on a regional map with coastlines
- Provide a small CLI/script entry point that produces both figures
- Save figures as PNGs to an untracked `output/` directory

**Clarified decisions:**
- Deliverable: Python module(s) in `src/nisar_play/` (reader + plotting) plus a CLI/script entry point
- Soil moisture map: cartopy GeoAxes with proper projection handling of the EASE-Grid 2.0 data
- Lat/lon bounds: separate footprint overview map (bounding box on a regional map with coastlines)
- Figures: saved as PNGs to untracked `output/`, with an option to display interactively
- Masking: apply `retrievalQualityFlag`/fill-value masking so only valid retrievals are shown; no extra ancillary-layer plots
- Testing: pytest unit tests for reader functions plus plot smoke tests (Agg backend, assert PNG produced); no pixel-comparison tests

**Detailed Plan:** See `docs/plan/v0.1-sprint2-data-exploration.md`

**GitHub Issue:** [#2](https://github.com/captainkirk99/nisar_play/issues/2)

### Sprint 3: Documentation Site
- Convert docstrings in `src/nisar_play/` to NumPy style
- Build a documentation site with MkDocs (Material theme) + mkdocstrings,
  including an auto-generated API reference and the existing `docs/` pages
- Publish the site to GitHub Pages via a GitHub Actions workflow on pushes
  to `main`

**Clarified decisions:**
- Docstring convention: NumPy style (scientific-Python standard; parseable by mkdocstrings)
- Generator: MkDocs + Material theme + mkdocstrings (Markdown-native, reuses existing `docs/*.md`)
- Hosting: GitHub Pages, deployed by a GitHub Actions workflow on push to `main`
- Docs dependencies added as a `docs` optional-dependency group in `pyproject.toml`

**Detailed Plan:** See `docs/plan/v0.1-sprint3-docs-site.md`

**GitHub Issue:** [#3](https://github.com/captainkirk99/nisar_play/issues/3)

### Sprint 4: Add CI
- Add a GitHub Actions CI workflow that runs the test suite and the strict
  docs build on pull requests targeting `main` and on pushes to `main`
- Make the test suite runnable without the large (119 MB, untracked) sample
  SME2 granule: generate a small synthetic SME2-like HDF5 fixture with the
  same group/dataset structure and use it when the real file is absent
- Document enabling branch protection on `main` requiring the CI check, so
  branches must pass CI before merge

**Clarified decisions:**
- Data in CI: synthetic SME2-like HDF5 test fixture (tiny grid, same
  structure); no data download, no Git LFS; real-file tests still run
  locally when the sample granule is present
- Triggers: `pull_request` targeting `main` plus `push` to `main`
- Checks: pytest and `mkdocs build --strict` (no linter this sprint)
- Python version: 3.12 only (matches `requires-python` and the docs workflow)
- Enforcement: branch protection rule on `main` requiring the CI check
  (manual repository-settings step, documented like the GitHub Pages setup)

**Detailed Plan:** See `docs/plan/v0.1-sprint4-ci.md`

**GitHub Issue:** [#5](https://github.com/captainkirk99/nisar_play/issues/5)
