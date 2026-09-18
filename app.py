"""
Crop Yield Prediction Web Application
Production-grade Flask server with ML pipeline inference, SQLite history, and farmer advisory.
"""

import csv
import io
import json
import os
import sys

# Configure UTF-8 encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from functools import wraps
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    Response,
    session,
    url_for,
)
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd

import database
from ml.agronomy_engine import analyze_crop_prediction, AGRONOMIC_KNOWLEDGE
from ml.ai_assistant import answer_farming_doubt

app = Flask(__name__)
app.config["SECRET_KEY"] = "crop-yield-farmer-ai-2026-secret"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_yield_model.pkl")
METADATA_PATH = os.path.join(BASE_DIR, "models", "model_metadata.json")

# Complete List of 28 States and 8 Union Territories in India
ALL_INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

# Global ML model and metadata
ml_model = None
model_metadata = {}


def load_ml_resources():
    global ml_model, model_metadata
    if os.path.exists(MODEL_PATH):
        try:
            ml_model = joblib.load(MODEL_PATH)
            print(f"✅ ML Model loaded successfully from {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error loading ML model: {e}")
    else:
        print(f"⚠️ Model file not found at {MODEL_PATH}. Please run ml/train_model.py")

    if os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                model_metadata = json.load(f)
            print(f"✅ Model metadata loaded successfully.")
        except Exception as e:
            print(f"❌ Error loading metadata: {e}")


# Initialize Database and ML resources on startup
database.init_db()
load_ml_resources()


def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in or register to use the Crop Yield Predictor.", "error")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# ---------------- PAGE ROUTES ---------------- #

@app.route("/")
def index():
    """Home / Landing page."""
    stats = database.get_stats()
    metrics = model_metadata.get("metrics", {})
    return render_template(
        "index.html",
        stats=stats,
        metrics=metrics,
        crops_count=len(model_metadata.get("options", {}).get("crops", [])),
    )


