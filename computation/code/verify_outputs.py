"""Read back generated results; scientific equivalence is distinct from image identity.

The frozen reference records manuscript values, array content hashes and PNG hashes.
PDF/SVG bytes contain metadata or generated identifiers and are not compared.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
reference = json.loads((ROOT / "audit/REFERENCE_OUTPUTS.json").read_text(encoding="utf-8"))
checks = []

def check(name, ok):
    checks.append({"check": name, "passed": bool(ok)})

for name, expected in reference["scientific_files_sha256"].items():
    p = ROOT / name
    check(name + " exact bytes", p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == expected)
for name, arrays in reference["array_contents"].items():
    p = ROOT / name
    if not p.is_file():
        check(name + " exists", False)
        continue
    with np.load(p, allow_pickle=False) as data:
        check(name + " array names", set(data.files) == set(arrays))
        for key, expected in arrays.items():
            a = data[key]
            actual = {"shape": list(a.shape), "dtype": a.dtype.str,
                      "sha256": hashlib.sha256(a.tobytes(order="C")).hexdigest()}
            check(name + ":" + key, actual == expected)
for name, expected in reference["exact_json_fields"].items():
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    for key, value in expected.items():
        check(name + ":" + key, data.get(key) == value)
rendering = []
for name, expected in reference["png_sha256"].items():
    p = ROOT / name
    rendering.append({"file": name, "exact_reference_bytes": p.is_file()
                      and hashlib.sha256(p.read_bytes()).hexdigest() == expected})
report = {
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "all_scientific_checks_passed": all(c["passed"] for c in checks),
    "checks": checks,
    "png_comparison": rendering,
    "all_png_bytes_match": all(c["exact_reference_bytes"] for c in rendering),
    "scope": "Exact scalar expressions, saved numerical arrays and profile CSV; PNG identity is recorded separately and can depend on fonts or platform. No proof verification or full critical-profile optimization.",
}
(ROOT / "audit/OUTPUT_READBACK.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps({k: v for k, v in report.items() if k not in ("checks", "png_comparison")}, indent=2))
sys.exit(0 if report["all_scientific_checks_passed"] else 1)
