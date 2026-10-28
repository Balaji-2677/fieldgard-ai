"""
AI Agricultural Assistant Intelligence Engine ("Kisan AI - Agricultural ChatGPT")
Provides conversational, empathetic, scientifically accurate, and step-by-step
problem-solving advice for all farmer doubts:
- Conversational greetings, identity, and website usage instructions
- Crop-specific fertilizer, sowing, irrigation, pest & disease, and harvest guidance
- Real-time diagnostic problem-solving for all common farming troubles (yellow leaves, flower drop,
  saline borewell water, frost, waterlogging, leaf curl, blights, wilts, stem borers, weed control)
- Organic bio-formulations (Jeevamrut, Neemastra, Brahmastra, Agniastra, Trichoderma)
- Government welfare subsidies (PM-KISAN, PMFBY insurance claims, KCC loans, PM-KUSUM)
- Multi-turn conversation memory and optional online LLM integration (Gemini / OpenAI)
"""

import os
import re
import json
import urllib.request
import urllib.error

# Regional Crop Aliases mapping to standard 32 crops
CROP_ALIASES = {
    "paddy": "Rice", "chawal": "Rice", "dhan": "Rice",
    "gehun": "Wheat", "gehu": "Wheat",
    "makka": "Maize", "bhutta": "Maize", "corn": "Maize",
    "kapas": "Cotton", "rui": "Cotton",
    "ganna": "Sugarcane", "ikshuu": "Sugarcane",
    "chana": "Chickpea", "gram": "Chickpea", "bengal gram": "Chickpea",
    "sarson": "Mustard", "rai": "Mustard", "toria": "Mustard", "rapeseed": "Mustard",
    "bajra": "Millets", "jowar": "Millets", "ragi": "Millets", "finger millet": "Millets",
    "pearl millet": "Millets", "sorghum": "Millets",
    "tur": "Pigeon Pea", "arhar": "Pigeon Pea", "red gram": "Pigeon Pea",
    "masoor": "Lentil", "moong": "Moong", "mung": "Moong", "green gram": "Moong",
    "urad": "Urad", "mash": "Urad", "black gram": "Urad",
    "peanut": "Groundnut", "moongphali": "Groundnut",
    "aaloo": "Potato", "alu": "Potato",
    "tamatar": "Tomato",
    "pyaz": "Onion", "piaz": "Onion", "kanda": "Onion",
    "lahsun": "Garlic", "lasun": "Garlic",
    "haldi": "Turmeric", "adrak": "Ginger",
    "mirch": "Chilli", "mirchi": "Chilli",
    "jau": "Barley",
    "pat": "Jute", "golden fibre": "Jute",
    "chai": "Tea",
    "nariyal": "Coconut",
    "seb": "Apple",
    "aam": "Mango",
    "kela": "Banana",
    "surajmukhi": "Sunflower",
    "elaichi": "Cardamom"
}

# Conversational & Website Usage Intents
CONVERSATIONAL_INTENTS = [
    {
        "intent": "greeting",
        "keywords": ["hi", "hello", "hey", "namaste", "pranam", "ram ram", "vanakkam", "sat sri akal", "adaab", "greetings", "good morning", "good afternoon", "good evening", "kem cho"],
        "title": "🌾 Namaste & Welcome to Kisan AI!",
        "reply": (
            "Namaste! 🙏 I am your **Kisan AI Agricultural ChatGPT Assistant**.\n\n"
            "I am here to solve any farming doubt you have, like an expert agronomist in your pocket:\n\n"
            "• **Crop Disease & Pest Diagnosis:** Yellow leaves, curling, black spots, stem borer, bollworms, fungus.\n"
            "• **Fertilizer & Nutrition Balance:** Urea, DAP, Potash, Zinc, Sulphur, Boron dosages.\n"
            "• **Organic Farming & Natural Sprays:** How to make and apply Jeevamrut, Neemastra, Brahmastra.\n"
            "• **Water & Soil Solutions:** Saline borewell water, soil pH correction, drip irrigation, frost & drought management.\n"
            "• **Government Subsidies & Insurance:** PM-KISAN ₹6,000 status, PMFBY crop insurance claims, 4% KCC loans.\n"
            "• **Yield Prediction & Website Guide:** How to calculate your harvest in tonnes/hectare.\n\n"
            "What doubt or crop problem can I solve for you today?"
        ),
        "suggestions": [
            "Why are rice leaves turning yellow?",
            "What fertilizer to use for wheat?",
            "How to control bollworm in cotton?",
            "Government schemes for farmers"
        ]
    },
    {
        "intent": "website_guide",
        "keywords": ["how to use", "how to predict", "use website", "how it works", "instructions", "guide", "tutorial", "steps", "how do i use", "how does this work", "predict yield"],
        "title": "📖 How to Use CropYield AI in 4 Easy Steps",
        "reply": (
            "Here is how to get the most out of **CropYield AI**:\n\n"
            "1. **Go to 'Predict Yield' Page:** Click **[Predict Yield](/predict)** in the top navigation.\n"
            "2. **Select State & District:** Choose your state and district (e.g. *Punjab -> Ludhiana* or *Maharashtra -> Nashik*). Weather data will auto-sync automatically!\n"
            "3. **Enter Crop & Field Parameters:** Select your Crop (from 32 crops), Soil Type, and Farm Area.\n"
            "4. **Click 'Calculate Expected Yield':** In under 1 second, our AI model ($R^2 = 98.82%$) predicts your harvest in **Tonnes/Hectare** & **Quintals/Acre**, gives personalized agronomic warnings, suggests alternative high-yield crops if yield is low, and provides a printable **Farmer Yield Card**!\n\n"
            "💡 *Tip:* Check out the full **[📖 How to Use Guide](/how-to-use)** in the top menu for detailed tips!"
        ),
        "suggestions": [
            "Go to Predict page",
            "How accurate is the AI model?",
            "How to print farmer yield card?"
        ]
    },
    {
        "intent": "who_are_you",
        "keywords": ["who are you", "what are you", "what can you do", "your name", "who made you", "about you", "help me"],
        "title": "🤖 About Kisan AI Agricultural Assistant",
        "reply": (
            "I am **Kisan AI**, an intelligent agricultural assistant designed to think and answer just like ChatGPT for Indian farmers.\n\n"
            "• **Agronomic Intelligence:** Calibrated with official ICAR, State Agricultural Universities, and Ministry of Agriculture benchmarks.\n"
            "• **Pan-India Coverage:** Supports all 32 major crops across all 28 States and 8 Union Territories with local district microclimates.\n"
            "• **Comprehensive Doubt Solver:** From diagnosing sick plants, calculating exact chemical & bio-pesticide sprays, to claiming insurance and maximizing farm profits.\n\n"
            "Ask me any question in English, Hindi, or Hinglish, and I will give you a step-by-step solution!"
        ),
        "suggestions": [
            "How to increase crop yield?",
            "Fertilizer dose for sugarcane",
            "How to control bollworm in cotton?"
        ]
    },
    {
        "intent": "thank_you",
        "keywords": ["thank you", "thanks", "dhanyawad", "shukriya", "nandri", "great help", "awesome", "helpful", "good job"],
        "title": "🌾 You Are Most Welcome!",
        "reply": (
            "You are very welcome! 🙏\n\n"
            "CropYield AI is built with love and respect for our farmers—the backbone of our nation. May your fields be green and your harvest abundant! 🌾✨\n\n"
            "Whenever you have another question or see any trouble in your field, just ask me anytime."
        ),
        "suggestions": [
            "Predict yield for my farm",
            "Check government agricultural schemes",
            "Explore India crop map on Dashboard"
        ]
    },
    {
        "intent": "model_accuracy",
        "keywords": ["accuracy", "accurate", "r2", "r-squared", "model error", "how accurate", "algorithm", "machine learning", "random forest"],
        "title": "⚙️ Machine Learning Pipeline & Accuracy",
        "reply": (
            "**CropYield AI Machine Learning Specifications:**\n\n"
            "• **Algorithm:** Scikit-Learn Random Forest Regression Ensemble (160 decision estimators).\n"
            "• **Accuracy Score:** **$R^2 = 0.9882$ (98.82% Accuracy)** on test split.\n"
            "• **Dataset:** 8,960 agro-climatic records spanning 32 crops and all 36 Indian states & UTs.\n"
            "• **Input Factors:** Evaluates non-linear interactions between crop biology, seasonal rainfall, ambient temperature, soil texture, N-P-K chemical fertilization, and pesticide usage.\n\n"
            "You can read the full scientific details on our **[About AI](/about)** page."
        ),
        "suggestions": [
            "Try a prediction now",
            "How to use the website?",
            "What crops are supported?"
        ]
    }
]

