from flask import Blueprint, render_template, request
from flask_login import login_required
import joblib
import numpy as np
from utils.history import save_prediction_history

breast_routes = Blueprint('breast_routes', __name__)

# Load models
detection_model = joblib.load("models/breast/breast_cancer__model.pkl")
stage_model = joblib.load("models/breast/breast_stage_model.pkl")

@breast_routes.route("/")
@login_required
def breast_home():
    """
    Render the Breast Cancer Prediction form.
    """
    return render_template("breast.html")

@breast_routes.route("/predict", methods=["POST"])
@login_required
def predict_breast():
    feature_keys = [
        "radius_mean", "texture_mean", "perimeter_mean", "area_mean",
        "smoothness_mean", "compactness_mean", "concavity_mean",
        "concave_points_mean", "symmetry_mean", "radius_worst",
        "texture_worst", "perimeter_worst", "area_worst",
        "smoothness_worst", "compactness_worst"
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

        # Make predictions
        cancer_prediction = detection_model.predict(features_array)[0]
        stage_prediction = stage_model.predict(features_array)[0]
        save_prediction_history(
            "Breast Cancer",
            dict(zip(feature_keys, features)),
            cancer_prediction,
            stage_prediction,
        )

        # Send results to result page
        return render_template(
            "result.html",
            cancer=cancer_prediction,
            stage=stage_prediction,
            disease="Breast Cancer",
        )
    except ValueError:
        return render_template(
            "error.html",
            message="Please enter valid numeric values for all breast cancer inputs."
        )
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {str(e)}")
