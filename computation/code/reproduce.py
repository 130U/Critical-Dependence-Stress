"""Recreate all four figures and the analytical polynomial checks.

This script runs local files only. It does not install dependencies, download
data, invoke an optimization solver, or modify the manuscript source.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib
import json
import os
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
AUDIT.mkdir(parents=True, exist_ok=True)
TASKS = [
    "code/generate_mechanism_figures.py",
    "new-computations/check_parameter_family.py",
    "new-computations/check_flow_formulas.py",
    "new-computations/plot_profiles_and_flows.py",
]
started = datetime.now(timezone.utc).isoformat()
versions = {name: importlib.import_module(name).__version__
            for name in ("numpy", "matplotlib", "sympy")}
runs = []
for relative in TASKS:
    start = time.monotonic()
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / relative)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    log = AUDIT / (Path(relative).stem + ".log")
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    runs.append({
        "script": relative, "return_code": result.returncode,
        "elapsed_seconds": round(time.monotonic()-start, 3),
        "log": str(log.relative_to(ROOT)),
        "source_sha256": hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(),
    })
    if result.returncode:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        break

figures = [
    f"source/en/figures/{name}.{ext}"
    for name in ("tail-layer-repair", "corner-capacity",
                 "budget-comparison", "optimal-flow-shares")
    for ext in ("pdf", "png", "svg")
]
data = [
    "new-computations/MECHANISM_FIGURES.json",
    "new-computations/PARAMETER_FAMILY_CHECK.json",
    "new-computations/COMPUTATION_REPORT.json",
    "new-computations/profile-envelopes.csv",
    "new-computations/flow-shares-U.npz",
    "new-computations/flow-shares-D.npz",
]
missing = [name for name in figures+data if not (ROOT / name).is_file()]
complete = (len(runs) == len(TASKS)
            and all(item["return_code"] == 0 for item in runs)
            and not missing)
report = {
    "started_utc": started,
    "finished_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "python_implementation": platform.python_implementation(),
    "platform": platform.platform(),
    "dependencies": versions,
    "dependency_loading": {
        "environment_pythonpath_supplied": bool(os.environ.get("PYTHONPATH", "")),
        "script_injected_paths": False,
        "note": "A normal installation uses code/requirements.txt. Workstation-specific dependency paths are omitted from this public record.",
    },
    "runs": runs,
    "all_requested_steps_passed": complete,
    "missing_outputs": missing,
    "scope": {
        "figures_1_2": "Schematic mechanisms with stated geometry and analytic order bounds.",
        "figure_3": "Proved piecewise-linear upper/lower envelopes and exact initial segment; no quadrature or parameter optimization.",
        "figure_4": "Explicit optimal boundary-flow shares for the two representative reference laws.",
        "polynomial_checks": "Exact SymPy integration and algebra for the full dependence parameter interval, fixed-amplitude lower bound, and pure-coordinate upper bound.",
        "not_computed": "No full F(s) solver, no finite-epsilon worst-case optimization, and no inherited refined-bound certificate rerun.",
    },
    "sha256": {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in figures+data if (ROOT / name).is_file()
    },
}
(AUDIT / "CODE_REEXECUTION.json").write_text(
    json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps({
    "all_requested_steps_passed": complete,
    "python": report["python"], "dependencies": versions,
    "runs": runs, "missing_outputs": missing,
}, indent=2))
sys.exit(0 if complete else 1)