# Detailed Crop-Specific Knowledge Matrix
CROP_SPECIFIC_KNOWLEDGE = {
    "Wheat": {
        "fertilizer": (
            "**🌾 Balanced Fertilizer Schedule for Wheat:**\n"
            "• **Total N-P-K Dose:** 120 kg Nitrogen, 60 kg P₂O₅ (Phosphorus), and 40 kg K₂O (Potash) per hectare.\n"
            "• **Basal Dose (At Sowing):** Apply 100% Phosphorus (DAP/SSP) + 100% Potash (MOP) + 1/3rd Nitrogen (Urea).\n"
            "• **First Top-Dress:** 1/3rd Nitrogen at 20-25 days after sowing (Crown Root Initiation stage) with first irrigation.\n"
            "• **Second Top-Dress:** Remaining 1/3rd Nitrogen at 40-45 days (Tillering/Jointing stage).\n"
            "• **Micronutrient:** In deficient soils, spray 0.5% Zinc Sulphate + 1% Urea at tillering."
        ),
        "sowing": (
            "**🌾 Optimal Wheat Sowing Schedule & Varieties:**\n"
            "• **Timely Sown Window:** First fortnight of November (Nov 1 – Nov 15) across Punjab, Haryana, UP, and Bihar.\n"
            "• **Late Sowing Window:** Up to December 10–15 (use short-duration varieties like DBW-187, PBW-771).\n"
            "• **Seed Rate:** 100 kg/ha for timely sowing; 125 kg/ha for late sowing.\n"
            "• **Recommended Varieties:** *HD-3086 (Pusa Gautami)*, *HD-2967*, *DBW-187 (Karan Vandana)*, *DBW-222*."
        ),
        "pest_disease": (
            "**🌾 Wheat Disease & Pest Management:**\n"
            "• **Yellow Rust (Puccinia striiformis):** Yellow powder pustules in linear stripes on leaves. Spray *Propiconazole 25% EC (Tilt)* @ 1 ml/L water immediately upon first detection.\n"
            "• **Termites:** Treat seed with *Chlorpyrifos 20% EC* (4 ml/kg seed) before sowing.\n"
            "• **Aphids:** Spray *Thiamethoxam 25% WG* @ 0.2 g/L if colonies exceed 10-15 aphids per earhead."
        ),
        "irrigation": (
            "**🌾 Critical Irrigation Stages in Wheat:**\n"
            "Wheat requires 4 to 6 light irrigations depending on winter rain. Critical stages:\n"
            "1. **CRI Stage (20-25 days):** Crown Root Initiation (MOST CRITICAL - never miss!).\n"
            "2. **Tillering (40-45 days):** Promotes strong shoot count.\n"
            "3. **Jointing (60-65 days):** Stem elongation.\n"
            "4. **Flowering (80-85 days):** Pollination and spikelet development.\n"
            "5. **Milking (100-105 days):** Grain filling (avoid water stress to prevent shriveled grain).\n"
            "6. **Dough Stage (115-120 days):** Light irrigation (avoid during high winds to prevent lodging)."
        )
    },
    "Rice": {
        "fertilizer": (
            "**🌾 Balanced Fertilizer Schedule for Rice / Paddy:**\n"
            "• **General Dose:** 120-150 kg N, 50-60 kg P₂O₅, 40-50 kg K₂O per hectare.\n"
            "• **Basal (Transplanting):** 100% Phosphorus (DAP) + 50% Potash + 25% Nitrogen + 25 kg Zinc Sulphate.\n"
            "• **Active Tillering (20-25 DAT):** Top-dress 50% Nitrogen (Urea).\n"
            "• **Panicle Initiation (40-45 DAT):** Top-dress remaining 25% Nitrogen + remaining 50% Potash."
        ),
        "pest_disease": (
            "**🌾 Rice Pest & Disease Remedies:**\n"
            "• **Yellowing Leaves (Khaira / Zinc Deficiency):** Lower leaves turn yellow and bronze with rusty brown spots. Spray *0.5% Zinc Sulphate (ZnSO₄) + 1% Urea* (5 kg ZnSO₄ + 10 kg Urea in 1000 L water/ha).\n"
            "• **Yellow Stem Borer (Dead Heart / White Earhead):** Apply *Cartap Hydrochloride 4G* @ 25 kg/ha or spray *Chlorantraniliprole 18.5% SC* @ 0.3 ml/L.\n"
            "• **Bacterial Leaf Blight (BLB):** Drain excess standing water; spray *Copper Oxychloride* (2.5 g/L) + *Streptocycline* (0.1 g/L).\n"
            "• **Brown Plant Hopper (BPH):** Avoid excess urea; spray *Pymetrozine 50% WDG* at the base of clumps."
        ),
        "irrigation": (
            "**🌾 Water Management in Paddy:**\n"
            "• Maintain 2-3 cm shallow water layer for the first week after transplanting to facilitate seedling establishment.\n"
            "• During tillering and panicle development, maintain 3-5 cm water depth.\n"
            "• Practice **Alternate Wetting and Drying (AWD)** to conserve water and reduce greenhouse methane emissions.\n"
            "• Drain standing water 10-12 days before harvest to facilitate mechanized reaping."
        ),
        "sowing": (
            "**🌾 Paddy Nursery & Sowing Guide:**\n"
            "• **Kharif Nursery:** May 20 – June 20; transplant 21-25 day old seedlings (2-3 seedlings per hill).\n"
            "• **Spacing:** 20x15 cm for dwarf varieties; 20x20 cm for hybrids.\n"
            "• **Popular High-Yielding Varieties:** *Swarna (MTU-7029)*, *IR-64*, *Pusa Basmati 1121*, *Pusa 1509*, *Samba Mahsuri (BPT-5204)*."
        )
    },
    "Cotton": {
        "fertilizer": (
            "**🌱 Cotton Fertilizer Dosage:**\n"
            "• **Recommended Dose:** 120-150 kg N, 60 kg P₂O₅, 60 kg K₂O per hectare (for Bt hybrids in black soils).\n"
            "• Apply 100% Phosphorus and 50% Potash as basal.\n"
            "• Split Nitrogen into 3 equal top-dressings: 30, 60, and 90 days after sowing.\n"
            "• Foliar spray of **1% Magnesium Sulphate + 1% 19:19:19** at flowering prevents leaf reddening."
        ),
        "pest_disease": (
            "**🌱 Managing Pink Bollworm & Pests in Cotton:**\n"
            "• **Pink Bollworm (Pectinophora gossypiella):** Install 8-10 pheromone traps (Gossyplure) per hectare at 45 DAS. Spray *Neem oil (1500 ppm)* early. If threshold exceeds 8 moths/trap, spray *Emamectin Benzoate 5% SG* @ 0.5 g/L or *Chlorantraniliprole 18.5% SC* @ 0.3 ml/L.\n"
            "• **Whitefly & Jassids:** Spray *Diafenthiuron 50% WP* (1.2 g/L) or *Flonicamid 50% WG* (0.3 g/L).\n"
            "• **Avoid Repeated Pyrethroids:** Repeated synthetic pyrethroid sprays cause massive whitefly flare-ups."
        ),
        "irrigation": (
            "**🌱 Cotton Irrigation Strategy:**\n"
            "• Black cotton soil retains deep moisture; avoid over-irrigation during vegetative growth.\n"
            "• Peak water requirement stages: **Flowering and Boll Development**.\n"
            "• Avoid heavy watering during square formation to stop square and flower drop."
        )
    },
    "Onion": {
        "fertilizer": (
            "**🧅 Balanced Fertilizer Regimen for Onion:**\n"
            "• **Dose:** 100-125 kg N, 50 kg P₂O₅, 80 kg K₂O, and **25-30 kg Sulphur** per hectare.\n"
            "• Sulphur is vital: it directly improves bulb pungency, firmness, and storage shelf-life!\n"
            "• Apply full P, K, and Sulphur + 50% N at transplanting; top dress remaining N in two splits at 30 and 45 days."
        ),
        "pest_disease": (
            "**🧅 Onion Pest & Disease Protection:**\n"
            "• **Onion Thrips (Thrips tabaci):** Causes silvery white patches on leaves. Spray *Spinetoram 11.7% SC* (1 ml/L) or *Fipronil 5% SC* (1.5 ml/L).\n"
            "• **Purple Blotch (Alternaria porri):** Purple centered sunken lesions. Spray *Mancozeb 75% WP* (2.5 g/L) or *Hexaconazole* (1 ml/L).\n"
            "• **Basal Rot / Damping Off:** Drench nursery beds with *Trichoderma viride* or *Carbendazim* (2 g/L)."
        ),
        "harvest": (
            "**🧅 Onion Harvesting & Storage Curing:**\n"
            "• Harvest when 50% tops have collapsed (neck fall).\n"
            "• **Critical:** Discontinue all irrigation 10-15 days before harvest to facilitate neck drying!\n"
            "• Field cure with tops intact for 3-5 days in windrows.\n"
            "• Cut leaves leaving 2-3 cm neck, then shade cure in well-ventilated sheds for 10-15 days before storage."
        )
    },
    "Tomato": {
        "pest_disease": (
            "**🍅 Combating Tomato Leaf Curl & Blight Diseases:**\n"
            "• **Tomato Leaf Curl Virus (ToLCV):** Transmitted by Whiteflies. Spray *Thiamethoxam 25% WG* @ 0.3 g/L or *Acetamiprid 20% SP* @ 0.5 g/L to suppress vectors; install yellow sticky traps (20-25/ha).\n"
            "• **Early / Late Blight:** Concentric dark rings on foliage. Spray *Metalaxyl 8% + Mancozeb 64%* (2 g/L) or *Azoxystrobin*.\n"
            "• **Fruit Borer (Helicoverpa):** Spray *Chlorantraniliprole 18.5% SC* (0.3 ml/L) or *Indoxacarb*.\n"
            "• **Blossom End Rot (Black base on fruits):** Physiological disorder caused by Calcium deficiency and erratic watering. Spray 0.5% Calcium Nitrate."
        ),
        "fertilizer": (
            "**🍅 Tomato Fertilizer Dosage:**\n"
            "• **Recommendation:** 150 kg N, 80 kg P₂O₅, 100 kg K₂O per hectare.\n"
            "• Heavy potassium feeder during fruit development.\n"
            "• Apply micronutrient foliar spray (Multiplex/Zinc/Boron) at flowering to boost fruit set."
        )
    },
    "Sugarcane": {
        "fertilizer": (
            "**🎋 Balanced Fertilizer Regimen for Sugarcane:**\n"
            "• **Dose:** 200-250 kg N, 60-80 kg P₂O₅, 60-80 kg K₂O per hectare.\n"
            "• Apply 100% P and 50% K with 1/3rd N as basal in furrows with 25 kg Zinc Sulphate.\n"
            "• Top dress 1/3rd N at tillering (45-60 days) and remaining 1/3rd N + 50% K at grand growth (90-120 days) before earthing up."
        ),
        "pest_disease": (
            "**🎋 Sugarcane Pest & Disease Control:**\n"
            "• **Early Shoot Borer:** Apply *Chlorantraniliprole 0.4% G* in soil furrows at planting, or spray *Cartap Hydrochloride*.\n"
            "• **Red Rot (Colletotrichum falcatum):** Use disease-free certified setts; dip setts in Carbendazim (1 g/L) hot water treatment before planting."
        )
    },
    "Apple": {
        "pest_disease": (
            "**🍎 High-Altitude Apple Orchard Care & Scab Defense:**\n"
            "• **Apple Scab (Venturia inaequalis):** Spray *Dodine 65% WP* (0.75 g/L) at green tip to pink bud stages, followed by *Mancozeb* or *Difenoconazole* post-petal fall.\n"
            "• **San Jose Scale:** Apply dormant spray of 2% Horticultural Mineral Oil (HMO) during late winter before bud break.\n"
            "• **Pruning:** Conduct winter dormant spur pruning to open up the canopy for optimum sunlight and air circulation."
        ),
        "fertilizer": (
            "**🍎 Apple Tree Nutrient Schedule:**\n"
            "• Mature bearing tree (10+ years): 700 g Nitrogen, 350 g P₂O₅, 700 g K₂O + 50 kg Farmyard Manure (FYM) per tree per year.\n"
            "• Apply FYM, full P & K, and 50% N during December-January (dormancy).\n"
            "• Apply remaining 50% N after fruit set in May."
        )
    }
}

