"""
Agronomy Intelligence Engine for Crop Yield Prediction
Provides scientific advisory, soil suitability, weather analysis, and yield health assessment.
"""

# Crop specific agronomic benchmarks
AGRONOMIC_KNOWLEDGE = {
    "Rice": {
        "icon": "🌾",
        "category": "Cereal / Grain",
        "ideal_seasons": ["Kharif", "Whole Year"],
        "ideal_soils": ["Clayey", "Alluvial"],
        "temp_opt": (22, 35),
        "rain_opt": (1000, 2000),
        "typical_fert": (120, 160),
        "avg_yield": 3.27,
        "tips": [
            "Maintain 2-5 cm of standing water during tillering to panicle initiation.",
            "Apply nitrogen in 3 split doses: 50% basal, 25% active tillering, 25% panicle initiation.",
            "Watch out for Brown Plant Hopper and Stem Borer during humid spells."
        ]
    },
    "Wheat": {
        "icon": "🌾",
        "category": "Cereal / Grain",
        "ideal_seasons": ["Rabi"],
        "ideal_soils": ["Alluvial", "Sandy Loam"],
        "temp_opt": (14, 25),
        "rain_opt": (350, 650),
        "typical_fert": (110, 140),
        "avg_yield": 3.34,
        "tips": [
            "Ensure critical first irrigation at Crown Root Initiation (CRI) stage (20-25 days after sowing).",
            "Avoid terminal heat stress during grain filling by light irrigation in late February/early March.",
            "Monitor for Yellow Rust symptoms on leaves during prolonged cool, moist spells."
        ]
    },
    "Maize": {
        "icon": "🌽",
        "category": "Coarse Cereal",
        "ideal_seasons": ["Kharif", "Rabi"],
        "ideal_soils": ["Alluvial", "Red", "Black"],
        "temp_opt": (20, 32),
        "rain_opt": (550, 950),
        "typical_fert": (100, 140),
        "avg_yield": 3.20,
        "tips": [
            "Maize is highly sensitive to waterlogging; ensure ridge and furrow sowing for proper drainage.",
            "Crucial water requirement periods are tasseling and silking stages.",
            "Scout weekly for Fall Armyworm (FAW) in the central whorl of young plants."
        ]
    },
    "Cotton": {
        "icon": "🌱",
        "category": "Commercial / Fiber",
        "ideal_seasons": ["Kharif"],
        "ideal_soils": ["Black", "Alluvial"],
        "temp_opt": (24, 35),
        "rain_opt": (550, 950),
        "typical_fert": (120, 170),
        "avg_yield": 1.67,
        "tips": [
            "Black cotton soil (Regur) retains deep moisture; avoid over-irrigation during vegetative growth.",
            "Boll development stage requires steady moisture and warm sunshine.",
            "Deploy pheromone traps to monitor Pink Bollworm activity early in the season."
        ]
    },
    "Sugarcane": {
        "icon": "🎋",
        "category": "Cash Crop",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Alluvial", "Black", "Clayey"],
        "temp_opt": (22, 35),
        "rain_opt": (1200, 2200),
        "typical_fert": (190, 260),
        "avg_yield": 64.77,
        "tips": [
            "Adopt trash mulching in furrows to conserve soil moisture and suppress weed emergence.",
            "Earthing up at 90-120 days prevents lodging of tall canes during monsoon winds.",
            "Maintain soil organic carbon by incorporating press mud or compost."
        ]
    },
    "Soybean": {
        "icon": "🌿",
        "category": "Oilseed / Legume",
        "ideal_seasons": ["Kharif"],
        "ideal_soils": ["Black", "Clayey"],
        "temp_opt": (22, 30),
        "rain_opt": (650, 1050),
        "typical_fert": (70, 110),
        "avg_yield": 1.57,
        "tips": [
            "Inoculate seeds with Rhizobium culture and PSB prior to sowing for biological nitrogen fixation.",
            "Ensure broad bed furrow (BBF) planting to prevent root rot during heavy downpours.",
            "Pod filling stage is critical; ensure adequate soil moisture if monsoon pauses."
        ]
    },
    "Groundnut": {
        "icon": "🥜",
        "category": "Oilseed",
        "ideal_seasons": ["Kharif", "Rabi"],
        "ideal_soils": ["Sandy Loam", "Red"],
        "temp_opt": (22, 32),
        "rain_opt": (450, 850),
        "typical_fert": (70, 100),
        "avg_yield": 1.84,
        "tips": [
            "Sandy loam soil allows smooth peg penetration and easy pod development.",
            "Apply Gypsum (200-400 kg/ha) at flowering/pegging for high pod filling and shell hardening.",
            "Do not disturb or weed the soil once pegging begins."
        ]
    },
    "Potato": {
        "icon": "🥔",
        "category": "Tuber / Vegetable",
        "ideal_seasons": ["Rabi"],
        "ideal_soils": ["Sandy Loam", "Alluvial"],
        "temp_opt": (15, 23),
        "rain_opt": (350, 600),
        "typical_fert": (150, 210),
        "avg_yield": 20.18,
        "tips": [
            "Loose, friable sandy loam prevents tuber malformation and promotes healthy stolon growth.",
            "Earth up rows twice to prevent greening of tubers exposed to sunlight.",
            "Spray Mancozeb prophylactically against Late Blight during cloudy, drizzly winter days."
        ]
    },
    "Tomato": {
        "icon": "🍅",
        "category": "Horticultural Vegetable",
        "ideal_seasons": ["Rabi", "Kharif", "Zaid"],
        "ideal_soils": ["Sandy Loam", "Red", "Alluvial"],
        "temp_opt": (19, 30),
        "rain_opt": (450, 800),
        "typical_fert": (140, 180),
        "avg_yield": 25.10,
        "tips": [
            "Staking with bamboo poles improves aeration and dramatically reduces fruit rot.",
            "Use drip irrigation to maintain uniform moisture and prevent fruit cracking.",
            "Ensure balanced calcium nutrition to prevent Blossom End Rot."
        ]
    },
    "Chickpea": {
        "icon": "🌱",
        "category": "Pulses",
        "ideal_seasons": ["Rabi"],
        "ideal_soils": ["Sandy Loam", "Clayey", "Black"],
        "temp_opt": (15, 26),
        "rain_opt": (300, 600),
        "typical_fert": (50, 80),
        "avg_yield": 1.27,
        "tips": [
            "Nip apical buds at 30-40 days after sowing to stimulate vigorous lateral branching.",
            "Excessive nitrogen or watering leads to vegetative growth without flowering.",
            "Monitor for Pod Borer (Helicoverpa) at flowering and pod setting."
        ]
    },
    "Mustard": {
        "icon": "🌼",
        "category": "Oilseed",
        "ideal_seasons": ["Rabi"],
        "ideal_soils": ["Alluvial", "Sandy Loam"],
        "temp_opt": (13, 25),
        "rain_opt": (250, 500),
        "typical_fert": (60, 95),
        "avg_yield": 1.33,
        "tips": [
            "Apply sulphur (20-30 kg/ha) to significantly enhance seed oil content.",
            "Perform early thinning 15-20 days after germination to maintain optimal plant spacing.",
            "Watch out for Mustard Aphid infestations during overcast winter mornings."
        ]
    },
    "Millets": {
        "icon": "🌾",
        "category": "Nutri-Cereal",
        "ideal_seasons": ["Kharif"],
        "ideal_soils": ["Sandy Loam", "Red"],
        "temp_opt": (25, 37),
        "rain_opt": (250, 600),
        "typical_fert": (50, 75),
        "avg_yield": 1.41,
        "tips": [
            "Exceptional drought resilience; suitable for dryland farming with minimal irrigation.",
            "Requires light basal fertilization; excessive nitrogen causes lodging.",
            "Promote intercropping with pulses (pigeonpea/cowpea) to boost soil organic fertility."
        ]
    },
    "Onion": {
        "icon": "🧅",
        "category": "Horticultural Vegetable",
        "ideal_seasons": ["Rabi", "Kharif"],
        "ideal_soils": ["Sandy Loam", "Alluvial", "Black"],
        "temp_opt": (15, 28),
        "rain_opt": (400, 750),
        "typical_fert": (120, 160),
        "avg_yield": 18.2,
        "tips": [
            "Ensure well-drained, fertile soil; standing water causes bulb rot (damping off).",
            "Stop irrigation 10-15 days before harvest to allow proper neck drying and prolong storage life.",
            "Spray Mancozeb or Hexaconazole at early signs of Purple Blotch."
        ]
    },
    "Banana": {
        "icon": "🍌",
        "category": "Horticultural Fruit",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Alluvial", "Clayey", "Red"],
        "temp_opt": (22, 35),
        "rain_opt": (1200, 2200),
        "typical_fert": (220, 280),
        "avg_yield": 41.5,
        "tips": [
            "Heavy feeder of potassium; apply muriate of potash regularly during shooting and bunch development.",
            "Desucker regularly to keep only one follower sucker per mother plant.",
            "Bag bunches with perforated polythene sleeves to prevent fruit scarring and improve market grade."
        ]
    },
    "Barley": {
        "icon": "🌾",
        "category": "Rabi Cereal",
        "ideal_seasons": ["Rabi"],
        "ideal_soils": ["Sandy Loam", "Alluvial"],
        "temp_opt": (12, 23),
        "rain_opt": (250, 500),
        "typical_fert": (60, 90),
        "avg_yield": 2.85,
        "tips": [
            "More tolerant to salinity and drought than wheat; ideal for semi-arid and northern regions.",
            "First irrigation at tillering stage (30-35 days) is critical.",
            "Avoid excess nitrogen if cultivating malt barley to maintain low grain protein standards."
        ]
    },
    "Jute": {
        "icon": "🌿",
        "category": "Commercial / Fiber",
        "ideal_seasons": ["Kharif"],
        "ideal_soils": ["Alluvial", "Clayey"],
        "temp_opt": (24, 35),
        "rain_opt": (1300, 2000),
        "typical_fert": (80, 110),
        "avg_yield": 2.55,
        "tips": [
            "Requires abundant clean retting water for high-grade golden fiber extraction.",
            "Weed thoroughly during first 30 days of seedling emergence.",
            "Harvest at small pod stage (120-135 days) for the best balance of yield and fiber tensile strength."
        ]
    },
    "Tea": {
        "icon": "🍵",
        "category": "Plantation Crop",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Laterite", "Red"],
        "temp_opt": (16, 28),
        "rain_opt": (1500, 2800),
        "typical_fert": (110, 150),
        "avg_yield": 2.15,
        "tips": [
            "Requires acidic well-drained soil (pH 4.5 - 5.5); avoid waterlogging on slopes.",
            "Maintain strict plucking table rounds (2 leaves and a bud) every 7-10 days.",
            "Pruning cycles every 3-5 years rejuvenate bush yield and leaf quality."
        ]
    },
    "Coffee": {
        "icon": "☕",
        "category": "Plantation Crop",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Laterite", "Red"],
        "temp_opt": (18, 27),
        "rain_opt": (1400, 2400),
        "typical_fert": (90, 130),
        "avg_yield": 1.08,
        "tips": [
            "Grow under two-tier shade trees (silver oak, dadap) to moderate microclimate.",
            "Blossom and backing showers (March-April) are critical for berry setting.",
            "Scout for White Stem Borer and Coffee Berry Borer regularly."
        ]
    },
    "Turmeric": {
        "icon": "🍠",
        "category": "Spices & Condiments",
        "ideal_seasons": ["Kharif", "Whole Year"],
        "ideal_soils": ["Sandy Loam", "Red", "Alluvial"],
        "temp_opt": (20, 32),
        "rain_opt": (1000, 1700),
        "typical_fert": (100, 140),
        "avg_yield": 6.1,
        "tips": [
            "Green leaf mulching at planting and after 45 and 90 days conserves moisture and suppresses weeds.",
            "Ensure loose, friable soil for smooth rhizome expansion.",
            "Drench with Trichoderma or Ridomil Gold to prevent rhizome rot."
        ]
    },
    "Ginger": {
        "icon": "🫚",
        "category": "Spices & Condiments",
        "ideal_seasons": ["Kharif"],
        "ideal_soils": ["Sandy Loam", "Laterite", "Red"],
        "temp_opt": (19, 30),
        "rain_opt": (1400, 2400),
        "typical_fert": (100, 135),
        "avg_yield": 5.65,
        "tips": [
            "Treat seed rhizomes with Mancozeb (3g/L) + Chlorpyrifos prior to planting.",
            "Apply heavy organic farmyard manure and mulch with tree leaves twice during early growth.",
            "Provide raised bed planting with proper drainage channels to prevent bacterial wilt."
        ]
    },
    "Chilli": {
        "icon": "🌶️",
        "category": "Spices & Vegetables",
        "ideal_seasons": ["Kharif", "Rabi"],
        "ideal_soils": ["Black", "Sandy Loam", "Red"],
        "temp_opt": (20, 32),
        "rain_opt": (500, 900),
        "typical_fert": (110, 150),
        "avg_yield": 2.35,
        "tips": [
            "Dip seedling roots in Pseudomonas fluorescens solution before transplanting.",
            "Install blue and yellow sticky traps to combat thrips and whiteflies (vectors for leaf curl virus).",
            "Spray neem cake slurry to repel soil nematodes and maintain root vigor."
        ]
    },
    "Lentil": {
        "icon": "🥣",
        "category": "Pulses",
        "ideal_seasons": ["Rabi"],
        "ideal_soils": ["Alluvial", "Clayey", "Sandy Loam"],
        "temp_opt": (12, 24),
        "rain_opt": (300, 550),
        "typical_fert": (35, 55),
        "avg_yield": 1.05,
        "tips": [
            "Seed inoculation with Rhizobium leguminosarum increases nodules and saves nitrogen costs.",
            "Very responsive to one light irrigation at pre-flowering and pod formation.",
            "Spray Mancozeb at early signs of rust or Ascochyta blight."
        ]
    },
    "Pigeon Pea": {
        "icon": "🍲",
        "category": "Pulses",
        "ideal_seasons": ["Kharif"],
        "ideal_soils": ["Black", "Alluvial", "Red"],
        "temp_opt": (20, 34),
        "rain_opt": (600, 950),
        "typical_fert": (40, 65),
        "avg_yield": 1.18,
        "tips": [
            "Deep taproot system breaks hardpan and enriches soil with 40 kg N/ha via leaf fall.",
            "Pinch terminal shoots at 45-50 days to promote branching and increase pod count.",
            "Deploy NPV (Nuclear Polyhedrosis Virus) or Emamectin Benzoate against Pod Borer."
        ]
    },
    "Moong": {
        "icon": "🌱",
        "category": "Pulses",
        "ideal_seasons": ["Kharif", "Zaid"],
        "ideal_soils": ["Sandy Loam", "Alluvial", "Red"],
        "temp_opt": (22, 34),
        "rain_opt": (350, 700),
        "typical_fert": (30, 50),
        "avg_yield": 0.82,
        "tips": [
            "Short duration crop (60-70 days); perfect for crop rotation after wheat or rice.",
            "Control Yellow Mosaic Virus by spraying Thiamethoxam against whitefly vectors.",
            "Harvest promptly when 80% pods turn black to prevent pod shattering in fields."
        ]
    },
    "Urad": {
        "icon": "🌱",
        "category": "Pulses",
        "ideal_seasons": ["Kharif", "Rabi"],
        "ideal_soils": ["Black", "Alluvial", "Clayey"],
        "temp_opt": (22, 33),
        "rain_opt": (450, 800),
        "typical_fert": (32, 52),
        "avg_yield": 0.88,
        "tips": [
            "Well-suited as a catch crop or intercrop in sugarcane and maize.",
            "Apply 2% DAP foliar spray at flowering and 15 days later to boost pod filling.",
            "Treat seed with Carbendazim (2g/kg) to shield against root rot and damping off."
        ]
    },
    "Coconut": {
        "icon": "🥥",
        "category": "Plantation / Fruit",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Laterite", "Alluvial", "Sandy Loam", "Red"],
        "temp_opt": (22, 33),
        "rain_opt": (1200, 2600),
        "typical_fert": (120, 160),
        "avg_yield": 11.2,
        "tips": [
            "Adopt basin irrigation and organic mulching with coconut coir pith or dried fronds.",
            "Apply Magnesium Sulphate (500g/palm/yr) in acidic soils to avoid yellowing fronds.",
            "Hook out Rhinoceros Beetles with iron rods and fill crown leaf axils with neem seed powder."
        ]
    },
    "Rubber": {
        "icon": "🌳",
        "category": "Plantation Crop",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Laterite", "Red"],
        "temp_opt": (21, 33),
        "rain_opt": (1800, 3000),
        "typical_fert": (80, 105),
        "avg_yield": 1.52,
        "tips": [
            "Ensure proper tapping angle (30 degrees for seedling trees, 34 degrees for budded trees).",
            "Apply rain-guarding polythene sheets before southwest monsoon to enable uninterrupted tapping.",
            "Maintain leguminous cover crops (Mucuna bracteata) in young plantations to prevent soil erosion."
        ]
    },
    "Apple": {
        "icon": "🍎",
        "category": "Temperate Fruit",
        "ideal_seasons": ["Rabi", "Whole Year"],
        "ideal_soils": ["Sandy Loam", "Alluvial"],
        "temp_opt": (4, 20),
        "rain_opt": (650, 1100),
        "typical_fert": (140, 180),
        "avg_yield": 12.5,
        "tips": [
            "Requires 800-1200 winter chilling hours (< 7 deg C) for healthy bud break and flowering.",
            "Perform winter dormant spur pruning to maintain sunlight penetration inside the canopy.",
            "Spray Dodine or Mancozeb to prevent Apple Scab during humid spring conditions."
        ]
    },
    "Mango": {
        "icon": "🥭",
        "category": "Fruit Crop",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Alluvial", "Red", "Laterite"],
        "temp_opt": (22, 35),
        "rain_opt": (700, 1500),
        "typical_fert": (130, 170),
        "avg_yield": 9.05,
        "tips": [
            "Withhold irrigation in October-November to encourage profuse floral bud induction.",
            "Control Mango Hopper and Powdery Mildew by spraying Imidacloprid + Dinocap at panicle emergence.",
            "Bag developing fruits with craft paper bags to protect against Fruit Fly damage."
        ]
    },
    "Garlic": {
        "icon": "🧄",
        "category": "Spices & Condiments",
        "ideal_seasons": ["Rabi"],
        "ideal_soils": ["Sandy Loam", "Alluvial", "Clayey"],
        "temp_opt": (12, 25),
        "rain_opt": (300, 600),
        "typical_fert": (110, 150),
        "avg_yield": 5.45,
        "tips": [
            "Plant bold, outer cloves (vertical orientation) with pointed tip upward at 10x8 cm spacing.",
            "Bulb initiation stage requires steady soil moisture; discontinue watering 10 days before harvest.",
            "Ensure sulphur application (25 kg/ha) to enhance allicin content and pungency."
        ]
    },
    "Sunflower": {
        "icon": "🌻",
        "category": "Oilseed",
        "ideal_seasons": ["Kharif", "Rabi", "Zaid"],
        "ideal_soils": ["Black", "Sandy Loam", "Alluvial"],
        "temp_opt": (18, 30),
        "rain_opt": (400, 750),
        "typical_fert": (60, 90),
        "avg_yield": 1.42,
        "tips": [
            "Keep 5 bee colonies/ha or hand-pollinate with soft cloth palm rub during morning 8-11 AM.",
            "Spray Borax (0.2%) at ray floret opening stage to dramatically improve seed filling and minimize chaffy seeds.",
            "Ensure uniform soil moisture at flowering and seed dough stages."
        ]
    },
    "Cardamom": {
        "icon": "🌿",
        "category": "Queen of Spices",
        "ideal_seasons": ["Whole Year"],
        "ideal_soils": ["Laterite", "Red"],
        "temp_opt": (14, 26),
        "rain_opt": (1500, 2800),
        "typical_fert": (60, 85),
        "avg_yield": 0.41,
        "tips": [
            "Cultivate under 50-60% shade canopy in forest loam rich in organic leaf litter.",
            "Mulch thick organic matter in circles around the clump to preserve feeder roots and moisture.",
            "Control Cardamom Thrips by spraying Quinalphos or spinosad during panicle elongation."
        ]
    }
}


