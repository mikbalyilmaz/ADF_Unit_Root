"""Common set-up for the analysis scripts: import path, data, labels and a CSV writer."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from unitroots import load, transformed  # noqa: E402
from unitroots.style import FIG_DIR  # noqa: E402

DATA = load()
SERIES = transformed(DATA)

LABELS = {
    "log_credit_weekly": "log card spending per week",
    "log_credit_real": "log real card spending per week",
    "usd": "USD loan rate",
    "log_tufe": "log CPI",
    "log_ito": "log ITO index",
}


def label(name):
    return LABELS[name]


def save_table(rows, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(FIG_DIR / f"{name}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote figures/{name}.csv ({len(rows)} rows)")