# Domain-Specific Broad Topics
BROAD_TOPICS = [
    {
        "intent": "fertilizer_general",
        "keywords": ["fertilizer", "fertilizers", "fert", "npk", "urea", "dap", "potash", "khad", "nitrogen", "phosphorus", "potassium", "zinc", "sulphur", "micronutrient", "dose", "nutrient"],
        "title": "🧪 Scientific Fertilizer & Balanced Nutrient Management",
        "reply": (
            "**Principles of Balanced Crop Nutrition (ICAR Standards):**\n\n"
            "1. **The 4R Nutrient Rule:** Right fertilizer source, Right rate, Right time, Right place.\n"
            "2. **Standard Indian N-P-K Ratio:** Recommended benchmark is **4:2:1** for cereals, **1:2:1** for pulses, and **3:2:1** for oilseeds.\n"
            "3. **Basal vs Top-Dressing:**\n"
            "   • Apply 100% Phosphorus (DAP/SSP) and Potash (MOP) as basal at sowing.\n"
            "   • Split Nitrogen (Urea) into 2-3 doses to avoid leaching and volatilization loss.\n"
            "4. **Secondary & Micronutrients:** Zinc (Zn), Boron (B), and Sulphur (S) enhance crop harvest by 15-25%.\n"
            "5. **Soil Testing:** Always refer to your **Soil Health Card** before purchasing bulk chemical fertilizer."
        ),
        "suggestions": [
            "What fertilizer to use for wheat?",
            "Fertilizer dose for rice paddy",
            "How to improve soil fertility?"
        ]
    },
    {
        "intent": "irrigation_general",
        "keywords": ["irrigation", "water", "watering", "drip", "sprinkler", "drought", "flood", "pmksy", "pani", "sinchai", "moisture"],
        "title": "💧 Modern Irrigation & Water Conservation Strategies",
        "reply": (
            "**Water Management Strategies for Maximum Crop Per Drop:**\n\n"
            "1. **Micro-Irrigation (Drip & Sprinkler):**\n"
            "   • Saves 40–60% water, increases yield by 20–35%, and reduces weed growth.\n"
            "   • Government subsidies up to **55% for small/marginal farmers** under *Per Drop More Crop (PDMC)*.\n"
            "2. **Critical Growth Stages:** Never let the crop suffer moisture stress during flowering and seed/pod development.\n"
            "3. **Organic Mulching:** Spread straw, crop residues, or plastic mulch to reduce soil surface evaporation by 50%.\n"
            "4. **Broad Bed & Furrow (BBF):** Provides drainage during excess monsoons and conserves moisture in dry spells."
        ),
        "suggestions": [
            "Critical irrigation stages in wheat",
            "Drip irrigation for tomatoes",
            "Water management in paddy"
        ]
    },
    {
        "intent": "pest_disease_general",
        "keywords": ["pest", "pests", "disease", "diseases", "insect", "insects", "keeda", "bimari", "fungus", "fungicide", "pesticide", "spray", "blight", "rust", "rot", "wilt", "aphid", "worm", "caterpillar", "borer"],
        "title": "🛡️ Integrated Pest & Disease Management (IPM)",
        "reply": (
            "**Safe & Effective Integrated Pest Management (IPM):**\n\n"
            "1. **Cultural & Mechanical:**\n"
            "   • Install **Yellow & Blue sticky traps** (15-20/ha) for whiteflies and thrips.\n"
            "   • Install **Pheromone traps** (8-10/ha) to monitor moth flights before caterpillars multiply.\n"
            "2. **Biological Spray (First Line of Defense):**\n"
            "   • Spray **Neem oil (1500 ppm)** @ 5 ml/L water.\n"
            "   • Use *Trichoderma viride* (seed treatment 5-10 g/kg) to prevent root rots and wilts.\n"
            "3. **Targeted Chemical Spray (Only when Economic Threshold Level is crossed):**\n"
            "   • Never spray broad-spectrum pyrethroids repeatedly; rotate chemical groups to prevent pest resistance.\n"
            "   • Spray during early morning (7-10 AM) or late afternoon (4-6 PM) to protect pollinator bees."
        ),
        "suggestions": [
            "How to control bollworm in cotton?",
            "Why are rice leaves turning yellow?",
            "How to prevent onion purple blotch?"
        ]
    },
    {
        "intent": "organic_farming",
        "keywords": ["organic", "jaivik", "natural farming", "compost", "vermicompost", "cow dung", "jeevamrut", "panchagavya", "biofertilizer", "green manure"],
        "title": "🌿 Organic & Natural Farming Practices",
        "reply": (
            "**Key Principles of Organic Farming in India:**\n\n"
            "1. **Soil Enrichment:** Apply 8-10 tonnes/ha of well-rotted FYM or 3-5 tonnes/ha of Vermicompost.\n"
            "2. **Jeevamrut Preparation:** Mix 10 kg native cow dung + 10 L cow urine + 2 kg jaggery + 2 kg pulse flour + handful of field soil in 200 L water; ferment for 48 hours.\n"
            "3. **Biofertilizers:** Inoculate seeds with *Rhizobium* (for pulses), *Azotobacter* (for cereals), and *PSB* (Phosphate Solubilizing Bacteria).\n"
            "4. **Green Manuring:** Sow *Dhaincha* (Sesbania) or *Sunnhemp* in summer and plough into soil at 45 days before Kharif sowing."
        ),
        "suggestions": [
            "How to make vermicompost?",
            "Government subsidy for organic farming",
            "Biofertilizer seed treatment procedure"
        ]
    },
    {
        "intent": "government_schemes",
        "keywords": ["scheme", "schemes", "subsidy", "subsidies", "pm kisan", "pm-kisan", "fasal bima", "pmfby", "kcc", "kisan credit card", "loan", "loans", "kusum", "soil health card", "yojana", "yojna"],
        "title": "🏛️ Major Indian Agricultural Welfare & Support Schemes",
        "reply": (
            "**Top Central Government Farmer Welfare Schemes:**\n\n"
            "1. **PM-KISAN (Samman Nidhi):**\n"
            "   • Direct income support of **₹6,000 per year** in 3 equal DBT installments of ₹2,000 directly into farmer bank accounts.\n"
            "2. **Pradhan Mantri Fasal Bima Yojana (PMFBY):**\n"
            "   • Comprehensive crop loss insurance against natural disasters. Farmer premium: 2% (Kharif), 1.5% (Rabi), 5% (Commercial/Horticulture). National Helpline: **14447**.\n"
            "3. **Kisan Credit Card (KCC):**\n"
            "   • Short-term subsidized production loans up to ₹3 Lakh at an effective **4% interest rate** (with prompt repayment incentive).\n"
            "4. **PM-KUSUM Scheme:**\n"
            "   • Up to 60–90% subsidy for setting up standalone **Solar Agriculture Water Pumps**.\n"
            "5. **Soil Health Card Scheme:**\n"
            "   • Free soil testing report issued every 2 years indicating 12 parameters."
        ),
        "suggestions": [
            "How to check PM Kisan payment status?",
            "Documents needed for Kisan Credit Card",
            "Crop insurance claim procedure"
        ]
    },
    {
        "intent": "yield_boost",
        "keywords": ["yield", "production", "paidaawar", "harvest", "maximize yield", "increase yield", "boost yield", "higher yield", "improve yield"],
        "title": "📈 5 Scientific Pillars to Increase Crop Yield",
        "reply": (
            "**Proven Agronomic Strategies for Maximum Crop Harvest:**\n\n"
            "1. **Quality Certified Seed:** Switch to certified disease-resistant hybrid seed (yield boost of 15-25%).\n"
            "2. **Soil Health & Balanced NPK:** Test soil every 2 years; do not overuse Urea without balanced Phosphorus, Potash, and Micronutrients (Zinc, Boron).\n"
            "3. **Timely Sowing:** Every 7-day delay past optimal sowing window reduces grain yield by 150-200 kg/ha.\n"
            "4. **Critical Irrigation:** Ensure soil moisture at flowering and seed/grain formation stages.\n"
            "5. **Weed Control within First 30 Days:** 80% of nutrient competition occurs during the first 30 days after germination."
        ),
        "suggestions": [
            "Predict yield for my farm now",
            "What fertilizer to use for wheat?",
            "How to use CropYield AI website?"
        ]
    },
    {
        "intent": "soil_health",
        "keywords": ["soil", "mitti", "saline", "alkaline", "acidic", "soil ph", "soil test", "soil health", "gypsum", "lime"],
        "title": "🌱 Soil Health Restoration & pH Correction",
        "reply": (
            "**Best Practices for Soil Health Management:**\n\n"
            "1. **Organic Carbon Enhancement:**\n"
            "   • Apply 8–10 tonnes/ha of Farm Yard Manure (FYM) or Vermicompost before land preparation.\n"
            "   • Incorporate Green Manuring (Dhaincha / Sunnhemp) once every two years.\n"
            "2. **Correction of Soil pH:**\n"
            "   • **Acidic Soil (pH < 6.0):** Broadcast agricultural lime or dolomite @ 2–4 tonnes/ha.\n"
            "   • **Alkaline/Sodic Soil (pH > 8.5):** Apply agricultural gypsum @ 3–5 tonnes/ha followed by leaching.\n"
            "3. **Microbial Biofertilizers:**\n"
            "   • Seed treatment with *Azotobacter* / *Rhizobium* and *Phosphorus Solubilizing Bacteria (PSB)* saves 20-25% chemical fertilizer."
        ),
        "suggestions": [
            "What soil is best for wheat?",
            "How to improve red soil fertility?",
            "Green manuring techniques"
        ]
    },
    {
        "intent": "mandi_prices",
        "keywords": ["mandi", "bhav", "market price", "market prices", "apmc", "enam", "msp", "rate", "rates", "selling price"],
        "title": "🏪 Mandi Market Prices & e-NAM Trading Portal",
        "reply": (
            "**Accessing Fair Mandi Prices & Government MSP:**\n\n"
            "1. **National Agriculture Market (e-NAM):**\n"
            "   • Check live electronic auction rates across 1,361+ integrated APMC mandis at **[enam.gov.in](https://enam.gov.in)**.\n"
            "2. **Agmarknet Portal:**\n"
            "   • Daily commodity-wise wholesale price arrival data available at **agmarknet.gov.in**.\n"
            "3. **Minimum Support Price (MSP):**\n"
            "   • Government announces MSP for 22 mandated crops before sowing seasons to safeguard farmers against distress sales.\n"
            "4. **Kisan Call Center:**\n"
            "   • Dial **1800-180-1551** (Toll-Free) for live APMC mandi prices in your district."
        ),
        "suggestions": [
            "Check government schemes for farmers",
            "Predict crop yield before harvest",
            "How to get Kisan Credit Card?"
        ]
    },
    {
        "intent": "organic_pesticides",
        "keywords": ["neemastra", "brahmastra", "agniastra", "bio pesticide", "organic pesticide", "natural spray", "homemade spray", "herbal spray"],
        "title": "🌿 Natural Bio-Pesticide Recipes (Neemastra & Brahmastra)",
        "reply": (
            "**Traditional Natural Formulations for Pest Defense (Zero Chemical):**\n\n"
            "1. **Neemastra (For Sucking Pests, Aphids & Whiteflies):**\n"
            "   • 5 kg crushed fresh neem leaves + 5 kg cow dung + 5 L cow urine in 100 L water. Ferment for 48 hours in shade. Filter and spray directly.\n\n"
            "2. **Brahmastra (For Tough Borers & Large Caterpillars):**\n"
            "   • Crush 2 kg neem leaves, 2 kg papaya leaves, 2 kg guava leaves, and 2 kg custard apple (sitaphal) leaves. Boil in 10 L cow urine until reduced to half. Dilute 2-3 L per 100 L water.\n\n"
            "3. **Agniastra (For Resistant Stem Borers & Leaf Folders):**\n"
            "   • Boil 500g crushed garlic + 500g spicy green chillies + 500g neem leaves in 15 L cow urine. Highly potent against stubborn insect infestations."
        ),
        "suggestions": [
            "How to make vermicompost?",
            "Organic farming tips",
            "How to control bollworm in cotton?"
        ]
    },
    {
        "intent": "crop_rotation",
        "keywords": ["rotation", "crop rotation", "intercropping", "intercrop", "companion", "mixed cropping", "soil exhaustion"],
        "title": "🔄 Scientific Crop Rotation & Intercropping Rules",
        "reply": (
            "**Principles of Sustainable Crop Rotation:**\n\n"
            "1. **Cereal followed by Legume:** Always follow heavy nitrogen eaters (Rice, Wheat, Maize) with nitrogen-fixing pulses (Chickpea, Moong, Urad). This naturally enriches your soil with 30–50 kg/ha atmospheric nitrogen!\n"
            "2. **Deep vs Shallow Root Alternation:** Alternate deep-rooted crops (Cotton, Pigeon Pea) with shallow-rooted crops (Wheat, Onion) to prevent hardpan formation and utilize multi-depth soil moisture.\n"
            "3. **Family Disruption:** Never plant crops of the same botanical family consecutively (e.g., Potato ➔ Tomato ➔ Chilli) to break soil-borne fungus and nematode lifecycles."
        ),
        "suggestions": [
            "How to improve soil health?",
            "Fertilizer dose for wheat",
            "What crops are supported?"
        ]
    }
]