def analyze_crop_prediction(crop, season, soil, rainfall, temp, fertilizer, predicted_yield, area):
    """
    Analyzes prediction against scientific agronomic criteria and generates tailored advice.
    """
    info = AGRONOMIC_KNOWLEDGE.get(crop, {
        "icon": "🌱",
        "category": "Agricultural Crop",
        "ideal_seasons": ["Kharif", "Rabi"],
        "ideal_soils": ["Alluvial", "Black", "Red"],
        "temp_opt": (18, 32),
        "rain_opt": (500, 1200),
        "typical_fert": (80, 150),
        "avg_yield": 3.0,
        "tips": ["Follow local agricultural extension advisories for optimal yield."]
    })

    avg_y = info["avg_yield"]
    ratio = predicted_yield / avg_y if avg_y > 0 else 1.0

    # Determine Yield Status & Badge
    if ratio >= 1.08:
        status = "Optimal / High Yield"
        badge_class = "badge-optimal"
        status_icon = "🌟"
        summary = f"Excellent yield projection! Expected to be {round((ratio - 1.0)*100, 1)}% above typical regional average."
    elif ratio >= 0.88:
        status = "Good / Normal Yield"
        badge_class = "badge-good"
        status_icon = "✅"
        summary = "Solid crop performance aligned with standard agricultural yields."
    else:
        status = "Below Average / Sub-Optimal"
        badge_class = "badge-warning"
        status_icon = "⚠️"
        summary = f"Yield is projected {round((1.0 - ratio)*100, 1)}% below normal. Review soil, water, and nutrient balance."

    # Insights & Warnings
    advisory_notes = []

    # Soil check
    if soil in info["ideal_soils"]:
        advisory_notes.append({
            "type": "positive",
            "title": "Soil Match",
            "text": f"'{soil}' soil is highly suitable for {crop}, supporting optimal root and nutrient uptake."
        })
    else:
        advisory_notes.append({
            "type": "warning",
            "title": "Soil Compatibility Notice",
            "text": f"{crop} generally thrives best in {', '.join(info['ideal_soils'])}. In '{soil}' soil, ensure extra organic matter and drainage."
        })

    # Weather check
    t_min, t_max = info["temp_opt"]
    if temp < t_min:
        advisory_notes.append({
            "type": "warning",
            "title": "Cooler Temperature",
            "text": f"Temperature ({temp}°C) is below the preferred range ({t_min}-{t_max}°C). Vegetative growth may slow down."
        })
    elif temp > t_max:
        advisory_notes.append({
            "type": "warning",
            "title": "Heat Stress Risk",
            "text": f"Temperature ({temp}°C) exceeds the optimal band ({t_min}-{t_max}°C). Ensure timely mulching and evening irrigation."
        })
    else:
        advisory_notes.append({
            "type": "positive",
            "title": "Ideal Temperature",
            "text": f"Temperature of {temp}°C falls comfortably within the optimal growth bracket ({t_min}-{t_max}°C)."
        })

    # Rainfall check
    r_min, r_max = info["rain_opt"]
    if rainfall < r_min:
        advisory_notes.append({
            "type": "alert",
            "title": "Moisture Deficit",
            "text": f"Rainfall ({rainfall} mm) is lower than the recommended requirement ({r_min}-{r_max} mm). Supplemental irrigation is strongly advised."
        })
    elif rainfall > r_max:
        advisory_notes.append({
            "type": "alert",
            "title": "Excess Moisture Risk",
            "text": f"Rainfall ({rainfall} mm) is elevated. Ensure proper drainage channels to prevent waterlogging and root fungal diseases."
        })
    else:
        advisory_notes.append({
            "type": "positive",
            "title": "Adequate Water Supply",
            "text": f"Water/rainfall availability ({rainfall} mm) matches {crop}'s natural moisture demand."
        })

    # Fertilizer check
    f_min, f_max = info["typical_fert"]
    if fertilizer < f_min:
        advisory_notes.append({
            "type": "warning",
            "title": "Low Fertilizer Application",
            "text": f"Fertilizer dose ({fertilizer} kg/ha) is below recommended levels ({f_min}-{f_max} kg/ha). Consider soil testing for top-dressing."
        })
    elif fertilizer > f_max * 1.3:
        advisory_notes.append({
            "type": "warning",
            "title": "Excess Nutrient Caution",
            "text": f"High fertilizer application ({fertilizer} kg/ha) may lead to diminishing returns and vegetative overgrowth without yield gain."
        })

    # Units conversions
    area_acres = round(area * 2.47105, 2)
    yield_quintals_per_acre = round((predicted_yield * 10) / 2.47105, 2)
    total_production_tonnes = round(predicted_yield * area, 2)
    total_production_quintals = round(total_production_tonnes * 10, 2)

    return {
        "crop": crop,
        "icon": info["icon"],
        "category": info["category"],
        "predicted_yield_t_ha": round(predicted_yield, 2),
        "predicted_yield_q_acre": yield_quintals_per_acre,
        "total_production_tonnes": total_production_tonnes,
        "total_production_quintals": total_production_quintals,
        "benchmark_yield_t_ha": round(avg_y, 2),
        "ratio_vs_benchmark": round(ratio * 100, 1),
        "status": status,
        "badge_class": badge_class,
        "status_icon": status_icon,
        "summary": summary,
        "advisories": advisory_notes,
        "expert_tips": info.get("tips", []),
        "area_ha": round(area, 2),
        "area_acres": area_acres
    }
