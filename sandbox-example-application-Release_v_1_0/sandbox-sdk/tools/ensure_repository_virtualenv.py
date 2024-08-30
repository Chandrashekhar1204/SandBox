import os
import sys
import shutil
from pathlib import Path
import hashlib
import logging
import subprocess
import urllib.request

REPOSITORY_ROOT = Path(os.environ['REPOSITORY_ROOT'])
# TOOLCHAIN_ENV = Path(os.environ['TOOLCHAIN_ENV'])

PYTHON_REQUIREMENTS_FILE = REPOSITORY_ROOT / 'python_requirements.txt'
NEW_VIRTUALENV_LOCATION = REPOSITORY_ROOT / 'build' / 'venv'
GENERATING_REQUIREMENTS_HASH_FILE = NEW_VIRTUALENV_LOCATION / 'generating_requirements_hash.sha1'

quiet_subprocess = False
virtualenv_recreated = False
clear_existing = False

def hash_of_file(file: Path) -> str:
    hash = hashlib.sha1(file.read_bytes()).hexdigest()
    return hash

def pip_install(python_executable: Path, install_args, cwd=None):
    python_executable_raw = r"{}".format(python_executable)

    pip_update_cmd = f"\"{python_executable_raw}\" -m pip install --no-color {install_args}"
    logging.info(f"Executing command {pip_update_cmd}")
    if quiet_subprocess:
        pip_update_cmd += ' -qq'
    
    import shlex
    pip_update_cmd_split = shlex.split(pip_update_cmd)
    p = subprocess.run(pip_update_cmd_split, cwd=cwd, check=True)
    return p.returncode

def install_requirements(python_executable: Path, requirements: Path):
    logging.info(f"Installing modules as defined in requirements file {str(requirements)}")
    working_dir = requirements.parent
    
    requirements_raw = r"{}".format(str(requirements))
    requirements_escaped = f"\"{requirements_raw}\""
    return pip_install(python_executable, f"-r {requirements_escaped}", working_dir)

def upgrade_pip(python_executable: Path):
    logging.info("Upgrading pip to latest version")
    return pip_install(python_executable, '--upgrade pip')

def create_virtualenv(python_executable: Path, virtualenv_location: Path):
    logging.info(f"Creating virtualenv in {virtualenv_location}")

    python_executable_raw = r"{}".format(python_executable)
    virtualenv_location_raw = r"{}".format(virtualenv_location)

    cmd = f"\"{python_executable_raw}\" -m venv --clear \"{virtualenv_location_raw}\""
    logging.debug(f"Executing command {cmd}")
    import shlex
    cmd_split = shlex.split(cmd)
    p = subprocess.run(cmd_split, check=True)

    global virtualenv_recreated
    virtualenv_recreated = True

    return p.returncode

def generate_virtualenv_hash(requirements_file: Path):
    logging.info("Generating virtualenv hash")

    GENERATING_REQUIREMENTS_HASH_FILE.write_text(hash_of_file(requirements_file))

    logging.debug(f"Hash file created in {GENERATING_REQUIREMENTS_HASH_FILE}")

def create_and_populate_virtualenv():
    """
    Create virtualenv with modules
    """
    logging.debug("Called create_and_populate_virtualenv()")

    upgrade_pip(sys.executable)

    pip_install(sys.executable, "virtualenv")

    create_virtualenv(sys.executable, NEW_VIRTUALENV_LOCATION)

    install_requirements(NEW_VIRTUALENV_LOCATION / 'Scripts' / 'python.exe', PYTHON_REQUIREMENTS_FILE)

    generate_virtualenv_hash(PYTHON_REQUIREMENTS_FILE)

def remove_virtualenv():
    logging.info(f"Removing virtualenv in {NEW_VIRTUALENV_LOCATION}")
    shutil.rmtree(NEW_VIRTUALENV_LOCATION)

def is_virtualenv_creation_required() -> bool:
    # Compute hash of python_requirements.txt
    if PYTHON_REQUIREMENTS_FILE.exists():
        current_requirements_hash = hash_of_file(PYTHON_REQUIREMENTS_FILE)
        logging.debug(f"{PYTHON_REQUIREMENTS_FILE} hash = {current_requirements_hash}")
    else:
        raise RuntimeError(f"Requirements file {PYTHON_REQUIREMENTS_FILE} doesn't exist")

    # Compare current hash with the one inside virtualenv
    logging.debug(f"Generating-requirements hash file = {GENERATING_REQUIREMENTS_HASH_FILE}")

    if GENERATING_REQUIREMENTS_HASH_FILE.exists():
        requirements_hash_of_virtualenv = GENERATING_REQUIREMENTS_HASH_FILE.read_text()
        logging.debug(f"Generating-requirements hash = {requirements_hash_of_virtualenv}")

        if current_requirements_hash == requirements_hash_of_virtualenv:
            logging.debug("Nothing to do, venv is up-to-date")
            return False
        else:
            logging.info("Requirements and virtualenv hash are different. Will recreate venv.")
            return True
    else:
        logging.info("Virtualenv hash is not present. Will create venv.")
        return True


if __name__ == "__main__":
    if '--debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    elif '--verbose' in sys.argv:
        logging.basicConfig(level=logging.INFO)

    if '--clear' in sys.argv:
        clear_existing = True

    recreation_required = False
    if '--recreate' in sys.argv:
        recreation_required = True

    try:
        if recreation_required:
            remove_virtualenv()

        if is_virtualenv_creation_required() or clear_existing:
            create_and_populate_virtualenv()
            sys.exit(0)
    except Exception as e:
        logging.error(f"Exception while executing: {e}")
        if virtualenv_recreated:
            logging.warning("Reverting changes...")
            remove_virtualenv()
        sys.exit(1)
