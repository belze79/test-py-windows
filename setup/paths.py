from pathlib import Path
from sys import platform

base_dir: Path = Path(__file__).resolve().parents[1]
setup_dir = base_dir / 'setup'
_venv = base_dir / '.venv'
bin_dir, _py_exe, _pip_exe = ('Scripts', 'python.exe', 'pip.exe') if platform == 'win32' else ('bin', 'python', 'pip')

class Paths:
    BASE = base_dir
    VENV = _venv
    PY_EXE = _venv / bin_dir / _py_exe
    PIP_EXE = _venv / bin_dir / _pip_exe
    REQUIREMENTS_TXT = setup_dir / 'requirements.txt'
    MAIN = base_dir / 'main.py'
    MODULE_CHECK = setup_dir / 'module_check.json'