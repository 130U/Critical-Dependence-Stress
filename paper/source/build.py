"""Compile the manuscript with Tectonic without changing source files."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--engine', default='tectonic', help='Tectonic executable or its path')
parser.add_argument('--cache', type=Path, help='Optional existing Tectonic cache directory')
parser.add_argument('--outdir', type=Path, default=ROOT/'build')
args = parser.parse_args()
engine = shutil.which(args.engine) or str(Path(args.engine).resolve())
output = args.outdir.resolve()
output.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
if args.cache:
    env['TECTONIC_CACHE_DIR'] = str(args.cache.resolve())
result = subprocess.run([engine, '--keep-logs', '--keep-intermediates', '--outdir',
                         str(output), 'paper.tex'], cwd=ROOT, env=env)
raise SystemExit(result.returncode)
