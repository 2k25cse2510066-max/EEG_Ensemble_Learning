# EEG State Classifier: frontend

React 19 + Vite dashboard for the Extra Trees EEG classifier. No new dependencies were added to the original template.

## Run

```bash
cd frontend
npm install        # first time only
npm run dev        # http://localhost:5173
npm run build      # production build into dist/
npm run lint       # oxlint
```

The UI calls the Flask backend at `http://localhost:5000` (`GET /` for health, `POST /api/predict`).
To use another address, copy `.env.example` to `.env.local` and set `VITE_API_BASE_URL`.

## Structure

```
src/
  App.jsx                 shell: sidebar, hash routing, focus management
  config.js               API base URL and endpoints
  pages/                  Overview, Analyze, Performance, Methodology
  components/
    analyze/              FeatureForm, FeatureField, ResultPanel
    charts/               BandSignature, ProbabilityBars, AccuracyBars, RankedBars, ConfusionMatrix (plain SVG/CSS)
    layout/               Sidebar, ResearchNotice
    ui/                   Button, Panel, Stat, Alert, Badge, ClassTag, Icon, Spinner
  hooks/                  useBackendStatus, usePrediction, useHashRoute
  services/api.js         fetch wrappers and typed errors
  utils/                  validation, formatting
  constants/              feature definitions, class display metadata, navigation
  data/projectData.js     GENERATED, see below
  styles/                 tokens, base, layout, ui, charts, pages
```

## Generated data

Static figures (cross-validation, confusion matrix, feature importance, dataset statistics, example rows) come from
the project's result files. After retraining, regenerate them from the project root:

```bash
python tools/generate_frontend_data.py
```

The script refuses to run if the headline CV accuracy in `final_model_information.csv` disagrees with
`systematic_model_comparison.csv`.

## Motion and interactivity

- Count-up KPIs, staged page entrance, animated bars/ring (all disabled for `prefers-reduced-motion`).
- Spectral explorer (Overview): hover or pin a class, switch between bars and radar.
- Live band profile (Analyze): band shares update as you type; optional class-median reference marks.
- Confusion matrix: hover or focus a cell to read it in words.
- Cursor-reactive card lighting and an ambient background. The wave beside the Overview title is decorative, not EEG data.
