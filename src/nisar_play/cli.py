"""Command-line interface: plot NISAR SME2 soil moisture and footprint.

Usage (from the project venv)::

    plot-sme2 [FILE] [--output-dir output] [--show]

or equivalently ``python -m nisar_play ...``. FILE defaults to the sample
SME2 product in the project's ``data/`` directory. Two PNGs are written to
the output directory: ``soil_moisture.png`` and ``footprint.png``.
"""

import argparse
from pathlib import Path

from . import plots, sme2


def main(argv: list[str] | None = None) -> int:
    """Entry point: produce the soil moisture and footprint figures."""
    parser = argparse.ArgumentParser(
        prog="plot-sme2",
        description="Plot soil moisture and lat/lon bounds from a NISAR SME2 file.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default=None,
        help="SME2 .h5 file (default: sample file in data/)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="directory for output PNGs (default: output/)",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="also display the figures interactively",
    )
    args = parser.parse_args(argv)

    path = args.file if args.file is not None else sme2.find_sample_file()
    sm = sme2.load_soil_moisture(path)
    bounds = sme2.lonlat_bounds(path)

    sm_png = plots.plot_soil_moisture(
        sm, out_path=args.output_dir / "soil_moisture.png", show=args.show
    )
    fp_png = plots.plot_footprint(
        bounds, out_path=args.output_dir / "footprint.png", show=args.show
    )
    print(f"Wrote {sm_png}")
    print(f"Wrote {fp_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
