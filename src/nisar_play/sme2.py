"""Reader utilities for NISAR Level 3 Soil Moisture (SME2) products.

SME2 products are HDF5 files structured to be CF/netCDF-compliant, with the
geophysical layers posted on the EASE-Grid 2.0 global grid (EPSG:6933) in
the ``/science/LSAR/SME2/grids`` group. This module opens that group with
xarray (netCDF4 engine) and exposes helpers to load a quality-masked soil
moisture grid and the granule's lat/lon bounds.
"""

from pathlib import Path

import numpy as np
import xarray as xr

GRIDS_GROUP = "/science/LSAR/SME2/grids"
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

#: Least significant bit of ``retrievalQualityFlag``:
#: 0 = retrieval recommended, 1 = not recommended.
NOT_RECOMMENDED_BIT = 0x1


def find_sample_file(data_dir: Path = DATA_DIR) -> Path:
    """Return the first SME2 sample file found in *data_dir*.

    Raises ``FileNotFoundError`` if no ``NISAR_L3_*_SME2_*.h5`` file exists.
    """
    files = sorted(Path(data_dir).glob("NISAR_L3_*_SME2_*.h5"))
    if not files:
        raise FileNotFoundError(f"No SME2 sample file found in {data_dir}")
    return files[0]


def open_grids(path: Path) -> xr.Dataset:
    """Open the SME2 ``grids`` group of *path* as an xarray Dataset.

    Fill values (``_FillValue = -9999``) are automatically masked to NaN
    by the netCDF4 engine.
    """
    return xr.open_dataset(path, engine="netcdf4", group=GRIDS_GROUP)


def load_soil_moisture(path: Path, mask_quality: bool = True) -> xr.DataArray:
    """Load the soil moisture grid from *path* with lat/lon coordinates.

    Returns a 2-D DataArray (dims ``yCoordinates`` x ``xCoordinates``) with
    1-D ``latitude`` and ``longitude`` coordinate variables attached.
    Fill values are always NaN. When *mask_quality* is true, pixels whose
    ``retrievalQualityFlag`` least significant bit marks the retrieval as
    "not recommended" are additionally masked to NaN.
    """
    with open_grids(path) as ds:
        sm = ds["soilMoisture"].copy()
        sm = sm.assign_coords(
            latitude=ds["latitude"], longitude=ds["longitude"]
        )
        if mask_quality:
            flag = ds["retrievalQualityFlag"].values
            not_recommended = np.zeros(flag.shape, dtype=bool)
            valid_flag = np.isfinite(flag)
            not_recommended[valid_flag] = (
                flag[valid_flag].astype(np.int64) & NOT_RECOMMENDED_BIT
            ).astype(bool)
            sm = sm.where(~not_recommended)
    return sm


def lonlat_bounds(path: Path) -> tuple[float, float, float, float]:
    """Return the granule's lat/lon bounds as (lon_min, lon_max, lat_min, lat_max)."""
    with open_grids(path) as ds:
        lat = ds["latitude"].values
        lon = ds["longitude"].values
    return (
        float(lon.min()),
        float(lon.max()),
        float(lat.min()),
        float(lat.max()),
    )