# ==============================================================================
# 🧠 ADVANCED CHATGPT-STYLE AGRICULTURAL DOUBT SOLVER ENGINE
# ==============================================================================

SPECIFIC_FARMING_DOUBTS = [
    {
        "id": "flower_fruit_dropping",
        "keywords": ["flower drop", "flower falling", "flowers falling", "fruit drop", "fruit falling", "phool gir", "phool jhad", "fal gir", "drop flowers", "dropping flowers", "shedding flowers"],
        "title": "🌸 Solution for Flower & Fruit Dropping in Crops",
        "solver": (
            "### 🩺 Diagnosis: Why Are Flowers and Young Fruits Dropping?\n\n"
            "Flower and fruit dropping is typically triggered by three main factors:\n"
            "1. **Hormonal Imbalance (Auxin deficiency):** The plant produces abscission layers at the flower pedicel.\n"
            "2. **Boron & Calcium Deficiency:** Essential for pollen tube growth and fertilization; without boron, flowers cannot set fruit.\n"
            "3. **Water & Temperature Stress:** Irregular heavy watering or sudden dry spells during peak flowering.\n\n"
            "---\n\n"
            "### ⚡ Step-by-Step Immediate Action Plan\n\n"
            "1. **Hormonal Growth Regulator Spray (Immediate Fruit Set):**\n"
            "   • Spray **Planofix (Alpha Naphthyl Acetic Acid - NAA 4.5% SL)** @ **4 ml per 15 Liters of water** (or 0.25 ml/L). Spray early morning during active flowering.\n"
            "   • *Important:* Do not overdose Planofix, as excessive concentration can burn buds.\n\n"
            "2. **Micronutrient Foliar Feeding (Boron + Calcium):**\n"
            "   • Spray **Water Soluble Boron (Disodium Octaborate Tetrahydrate 20%)** @ **1.0 g to 1.5 g per Liter of water** along with **Chelated Calcium** (1 g/L).\n\n"
            "3. **Irrigation Regulation:**\n"
            "   • Maintain uniform, light soil moisture. **Never flood irrigate or let the field completely dry out** during active flowering!\n\n"
            "4. **Organic Remedy:**\n"
            "   • Spray **Sour Buttermilk (Khatta Chhaach)**: 5 Liters of 5-day fermented sour buttermilk diluted in 100 Liters of water per acre. It provides natural lactic acid and micro-elements that arrest flower shedding."
        ),
        "suggestions": [
            "What fertilizer to apply after fruit set?",
            "How to control thrips in chili?",
            "Drip irrigation schedule for vegetables"
        ]
    },
    {
        "id": "yellow_leaves",
        "keywords": ["yellow leaf", "yellow leaves", "leaves yellow", "yellowing", "patti peeli", "patte peele", "khaira", "chlorosis", "pale leaves", "yellow spots on leaves"],
        "title": "🟡 Diagnosis & Solution for Yellowing Leaves (Chlorosis)",
        "solver": (
            "### 🩺 Diagnosis: Why Are Your Crop Leaves Turning Yellow?\n\n"
            "The exact location of yellowing reveals the underlying cause:\n"
            "1. **Lower / Older Leaves Yellow First:** **Nitrogen (Urea) Deficiency** — mobile nutrient translocating to young shoots.\n"
            "2. **Lower Leaves Bronze / Rusty Brown Spots (Especially in Paddy):** **Zinc Deficiency (Khaira Disease)** — widespread across Indo-Gangetic and alkaline soils.\n"
            "3. **Top / Young Leaves Yellow First (Veins stay green):** **Iron (Fe) or Sulphur (S) Deficiency** — common in calcareous, high-pH soils.\n"
            "4. **Entire Plant Pale + Stunted Growth:** Waterlogged roots choking oxygen, or severe root nematode attack.\n\n"
            "---\n\n"
            "### ⚡ Step-by-Step Immediate Solution\n\n"
            "1. **For Paddy / Rice (Zinc Deficiency - Khaira Disease):**\n"
            "   • Spray **0.5% Zinc Sulphate (21% or 33%) + 1.0% Urea**.\n"
            "   • **Dosage:** 5 kg Zinc Sulphate + 10 kg Urea dissolved in 1,000 Liters of water per hectare (or 75g Zinc + 150g Urea per 15L pump).\n\n"
            "2. **For General Nitrogen Deficiency (Vegetables, Wheat, Maize):**\n"
            "   • Top-dress Urea @ 25-30 kg/acre, or foliar spray **Water Soluble NPK 19:19:19** @ **5 g/Liter of water** for rapid recovery within 4 days.\n\n"
            "3. **For Iron Chlorosis (Young leaves pale yellow in alkaline soils):**\n"
            "   • Spray **Ferrous Sulphate (FeSO₄)** @ 5 g/L + Citric acid (nimbu sat) @ 0.5 g/L.\n\n"
            "4. **Drainage Check:**\n"
            "   • If field is soggy, dig drainage furrows immediately. Roots need oxygen to absorb nutrients."
        ),
        "suggestions": [
            "Fertilizer schedule for paddy",
            "How to test soil pH?",
            "Organic compost preparation"
        ]
    },
    {
        "id": "leaf_curl_crinkling",
        "keywords": ["leaf curl", "leaves curling", "curled leaves", "patti mud", "patti sikud", "churda murda", "crinkling", "curling up", "curling down"],
        "title": "🌿 Curing Leaf Curl & Crinkling in Crops (Chilli, Tomato, Cotton)",
        "solver": (
            "### 🩺 Diagnosis: What Causes Leaf Curl?\n\n"
            "1. **Upward Leaf Curling (Boat Shape):** Caused by **Thrips** sucking sap from the upper leaf surface.\n"
            "2. **Downward Leaf Curling (Inverted Cup):** Caused by **Mites (Yellow/Red Spider Mites)** feeding on the underside of leaves.\n"
            "3. **Thickened, Puckered Leaves with Yellow Veins:** **Leaf Curl Virus (Chilli/Tomato Leaf Curl)** — transmitted exclusively by **Whiteflies (*Bemisia tabaci*)**.\n\n"
            "---\n\n"
            "### ⚡ Step-by-Step Treatment & Remedy\n\n"
            "1. **Vector & Sucking Pest Knockdown (Whiteflies & Thrips):**\n"
            "   • Spray **Acetamiprid 20% SP** @ **0.5 g/L** OR **Thiamethoxam 25% WG** @ **0.3 g/L** OR **Diafenthiuron 50% WP** @ **1.2 g/L**.\n"
            "2. **For Downward Mite Curl:**\n"
            "   • Spray **Spiromesifen 22.9% SC (Oberon)** @ **1 ml/L** OR **Wettable Sulphur 80% WP** @ **3 g/L**.\n"
            "3. **Physical Traps (Non-Chemical Prevention):**\n"
            "   • Hang **Yellow Sticky Traps** (for Whiteflies) and **Blue Sticky Traps** (for Thrips) @ **20 to 25 traps per acre** at plant canopy height.\n"
            "4. **Organic Spray:**\n"
            "   • Spray **Neem Oil (10,000 ppm)** @ **2 ml/L** mixed with a few drops of mild soap. Repeat every 7 days."
        ),
        "suggestions": [
            "How to control whiteflies organically?",
            "Fertilizer dose for tomato",
            "Pesticide spray precautions"
        ]
    },
    {
        "id": "wilting_sudden_death",
        "keywords": ["wilting", "wilt", "plant drying", "sudden drying", "ukhta", "murjhana", "root rot", "collar rot", "damping off", "plants dying"],
        "title": "🥀 Stopping Crop Wilting, Root Rot & Damping-Off",
        "solver": (
            "### 🩺 Diagnosis: Why Are Plants Suddenly Wilting?\n\n"
            "Wilting occurs when water-conducting vessels (xylem) are clogged by fungal pathogens (*Fusarium*, *Rhizoctonia*, *Pythium*) or bacteria (*Ralstonia*).\n"
            "• **Diagnostic Test:** Cut the lower stem and place it in clear water. If white milky threads stream out, it is **Bacterial Wilt**. If the inside vascular ring is brown/black, it is **Fusarium Fungal Wilt**.\n\n"
            "---\n\n"
            "### ⚡ Immediate Step-by-Step Solution\n\n"
            "1. **Soil Drenching (Target Root Zone Immediately):**\n"
            "   • For Fungal Wilt / Root Rot: Drench roots with **Copper Oxychloride 50% WP (Blitox)** @ **3 g/L** OR **Carbendazim 12% + Mancozeb 63% WP (Saaf)** @ **2 g/L**.\n"
            "   • For Bacterial Wilt: Add **Streptocycline (Streptomycin sulphate)** @ **1 g per 10 Liters of water** to the drench.\n"
            "2. **Biological Soil Immunization (Best Long-term Protection):**\n"
            "   • Mix **Trichoderma viride or T. harzianum** (2 kg) in 100 kg moist Farm Yard Manure (FYM). Keep under shade for 7 days to multiply, then broadcast near plant root zones.\n"
            "3. **Moisture Management:**\n"
            "   • Stop heavy flood watering immediately! Saturated soil without oxygen accelerates root rot by 500%."
        ),
        "suggestions": [
            "Seed treatment with Trichoderma",
            "Soil solarization before sowing",
            "Crop rotation to break wilt cycle"
        ]
    },
    {
        "id": "saline_borewell_water",
        "keywords": ["borewell water", "salty water", "saline water", "saline soil", "alkaline water", "hard water", "salt in water", "khaara paani", "usar", "namak wala paani"],
        "title": "🌊 Managing Saline / Hard Borewell Water & Salty Soils",
        "solver": (
            "### 🩺 Understanding Saline & Hard Borewell Water in Agriculture\n\n"
            "High EC (Electrical Conductivity) and Sodium Adsorption Ratio (SAR) cause salt toxicity, leaf tip scorch, and block plant roots from taking up calcium and phosphorus.\n\n"
            "---\n\n"
            "### ⚡ Action Plan: How to Farm Successfully with Saline Water\n\n"
            "1. **Gypsum Application (Salt Neutralizer):**\n"
            "   • Apply agricultural **Gypsum (Calcium Sulphate)** @ **1 to 2 tonnes per acre**. Calcium replaces toxic sodium on soil particles, allowing sodium to leach away.\n"
            "   • Place bags of crushed gypsum in irrigation channels/tanks so the flowing water dissolves calcium continuously.\n"
            "2. **Switch to Salt-Tolerant Crops:**\n"
            "   • **High Salt Tolerance:** Barley (*Jau*), Mustard (*Sarson*), Cotton (*Kapas*), Sugarbeet, Dates, Pomegranate.\n"
            "   • **Medium Salt Tolerance:** Wheat, Sorghum (*Jowar*), Pearl Millet (*Bajra*), Spinach.\n"
            "   • **Avoid (Highly Sensitive):** Pulses (Gram, Moong, Urad), Onion, Strawberry, Citrus.\n"
            "3. **Organic Carbon Buffer:**\n"
            "   • Add heavy doses of **Farm Yard Manure (FYM)** (8-10 tonnes/acre) or Green Manure (*Dhaincha* / Sesbania). Organic matter acts as a sponge, shielding roots from salt.\n"
            "4. **Drip Irrigation Over Flood Irrigation:**\n"
            "   • Drip irrigation keeps the active root zone continuously moist, pushing salts to the periphery of the wetting bulb."
        ),
        "suggestions": [
            "How to test water EC and TDS?",
            "Green manuring with Dhaincha",
            "Gypsum dosage calculation"
        ]
    },
    {
        "id": "frost_cold_wave",
        "keywords": ["frost", "cold wave", "winter cold", "pala", "sheet lahar", "frost protection", "freezing temperature", "fog damage"],
        "title": "❄️ Protecting Crops from Frost & Severe Winter Cold (Pala)",
        "solver": (
            "### 🩺 How Frost Damages Crops\n\n"
            "When night temperatures drop below 4°C with calm winds, water inside plant cell walls freezes, expanding and bursting the plant tissues. Potato, Mustard, Gram, Tomato, and young fruit orchards are most vulnerable.\n\n"
            "---\n\n"
            "### ⚡ Immediate Frost Defense Measures\n\n"
            "1. **Evening Light Irrigation (Most Effective!):**\n"
            "   • Water has a high specific heat capacity. Irrigating your field on the evening of an anticipated frost keeps soil temperature 2°C to 4°C warmer through the night!\n"
            "2. **Smoke Screening (Dhuan / Hearth along Windward Border):**\n"
            "   • Burn dry and moist weeds, cow dung cakes, and leaf residue along the northern and western field borders at 11 PM to 4 AM. The smoke cloud blocks radiant heat loss.\n"
            "3. **Chemical Foliar Protection (Anti-Frost Spray):**\n"
            "   • Spray **Soluble Sulphur 80% WDG** @ **2 g to 3 g per Liter of water** (increases plant cell sap osmotic pressure).\n"
            "   • Spray **0.1% Commercial Sulphuric Acid (H₂SO₄)** (1 ml in 1 Liter water) across standing mustard and potato crops.\n"
            "4. **Thatched Covers (Tat/Palli):**\n"
            "   • Cover young saplings and nursery beds with straw or polythene on the north-west side."
        ),
        "suggestions": [
            "Weather auto-sync on predict page",
            "Mustard crop winter care",
            "Protecting potato from late blight in fog"
        ]
    },
    {
        "id": "jeevamrut_preparation",
        "keywords": ["how to make jeevamrut", "prepare jeevamrut", "jeevamrutham", "jeevamrit", "recipe jeevamrut", "panchagavya", "ghanjeevamrut"],
        "title": "🌿 Authentic Step-by-Step Jeevamrut Preparation for 1 Acre",
        "solver": (
            "### 🌾 Traditional Subhash Palekar Natural Farming (ZBNF) Formulation\n\n"
            "Jeevamrut is not a fertilizer; it is a **microbial culture** that multiplies trillions of beneficial soil bacteria and mycorrhizal fungi.\n\n"
            "---\n\n"
            "### 🧪 Ingredients Required for 1 Acre (200 Liters Water)\n\n"
            "1. **Native Cow Dung (*Desi Gai ka Gobar*):** 10 kg (fresh)\n"
            "2. **Native Cow Urine (*Gau Mutra*):** 5 to 10 Liters (aged urine is fine)\n"
            "3. **Jaggery (*Gud*):** 2 kg (organic/dark unrefined jaggery)\n"
            "4. **Pulse Flour (*Besan*):** 2 kg (gram, pigeon pea, or moong flour — protein for microbes)\n"
            "5. **Virgin Bio-active Soil:** Handful (100g) taken from beneath a Banyan tree or undisturbed field bund.\n"
            "6. **Clean Water:** 200 Liters in a plastic drum.\n\n"
            "---\n\n"
            "### 🥣 Preparation Steps (48 Hours Fermentation)\n\n"
            "1. Fill a 200L plastic drum with 190 Liters of water.\n"
            "2. In a bucket, thoroughly mix 10 kg cow dung + 10L urine + 2 kg jaggery + 2 kg pulse flour + virgin soil with water into a smooth paste.\n"
            "3. Pour this slurry into the drum and stir vigorously in a **clockwise direction** with a wooden stick for 2 minutes.\n"
            "4. Cover the drum with a jute gunny bag and keep in shaded location.\n"
            "5. Stir clockwise for 2 minutes every morning and evening.\n"
            "6. **Ready in 48 hours in summer (3-4 days in winter).** Use within 7 days.\n\n"
            "---\n\n"
            "### 💧 Application Dosage\n\n"
            "• **Through Irrigation Channel / Drip:** Filter through double cloth and mix 200L per acre with irrigation water twice a month.\n"
            "• **Foliar Spray:** Filter through fine muslin cloth; dilute 10% (10 L Jeevamrut in 100 L water) per acre."
        ),
        "suggestions": [
            "How to prepare Neemastra?",
            "How to prepare Brahmastra?",
            "Beejamrut seed treatment guide"
        ]
    },
    {
        "id": "crop_insurance_pmfby_claim",
        "keywords": ["insurance", "bima", "claim", "pmfby", "fasal bima", "crop damage", "crop damaged", "rain damage", "flood damage", "flood claim", "hail damage", "drought damage", "bima claim", "insurance claim"],
        "title": "🏛️ Step-by-Step Crop Insurance Claim Procedure (PMFBY)",
        "solver": (
            "### 🚨 What to Do Immediately When Crop Loss Occurs\n\n"
            "Under **Pradhan Mantri Fasal Bima Yojana (PMFBY)**, you have a strict **72-hour window** to notify authorities for localized calamities (Hailstorm, Landslide, Inundation/Flooding, Cloudburst, Post-harvest unseasonal rain).\n\n"
            "---\n\n"
            "### ⚡ 4-Step Claim Process (Within 72 Hours!)\n\n"
            "1. **Intimate Loss Within 72 Hours (Any of these 3 ways):**\n"
            "   • **Mobile App:** Download the official **Crop Insurance App** on Android, upload photos of the damaged field with GPS coordinates.\n"
            "   • **Toll-Free Helpline:** Dial **14447** (National PMFBY Helpline) or your insurance company's dedicated number.\n"
            "   • **In-Person:** Submit written notice to your local Agriculture Officer (DAO/ADO), Bank branch where premium was deducted, or nearest CSC Center.\n\n"
            "2. **Loss Assessment (Within 7-10 Days):**\n"
            "   • A joint survey team consisting of an Agricultural Officer, Insurance representative, and Village Sarpanch will inspect your field.\n"
            "   • Be present during the inspection and take photographs.\n\n"
            "3. **Documents Required:**\n"
            "   • Land records (7/12 extract, Khasra/Khatauni).\n"
            "   • Sowing certificate / Self-declaration.\n"
            "   • Bank passbook copy & Aadhaar card.\n"
            "   • Premium deduction slip / receipt from bank.\n\n"
            "4. **Settlement:**\n"
            "   • Claim amount is directly transferred via Direct Benefit Transfer (DBT) into your linked bank account."
        ),
        "suggestions": [
            "Check PM-KISAN status",
            "Kisan Credit Card loan process",
            "Soil health card testing"
        ]
    },
    {
        "id": "fertilizer_mixing_compatibility",
        "keywords": ["mix urea and dap", "urea and dap together", "mixing fertilizers", "can i mix", "fertilizer compatibility", "urea with potash", "pesticide with fertilizer"],
        "title": "🧪 Scientific Fertilizer & Chemical Tank-Mix Compatibility",
        "solver": (
            "### 🩺 Can You Mix Urea, DAP, Potash, and Pesticides?\n\n"
            "Mixing incompatible agricultural chemicals causes precipitation, nutrient lock-up, scorching of leaves, or complete loss of chemical efficacy!\n\n"
            "---\n\n"
            "### ✅ Compatible Mixes (Safe to Combine)\n\n"
            "1. **Urea + MOP (Muriate of Potash):** Safe to mix, but apply on the same day (hygroscopic; absorbs moisture quickly).\n"
            "2. **Urea + DAP:** Can be mixed **immediately prior to application**. Do not store mixed.\n"
            "3. **Water Soluble NPK (19:19:19) + Micronutrient Chelates (Zinc/Iron/Boron):** Excellent for foliar sprays.\n"
            "4. **Neem Oil + Chemical Insecticides:** Compatible and acts as a synergistic spreader/sticker.\n\n"
            "---\n\n"
            "### ❌ Dangerous / Incompatible Mixes (NEVER Combine!)\n\n"
            "1. **DAP + Zinc Sulphate:** **STRICTLY FORBIDDEN!** The Phosphorus in DAP binds with Zinc, forming insoluble Zinc Phosphate that turns like rock powder; both nutrients become 100% wasted!\n"
            "2. **Calcium Fertilizers + Sulphates / Phosphates:** Forms insoluble Calcium Sulphate (gypsum) or Calcium Phosphate sludge that chokes drip nozzles.\n"
            "3. **Copper Fungicides (Bordeaux/COC) + Organophosphate Pesticides / Urea:** Highly alkaline Copper decomposes pesticides and causes severe crop phytotoxicity.\n"
            "4. **Herbicides + Insecticides:** Never mix weedicides with other sprays unless specifically approved on product label.\n\n"
            "💡 *The Golden Jar Test:* Mix 1 teaspoon of each product in 1 Liter of water. If you see curdling, heating, gas bubbles, or milky sediment, **do not spray!**"
        ),
        "suggestions": [
            "Balanced fertilizer schedule for wheat",
            "Fertilizer dose for rice paddy",
            "Soil health card guidelines"
        ]
    },
    {
        "id": "high_profit_farming",
        "keywords": ["highest profit", "maximum profit", "profitable crop", "high income", "high yield crops", "best crop for 1 acre", "best crop for 2 acres", "kam kharche me jyada munafa", "cash crop"],
        "title": "💰 High-Profit Crop Planning & Maximizing Income per Acre",
        "solver": (
            "### 🌾 Top Commercial High-Value Cropping Models in India\n\n"
            "To generate maximum net profit from small landholdings (1 to 2 acres), shift from monoculture grain to high-value horticulture and spices:\n\n"
            "---\n\n"
            "### 🥇 Model 1: High-Density Spices & Condiments (₹1.5 to ₹3 Lakh net/acre)\n\n"
            "• **Ginger & Turmeric:** 8-9 month duration; yield 8-12 tonnes/acre; high market stability and export demand.\n"
            "• **Garlic (Ooty / Yamuna Safed):** Winter crop; net returns of ₹1.5–₹2.5 Lakh/acre with 4-6 month shelf life.\n\n"
            "---\n\n"
            "### 🥈 Model 2: Protected Cultivation / Polyhouse Vegetables (₹3 to ₹6 Lakh net/acre)\n\n"
            "• **Colored Capsicum (Red/Yellow Bell Peppers) & Parthenocarpic Cucumbers:** Controlled temperature allows 9-month continuous harvest with government subsidies up to 50% under National Horticulture Mission (NHM).\n\n"
            "---\n\n"
            "### 🥉 Model 3: Multilayer Intercropping (Zero Waste Land Model)\n\n"
            "• **Layer 1 (Underground):** Ginger or Turmeric or Colocasia (Arbi).\n"
            "• **Layer 2 (Ground):** Marigold (controls nematodes) or Coriander or Mint.\n"
            "• **Layer 3 (Medium Height):** Papaya (Red Lady 786) or Banana.\n"
            "• **Layer 4 (Tall / Boundary):** Drumstick (Moringa PKM-1) or Teakwood on field borders.\n\n"
            "💡 *Tip:* Test your plot's soil chemistry on our **[Predict Yield](/predict)** page to simulate expected harvest tonnage before investing!"
        ),
        "suggestions": [
            "Go to Predict Yield page",
            "Government subsidy for drip irrigation",
            "Organic vegetable farming tips"
        ]
    },
    {
        "id": "wild_animal_protection",
        "keywords": ["wild boar", "wild animal", "monkeys", "nilgai", "suar", "bandar", "crop damage by animals", "protect from animals", "fence", "animal repellent"],
        "title": "🐗 Protecting Crops from Wild Boars, Blue Bulls (Nilgai) & Monkeys",
        "solver": (
            "### 🛡️ Non-Lethal, Eco-Friendly Animal Deterrents\n\n"
            "1. **Solar Powered Zatka / Electric Fencing (Govt Subsidized):**\n"
            "   • Delivers non-lethal, high-voltage, low-amperage pulsating shock (safe for humans and animals) that deters boars and nilgai permanently. Subsidies available in many states (50%).\n"
            "2. **Herbal & Bio-Repellents for Wild Boars & Nilgai:**\n"
            "   • **Castor Oil + Cow Urine Emulsion:** Spray around border rows; strong smell repels nocturnal herbivores.\n"
            "   • **Fish Oil / Egg Wash Barrier:** Mix 20 rotten eggs in 100 L water and spray boundary fence; blue bulls avoid the pungent sulfur odor.\n"
            "3. **Monkey Deterrence:**\n"
            "   • **Acoustic Sound Cannons:** Gas-operated sound guns that fire periodic loud bangs.\n"
            "   • **Bonnet Bonnet Langur Cutouts / Recordings:** Visual and audio recordings of predators.\n"
            "4. **Bio-Fencing (Living Barrier):**\n"
            "   • Plant dense rows of Thorny Karonda (*Carissa carandas*), Cactus, or Agave around your perimeter bunds."
        ),
        "suggestions": [
            "Government subsidy for solar fencing",
            "Protecting crops from pests",
            "Kisan Call Center support"
        ]
    },
    {
        "id": "weed_control_herbicides",
        "keywords": ["weed", "weeds", "weedicide", "herbicide", "kharpatwar", "ghas", "gudaee", "weed control", "remove weeds", "pendimethalin", "atrazine", "2,4-d", "glyphosate", "bispyribac"],
        "title": "🌿 Comprehensive Weed Control & Safe Herbicide Guide",
        "solver": (
            "### 🩺 Principles of Scientific Weed Management\n\n"
            "Weeds compete aggressively with your crop for water, light, and fertilizer, reducing harvest yield by **25% to 50%** if not checked during the first 30 days.\n\n"
            "---\n\n"
            "### ⚡ 3-Pronged Weed Defense Strategy\n\n"
            "1. **Pre-Emergence Herbicides (Apply within 0–3 Days of Sowing / Transplanting):**\n"
            "   • **For Wheat, Mustard, Onion, Pulses:** Spray **Pendimethalin 30% EC (Stomp)** @ **1.0 to 1.5 Liters per acre** in 200 L water on moist soil. Forms a chemical seal that prevents weed seeds from germinating.\n"
            "   • **For Maize, Sugarcane:** Spray **Atrazine 50% WP** @ **800 g to 1 kg per acre**.\n\n"
            "2. **Post-Emergence Targeted Herbicides (Apply at 20–30 Days when weeds have 2–4 leaves):**\n"
            "   • **In Wheat (Broadleaf Weeds - Bathua, Wild Spinach):** Spray **2,4-D Ethyl Ester 38% EC** @ **500 ml/acre** OR **Metsulfuron Methyl 20% WP (Algrip)** @ **8 g/acre**.\n"
            "   • **In Wheat (Grassy Weeds - Gullidanda / Phalaris minor):** Spray **Clodinafop-propargyl 15% WP** @ **160 g/acre** with surfactant.\n"
            "   • **In Rice / Paddy:** Spray **Bispyribac Sodium 10% SC (Nominee Gold)** @ **80–100 ml/acre** in 120 L water (drain standing water before spray; re-irrigate after 48 hrs).\n\n"
            "3. **Organic & Mechanical Methods:**\n"
            "   • Wheel hoeing or cono-weeder at 20 and 40 days aerates roots while incorporating weeds into soil as green manure.\n"
            "   • Mulching with dry paddy straw (5–7 cm thick) blocks sunlight and prevents 90% weed germination in vegetables."
        ),
        "suggestions": [
            "Weed control in wheat",
            "Weed control in rice paddy",
            "Mulching techniques in farming"
        ]
    },
    {
        "id": "grain_storage_protection",
        "keywords": ["grain storage", "store grain", "store wheat", "weevils", "ghun", "keeda in grain", "anaaj suraksha", "protect grain", "celphos", "aluminium phosphide", "safely store grain"],
        "title": "🌾 Protecting Stored Grains from Weevils, Beetles & Rodents",
        "solver": (
            "### 🩺 The Golden Rules of Safe Grain Storage\n\n"
            "Post-harvest insects (*Ghun*, Khapra beetle, Rice weevil) destroy 10-15% of stored grains. Insects cannot multiply if grain moisture is below **10–12%**.\n\n"
            "---\n\n"
            "### ⚡ Step-by-Step Grain Preservation Protocol\n\n"
            "1. **Sun-Drying to Safe Moisture (< 12%):**\n"
            "   • Dry threshed grains under bright sun on clean tarpaulins for 2–3 days. Test hardness: a dry wheat grain should crack sharply between your teeth with a distinct snap.\n\n"
            "2. **Storage Structure Preparation:**\n"
            "   • Clean metal silos, bins (*Kothi*), or store rooms thoroughly. Discard old infested grains and cobwebs.\n"
            "   • Spray walls and floor with **Malathion 50% EC** (10 ml/L) 3 days before loading grain.\n\n"
            "3. **Organic / Traditional Grain Protectors:**\n"
            "   • Mix **Dry Neem Leaves** (2–3 kg per quintal) or **Wood Ash** (1 kg per quintal) thoroughly with grain.\n"
            "   • For pulses (*Dal*): Smear seeds with **Mustard oil or Castor oil** (5 ml per kg seed). Oil film suffocates beetle larvae completely.\n\n"
            "4. **Hermetic Storage Bags (PUSA Bin / GrainPro):**\n"
            "   • Air-tight multi-layer hermetic bags stop oxygen exchange, causing insects to die naturally within days without any chemicals!\n\n"
            "5. **Fumigation for Bulk Storage (Caution: Highly Toxic!):**\n"
            "   • For air-tight sealed silos only: Insert **Aluminium Phosphide (Celphos/Quickphos 3g tablets)** @ **1 tablet per tonne (10 quintals)** wrapped in cloth. Seal hermetically for 7 days. *Never use in living rooms!*"
        ),
        "suggestions": [
            "How to dry grains before storage?",
            "Preventing fungus in stored onions",
            "Hermetic bag suppliers"
        ]
    },
    {
        "id": "seed_treatment_fir",
        "keywords": ["seed treatment", "beej upchar", "how to treat seed", "fungicide on seed", "treat seeds", "beej sanskar"],
        "title": "🌱 The Scientific 'FIR' Seed Treatment Protocol",
        "solver": (
            "### 🩺 Why Seed Treatment is the Highest-ROI Farming Step\n\n"
            "Spending just ₹50–₹100 per acre on seed treatment saves up to ₹2,000 in chemical sprays later by immunizing seedlings against seed-borne and soil-borne diseases.\n\n"
            "---\n\n"
            "### ⚡ Follow the Universal 'F - I - R' Sequence\n\n"
            "Always treat in this exact order: **Fungicide First ➔ Insecticide Second ➔ Rhizobium/Biofertilizer Last**!\n\n"
            "1. **Step 1: F - Fungicide Treatment (Protects from Damping-off, Collar Rot, Smut):**\n"
            "   • Chemical: **Carbendazim 50% WP (Bavistin)** @ **2 g per kg seed** OR **Carboxin + Thiram (Vitavax)** @ **2.5 g/kg**.\n"
            "   • Organic alternative: **Trichoderma viride** @ **5–10 g per kg seed**.\n\n"
            "2. **Step 2: I - Insecticide Treatment (Protects from Termites, White Grubs, Sucking Pests for 30 Days):**\n"
            "   • **Thiamethoxam 30% FS** @ **3 ml per kg seed** OR **Chlorpyrifos 20% EC** @ **4 ml per kg seed** (especially for wheat and pulses against termites).\n\n"
            "3. **Step 3: R - Rhizobium / Biofertilizer Inoculation (Boosts Root Nodules & N-P-K Uptake):**\n"
            "   • For Pulses: Treat with **Rhizobium culture** (200 g / 10 kg seed).\n"
            "   • For Cereals (Wheat/Paddy): Treat with **Azotobacter** and **PSB (Phosphate Solubilizing Bacteria)**.\n"
            "   • Mix in a cooled jaggery syrup (*Gud ka ghol*) so the bacterial inoculant sticks to the seed coat.\n\n"
            "💡 *Tip:* Dry treated seeds in shade for 30–60 minutes before sowing in the soil. **Never expose treated seed to direct hot sunlight!**"
        ),
        "suggestions": [
            "Seed rate and spacing for wheat",
            "Nursery management in paddy",
            "Trichoderma viride usage guide"
        ]
    }
]


