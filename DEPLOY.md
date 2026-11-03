# Deploying the EEG State Classifier

Backend (Flask + model) on **Render**, frontend (static React) on **Vercel**.

## 1. Push to GitHub
Make the `EEG_Ensemble_Learning` folder the root of a new repo (so `render.yaml` and `backend/` sit at the top level).
```bash
git init && git add . && git commit -m "EEG classifier" 
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git && git push -u origin main
```
The `.gitignore` keeps `venv`, `node_modules` and build output out. The model file (~26 MB) is committed normally.

## 2. Backend on Render
1. Render dashboard > **New > Blueprint** > pick your repo. It reads `render.yaml`.
2. When asked, set `ALLOWED_ORIGINS` to your frontend URL. If you don't have it yet, use `*` for now and tighten it in step 4.
3. Deploy. Open `https://<your-service>.onrender.com/`. You should see `{"status":"running", ...}`.

Manual alternative (no Blueprint): New > Web Service, Build `pip install -r backend/requirements-prod.txt`,
Start `gunicorn --chdir backend app:app --workers 1 --timeout 120`, env `PYTHON_VERSION=3.13.5`.

Keep the pinned versions in `backend/requirements.txt`: the model was pickled with scikit-learn 1.9.1.

## 3. Frontend on Vercel
1. Vercel > **Add New > Project** > import the same repo.
2. Set **Root Directory** to `frontend`. Vite is detected automatically (`vercel.json` also sets it).
3. Add environment variable `VITE_API_BASE_URL` = your Render URL (no trailing slash).
4. Deploy. Routing uses `#/` hashes, so no rewrites are needed.

## 4. Lock down CORS
In Render, set `ALLOWED_ORIGINS` to your exact Vercel URL (comma-separate several). Redeploy the backend.
`VITE_API_BASE_URL` is baked in at build time: if the backend URL changes, redeploy the frontend.

## 5. Check
Open the Vercel site. The top-bar chip should say **Backend online**, and Analyze > "Seizure" example > Run classifier should return a result.

## Notes
- Render's free plan sleeps after inactivity: the first request can take 30 to 60 seconds. The chip may say "offline" until it wakes; press it to re-check.
- Plans and limits change, so check Render's and Vercel's current free-tier terms.
- This is a research prototype. Don't present it as a diagnostic tool.
