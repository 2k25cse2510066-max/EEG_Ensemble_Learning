@echo off
setlocal
cd /d "%~dp0"
echo.
echo ===== EEG project setup (run once) =====
echo This can take several minutes the first time. Please do not close the window.
echo.

rem ---- choose a Python that has ready-made packages (3.13 or 3.12 preferred) ----
set "PYCMD="
py -3.13 --version >nul 2>nul && set "PYCMD=py -3.13"
if not defined PYCMD ( py -3.12 --version >nul 2>nul && set "PYCMD=py -3.12" )
if not defined PYCMD ( py -3 --version >nul 2>nul && set "PYCMD=py -3" )
if not defined PYCMD ( python --version >nul 2>nul && set "PYCMD=python" )
if not defined PYCMD (
  echo ERROR: Python was not found. Install Python 3.12 or 3.13 from python.org and run this again.
  pause
  exit /b 1
)
echo Using: %PYCMD%
%PYCMD% --version

echo.
echo ===== Backend: creating virtual environment =====
if exist venv\Scripts\python.exe (
  echo Existing venv found. Checking it...
  venv\Scripts\python.exe -c "import sys; print(sys.version)" >nul 2>nul
  if errorlevel 1 (
    echo The old venv is broken. Rebuilding it.
    rmdir /s /q venv
  )
)
if not exist venv\Scripts\python.exe (
  %PYCMD% -m venv venv
  if errorlevel 1 ( echo ERROR: could not create venv & pause & exit /b 1 )
)

echo.
echo ===== Backend: installing packages =====
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r backend\requirements.txt
if errorlevel 1 (
  echo Pinned versions failed. Trying the latest compatible versions instead...
  venv\Scripts\python.exe -m pip install flask flask-cors numpy joblib scikit-learn
  if errorlevel 1 ( echo ERROR: package install failed & pause & exit /b 1 )
)

echo.
echo ===== Frontend: installing packages =====
cd frontend
if exist node_modules\.bin\vite.cmd (
  echo node_modules looks installed.
) else (
  if exist node_modules rmdir /s /q node_modules
  call npm install
  if errorlevel 1 ( echo ERROR: npm install failed. Is Node.js 18+ installed? & pause & exit /b 1 )
)
cd ..

echo.
echo ===== Setup finished. Now double-click run.bat =====
pause
