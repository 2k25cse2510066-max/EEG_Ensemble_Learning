from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import os

app = Flask(__name__)

# Deployment: set ALLOWED_ORIGINS to your frontend URL(s), comma-separated
# (e.g. https://my-eeg-app.vercel.app). Unset = allow any origin (local development).
_origins = os.environ.get("ALLOWED_ORIGINS", "*")
CORS(app, origins=[o.strip() for o in _origins.split(",") if o.strip()])

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "extra_trees_final.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "label_encoder.pkl"
)

FEATURE_NAMES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "feature_names.csv"
)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


# --------------------------------------------------
# Original 15 EEG features
# --------------------------------------------------

ORIGINAL_FEATURES = [
    "mean",
    "std",
    "variance",
    "minimum",
    "maximum",
    "range",
    "rms",
    "skewness",
    "kurtosis",
    "delta_power",
    "theta_power",
    "alpha_power",
    "beta_power",
    "gamma_power",
    "total_power"
]


# --------------------------------------------------
# Feature Engineering
# Same logic used during model training
# --------------------------------------------------

def engineer_features(data):

    eps = 1e-10

    mean = data["mean"]
    std = data["std"]
    variance = data["variance"]
    minimum = data["minimum"]
    maximum = data["maximum"]
    range_value = data["range"]
    rms = data["rms"]

    delta = data["delta_power"]
    theta = data["theta_power"]
    alpha = data["alpha_power"]
    beta = data["beta_power"]
    gamma = data["gamma_power"]
    total = data["total_power"]

    engineered = {
        "mean": mean,
        "std": std,
        "variance": variance,
        "minimum": minimum,
        "maximum": maximum,
        "range": range_value,
        "rms": rms,
        "skewness": data["skewness"],
        "kurtosis": data["kurtosis"],

        "delta_power": delta,
        "theta_power": theta,
        "alpha_power": alpha,
        "beta_power": beta,
        "gamma_power": gamma,
        "total_power": total,

        "delta_ratio": delta / (total + eps),
        "theta_ratio": theta / (total + eps),
        "alpha_ratio": alpha / (total + eps),
        "beta_ratio": beta / (total + eps),
        "gamma_ratio": gamma / (total + eps),

        "theta_alpha_ratio": theta / (alpha + eps),
        "delta_alpha_ratio": delta / (alpha + eps),
        "delta_beta_ratio": delta / (beta + eps),
        "theta_beta_ratio": theta / (beta + eps),

        # NOTE: these two are sums in preprocessing/feature_engineering.py
        # (the training data), so they must be sums here as well.
        "delta_theta_power": delta + theta,
        "alpha_beta_power": alpha + beta,

        "delta_alpha_difference": delta - alpha,
        "theta_alpha_difference": theta - alpha,
        "beta_gamma_difference": beta - gamma
    }

    return engineered


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "running",
        "message": "EEG AI Prediction Backend is running"
    })


# --------------------------------------------------
# Prediction API
# --------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def predict():

    try:

        request_data = request.get_json()

        if not request_data:
            return jsonify({
                "error": "No input data received"
            }), 400

        # Check all 15 original features
        missing_features = [
            feature
            for feature in ORIGINAL_FEATURES
            if feature not in request_data
        ]

        if missing_features:
            return jsonify({
                "error": "Missing features",
                "missing": missing_features
            }), 400

        # Convert values to float
        data = {}

        for feature in ORIGINAL_FEATURES:

            try:
                data[feature] = float(request_data[feature])

            except (ValueError, TypeError):

                return jsonify({
                    "error": f"Invalid value for feature: {feature}"
                }), 400

        # Create engineered features
        engineered = engineer_features(data)

        # Convert to model input
        feature_vector = np.array([
            engineered[feature]
            for feature in engineered.keys()
        ]).reshape(1, -1)

        # Prediction
        prediction_encoded = model.predict(feature_vector)[0]

        prediction_label = label_encoder.inverse_transform(
            [prediction_encoded]
        )[0]

        # Probability
        probabilities = model.predict_proba(feature_vector)[0]

        max_probability = float(np.max(probabilities) * 100)

        # Class probabilities
        class_probabilities = {}

        for class_name, probability in zip(
            label_encoder.classes_,
            probabilities
        ):
            class_probabilities[class_name] = round(
                float(probability * 100),
                2
            )

        return jsonify({

            "success": True,

            "prediction": prediction_label,

            "probability": round(
                max_probability,
                2
            ),

            "class_probabilities": class_probabilities

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Run Server
# --------------------------------------------------

if __name__ == "__main__":

    # Local development only. In production the host runs: gunicorn --chdir backend app:app
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
        use_reloader=False  # the reloader loads the model twice and scans every venv file; slow on Windows
    )
