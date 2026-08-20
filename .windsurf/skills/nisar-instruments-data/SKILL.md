---
name: nisar-instruments-data
description: Use when working with NISAR (NASA-ISRO SAR) mission data in this workspace - explains the NISAR instruments (L-SAR/S-SAR, SweepSAR), data product levels (L0-L3), file naming conventions, HDF5/netCDF file structure, and the SME2 soil moisture product used here. Invoke when reading, plotting, or reasoning about any NISAR .h5 file or when the user asks about NISAR bands, polarizations, product types, or data access.
---

# NISAR Instruments and Data

Reference knowledge for the NASA-ISRO SAR (NISAR) mission, distilled from the
[NISAR Data User Guide](https://nisar-docs.asf.alaska.edu/) (Alaska Satellite
Facility, ASF DAAC). Use this skill when reading, exploring, or plotting any
NISAR product (e.g. the `.h5` files in `@/home/ed/nisar_play/data`).

## Mission Overview

NISAR is a joint NASA/ISRO Synthetic Aperture Radar (SAR) mission providing
global, repeat-pass radar coverage. NASA's Jet Propulsion Laboratory and ISRO
jointly built the spacecraft; ASF is the NASA DAAC that archives and
distributes NISAR L-band data. See the
[About NISAR](https://nisar-docs.asf.alaska.edu/nisar-intro) page and the
[NISAR Mission Science Users' Handbook](https://doi.org/10.48577/jpl.UD4HV3).

## Instrumentation

- **SweepSAR** - NISAR's scan-on-receive technique, jointly developed by
  NASA and DLR, allows full-resolution, multi-polarimetric imaging across a
  wide (>240 km) swath by digitally beamforming on receive across a large
  reflector antenna.
- **Pulse Repetition Frequency (PRF)** - Most modes use a *variable*
  (dithered) PRF to avoid fixed data gaps. Quad-pol acquisitions currently
  use a *fixed* PRF, which produces permanent, moving bands of missing data
  in quad-pol products.
- **Look direction** - NISAR is **left-looking**, giving complete coverage
  of Antarctica but leaving a small gap in coverage near the North Pole.
- **Bands** - two independent SAR instruments:
  - **L-SAR** (L-band, 24 cm wavelength): the primary NASA science
    instrument, global coverage, ~240 km swath, ~7 m along-track resolution,
    2-8 m cross-track resolution (mode dependent). This is the band used for
    essentially all products distributed via ASF.
  - **S-SAR** (S-band, 9.3 cm wavelength): built by ISRO, primarily
    acquired over India.
- **Frequencies** - each band records up to two center frequencies:
  - **Frequency A**: primary science frequency, higher resolution.
  - **Frequency B**: coarser resolution, smaller files, mainly for
    atmospheric correction; stored in a `frequencyB/` HDF5 group alongside
    `frequencyA/` when present.
- **Polarization** - transmit+receive combination, encoded as a 2-letter
  code in product filenames:
  - Single-pol: `SH` (HH), `SV` (VV)
  - Dual-pol: `DH` (HH+HV), `DV` (VV+VH)
  - Quad-pol: `QP` (HH+HV+VH+VV)
  - Compact/circular: `RH` (right-circular HH), `RV` (right-circular VV)

## Data Product Levels

NISAR data maturity progresses from raw instrument data to
analysis-ready geophysical products. See
[NISAR Data Products](https://nisar-docs.asf.alaska.edu/products-overview).

| Level | Type | Products | Notes |
|-------|------|----------|-------|
| L0 | Unfocused raw | RRSD (L0B) | Raw radar pulse data; for SAR processing specialists only |
| L1 | Range-Doppler | RSLC, RIFG, ROFF, RUNW | Focused, but in radar (not map) coordinates |
| L2 | Geocoded | GSLC, GCOV, GOFF, GUNW | Map-projected, analysis-ready; projection depends on location (see Projections doc) |
| L3 | Geophysical | SME2 (Soil Moisture) | Derived geophysical parameter, projected to EASE-Grid 2.0 |

Key product descriptions:
- **RSLC** (Range-Doppler Single Look Complex) - focused SAR image, radar coordinates; basis for other L1/L2 pair products.
- **RIFG / RUNW** - wrapped / unwrapped interferograms in radar coordinates (grounding lines, surface displacement).
- **ROFF / GOFF** - dense pixel offset (speckle-tracking) products, mainly cryosphere applications.
- **GSLC** - geocoded single-look complex; backscatter amplitude analysis, can be combined to form interferograms.
- **GCOV** - Geocoded Polarimetric Covariance Matrix; radiometrically terrain-corrected backscatter, supports biomass, soil moisture, disturbance, inundation, and crop-area applications. **GCOV is the direct input to SME2 time-series processing.**
- **GUNW** - geocoded unwrapped interferogram; ground surface displacement.
- **SME2** - Soil Moisture (see below).

### Data Maturity Levels
- **BETA**: Jan/Feb 2026 releases, not fully calibrated, known issues.
- **PROVISIONAL**: from the July 2026 release onward (acquisitions from
  June 17, 2026), fully calibrated but still being validated; will
  eventually be superseded by a reprocessing campaign back to mission start.
- Do not casually mix BETA and PROVISIONAL products in one analysis -
  differences may reflect processing changes, not real surface change.

## Soil Moisture (SME2) Product

Reference: [SME2 product page](https://nisar-docs.asf.alaska.edu/sme2).

- Global soil moisture at **200 m** pixel spacing (500 m over the Sahara),
  generated from a **time-series analysis of L2 GCOV** products, using three
  different retrieval algorithms.
- Nominal repeat: ~twice every 12 days; expected latency ~72 hours.
- Accuracy goal: 0.06 m3/m3 over unflagged, low-vegetation areas
  (vegetation water content < 5 kg/m2).
- Retrievals are flagged/withheld over: dense vegetation (VWC > 5 kg/m2,
  flagged unreliable), active precipitation (flagged unreliable), urban
  areas, permanent snow/ice, permanent inland water (no retrieval), and
  frozen ground or snow-covered ground (no retrieval).
- The 5+5 MHz product is aggregated to 400 m but still posted on the 200 m
  EASE-Grid 2.0 grid.
- PROVISIONAL SME2 products are not yet fully calibrated because long
  GCOV time series aren't yet available; check
  [PROVISIONAL Known Issues](https://nisar-docs.asf.alaska.edu/provisional-known-issues).
- Applications: reservoir management, drought early warning, irrigation
  scheduling, crop yield forecasting.

## File Format: HDF5 (netCDF/CF-compliant)

Reference: [Data Format: HDF5](https://nisar-docs.asf.alaska.edu/data-format).

- All standard NISAR products are HDF5 files, internally structured to
  comply with the CF metadata convention (i.e. netCDF-compatible).
- Structure: `/` (root, empty) -> nested **groups** (like folders) ->
  **datasets** (arrays) -> **attributes** (units, descriptions, valid
  ranges, processing details).
- Radar layers are generally split into `frequencyA/` and (if present)
  `frequencyB/` groups. Example dataset path in a GCOV product:
  `/science/LSAR/GCOV/grids/frequencyA/HH`.
- **GDAL/QGIS caveat**: GDAL does not yet have a NISAR-compliant HDF5
  driver. Workaround: rename/copy the `.h5` extension to `.nc` so GDAL
  picks the correct netCDF/CF driver and recognizes the CRS. ArcGIS Pro
  >= 3.4.0 reads NISAR HDF5 natively. In Python, `h5py` or `xarray`
  (via the netCDF4/h5netcdf engine) can read the files directly without
  renaming.

## File Naming Convention

Reference: [NISAR Naming Conventions](https://nisar-docs.asf.alaska.edu/naming-conventions)
(full field-by-field spec: Cuddy et al. 2025, JPL D-102255 Rev C).

Three filename patterns exist:
1. **Single-acquisition products** (RSLC, GSLC, GCOV, and SME2 - SME2 uses
   this pattern even though it consumes a time series).
2. **Paired-acquisition products** (RIFG, RUNW, GUNW, ROFF, GOFF).
3. **Raw data products** (RRSD / L0B only).

All patterns share the same general shape:
`NISAR_<Level>_<Source>_<ProductType>_<Track>_<Frame>_<Direction>_...` followed
by polarization code(s), acquisition start/end timestamps (`YYYYMMDDThhmmss`),
a **CRID** (Composite Release ID, ties the granule to the exact processing
software/ancillary file versions - see the
[CRID reference](https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/nisar/nisar-composite-release-id-crid)),
quality/coverage flags, and a trailing product version number.

Example from this workspace's data file
(`@/home/ed/nisar_play/data/NISAR_L3_PR_SME2_028_005_A_020_4005_DHDH_A_20260813T125218_20260813T125253_P05023_N_F_J_001.h5`):

| Field | Value | Meaning |
|-------|-------|---------|
| Level | `L3` | Geophysical product |
| Source | `PR` | Product source/provider code |
| ProductType | `SME2` | Soil Moisture |
| Track/Frame | `028_005` | Orbit track and frame number |
| Direction | `A` | Ascending pass |
| Pol code | `DHDH` | Dual-pol HH+HV, frequency A/B channel indicator |
| Start/End | `20260813T125218` / `20260813T125253` | Acquisition time window (UTC) |
| CRID | `P05023` | Composite Release ID (processing software/ancillary version) |
| Flags | `N_F_J` | Coverage/quality flags |
| Version | `001` | Product version |

Ancillary products (e.g. Orbit Ephemeris) use a different scheme, e.g.
`NISAR_ANC_J_PR_{ProductType}_{CreationTime}_{ValidityStart}_{ValidityEnd}.xml`
where `ProductType` is one of `FOE`, `NOE`, `MOE`, `POE`.

## Accessing NISAR Data

- Search/download via [ASF Vertex](https://search.asf.alaska.edu/),
  [NASA Earthdata Search](https://search.earthdata.nasa.gov/), or the
  `earthaccess` Python package.
- Direct AWS S3 cloud access is also available for supported product types.
- See [Accessing NISAR Data](https://nisar-docs.asf.alaska.edu/access-overview)
  and [Using NISAR Data](https://nisar-docs.asf.alaska.edu/using-overview)
  for tutorials and tooling.

## Further Reading

- [Available Data / release timeline](https://nisar-docs.asf.alaska.edu/availability-overview)
- [Data Products Overview](https://nisar-docs.asf.alaska.edu/products-overview)
- [Metadata structure](https://nisar-docs.asf.alaska.edu/metadata)
- [Projections (EASE-Grid 2.0, UTM/Polar Stereo for L1/L2)](https://nisar-docs.asf.alaska.edu/projections)
- [Known Issues (PROVISIONAL)](https://nisar-docs.asf.alaska.edu/provisional-known-issues)
