"""Portable equivalent of make build, including Windows."""
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for name in ('validate_registry','export_registry','coverage_report','render_family_pages','render_readme','build_site'):
    subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py')],cwd=ROOT,check=True)
