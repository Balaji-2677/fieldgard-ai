# 🌾 Crop Yield AI - Smart Agricultural Yield Prediction Platform

An end-to-end Machine Learning web application designed for farmers, agronomists, and agricultural researchers to accurately predict seasonal crop yields, evaluate soil/weather compatibility, and access actionable agronomic advice.

---

## 🌟 Key Features

1. **Precision Machine Learning Pipeline**:
   - Trained on realistic agricultural data with **98.69% $R^2$ accuracy** using a Scikit-Learn Random Forest ensemble pipeline.
   - Takes multi-factor inputs: `Crop`, `State/Region`, `Season`, `Soil Type`, `Land Area`, `Seasonal Rainfall`, `Average Temperature`, `Fertilizer Application (NPK)`, and `Pesticide Usage`.

2. **Farmer-Centric Result Insights**:
   - **Dual Unit Conversions**: Seamlessly toggle land area between **Hectares** and **Acres**.
   - Yield outputs displayed in both **Tonnes / Hectare** and **Quintals / Acre**.
   - **Total Farm Output**: Computes total expected production (in Tonnes and Quintals) based on the farm size.
   - **Yield Health Indicator**: Categorizes harvest projections into *Optimal 🌟*, *Good ✅*, or *Sub-optimal ⚠️* against regional benchmarks.
   - **Soil & Climate Suitability Analysis**: Automated warnings for heat stress, water deficits, and soil incompatibility.
   - **Agronomic Recommendations**: Tailored tips on irrigation scheduling, fertilizer splits, and pest monitoring.
   - **Printable Farmer Yield Card**: Instant one-click print or save-as-PDF summary for banks, Kisan Credit Card applications, or agricultural extension officers.

3. **Interactive Farm Analytics Dashboard**:
   - Built with **Chart.js**:
     - *Crop Yield Bar Chart*: Compare average harvest productivity across crops.
     - *Soil Suitability Doughnut Chart*: Visualize soil type distributions.
     - *Rainfall vs. Yield Correlation Scatter Plot*: Analyze the impact of water availability on production.
   - **Historical Field Logs Table**: Instant real-time search, crop filtering, and record deletion.
   - **CSV Export**: One-click download of all historical predictions for spreadsheet analysis.

4. **Farmer Support & Helplines**:
   - Direct directory to national agricultural helplines (Kisan Call Center: `1800-180-1551`, PM Fasal Bima Yojana: `14447`, Soil Health Card Scheme).
   - Interactive feedback and variety inquiry form.

---

## 📂 Project Architecture

```
🌾 Crop Yield Prediction Website/
│
├── app.py                      # Flask Application server & REST API
├── database.py                 # SQLite database persistence layer (crop_yield.db)
├── requirements.txt            # Python dependencies
├── run.bat                     # Easy Windows one-click launcher
├── test_app.py                 # Automated unit and integration test suite
│
├── data/
│   ├── generate_dataset.py     # Agricultural dataset generator (ICAR/DES calibrated)
│   └── crop_yield_data.csv     # 4,800 records across 12 crops, 12 states, 4 seasons
│
├── ml/
│   ├── train_model.py          # Random Forest Pipeline training & evaluation script
│   └── agronomy_engine.py      # Rules-based agronomic advisory & unit conversions
│
├── models/
│   ├── crop_yield_model.pkl    # Serialized Scikit-learn Pipeline
│   └── model_metadata.json     # Feature mappings, metadata & evaluation metrics
│
├── templates/
│   ├── base.html               # Base layout with navbar, footer & farmer helpline banner
│   ├── index.html              # Landing page (hero, problem vs solution, 3-step guide)
│   ├── predict.html            # Prediction interface, demo presets, dynamic result card
│   ├── dashboard.html          # Historical logs, Chart.js analytics & CSV export
│   ├── about.html              # AI model architecture, metrics, and farmer FAQs
│   └── contact.html            # Official government farmer helplines & feedback form
│
└── static/
    ├── css/
    │   └── style.css           # Modern agricultural design system & print stylesheet
    └── js/
        ├── main.js             # Mobile nav toggles & toast alerts
        ├── predict.js          # Async form submission, unit toggle, demo presets
        └── dashboard.js        # Chart.js initialization & live table filtering
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Web browser (Chrome, Edge, Firefox)

### 2. Quick Launch (Windows)
Double-click the **`run.bat`** file in the project folder, or run:
```powershell
.\.venv\Scripts\python.exe app.py
```

### 3. Open in Browser
Visit **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 🧪 Retraining the Model (Optional)

If you wish to re-generate the dataset or retrain the model with custom parameters:

```powershell
# 1. Re-generate dataset
.\.venv\Scripts\python.exe data\generate_dataset.py

# 2. Retrain Machine Learning Model
.\.venv\Scripts\python.exe ml\train_model.py
```

---

## 📊 Model Evaluation Results

- **Model Type**: Random Forest Regressor Ensemble (160 estimators, max depth 18)
- **Data Preprocessing**: `ColumnTransformer` (OneHotEncoder for categorical features + StandardScaler for numerical features)
- **$R^2$ Score**: **0.9869 (98.69%)**
- **Mean Absolute Error (MAE)**: **0.82 tonnes/hectare**
- **Root Mean Squared Error (RMSE)**: **1.91 tonnes/hectare**
- **Mean Absolute Percentage Error (MAPE)**: **10.34%**

---

## 🌾 Supported Crops
- **Cereals / Grains**: Rice, Wheat, Maize, Millets (Bajra/Jowar)
- **Cash & Commercial Crops**: Cotton, Sugarcane
- **Pulses & Legumes**: Chickpea (Gram), Soybean
- **Oilseeds**: Groundnut, Mustard
- **Vegetables / Horticulture**: Potato, Tomato
