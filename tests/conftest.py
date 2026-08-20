"""Shared pytest fixtures for the nisar_play test suite.

Provides an SME2 product path for data-dependent tests. When the real
sample granule is present in ``data/`` it is used; otherwise (e.g. in CI,
where the 119 MB file is not tracked) a small synthetic SME2-like HDF5
file with the same group/dataset structure is generated. Setting the
``NISAR_PLAY_FORCE_SYNTHETIC`` environment variable forces the synthetic
file even when the real granule is available (used to verify the CI path
locally).
"""

import os
from pathlib import Path

import numpy as np
import netCDF4
import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

#: Synthetic granule filename, conforming to the SME2 naming convention so
#: filename-based discovery (``NISAR_L3_*_SME2_*.h5``) finds it.
SYNTHETIC_NAME = (
    "NISAR_L3_PR_SME2_000_000_A_000_0000_DHDH_A_"
    "20260101T000000_20260101T000035_P00000_N_F_J_001.h5"
)

FILL = -9999


def make_synthetic_sme2(path: Path, ny: int = 12, nx: int = 10) -> Path:
    """Write a small synthetic SME2-like HDF5 file.

    Mirrors the group/dataset structure of a real SME2 granule used by
    the reader and tests: ``/science/LSAR/identification`` and
    ``/science/LSAR/SME2/{grids,metadata}`` with the key ``grids``
    datasets (soil moisture, uncertainty, quality flag, EASE-Grid 2.0
    coordinates). Includes fill values and "not recommended" quality-flag
    pixels so masking logic is exercised.

    Parameters
    ----------
    path : Path
        Destination ``.h5`` file path.
    ny, nx : int, optional
        Grid size (rows ``yCoordinates`` x columns ``xCoordinates``).

    Returns
    -------
    Path
        The written file path.
    """
    rng = np.random.default_rng(42)
    sm = rng.uniform(0.05, 0.45, size=(ny, nx)).astype(np.float32)
    unc = rng.uniform(0.01, 0.06, size=(ny, nx)).astype(np.float32)
    flag = np.zeros((ny, nx), dtype=np.int16)
    # Mark some pixels "not recommended" (LSB set) and some as fill.
    flag[0, :] = 1
    sm[1, :2] = FILL
    flag[2, :2] = FILL

    # Small footprint over the southwestern US, similar to the sample file.
    lat = np.linspace(38.0, 35.0, ny).astype(np.float32)
    lon = np.linspace(-117.6, -113.4, nx).astype(np.float32)
    # Nominal 200 m EASE-Grid 2.0 posting (values are placeholders).
    x = (np.arange(nx) * 200.0).astype(np.float64)
    y = (np.arange(ny) * -200.0).astype(np.float64)

    with netCDF4.Dataset(path, "w", format="NETCDF4") as ds:
        science = ds.createGroup("science")
        lsar = science.createGroup("LSAR")
        lsar.createGroup("identification")
        sme2 = lsar.createGroup("SME2")
        sme2.createGroup("metadata")
        grids = sme2.createGroup("grids")

        grids.createDimension("yCoordinates", ny)
        grids.createDimension("xCoordinates", nx)

        def var(name, dtype, dims, data, units, fill=None):
            v = grids.createVariable(name, dtype, dims, fill_value=fill)
            v.units = units
            v[:] = data
            return v

        var("yCoordinates", "f8", ("yCoordinates",), y, "meters")
        var("xCoordinates", "f8", ("xCoordinates",), x, "meters")
        var("latitude", "f4", ("yCoordinates",), lat, "degree_north")
        var("longitude", "f4", ("xCoordinates",), lon, "degree_east")
        var(
            "soilMoisture", "f4", ("yCoordinates", "xCoordinates"),
            sm, "meter^3/meter^3", fill=np.float32(FILL),
        )
        var(
            "soilMoistureUncertainty", "f4", ("yCoordinates", "xCoordinates"),
            unc, "meter^3/meter^3", fill=np.float32(FILL),
        )
        var(
            "retrievalQualityFlag", "i2", ("yCoordinates", "xCoordinates"),
            flag, "1", fill=np.int16(FILL),
        )
    return path


@pytest.fixture(scope="session")
def real_sme2_path():
    """Path to the real sample granule in ``data/``, or None if absent."""
    if os.environ.get("NISAR_PLAY_FORCE_SYNTHETIC"):
        return None
    files = sorted(DATA_DIR.glob("NISAR_L3_*_SME2_*.h5"))
    return files[0] if files else None


@pytest.fixture(scope="session")
def sme2_path(real_sme2_path, tmp_path_factory):
    """SME2 product path: the real granule if present, else synthetic."""
    if real_sme2_path is not None:
        return real_sme2_path
    out_dir = tmp_path_factory.mktemp("synthetic_data")
    return make_synthetic_sme2(out_dir / SYNTHETIC_NAME)
