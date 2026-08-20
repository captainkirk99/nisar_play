# nisar_play

Exploration of NISAR (NASA-ISRO SAR) data products in Python, currently
focused on the Level 3 Soil Moisture (SME2) product.

NISAR products are HDF5 files internally structured to be
CF/netCDF-compliant. This project reads them with xarray (netCDF4 engine)
and plots them with matplotlib + cartopy. See the
[NISAR Data User Guide](https://nisar-docs.asf.alaska.edu/) for mission
and product documentation.

## Quick Start

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/plot-sme2          # plot the sample SME2 granule
```

`plot-sme2` writes two PNGs to `output/`: a soil moisture map and a
footprint overview map showing the granule's lat/lon bounds.

## Contents

- [API Reference](api/sme2.md) — the `nisar_play` package
  (`sme2` reader, `plots`, `cli`)
- [Requirements](requirements.md) — project requirements
- [Design](design.md) — architecture and design decisions
- [Roadmap](roadmap.md) — version/sprint plan
