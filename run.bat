@echo off
cd /d "%~dp0"
if not exist venv\Scripts\python.exe (
  echo Setup has not been run yet. Run setup.bat first.
  pause
  exit /b 1
)
if not exist frontend\node_modules (
  echo Frontend packages are missing. Run setup.bat first.
  pause
  exit /b 1
)
echo Starting backend (wait for "Running on http://127.0.0.1:5000" - the first start can take a minute)...
start "EEG Backend" /D "%~dp0" cmd /k venv\Scripts\python.exe backend\app.py
echo Starting frontend...
start "EEG Frontend" /D "%~dp0frontend" cmd /k npm run dev
timeout /t 10 >nul
start "" http://localhost:5173
echo.
echo Two windows opened (Backend and Frontend). Close them to stop the project.
