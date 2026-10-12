"""Runs every analysis script in order, each in a fresh Python process. Run from inside analysis/."""

import subprocess
import sys

for script in ("01_data.py", "02_integration_order.py", "03_breaks.py"):
    print(f"Running {script}", flush=True)
    subprocess.run([sys.executable, script], check=True)
print("Done. Figures and tables are in ../figures.")