# ---------------- AUTHENTICATION ROUTES ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    """Farmer Account Registration."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        phone = request.form.get("phone", "").strip()
        state = request.form.get("state", "").strip()
        farm_size = request.form.get("farm_size", "2.0")

        if not name or not email or not password:
            flash("Please fill in all required fields.", "error")
            return render_template("register.html", states=model_metadata.get("options", {}).get("states", []))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template("register.html", states=model_metadata.get("options", {}).get("states", []))

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("register.html", states=model_metadata.get("options", {}).get("states", []))

        existing = database.get_user_by_email(email)
        if existing:
            flash("An account with this email already exists. Please log in.", "error")
            return redirect(url_for("login"))

        password_hash = generate_password_hash(password)
        user_id = database.create_user(
            name=name,
            email=email,
            password_hash=password_hash,
            phone=phone,
            state=state,
            farm_size_ha=farm_size,
        )

        session["user_id"] = user_id
        session["user_name"] = name
        session["user_email"] = email
        session["user_state"] = state

        flash(f"Welcome to CropYield AI, {name}! Your account is now active.", "success")
        return redirect(url_for("predict_page"))

    states = model_metadata.get("options", {}).get("states", ALL_INDIAN_STATES)
    return render_template("register.html", states=states)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Farmer Login."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        next_url = request.args.get("next")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template("login.html")

        user = database.get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password. Please try again.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        session["user_state"] = user["state"]

        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(next_url or url_for("predict_page"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log out current user."""
    user_name = session.get("user_name")
    session.clear()
    if user_name:
        flash(f"Goodbye, {user_name}. You have been logged out.", "info")
    return redirect(url_for("index"))


# ---------------- AI ASSISTANT ROUTES ---------------- #

@app.route("/assistant")
def assistant_page():
    """Kisan AI Assistant consultation page."""
    return render_template("assistant.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """AI Assistant NLP Chat Endpoint."""
    data = request.get_json(silent=True) or request.form.to_dict()
    message = data.get("message", "").strip() if data else ""
    if not message:
        return jsonify({"success": False, "error": "Message cannot be empty."}), 400

    user_name = session.get("user_name", "Farmer")
    res = answer_farming_doubt(message, user_name=user_name)
    return jsonify({
        "success": True,
        "reply": res["reply"],
        "suggestions": res.get("suggestions", [])
    })


@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    """Crop Yield Prediction interface and dual POST endpoint."""
    if request.method == "POST":
        return api_predict()

    # Require registration / login to access prediction form
    if "user_id" not in session:
        flash("Please log in or register to use the Crop Yield Predictor.", "info")
        return redirect(url_for("login", next=request.url))

    options = model_metadata.get(
        "options",
        {
            "crops": sorted(list(AGRONOMIC_KNOWLEDGE.keys())),
            "states": ALL_INDIAN_STATES,
            "seasons": ["Kharif", "Rabi", "Zaid", "Whole Year"],
            "soils": ["Alluvial", "Black", "Red", "Clayey", "Sandy Loam", "Laterite"],
        },
    )
    return render_template(
        "predict.html",
        options=options,
        agri_knowledge=AGRONOMIC_KNOWLEDGE,
    )


@app.route("/dashboard")
def dashboard_page():
    """Historical Dashboard, Visual Analytics, and Location Map."""
    stats = database.get_stats()
    user_id = session.get("user_id")
    history = database.get_history(limit=50, user_id=user_id) if user_id else database.get_history(limit=50)
    crops = model_metadata.get("options", {}).get("crops", list(AGRONOMIC_KNOWLEDGE.keys()))
    metrics = model_metadata.get("metrics", {})
    return render_template(
        "dashboard.html",
        stats=stats,
        history=history,
        crops=crops,
        metrics=metrics,
    )


@app.route("/about")
def about_page():
    """About page explaining AI methodology, dataset, and accuracy."""
    metrics = model_metadata.get("metrics", {})
    return render_template("about.html", metrics=metrics, metadata=model_metadata)


@app.route("/contact")
def contact_page():
    """Farmer assistance, government helpline numbers, and feedback."""
    return render_template("contact.html")


@app.route("/how-to-use")
def how_to_use_page():
    """Step-by-step user guide on how to use CropYield AI website."""
    crops_count = len(model_metadata.get("options", {}).get("crops", list(AGRONOMIC_KNOWLEDGE.keys())))
    states_count = len(model_metadata.get("options", {}).get("states", ALL_INDIAN_STATES))
    return render_template("how_to_use.html", crops_count=crops_count, states_count=states_count)


# ---------------- API ENDPOINTS ---------------- #

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    Inference endpoint:
    Accepts JSON farm parameters, validates all inputs, runs model prediction,
    executes agronomic advisory, and saves to database.
    """
    global ml_model
    if ml_model is None:
        return jsonify({"success": False, "error": "ML model is not loaded."}), 500

    try:
        data = request.get_json(silent=True) or request.form.to_dict()

        if not data:
            return jsonify({
                "success": False,
                "error": "Please enter all required information."
            }), 400

        # Retrieve parameters with support for shorthand or full field names
        raw_rain = data.get("rainfall_mm") if "rainfall_mm" in data else data.get("rainfall")
        raw_temp = data.get("temp_c") if "temp_c" in data else data.get("temperature")
        raw_area = data.get("area_ha") if "area_ha" in data else data.get("area")
        raw_fert = data.get("fertilizer_kg") if "fertilizer_kg" in data else data.get("fertilizer")
        raw_pest = data.get("pesticide_kg") if "pesticide_kg" in data else data.get("pesticide")

        # Test 2: Check for missing or empty mandatory inputs
        if raw_rain is None or raw_temp is None or raw_area is None:
            return jsonify({
                "success": False,
                "error": "Please enter all required information."
            }), 400

        if str(raw_rain).strip() == "" or str(raw_temp).strip() == "" or str(raw_area).strip() == "":
            return jsonify({
                "success": False,
                "error": "Please enter all required information."
            }), 400

        # Numerical conversion & validation
        try:
            rainfall_mm = float(raw_rain)
            temp_c = float(raw_temp)
            area_ha = float(raw_area)
            fertilizer_kg = float(raw_fert) if raw_fert is not None and str(raw_fert).strip() != "" else 125.0
            pesticide_kg = float(raw_pest) if raw_pest is not None and str(raw_pest).strip() != "" else 1.5
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "Please enter valid numeric values for rainfall, temperature, and area."
            }), 400

        # Test 3: Validate negative / out-of-bound values
        if rainfall_mm < 0:
            return jsonify({
                "success": False,
                "error": "Invalid input: Rainfall cannot be negative."
            }), 400

        if area_ha <= 0:
            return jsonify({
                "success": False,
                "error": "Invalid input: Farm area must be greater than zero."
            }), 400

        if temp_c < -15 or temp_c > 65:
            return jsonify({
                "success": False,
                "error": "Invalid input: Temperature must be between -15°C and 65°C."
            }), 400

        if fertilizer_kg < 0 or pesticide_kg < 0:
            return jsonify({
                "success": False,
                "error": "Invalid input: Fertilizer and pesticide amounts cannot be negative."
            }), 400

        # Defaults for categorical variables if shorthand input is supplied
        crop = str(data.get("crop", "Rice")).strip() or "Rice"
        state = str(data.get("state", "Punjab")).strip() or "Punjab"
        season = str(data.get("season", "Kharif")).strip() or "Kharif"
        soil_type = str(data.get("soil_type", "Clayey")).strip() or "Clayey"
        farmer_name = str(data.get("farmer_name", "Farmer")).strip() or "Farmer"
        notes = str(data.get("notes", "")).strip()

        # Construct DataFrame for Model Pipeline
        input_df = pd.DataFrame([{
            "Crop": crop,
            "State": state,
            "Season": season,
            "Soil_Type": soil_type,
            "Area_Hectares": area_ha,
            "Rainfall_mm": rainfall_mm,
            "Temperature_Celsius": temp_c,
            "Fertilizer_kg_per_ha": fertilizer_kg,
            "Pesticide_kg_per_ha": pesticide_kg,
        }])

        # Perform ML Model Inference
        raw_prediction = float(ml_model.predict(input_df)[0])
        predicted_yield = max(0.1, round(raw_prediction, 2))
        total_production = round(predicted_yield * area_ha, 2)

        # Generate Agronomic Analysis and Advisory
        agri_analysis = analyze_crop_prediction(
            crop=crop,
            season=season,
            soil=soil_type,
            rainfall=rainfall_mm,
            temp=temp_c,
            fertilizer=fertilizer_kg,
            predicted_yield=predicted_yield,
            area=area_ha,
        )

        # Save to SQLite Database
        user_id = session.get("user_id")
        db_record = {
            "farmer_name": farmer_name if farmer_name != "Farmer" else (session.get("user_name") or "Farmer"),
            "state": state,
            "crop": crop,
            "season": season,
            "soil_type": soil_type,
            "area_ha": area_ha,
            "rainfall_mm": rainfall_mm,
            "temp_c": temp_c,
            "fertilizer_kg": fertilizer_kg,
            "pesticide_kg": pesticide_kg,
            "predicted_yield_t_ha": predicted_yield,
            "total_production_tonnes": total_production,
            "yield_status": agri_analysis["status"],
            "notes": notes,
        }
        saved_id = database.save_prediction(db_record, user_id=user_id)

        return jsonify({
            "success": True,
            "prediction": predicted_yield,
            "predicted_yield": predicted_yield,
            "predicted_yield_t_ha": predicted_yield,
            "unit": "tonnes/hectare",
            "total_production_tonnes": total_production,
            "prediction_id": saved_id,
            "analysis": agri_analysis,
        })

    except Exception as e:
        return jsonify({"success": False, "error": f"Prediction failed: {str(e)}"}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    """Retrieve filtered prediction logs."""
    crop_filter = request.args.get("crop", None)
    search_query = request.args.get("search", None)
    limit = int(request.args.get("limit", 50))
    records = database.get_history(limit=limit, crop_filter=crop_filter, search_query=search_query)
    return jsonify({"success": True, "records": records})


@app.route("/api/stats", methods=["GET"])
def api_stats():
    """Retrieve statistical aggregations for Chart.js."""
    stats = database.get_stats()
    return jsonify({"success": True, "stats": stats})


@app.route("/api/delete/<int:pred_id>", methods=["POST", "DELETE"])
def api_delete(pred_id):
    """Delete a prediction record."""
    try:
        database.delete_prediction(pred_id)
        return jsonify({"success": True, "message": f"Record #{pred_id} deleted."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/export-csv")
def api_export_csv():
    """Export all predictions to a downloadable CSV file."""
    columns, rows = database.get_all_for_csv()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    for row in rows:
        writer.writerow(list(row))
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=crop_yield_predictions.csv"}
    )


@app.route("/api/crop-defaults/<crop_name>")
def api_crop_defaults(crop_name):
    """Returns typical/average agronomic values for autofilling forms."""
    crop_data = AGRONOMIC_KNOWLEDGE.get(crop_name)
    if not crop_data:
        return jsonify({"success": False, "error": "Crop not found"}), 404

    t_opt = crop_data["temp_opt"]
    r_opt = crop_data["rain_opt"]
    f_opt = crop_data["typical_fert"]

    defaults = {
        "season": crop_data["ideal_seasons"][0],
        "soil_type": crop_data["ideal_soils"][0],
        "rainfall_mm": round((r_opt[0] + r_opt[1]) / 2),
        "temp_c": round((t_opt[0] + t_opt[1]) / 2),
        "fertilizer_kg": round((f_opt[0] + f_opt[1]) / 2),
        "pesticide_kg": 1.5,
        "area_ha": 2.5
    }
    return jsonify({"success": True, "defaults": defaults})


if __name__ == "__main__":
    print("\n🌾 Starting Crop Yield Prediction Web App on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