# ==============================================================================
# 🌐 OPTIONAL LIVE ONLINE LLM API BRIDGE (GEMINI / OPENAI)
# ==============================================================================

def try_online_llm_generation(prompt: str, user_name: str = "Farmer", history: list = None) -> dict:
    """
    Attempts to generate a real-time conversational response using an external LLM
    if an API key (GEMINI_API_KEY, GOOGLE_API_KEY, or OPENAI_API_KEY) is configured.
    Falls back cleanly to offline AgroGPT engine if no key or upon any network/quota issue.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    system_instruction = (
        f"You are Kisan AI, an expert, empathetic Agricultural ChatGPT assistant for Indian farmers. "
        f"The farmer's name is {user_name}. "
        f"Answer their doubt clearly, practically, and scientifically. "
        f"Always provide: "
        f"1. A direct diagnosis/answer in clear language. "
        f"2. Actionable immediate remedies with exact dosages (in ml/L, g/L, or kg/acre). "
        f"3. Organic/natural solutions (Neem, Trichoderma, Jeevamrut) alongside ICAR-approved chemical options. "
        f"4. Long-term preventative measures. "
        f"Format in beautiful, clean Markdown with bullet points and friendly emojis. Keep advice tailored to Indian agricultural conditions."
    )

    # 1. Try Gemini Live API
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            
            contents = []
            if history:
                for h in history[-4:]:
                    role = "user" if h.get("role") == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": h.get("content", "")}]})
            contents.append({"role": "user", "parts": [{"text": f"System context: {system_instruction}\n\nFarmer's Query: {prompt}"}]})

            payload = json.dumps({"contents": contents}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=8) as response:
                result = json.loads(response.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "reply": text,
                    "suggestions": [
                        "How to apply this in my field?",
                        "What is the organic alternative?",
                        "Predict crop yield for my land"
                    ]
                }
        except Exception:
            pass

    # 2. Try OpenAI Live API
    if openai_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            messages = [{"role": "system", "content": system_instruction}]
            if history:
                for h in history[-4:]:
                    messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
            messages.append({"role": "user", "content": prompt})

            payload = json.dumps({
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.5
            }).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                }
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                result = json.loads(response.read().decode("utf-8"))
                text = result["choices"][0]["message"]["content"]
                return {
                    "reply": text,
                    "suggestions": [
                        "What is the organic alternative?",
                        "How to apply this in my field?",
                        "Calculate crop harvest on Predict page"
                    ]
                }
        except Exception:
            pass

    return None


# ==============================================================================
# 🎯 CROP DETECTION UTILITY
# ==============================================================================

def detect_crop_in_query(query: str) -> str:
    """Detects standard crop name from user query using direct names and regional aliases."""
    q = query.lower()

    # 1. Check regional aliases first
    for alias, standard in CROP_ALIASES.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", q):
            return standard

    # 2. Check standard 32 crops
    from ml.agronomy_engine import AGRONOMIC_KNOWLEDGE
    for crop_name in AGRONOMIC_KNOWLEDGE.keys():
        if re.search(r"\b" + re.escape(crop_name.lower()) + r"\b", q):
            return crop_name

    return None


# ==============================================================================
# 🚀 MAIN CHATGPT ENTRYPOINT: answer_farming_doubt
# ==============================================================================

def answer_farming_doubt(query: str, user_name: str = "Farmer", history: list = None) -> dict:
    """
    Answers farmer queries like ChatGPT:
    1. Checks for online LLM API keys first (Gemini / OpenAI).
    2. Matches conversational & operational prompts (Greetings, How to use, Model accuracy).
    3. Solves practical farming troubles through SPECIFIC_FARMING_DOUBTS engine.
    4. Provides crop-specific subtopic details (Sowing, Fertilizer, Pest, Irrigation).
    5. Returns scientific crop profile if a crop is identified.
    6. Returns domain knowledge for broad topics.
    7. Synthesizes a structured ChatGPT-style diagnostic answer for open-ended queries.
    """
    cleaned_query = query.lower().strip()
    words = set(re.findall(r"\b\w+\b", cleaned_query))

    # 1. Attempt Live Online LLM generation if API Key is configured
    online_response = try_online_llm_generation(query, user_name=user_name, history=history)
    if online_response:
        return online_response

    # 2. Check Conversational & Website Intents
    for conv in CONVERSATIONAL_INTENTS:
        for kw in conv["keywords"]:
            if re.search(r"\b" + re.escape(kw) + r"\b", cleaned_query):
                return {
                    "reply": f"### {conv['title']}\n\n{conv['reply']}",
                    "suggestions": conv["suggestions"]
                }

    # 3. Detect Crop from query or conversation history
    detected_crop = detect_crop_in_query(cleaned_query)
    if not detected_crop and history:
        for msg in reversed(history):
            prev_text = msg.get("content", "") or msg.get("message", "")
            prev_crop = detect_crop_in_query(prev_text)
            if prev_crop:
                detected_crop = prev_crop
                break

    # 4. Check Advanced Doubt Solver Engine (Pests, Symptoms, Water, Frost, Insurance, Jeevamrut, Mixing)
    for doubt in SPECIFIC_FARMING_DOUBTS:
        for kw in doubt["keywords"]:
            if kw in cleaned_query or re.search(r"\b" + re.escape(kw) + r"\b", cleaned_query):
                crop_prefix = f"### 🌾 Advice for **{detected_crop}**\n\n" if detected_crop else ""
                return {
                    "reply": f"{crop_prefix}{doubt['solver']}",
                    "suggestions": doubt["suggestions"]
                }

    # 5. Detect Query Sub-Intent for Crop
    detected_subtopic = None
    if any(w in words for w in ["fertilizer", "fertilizers", "fert", "urea", "dap", "npk", "potash", "manure", "khad", "nutrient", "nutrients", "zinc", "sulphur", "nitrogen", "phosphorus"]):
        detected_subtopic = "fertilizer"
    elif any(w in words for w in ["sow", "sowing", "seed", "seeds", "variety", "varieties", "plant", "planting", "month", "time", "date", "when", "season"]):
        detected_subtopic = "sowing"
    elif any(w in words for w in ["pest", "pests", "disease", "diseases", "insect", "insects", "keeda", "bimari", "fungus", "spray", "blight", "rust", "yellow", "yellowing", "curl", "borer", "aphid", "aphids", "worm", "bollworm", "bollworms", "whitefly", "thrips", "rot", "scab", "control", "caterpillar"]):
        detected_subtopic = "pest_disease"
    elif any(w in words for w in ["water", "irrigation", "drip", "watering", "dry", "drought", "moisture", "pani", "sinchai"]):
        detected_subtopic = "irrigation"
    elif any(w in words for w in ["harvest", "harvesting", "cut", "storage", "yield", "katayi", "produce", "tonnes", "quintal", "curing"]):
        detected_subtopic = "harvest"

    # 6. If Crop + Sub-Intent matches detailed database
    if detected_crop and detected_crop in CROP_SPECIFIC_KNOWLEDGE:
        crop_details = CROP_SPECIFIC_KNOWLEDGE[detected_crop]
        if detected_subtopic and detected_subtopic in crop_details:
            return {
                "reply": f"Hello {user_name}! Here is the specific guidance for **{detected_crop}**:\n\n{crop_details[detected_subtopic]}",
                "suggestions": [
                    f"Predict yield for {detected_crop}",
                    f"Other farming tips for {detected_crop}",
                    "Ask Kisan AI another question"
                ]
            }

    # 7. If Crop is detected without subtopic
    if detected_crop:
        from ml.agronomy_engine import AGRONOMIC_KNOWLEDGE
        info = AGRONOMIC_KNOWLEDGE.get(detected_crop, {})
        t_min, t_max = info.get("temp_opt", (15, 30))
        r_min, r_max = info.get("rain_opt", (400, 1000))
        fert_min, fert_max = info.get("typical_fert", (80, 140))
        seasons = ", ".join(info.get("ideal_seasons", []))
        soils = ", ".join(info.get("ideal_soils", []))
        tips = "\n".join([f"• {tip}" for tip in info.get("tips", [])])

        crop_reply = (
            f"Hello {user_name}! 🌾 Here is the complete agronomic management plan for **{info.get('icon', '🌱')} {detected_crop}**:\n\n"
            f"**Agronomic Standards:**\n"
            f"• **Category:** {info.get('category', 'Crop')}\n"
            f"• **Ideal Seasons:** {seasons}\n"
            f"• **Suitable Soils:** {soils}\n"
            f"• **Temperature Window:** {t_min}°C – {t_max}°C\n"
            f"• **Seasonal Rainfall:** {r_min} mm – {r_max} mm\n"
            f"• **Typical Fertilizer Rate:** {fert_min} – {fert_max} kg/ha\n"
            f"• **Regional Benchmark Harvest:** ~{info.get('avg_yield', 2.5)} tonnes/ha\n\n"
            f"**Expert Farming Recommendations:**\n"
            f"{tips}\n\n"
            f"💡 *Would you like specific advice on fertilizer dosage, pest remedies, or sowing dates for {detected_crop}? Just ask!*"
        )
        return {
            "reply": crop_reply,
            "suggestions": [
                f"Predict {detected_crop} yield for my acreage",
                f"Fertilizer dose for {detected_crop}",
                f"How to protect {detected_crop} from pests"
            ]
        }

    # 8. Check Broad Agronomic Topics
    for topic in BROAD_TOPICS:
        for kw in topic["keywords"]:
            if re.search(r"\b" + re.escape(kw) + r"\b", cleaned_query):
                return {
                    "reply": f"Hello {user_name}! Here is the information on **{topic['title']}**:\n\n{topic['reply']}",
                    "suggestions": topic["suggestions"]
                }

    # 9. Dynamic Cognitive Solver for Open-Ended Queries
    # Solves any unclassified farming doubt in structured ChatGPT format
    query_display = query[:70] + ("..." if len(query) > 70 else "")
    dynamic_solution = (
        f"### 🌾 Expert Agronomic Guidance on: \"{query_display}\"\n\n"
        f"Hello {user_name}! Here is the practical solution for your query:\n\n"
        "#### 1. 🔍 Diagnosis & Immediate Assessment\n"
        "• To protect your crop and maintain yield, first inspect 10 random plants across your field to evaluate whether the issue is biological (insects/fungus) or environmental (water/soil/weather).\n"
        "• Ensure your crop is not suffering from moisture stress or poor aeration at the root zone.\n\n"
        "#### 2. ⚡ Immediate First-Aid & Organic Protection\n"
        "• **Bio-Pesticide Spray:** Spray **Neem Oil (1500 ppm)** @ **5 ml per Liter of water** (mixed with 1 ml liquid soap) as an immediate safe deterrent against pests and surface fungal spores.\n"
        "• **Soil Vitality:** Apply **Jeevamrut** (200 L/acre) or top-dress well-rotted vermicompost to re-energize beneficial microbial activity.\n\n"
        "#### 3. 🧪 Chemical Intervention Protocol (If Symptoms Persist)\n"
        "• For fungal spots or blights, spray **Mancozeb 75% WP** @ **2.5 g/L** or **Copper Oxychloride** @ **3 g/L**.\n"
        "• For sucking pests (aphids, thrips, whiteflies), spray **Thiamethoxam 25% WG** @ **0.3 g/L**.\n"
        "• Always spray during calm weather (early morning or late afternoon).\n\n"
        "#### 4. 📈 Yield Optimization\n"
        "• You can forecast the expected harvest for your land on our **[Predict Yield](/predict)** page using local district weather auto-sync!\n"
        "• For emergency on-field inspection in your taluka, contact your local **Krishi Vigyan Kendra (KVK)** or dial the **Kisan Call Center at 1800-180-1551** (Toll-Free, 6 AM to 10 PM)."
    )

    return {
        "reply": dynamic_solution,
        "suggestions": [
            "How to use this website?",
            "What fertilizer to use for wheat?",
            "How to control bollworm in cotton?",
            "Government schemes for farmers"
        ]
    }
