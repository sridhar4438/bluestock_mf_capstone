"""Run the full Bluestock MF pipeline in order.

Raw CSVs in Data/raw -> cleaned CSVs in Data/processed
-> SQLite database -> metrics -> charts.
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
SCRIPTS = BASE / "Scripts"

STEPS = [
    "clean_nav.py",
    "clean_transactions.py",
    "clean_performance.py",
    "clean_others.py",
    "load_db.py",
    "compute_metrics.py",
    "compute_cagr.py",
    "fund_scorecard.py",
    "compute_var.py",
    "sector_hhi.py",
    "investor_cohorts.py",
    "sip_continuity.py",
    "recommender.py",
]

def main():
    for step in STEPS:
        print(f"\n=== Running {step} ===")
        result = subprocess.run([sys.executable, str(SCRIPTS / step)], cwd=BASE)
        if result.returncode != 0:
            print(f"Stopped: {step} failed.")
            sys.exit(result.returncode)
    print("\nPipeline complete.")

if __name__ == "__main__":
    main()