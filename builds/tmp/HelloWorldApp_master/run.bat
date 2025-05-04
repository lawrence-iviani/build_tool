@echo off

SET WINPYTHON_PATH=%~dp0\python-3.12-win
SET PYTHON_BIN=%WINPYTHON_PATH%\python.exe
SET VENV_DIR=%~dp0venv

IF NOT EXIST "%VENV_DIR%" (
    echo Virtual Environment not existing... Run setup.bat first
    exit /b 1
)

CALL "%VENV_DIR%\Scripts\activate.bat" || exit /b 1

cd "%~dp0app"
python main_folder\main.py

pause
CALL deactivate
exit /b 0