"""Smoke tests: verify the environment can read NISAR SME2 netCDF4/HDF5 files.

Opens an SME2 (Level 3 Soil Moisture) product — the sample granule in
``data/`` when present, else the synthetic fixture (see ``conftest.py``) —
with xarray (netCDF4 engine) and asserts the expected group structure and
a non-empty soil moisture dataset.
"""

import numpy as np
import pytest
import xarray as xr

GRIDS_GROUP = "/science/LSAR/SME2/grids"


@pytest.fixture(scope="module")
def grids(sme2_path):
    with xr.open_dataset(sme2_path, engine="netcdf4", group=GRIDS_GROUP) as ds:
        yield ds


def test_imports():
    """All Sprint 1 dependencies import successfully."""
    import cartopy  # noqa: F401
    import matplotlib  # noqa: F401
    import netCDF4  # noqa: F401


def test_expected_group_structure(sme2_path):
    """The SME2 file contains the expected NISAR HDF5 groups."""
    import netCDF4

    with netCDF4.Dataset(sme2_path) as ds:
        science = ds.groups["science"]
        lsar = science.groups["LSAR"]
        assert "identification" in lsar.groups
        sme2 = lsar.groups["SME2"]
        assert "grids" in sme2.groups
        assert "metadata" in sme2.groups


def test_soil_moisture_present_and_nonempty(grids):
    """Soil moisture dataset exists, has 2-D shape, and contains valid data."""
    assert "soilMoisture" in grids
    sm = grids["soilMoisture"]
    assert sm.ndim == 2
    assert sm.size > 0
    assert np.isfinite(sm.values).any(), "soilMoisture contains no valid values"


def test_coordinates_present(grids):
    """Latitude/longitude coordinate variables exist and are plausible."""
    lat = grids["latitude"].values
    lon = grids["longitude"].values
    assert lat.size > 0 and lon.size > 0
    assert np.all((lat >= -90) & (lat <= 90))
    assert np.all((lon >= -180) & (lon <= 180))
