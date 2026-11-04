"""Compatibility entry point for the current handbook edition."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('update_handbook_completion.py')), run_name='__main__')
