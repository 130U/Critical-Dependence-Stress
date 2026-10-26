"""Run the manuscript calculations and compare fresh outputs with the frozen reference."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
AUDIT.mkdir(exist_ok=True)
steps = ["code/reproduce.py", "new-computations/check_simple_example.py",
         "code/verify_outputs.py"]
record = {"started_utc": datetime.now(timezone.utc).isoformat(), "steps": []}
for name in steps:
    start = time.monotonic()
    result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / name)],
                            cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8")
    log = AUDIT / (Path(name).stem + "_entry.log")
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    record["steps"].append({"script": name, "return_code": result.returncode,
                            "elapsed_seconds": round(time.monotonic()-start, 3),
                            "log": log.relative_to(ROOT).as_posix()})
    print(f"{name}: {'PASS' if result.returncode == 0 else 'FAIL'}")
    if result.returncode:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        break
record["all_passed"] = (len(record["steps"]) == len(steps)
                        and all(s["return_code"] == 0 for s in record["steps"]))
record["finished_utc"] = datetime.now(timezone.utc).isoformat()
(AUDIT / "RUN_ALL.json").write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
sys.exit(0 if record["all_passed"] else 1)
