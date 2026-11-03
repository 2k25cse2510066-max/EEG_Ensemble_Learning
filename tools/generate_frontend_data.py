"""
Generate frontend/src/data/projectData.js from the project's own artifacts.

Every figure shown on the dashboard's static pages (evaluation metrics,
confusion matrix, feature importance, dataset statistics, ...) is read from
the CSV files produced by the training / evaluation scripts, so nothing is
typed in by hand. Re-run this script after retraining:

    python tools/generate_frontend_data.py

Requires: pandas, numpy (already used by the project).
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "frontend" / "src" / "data" / "projectData.js"

ORIGINAL_FEATURES = [
    "mean", "std", "variance", "minimum", "maximum", "range", "rms",
    "skewness", "kurtosis", "delta_power", "theta_power", "alpha_power",
    "beta_power", "gamma_power", "total_power",
]
BANDS = ["delta", "theta", "alpha", "beta", "gamma"]


def r(value, digits=4):
    return round(float(value), digits)


# ---------------------------------------------------------------- dataset
raw = pd.read_csv(BASE / "dataset" / "EEG_Extracted_Features.csv")
eng = pd.read_csv(BASE / "dataset" / "EEG_Engineered_Features.csv")
classes = sorted(raw["Label"].unique())

feature_stats = {}
for f in ORIGINAL_FEATURES:
    col = raw[f]
    feature_stats[f] = {
        "min": float(col.min()),
        "p25": float(col.quantile(0.25)),
        "median": float(col.median()),
        "p75": float(col.quantile(0.75)),
        "max": float(col.max()),
    }

class_counts = {c: int((raw["Label"] == c).sum()) for c in classes}

# Median relative band power per class (from the engineered ratio columns).
band_signature = {
    c: {
        b: r(eng.loc[eng["Label"] == c, f"{b}_ratio"].median())
        for b in BANDS
    }
    for c in classes
}

# One representative real row per class: the row closest to the class median
# in a robust (median / IQR) standardised space. These are TRAINING rows.
iqr = (raw[ORIGINAL_FEATURES].quantile(0.75) - raw[ORIGINAL_FEATURES].quantile(0.25)).replace(0, 1)
examples = {}
for c in classes:
    sub = raw[raw["Label"] == c]
    med = sub[ORIGINAL_FEATURES].median()
    dist = (((sub[ORIGINAL_FEATURES] - med) / iqr) ** 2).sum(axis=1)
    row = sub.loc[dist.idxmin()]
    examples[c] = {f: float(row[f]) for f in ORIGINAL_FEATURES}

# ------------------------------------------------------------------ model
info = pd.read_csv(BASE / "results" / "final_model" / "final_model_information.csv")
model_info = dict(zip(info["Parameter"], info["Value"]))

# ------------------------------------------------- verify the headline CV
sysm = pd.read_csv(BASE / "results" / "systematic_evaluation" / "systematic_model_comparison.csv")
et = sysm[sysm["Model"] == "Extra Trees Baseline"].iloc[0]
cv_mean = round(float(et["Accuracy_Mean"]) * 100, 2)
cv_std = round(float(et["Accuracy_STD"]) * 100, 2)
claimed = model_info["CV Accuracy"].replace(" ", "")
computed = f"{cv_mean:.2f}%+/-{cv_std:.2f}%"
if claimed != computed:
    raise SystemExit(f"CV accuracy mismatch: model info says {claimed}, results CSV says {computed}")
print(f"Verified 10-fold CV accuracy: {cv_mean:.2f}% +/- {cv_std:.2f}%")

holdout = float(model_info["Holdout Accuracy"].strip("%"))
cv_models = [
    {
        "model": row["Model"],
        "mean": r(row["Accuracy_Mean"] * 100, 2),
        "std": r(row["Accuracy_STD"] * 100, 2),
    }
    for _, row in sysm.iterrows()
]
bench = pd.read_csv(BASE / "results" / "model_benchmark_results.csv")
benchmark = [
    {"model": row["Model"], "mean": r(row["Mean Accuracy"], 2), "std": r(row["Std"], 2)}
    for _, row in bench.iterrows()
]

# ----------------------------------------------------- holdout evaluation
cm = pd.read_csv(BASE / "results" / "final_evaluation" / "extra_trees_confusion_matrix.csv", index_col=0)
cm_classes = list(cm.columns)
confusion = cm.values.astype(int).tolist()

rep = pd.read_csv(BASE / "results" / "final_evaluation" / "extra_trees_classification_report.csv", index_col=0)
per_class = [
    {
        "class": c,
        "precision": r(rep.loc[c, "precision"]),
        "recall": r(rep.loc[c, "recall"]),
        "f1": r(rep.loc[c, "f1-score"]),
        "support": int(rep.loc[c, "support"]),
    }
    for c in cm_classes
]
macro = {
    "precision": r(rep.loc["macro avg", "precision"]),
    "recall": r(rep.loc["macro avg", "recall"]),
    "f1": r(rep.loc["macro avg", "f1-score"]),
}

# -------------------------------------------------- feature importance
imp = pd.read_csv(BASE / "results" / "final_model" / "final_feature_importance.csv")
importance = [
    {
        "feature": row["Feature"],
        "importance": r(row["Importance"], 5),
        "derived": row["Feature"] not in ORIGINAL_FEATURES,
    }
    for _, row in imp.iterrows()
]

data = {
    "dataset": {
        "samples": int(len(raw)),
        "classes": classes,
        "classCounts": class_counts,
        "originalFeatureCount": len(ORIGINAL_FEATURES),
        "engineeredFeatureCount": int(eng.shape[1] - 1),
        "missingValues": int(raw.isna().sum().sum()),
        "duplicateRows": int(raw.duplicated().sum()),
        "featureStats": feature_stats,
        "bandSignature": band_signature,
        "examples": examples,
    },
    "model": {
        "info": model_info,
        "cvMean": cv_mean,
        "cvStd": cv_std,
        "holdoutAccuracy": holdout,
        "trainingSamples": int(model_info["Training Samples"]),
        "featureCount": int(model_info["Number of Features"]),
    },
    "evaluation": {
        "cvModels": cv_models,
        "benchmark": benchmark,
        "confusionClasses": cm_classes,
        "confusion": confusion,
        "perClass": per_class,
        "macro": macro,
        "holdoutSupport": int(rep.loc["macro avg", "support"]),
        "importance": importance,
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    "// Generated by tools/generate_frontend_data.py from the project's result files.\n"
    "// Do not edit by hand; re-run the script after retraining.\n\n"
    f"export const projectData = {json.dumps(data, indent=2)}\n",
    encoding="utf-8",
)
print("Wrote", OUT.relative_to(BASE))
