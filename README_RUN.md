# Running the EEG State Classifier (Windows)

## Easiest way
1. Extract this folder somewhere with a SHORT path, for example `C:\EEG` (not inside OneDrive or Desktop).
2. Double-click **setup.bat** and wait until it says "Setup finished". Do this once. It can take several minutes.
3. Double-click **run.bat**. Two windows open (backend and frontend) and your browser opens http://localhost:5173.

Requirements: Python 3.12 or 3.13 (3.14 may lack ready-made packages), and Node.js 18 or newer.

## Manual way
```powershell
# Terminal 1: backend
cd C:\EEG\EEG_Ensemble_Learning
py -3.13 -m venv venv
venv\Scripts\python.exe -m pip install -r backend\requirements.txt
venv\Scripts\python.exe backend\app.py        # wait for: Running on http://127.0.0.1:5000

# Terminal 2: frontend
cd C:\EEG\EEG_Ensemble_Learning\frontend
npm install
npm run dev                                    # open http://localhost:5173
```

## If something goes wrong
- **Looks frozen / KeyboardInterrupt**: do not press Ctrl+C. The first start is slow while Windows Defender scans new
  files. Add the project folder as a Defender exclusion (Windows Security > Virus & threat protection > Manage settings >
  Exclusions) and keep it out of OneDrive.
- **Two Pythons**: a venv only works with the Python it was created with. Never copy a venv between PCs or after
  upgrading Python. Delete the `venv` folder and run setup.bat again.
- **"Failed to resolve import ..."**: some files did not extract. Re-extract the ZIP with 7-Zip or
  `tar -xf file.zip`, not by dragging files out of Explorer's preview.
- **Sidebar says "Backend unreachable"**: the backend window is not running or is still loading.

## Backend changes
- `delta_theta_power` and `alpha_beta_power` are now sums, matching `preprocessing/feature_engineering.py`.
- The Flask auto-reloader is off (`use_reloader=False`). The API is otherwise unchanged. Restart the backend window
  yourself after editing `backend/app.py`.

## New interface (v2)
The frontend now uses a dark glass dashboard. Nothing changed in the backend or the API.
- **Overview**: drag the brain to rotate it, use + / - / target to zoom and reset. Pick a class from the menu or the
  slider at the bottom (or press the play button for an automatic tour). Everything on the page follows that class.
- **Analyze**: the brain next to the result glows in the colour of the predicted class.
- **Methods**: the spectral explorer (bars / radar) now lives here.
- Fonts are bundled (Poppins), so the UI works offline. Reduced-motion settings are respected.
- The brain and wave animations are illustrations. The numbers beside them are measured from the training data.
