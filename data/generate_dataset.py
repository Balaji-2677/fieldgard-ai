"""
Agricultural Dataset Generator for Real-World Crop Yield Prediction
Curated based on agricultural benchmarks (ICAR, Directorate of Economics and Statistics, MoAFW).
Covers ALL 28 States and 8 Union Territories of India, and 32 Major Indian Agricultural Crops.
"""

import os
import sys

# Configure UTF-8 encoding for standard output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd

# Define random seed for reproducibility
np.random.seed(42)

# All 28 States and 8 Union Territories of India (36 total)
ALL_STATES = [
    # 28 States
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    # 8 Union Territories
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

# 32 Major Agricultural Crops with Agronomic Profiles
CROP_PROFILES = {
    "Rice": {
        "seasons": ["Kharif", "Whole Year"],
        "soils": ["Clayey", "Alluvial"],
        "states": ["West Bengal", "Uttar Pradesh", "Punjab", "Andhra Pradesh", "Tamil Nadu", "Bihar", "Odisha", "Assam", "Chhattisgarh", "Kerala", "Telangana", "Tripura", "Puducherry"],
        "temp_range": (20, 37),
        "rain_range": (900, 2400),
        "base_yield": 3.6,
        "yield_std": 0.7,
        "opt_fert": 140,
        "opt_pest": 2.2,
    },
    "Wheat": {
        "seasons": ["Rabi"],
        "soils": ["Alluvial", "Sandy Loam"],
        "states": ["Uttar Pradesh", "Punjab", "Haryana", "Madhya Pradesh", "Rajasthan", "Bihar", "Gujarat", "Uttarakhand", "Himachal Pradesh", "Jammu and Kashmir", "Delhi", "Chandigarh"],
        "temp_range": (12, 26),
        "rain_range": (300, 750),
        "base_yield": 3.8,
        "yield_std": 0.65,
        "opt_fert": 130,
        "opt_pest": 1.5,
    },
    "Maize": {
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Alluvial", "Red", "Black"],
        "states": ["Karnataka", "Madhya Pradesh", "Maharashtra", "Bihar", "Rajasthan", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Odisha", "Jharkhand", "Himachal Pradesh"],
        "temp_range": (18, 34),
        "rain_range": (500, 1100),
        "base_yield": 3.5,
        "yield_std": 0.7,
        "opt_fert": 120,
        "opt_pest": 1.8,
    },
    "Cotton": {
        "seasons": ["Kharif"],
        "soils": ["Black", "Alluvial"],
        "states": ["Gujarat", "Maharashtra", "Telangana", "Andhra Pradesh", "Rajasthan", "Haryana", "Punjab", "Karnataka", "Madhya Pradesh", "Tamil Nadu", "Odisha"],
        "temp_range": (22, 36),
        "rain_range": (500, 1100),
        "base_yield": 1.9,
        "yield_std": 0.45,
        "opt_fert": 150,
        "opt_pest": 3.2,
    },
    "Sugarcane": {
        "seasons": ["Whole Year"],
        "soils": ["Alluvial", "Black", "Clayey"],
        "states": ["Uttar Pradesh", "Maharashtra", "Karnataka", "Tamil Nadu", "Bihar", "Gujarat", "Haryana", "Punjab", "Andhra Pradesh", "Telangana", "Uttarakhand"],
        "temp_range": (20, 36),
        "rain_range": (1100, 2300),
        "base_yield": 72.0,
        "yield_std": 10.5,
        "opt_fert": 220,
        "opt_pest": 3.5,
    },
    "Soybean": {
        "seasons": ["Kharif"],
        "soils": ["Black", "Clayey"],
        "states": ["Madhya Pradesh", "Maharashtra", "Rajasthan", "Karnataka", "Gujarat", "Telangana", "Chhattisgarh", "Jharkhand"],
        "temp_range": (20, 32),
        "rain_range": (600, 1150),
        "base_yield": 1.8,
        "yield_std": 0.35,
        "opt_fert": 90,
        "opt_pest": 1.6,
    },
    "Groundnut": {
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Sandy Loam", "Red"],
        "states": ["Gujarat", "Rajasthan", "Tamil Nadu", "Andhra Pradesh", "Karnataka", "Maharashtra", "Telangana", "Odisha"],
        "temp_range": (21, 33),
        "rain_range": (450, 950),
        "base_yield": 2.1,
        "yield_std": 0.45,
        "opt_fert": 85,
        "opt_pest": 1.7,
    },
    "Potato": {
        "seasons": ["Rabi"],
        "soils": ["Sandy Loam", "Alluvial"],
        "states": ["Uttar Pradesh", "West Bengal", "Bihar", "Gujarat", "Punjab", "Madhya Pradesh", "Assam", "Karnataka", "Himachal Pradesh", "Meghalaya"],
        "temp_range": (14, 25),
        "rain_range": (350, 700),
        "base_yield": 23.5,
        "yield_std": 4.2,
        "opt_fert": 180,
        "opt_pest": 2.5,
    },
    "Tomato": {
        "seasons": ["Rabi", "Kharif", "Zaid"],
        "soils": ["Sandy Loam", "Red", "Alluvial"],
        "states": ["Andhra Pradesh", "Madhya Pradesh", "Karnataka", "Gujarat", "Maharashtra", "Tamil Nadu", "Odisha", "Bihar", "Chhattisgarh", "Haryana", "Punjab"],
        "temp_range": (18, 32),
        "rain_range": (400, 850),
        "base_yield": 28.0,
        "yield_std": 5.5,
        "opt_fert": 160,
        "opt_pest": 2.8,
    },
    "Chickpea": {
        "seasons": ["Rabi"],
        "soils": ["Sandy Loam", "Clayey", "Black"],
        "states": ["Madhya Pradesh", "Maharashtra", "Rajasthan", "Uttar Pradesh", "Karnataka", "Gujarat", "Andhra Pradesh", "Haryana"],
        "temp_range": (14, 28),
        "rain_range": (300, 650),
        "base_yield": 1.4,
        "yield_std": 0.3,
        "opt_fert": 65,
        "opt_pest": 1.2,
    },
    "Mustard": {
        "seasons": ["Rabi"],
        "soils": ["Alluvial", "Sandy Loam"],
        "states": ["Rajasthan", "Haryana", "Madhya Pradesh", "Uttar Pradesh", "West Bengal", "Gujarat", "Assam", "Punjab", "Bihar"],
        "temp_range": (12, 26),
        "rain_range": (250, 600),
        "base_yield": 1.5,
        "yield_std": 0.32,
        "opt_fert": 80,
        "opt_pest": 1.1,
    },
    "Millets": {
        "seasons": ["Kharif"],
        "soils": ["Sandy Loam", "Red"],
        "states": ["Rajasthan", "Maharashtra", "Karnataka", "Uttar Pradesh", "Gujarat", "Haryana", "Tamil Nadu", "Madhya Pradesh", "Andhra Pradesh", "Telangana"],
        "temp_range": (24, 38),
        "rain_range": (250, 650),
        "base_yield": 1.6,
        "yield_std": 0.35,
        "opt_fert": 60,
        "opt_pest": 0.9,
    },
    "Onion": {
        "seasons": ["Rabi", "Kharif"],
        "soils": ["Sandy Loam", "Alluvial", "Black"],
        "states": ["Maharashtra", "Karnataka", "Madhya Pradesh", "Gujarat", "Rajasthan", "Bihar", "Andhra Pradesh", "Haryana", "Tamil Nadu", "Telangana"],
        "temp_range": (15, 30),
        "rain_range": (400, 800),
        "base_yield": 18.5,
        "yield_std": 3.2,
        "opt_fert": 140,
        "opt_pest": 2.0,
    },
    "Banana": {
        "seasons": ["Whole Year"],
        "soils": ["Alluvial", "Clayey", "Red"],
        "states": ["Tamil Nadu", "Maharashtra", "Gujarat", "Andhra Pradesh", "Kerala", "Karnataka", "Bihar", "Assam", "West Bengal", "Odisha"],
        "temp_range": (22, 36),
        "rain_range": (1200, 2400),
        "base_yield": 42.0,
        "yield_std": 6.5,
        "opt_fert": 250,
        "opt_pest": 2.8,
    },
    "Barley": {
        "seasons": ["Rabi"],
        "soils": ["Sandy Loam", "Alluvial"],
        "states": ["Rajasthan", "Uttar Pradesh", "Punjab", "Haryana", "Madhya Pradesh", "Bihar", "Himachal Pradesh", "Jammu and Kashmir", "Ladakh", "Uttarakhand"],
        "temp_range": (10, 24),
        "rain_range": (250, 550),
        "base_yield": 2.9,
        "yield_std": 0.5,
        "opt_fert": 75,
        "opt_pest": 1.0,
    },
    "Jute": {
        "seasons": ["Kharif"],
        "soils": ["Alluvial", "Clayey"],
        "states": ["West Bengal", "Bihar", "Assam", "Odisha", "Meghalaya", "Tripura", "Nagaland"],
        "temp_range": (24, 37),
        "rain_range": (1300, 2200),
        "base_yield": 2.6,
        "yield_std": 0.45,
        "opt_fert": 90,
        "opt_pest": 1.8,
    },
    "Tea": {
        "seasons": ["Whole Year"],
        "soils": ["Laterite", "Red"],
        "states": ["Assam", "West Bengal", "Tamil Nadu", "Kerala", "Himachal Pradesh", "Tripura", "Arunachal Pradesh", "Sikkim", "Meghalaya", "Nagaland", "Uttarakhand"],
        "temp_range": (16, 30),
        "rain_range": (1500, 3000),
        "base_yield": 2.2,
        "yield_std": 0.38,
        "opt_fert": 130,
        "opt_pest": 2.2,
    },
    "Coffee": {
        "seasons": ["Whole Year"],
        "soils": ["Laterite", "Red"],
        "states": ["Karnataka", "Kerala", "Tamil Nadu", "Andhra Pradesh", "Odisha", "Nagaland", "Manipur", "Mizoram", "Arunachal Pradesh"],
        "temp_range": (18, 28),
        "rain_range": (1400, 2500),
        "base_yield": 1.1,
        "yield_std": 0.22,
        "opt_fert": 110,
        "opt_pest": 1.9,
    },
    "Turmeric": {
        "seasons": ["Kharif", "Whole Year"],
        "soils": ["Sandy Loam", "Red", "Alluvial"],
        "states": ["Telangana", "Andhra Pradesh", "Tamil Nadu", "Maharashtra", "Odisha", "Karnataka", "Kerala", "West Bengal", "Meghalaya", "Mizoram", "Assam"],
        "temp_range": (20, 34),
        "rain_range": (1000, 1800),
        "base_yield": 6.2,
        "yield_std": 1.1,
        "opt_fert": 120,
        "opt_pest": 1.7,
    },
    "Ginger": {
        "seasons": ["Kharif"],
        "soils": ["Sandy Loam", "Laterite", "Red"],
        "states": ["Kerala", "Karnataka", "Assam", "Meghalaya", "Sikkim", "Arunachal Pradesh", "Odisha", "West Bengal", "Mizoram", "Nagaland", "Himachal Pradesh"],
        "temp_range": (19, 32),
        "rain_range": (1400, 2600),
        "base_yield": 5.8,
        "yield_std": 1.05,
        "opt_fert": 115,
        "opt_pest": 1.6,
    },
    "Chilli": {
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Black", "Sandy Loam", "Red"],
        "states": ["Andhra Pradesh", "Telangana", "Madhya Pradesh", "Karnataka", "West Bengal", "Gujarat", "Maharashtra", "Odisha", "Tamil Nadu", "Rajasthan", "Assam"],
        "temp_range": (20, 33),
        "rain_range": (500, 1000),
        "base_yield": 2.4,
        "yield_std": 0.45,
        "opt_fert": 130,
        "opt_pest": 2.7,
    },
    "Lentil": {
        "seasons": ["Rabi"],
        "soils": ["Alluvial", "Clayey", "Sandy Loam"],
        "states": ["Uttar Pradesh", "Madhya Pradesh", "Bihar", "West Bengal", "Rajasthan", "Jharkhand", "Chhattisgarh", "Haryana"],
        "temp_range": (12, 25),
        "rain_range": (300, 600),
        "base_yield": 1.1,
        "yield_std": 0.22,
        "opt_fert": 45,
        "opt_pest": 0.8,
    },
    "Pigeon Pea": {
        "seasons": ["Kharif"],
        "soils": ["Black", "Alluvial", "Red"],
        "states": ["Maharashtra", "Karnataka", "Madhya Pradesh", "Uttar Pradesh", "Gujarat", "Telangana", "Jharkhand", "Odisha", "Chhattisgarh", "Andhra Pradesh"],
        "temp_range": (20, 35),
        "rain_range": (600, 1000),
        "base_yield": 1.2,
        "yield_std": 0.25,
        "opt_fert": 50,
        "opt_pest": 1.4,
    },
    "Moong": {
        "seasons": ["Kharif", "Zaid"],
        "soils": ["Sandy Loam", "Alluvial", "Red"],
        "states": ["Rajasthan", "Maharashtra", "Madhya Pradesh", "Karnataka", "Gujarat", "Andhra Pradesh", "Bihar", "Punjab", "Haryana", "Tamil Nadu"],
        "temp_range": (22, 35),
        "rain_range": (350, 750),
        "base_yield": 0.85,
        "yield_std": 0.18,
        "opt_fert": 40,
        "opt_pest": 0.9,
    },
    "Urad": {
        "seasons": ["Kharif", "Rabi"],
        "soils": ["Black", "Alluvial", "Clayey"],
        "states": ["Madhya Pradesh", "Uttar Pradesh", "Andhra Pradesh", "Tamil Nadu", "Maharashtra", "West Bengal", "Odisha", "Karnataka", "Gujarat"],
        "temp_range": (22, 34),
        "rain_range": (450, 850),
        "base_yield": 0.9,
        "yield_std": 0.2,
        "opt_fert": 42,
        "opt_pest": 0.95,
    },
    "Coconut": {
        "seasons": ["Whole Year"],
        "soils": ["Laterite", "Alluvial", "Sandy Loam", "Red"],
        "states": ["Kerala", "Tamil Nadu", "Karnataka", "Andhra Pradesh", "Goa", "Odisha", "West Bengal", "Maharashtra", "Puducherry", "Andaman and Nicobar Islands", "Lakshadweep"],
        "temp_range": (22, 34),
        "rain_range": (1200, 2800),
        "base_yield": 11.5,
        "yield_std": 2.2,
        "opt_fert": 140,
        "opt_pest": 1.8,
    },
    "Rubber": {
        "seasons": ["Whole Year"],
        "soils": ["Laterite", "Red"],
        "states": ["Kerala", "Tripura", "Tamil Nadu", "Karnataka", "Assam", "Meghalaya", "Goa", "Andaman and Nicobar Islands"],
        "temp_range": (21, 34),
        "rain_range": (1800, 3200),
        "base_yield": 1.55,
        "yield_std": 0.28,
        "opt_fert": 90,
        "opt_pest": 1.2,
    },
    "Apple": {
        "seasons": ["Rabi", "Whole Year"],
        "soils": ["Sandy Loam", "Alluvial"],
        "states": ["Jammu and Kashmir", "Himachal Pradesh", "Uttarakhand", "Arunachal Pradesh", "Ladakh"],
        "temp_range": (4, 22),
        "rain_range": (600, 1200),
        "base_yield": 12.8,
        "yield_std": 2.6,
        "opt_fert": 160,
        "opt_pest": 2.6,
    },
    "Mango": {
        "seasons": ["Whole Year"],
        "soils": ["Alluvial", "Red", "Laterite"],
        "states": ["Uttar Pradesh", "Andhra Pradesh", "Karnataka", "Bihar", "Gujarat", "Tamil Nadu", "Maharashtra", "West Bengal", "Kerala", "Odisha", "Telangana", "Goa"],
        "temp_range": (20, 36),
        "rain_range": (650, 1600),
        "base_yield": 9.2,
        "yield_std": 1.8,
        "opt_fert": 150,
        "opt_pest": 2.2,
    },
    "Garlic": {
        "seasons": ["Rabi"],
        "soils": ["Sandy Loam", "Alluvial", "Clayey"],
        "states": ["Madhya Pradesh", "Gujarat", "Rajasthan", "Uttar Pradesh", "Assam", "Punjab", "Haryana", "Maharashtra", "Himachal Pradesh"],
        "temp_range": (12, 26),
        "rain_range": (300, 650),
        "base_yield": 5.6,
        "yield_std": 1.1,
        "opt_fert": 130,
        "opt_pest": 1.6,
    },
    "Sunflower": {
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "soils": ["Black", "Sandy Loam", "Alluvial"],
        "states": ["Karnataka", "Andhra Pradesh", "Maharashtra", "Bihar", "Haryana", "Punjab", "Tamil Nadu", "Telangana", "Odisha"],
        "temp_range": (18, 32),
        "rain_range": (400, 800),
        "base_yield": 1.45,
        "yield_std": 0.28,
        "opt_fert": 75,
        "opt_pest": 1.3,
    },
    "Cardamom": {
        "seasons": ["Whole Year"],
        "soils": ["Laterite", "Red"],
        "states": ["Kerala", "Karnataka", "Tamil Nadu", "Sikkim", "Nagaland", "Arunachal Pradesh", "West Bengal", "Mizoram"],
        "temp_range": (14, 28),
        "rain_range": (1500, 3000),
        "base_yield": 0.42,
        "yield_std": 0.08,
        "opt_fert": 70,
        "opt_pest": 1.4,
    },
}

ALL_SOILS = ["Alluvial", "Black", "Red", "Clayey", "Sandy Loam", "Laterite"]
ALL_SEASONS = ["Kharif", "Rabi", "Zaid", "Whole Year"]


def generate_crop_dataset(num_samples_per_crop=280):
    rows = []

    for crop, profile in CROP_PROFILES.items():
        crop_states = profile["states"]
        for _ in range(num_samples_per_crop):
            if np.random.rand() < 0.85:
                state = np.random.choice(crop_states)
            else:
                state = np.random.choice(ALL_STATES)

            if np.random.rand() < 0.85:
                season = np.random.choice(profile["seasons"])
            else:
                season = np.random.choice(ALL_SEASONS)

            if np.random.rand() < 0.82:
                soil = np.random.choice(profile["soils"])
            else:
                soil = np.random.choice(ALL_SOILS)

            area = round(float(np.random.exponential(scale=2.8) + 0.5), 2)
            area = min(max(area, 0.4), 25.0)

            t_min, t_max = profile["temp_range"]
            r_min, r_max = profile["rain_range"]

            temp = float(np.random.normal(loc=(t_min + t_max) / 2, scale=3.2))
            temp = round(min(max(temp, 2.0), 45.0), 1)

            rain = float(np.random.normal(loc=(r_min + r_max) / 2, scale=(r_max - r_min) * 0.22))
            rain = round(min(max(rain, 120.0), 3400.0), 1)

            fert = float(np.random.normal(loc=profile["opt_fert"], scale=profile["opt_fert"] * 0.22))
            fert = round(min(max(fert, 15.0), 380.0), 1)

            pest = float(np.random.normal(loc=profile["opt_pest"], scale=profile["opt_pest"] * 0.28))
            pest = round(min(max(pest, 0.1), 6.5), 2)

            base = profile["base_yield"]

            t_opt = (t_min + t_max) / 2
            t_width = (t_max - t_min) / 2
            temp_factor = np.exp(-0.5 * ((temp - t_opt) / (t_width * 1.2)) ** 2)

            r_opt = (r_min + r_max) / 2
            r_width = (r_max - r_min) / 2
            rain_factor = np.exp(-0.5 * ((rain - r_opt) / (r_width * 1.3)) ** 2)

            soil_factor = 1.05 if soil in profile["soils"] else 0.88

            fert_ratio = fert / profile["opt_fert"]
            if fert_ratio < 1.0:
                fert_factor = 0.75 + 0.25 * (fert_ratio ** 0.8)
            else:
                fert_factor = 1.0 + 0.08 * (1.0 - np.exp(-0.8 * (fert_ratio - 1.0))) - 0.05 * max(0, fert_ratio - 1.5)

            season_factor = 1.02 if season in profile["seasons"] else 0.86

            noise = np.random.normal(0, profile["yield_std"] * 0.32)
            calc_yield = base * temp_factor * rain_factor * soil_factor * fert_factor * season_factor + noise

            min_possible = base * 0.32
            max_possible = base * 1.68
            final_yield = round(float(min(max(calc_yield, min_possible), max_possible)), 2)

            total_production = round(final_yield * area, 2)

            rows.append({
                "Crop": crop,
                "State": state,
                "Season": season,
                "Soil_Type": soil,
                "Area_Hectares": area,
                "Rainfall_mm": rain,
                "Temperature_Celsius": temp,
                "Fertilizer_kg_per_ha": fert,
                "Pesticide_kg_per_ha": pest,
                "Yield_tonnes_per_ha": final_yield,
                "Total_Production_tonnes": total_production
            })

    # Ensure every single state in ALL_STATES appears across multiple crops
    present_states = set(r["State"] for r in rows)
    missing_states = set(ALL_STATES) - present_states
    for st in missing_states:
        for cr in ["Rice", "Wheat", "Maize", "Tomato", "Potato"]:
            pr = CROP_PROFILES[cr]
            rows.append({
                "Crop": cr,
                "State": st,
                "Season": pr["seasons"][0],
                "Soil_Type": pr["soils"][0],
                "Area_Hectares": 2.0,
                "Rainfall_mm": float(sum(pr["rain_range"]) / 2),
                "Temperature_Celsius": float(sum(pr["temp_range"]) / 2),
                "Fertilizer_kg_per_ha": float(pr["opt_fert"]),
                "Pesticide_kg_per_ha": float(pr["opt_pest"]),
                "Yield_tonnes_per_ha": float(pr["base_yield"]),
                "Total_Production_tonnes": float(pr["base_yield"] * 2.0)
            })

    df = pd.DataFrame(rows)
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(output_dir, "crop_yield_data.csv")

    print("🌾 Generating comprehensive agricultural crop yield dataset for ALL Indian States & Crops...")
    df = generate_crop_dataset(num_samples_per_crop=280)
    df.to_csv(csv_path, index=False)
    print(f"✅ Successfully saved dataset with {len(df)} records across {df['Crop'].nunique()} crops and {df['State'].nunique()} states/UTs to {csv_path}")
