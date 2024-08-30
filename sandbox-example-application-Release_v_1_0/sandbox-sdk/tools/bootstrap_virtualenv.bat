REM Ensure repository virtualenv
set "REPOSITORY_ROOT=%cd%"
set "TOOLCHAIN_SCRIPTS_DIR=%REPOSITORY_ROOT%\sandbox-sdk\tools"
call copy sandbox-sdk\python_requirements.txt . /Y > nul

set "NUN_RETRIES=0"
:ensure_venv

python "sandbox-sdk\tools\ensure_repository_virtualenv.py"
if %errorlevel% NEQ 0 (
    echo Error in ensuring repository virtualenv
    goto :exit
)

REM Activate virtualenv
set "VIRTUALENV_DIR=%REPOSITORY_ROOT%\build\venv"
call "%VIRTUALENV_DIR%\Scripts\activate.bat"

:: check if SCons can be called, otherwise recreate virtualenv
scons --version > nul 2> nul
if %errorlevel% NEQ 0 (
    if %NUN_RETRIES% GTR 0 (
        echo Error: failed to bootstrap virtualenv
        exit 1
    )
    set /A NUN_RETRIES+=1

    echo Error in using virtualenv, trying to recreate it
    python "sandbox-sdk\tools\ensure_repository_virtualenv.py" --recreate

    goto :ensure_venv
)