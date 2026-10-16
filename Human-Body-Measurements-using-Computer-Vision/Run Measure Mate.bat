@echo off
setlocal
cd /d "%~dp0"

set "CONDA_BAT="
if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" set "CONDA_BAT=%USERPROFILE%\anaconda3\Scripts\activate.bat"
if not defined CONDA_BAT if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" set "CONDA_BAT=%USERPROFILE%\miniconda3\Scripts\activate.bat"
if defined CONDA_BAT (
    call "%CONDA_BAT%" hmr
) else (
    call conda activate hmr
)
if errorlevel 1 (
    echo Could not activate the conda environment "hmr".
    echo Create it first, or edit this file to use your environment name.
    pause
    exit /b 1
)

start "Measure Mate server" cmd /k python app.py
timeout /t 3 /nobreak >nul
start "" http://127.0.0.1:5000

echo Measure Mate is running at http://127.0.0.1:5000
echo Close the server window to stop the application.
endlocal