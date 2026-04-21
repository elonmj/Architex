#!/usr/bin/env python3
"""Download the official single-sample ResBIM package from Google Drive.

This intentionally fetches only the published "One data sample" link, not the
700 MB or 7 GB archives, to stay within free-tier Codespaces storage.

Usage:
  python scripts/download_resbim_sample.py
  python scripts/download_resbim_sample.py --output data/samples/resbim_one_sample.zip
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import gdown

RESBIM_ONE_SAMPLE_URL = "https://drive.google.com/uc?id=1gh4TiEJGkcjuqtO2e13mVQOYxWl5oGbI"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download one official ResBIM sample from Google Drive")
    parser.add_argument(
        "--output",
        default="data/samples/resbim_one_sample.zip",
        help="Output path for the downloaded archive",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = pathlib.Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("[INFO] Downloading official ResBIM one-sample archive")
    print(f"[INFO] Output: {output_path}")

    try:
        gdown.download(RESBIM_ONE_SAMPLE_URL, str(output_path), quiet=False, fuzzy=True)
    except Exception as exc:
        print(f"[ERROR] Download failed: {exc}")
        return 1

    if not output_path.exists() or output_path.stat().st_size == 0:
        print("[ERROR] Download finished but output file is missing or empty")
        return 2

    print("[OK] Sample downloaded")
    print(f"[OK] Size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
