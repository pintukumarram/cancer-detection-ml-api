from flask import Blueprint, render_template, request
from flask_login import login_required
import joblib
import numpy as np
from utils.history import save_prediction_history

# Define Blueprint
lung_routes = Blueprint('lung_routes', __name__)

# Load the models
lung_cancer_model = joblib.load("models/lung/lung_cancer_prediction_model.pkl")
lung_stage_model = joblib.load("models/lung/lung_stage_prediction_model.pkl")

@lung_routes.route("/")
@login_required
def lung_home():
    """Render the lung cancer prediction home page."""
    return render_template("lung.html")

@lung_routes.route("/predict", methods=["POST"])
@login_required
def predict_lung():
    """Handle lung cancer and stage predictions."""
    feature_keys = [
        "ALLERGY ",
        "ALCOHOL_CONSUMING",
        "wheezing",
        "swallowing_difficulty",
        "COUGHING",
    ]

    try:
        missing_fields = [key for key in feature_keys if key not in request.form]
        if missing_fields:
            return render_template(
                "error.html",
                message=f"Missing required fields: {', '.join(missing_fields)}"
            )

        features = [float(request.form[key]) for key in feature_keys]
        features_array = np.array([features])

        # Predictions
        cancer_prediction = lung_cancer_model.predict(features_array)[0]
        stage_prediction = lung_stage_model.predict(features_array)[0]
        save_prediction_history(
            "Lung Cancer",
            dict(zip(feature_keys, features)),
            cancer_prediction,
            stage_prediction,
        )

        # Render result page
        return render_template(
            "result.html",
            cancer=cancer_prediction,
            stage=stage_prediction,
            disease="Lung Cancer"
        )
    except ValueError:
        return render_template(
            "error.html",
            message="Please enter valid numeric values for all lung cancer inputs."
        )
    except Exception as e:
        # Render an error page in case of failure
        return render_template("error.html", message=str(e))
