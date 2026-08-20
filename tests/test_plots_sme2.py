"""Sprint 2 tests: SME2 reader functions, plotting smoke tests, and CLI.

Uses the sample SME2 product in ``data/`` when present, else the
synthetic fixture (see ``conftest.py``). Plot tests run on the
matplotlib Agg backend and only assert that a non-trivial PNG is
produced (no image comparisons).
"""

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

from nisar_play import cli, plots, sme2


@pytest.fixture(scope="module")
def soil_moisture(sme2_path):
    return sme2.load_soil_moisture(sme2_path)


def test_find_sample_file(sme2_path):
    """SME2 file discovery finds the fixture file in its directory."""
    assert sme2_path.exists()
    assert sme2_path.suffix == ".h5"
    assert sme2.find_sample_file(sme2_path.parent) == sme2_path


def test_load_soil_moisture_masked(sme2_path, soil_moisture):
    """Quality masking removes fill/not-recommended pixels; values plausible."""
    sm = soil_moisture
    assert sm.ndim == 2
    valid = sm.values[np.isfinite(sm.values)]
    assert valid.size > 0, "no valid soil moisture after masking"
    assert np.all(valid >= 0) and np.all(valid <= 1), "values outside 0-1 m^3/m^3"
    unmasked = sme2.load_soil_moisture(sme2_path, mask_quality=False)
    n_unmasked = int(np.isfinite(unmasked.values).sum())
    assert valid.size <= n_unmasked, "masking added valid pixels"


def test_load_soil_moisture_coords(soil_moisture):
    """Loaded grid carries plausible 1-D latitude/longitude coordinates."""
    lat = soil_moisture["latitude"].values
    lon = soil_moisture["longitude"].values
    assert lat.ndim == lon.ndim == 1
    assert soil_moisture.shape == (lat.size, lon.size)
    assert np.all((lat >= -90) & (lat <= 90))
    assert np.all((lon >= -180) & (lon <= 180))


def test_lonlat_bounds(sme2_path, soil_moisture):
    """Bounds match the min/max of the lat/lon coordinate arrays."""
    lon_min, lon_max, lat_min, lat_max = sme2.lonlat_bounds(sme2_path)
    lat = soil_moisture["latitude"].values
    lon = soil_moisture["longitude"].values
    assert lon_min == pytest.approx(float(lon.min()))
    assert lon_max == pytest.approx(float(lon.max()))
    assert lat_min == pytest.approx(float(lat.min()))
    assert lat_max == pytest.approx(float(lat.max()))
    assert lon_min < lon_max and lat_min < lat_max


def test_plot_soil_moisture_writes_png(soil_moisture, tmp_path):
    """Soil moisture plot runs and writes a non-trivial PNG."""
    out = plots.plot_soil_moisture(soil_moisture, out_path=tmp_path / "sm.png")
    assert out.exists() and out.stat().st_size > 1000


def test_plot_footprint_writes_png(sme2_path, tmp_path):
    """Footprint plot runs and writes a non-trivial PNG."""
    bounds = sme2.lonlat_bounds(sme2_path)
    out = plots.plot_footprint(bounds, out_path=tmp_path / "fp.png")
    assert out.exists() and out.stat().st_size > 1000


def test_cli_produces_both_pngs(sme2_path, tmp_path):
    """The CLI entry point produces both expected PNGs."""
    rc = cli.main([str(sme2_path), "--output-dir", str(tmp_path)])
    assert rc == 0
    for name in ("soil_moisture.png", "footprint.png"):
        f = tmp_path / name
        assert f.exists() and f.stat().st_size > 1000
