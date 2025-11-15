from sys import executable as exe, exit as s_exit
from subprocess import Popen, PIPE, STDOUT, run as sub_run
from pathlib import Path
from typing import Tuple, List
from json import load, dump

from setup.paths import Paths

TypeCommand = Tuple[str | Path, ...]
TypeProcess = List[Tuple[TypeCommand, str]]
modules = 'modules'

def run_cmd(command: TypeCommand, description: str = ''):
    running = description if description else ' '.join(map(str, command))
    print(f'\nStart {running}...')
    process = Popen(command, stdout=PIPE, stderr=STDOUT, text=True, bufsize=1)
    for line in process.stdout:
        if line: print(line)
    if not process.wait() == 0:
        raise ChildProcessError(f'Error in {running}')


def read_requirements() -> list[str]:
    with open(Paths.REQUIREMENTS_TXT) as f:
        return [s.strip() for s in f.readlines()]


def read_module_json() -> list[str]:
    with open(Paths.MODULE_CHECK) as f:
        return load(f)[modules]


def write_module_json(list_modules: list[str]):
    with open(Paths.MODULE_CHECK, 'w',encoding='utf-8') as f:
        dump({modules: list_modules}, f, indent=2, ensure_ascii=False)


env_processes: TypeProcess = [
    ((exe, '-m', 'venv', Paths.VENV, '--copies'), 'Creating Virtual Environment'),
    ((Paths.PIP_EXE, 'install', '--upgrade', 'pip'), 'Upgrading pip'),
    ((Paths.PIP_EXE, 'install', '-r', Paths.REQUIREMENTS_TXT), f'Installing modules from {Paths.REQUIREMENTS_TXT.name}')
]


if not Paths.VENV.exists():
    print('STARTING SETUP...')
    for cmd, desc in env_processes:
        if Paths.REQUIREMENTS_TXT in cmd and not read_requirements():
            print(f'Nessun modulo in {Paths.REQUIREMENTS_TXT.name}')
            continue
        run_cmd(cmd, desc)
        print(f'End {desc}')
    else: print('END SETUP!')
    write_module_json(read_requirements())
else:
    mod_txt = read_requirements()
    mod_json = read_module_json()
    added = [m for m in mod_txt if m not in mod_json]
    removed = [m for m in mod_json if m not in mod_txt]
    if added:
        run_cmd((Paths.PIP_EXE, 'install', *added))
    if removed:
        run_cmd((Paths.PIP_EXE, 'uninstall', '-y', *removed))
    write_module_json(mod_txt)


if not Path(exe).resolve() == Paths.PY_EXE:
    try:
        sub_run((Paths.PY_EXE, Paths.MAIN), check=True)
        s_exit(0)
    except KeyboardInterrupt:
        print('Interruzione da tastiera')
        s_exit(1)

