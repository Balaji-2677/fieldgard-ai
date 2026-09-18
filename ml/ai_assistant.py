"""
AI Agricultural Assistant Intelligence Engine ("Kisan AI")
Provides contextual, highly varied, and scientifically accurate advice for:
- Conversational greetings & Website usage instructions
- Crop-specific fertilizer, sowing, irrigation, pest & disease, and harvest guidance
- General agronomic domain expertise (soil health, organic farming, schemes, weather)
"""

import re

# Indian Crop Aliases & Regional Names mapping to standard crop names
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
            "Namaste! 🙏 I am your **Kisan AI Agricultural Assistant**.\n\n"
            "I can help you with:\n"
            "• **Crop Sowing & High-Yield Seeds** (Wheat, Rice, Cotton, Onion, Apple, etc.)\n"
            "• **Balanced Fertilizer Dosages** (Urea, DAP, Potash, Micronutrients)\n"
            "• **Pest & Disease Diagnosis** (Blight, Rust, Bollworms, Yellowing leaves)\n"
            "• **Water & Irrigation Scheduling** (Critical stages, Drip irrigation)\n"
            "• **Government Farmer Schemes** (PM-KISAN ₹6,000, PMFBY crop insurance, KCC loans)\n"
            "• **How to use this prediction website**\n\n"
            "What crop or farming topic would you like advice on today?"
        ),
        "suggestions": [
            "How to use this website?",
            "What fertilizer to use for wheat?",
            "Why are rice leaves turning yellow?",
            "Government schemes for farmers"
        ]
    },
    {
        "intent": "website_guide",
        "keywords": ["how to use", "how to predict", "use website", "how it works", "instructions", "guide", "tutorial", "steps", "how do i use", "how does this work", "predict yield"],
        "title": "📖 How to Use CropYield AI in 4 Easy Steps",
        "reply": (
            "Here is how to get the most out of **CropYield AI**:\n\n"
            "1. **Go to 'Predict Yield' Page:** Click **[Predict Yield](/predict)** in the top menu.\n"
            "2. **Enter Farm Parameters:** Select your Crop (from 32 crops), State (from 36 States/UTs), Season, Soil Type, and Acreage.\n"
            "3. **Enter Climate & Soil Data:** Input expected rainfall, average temperature, and fertilizer usage (or click one of our **✨ Quick Autofill Presets**).\n"
            "4. **Click 'Predict Crop Yield':** In under 1 second, our ML Model ($R^2 = 98.82%$) gives your predicted harvest in **Tonnes/Ha** & **Quintals/Acre**, tailored agronomy warnings, and a printable **Farmer Yield Card**!\n\n"
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
            "I am **Kisan AI**, an intelligent agronomic assistant developed specifically for Indian farmers and agricultural researchers.\n\n"
            "• **Science-Backed:** Calibrated with official ICAR, State Agricultural Universities, and Ministry of Agriculture benchmarks.\n"
            "• **Comprehensive Coverage:** Supports all 32 major Indian crops across all 28 States and 8 Union Territories.\n"
            "• **Multi-Topic Guidance:** From soil preparation to harvesting, disease remedies, and central welfare schemes.\n\n"
            "Feel free to ask me any farming question in plain language!"
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
        "title": "🌾 You Are Welcome!",
        "reply": (
            "You are very welcome! 🙏\n\n"
            "CropYield AI is dedicated to supporting the hard work of our farmers. May your fields prosper with abundant, healthy harvest! 🌾✨\n\n"
            "Feel free to ask whenever you have another farming doubt."
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
    },
    {
        "intent": "joke",
        "keywords": ["joke", "jokes", "funny", "laugh", "make me laugh", "humour", "humor"],
        "title": "😄 Farming Humour & Kisan Wisdom",
        "reply": (
            "Why did the scarecrow win a national agricultural award?\n\n"
            "Because he was **outstanding in his field**! 🌾😄\n\n"
            "Here is another one for you:\n"
            "*Why do farmers make wonderful musicians? Because they always grow a magnificent crop of beets!* 🎶🚜\n\n"
            "Farming is hard work, but a happy heart brings an abundant harvest! What crop can I help you with today?"
        ),
        "suggestions": [
            "How to increase crop yield?",
            "What fertilizer to use for wheat?",
            "Government schemes for farmers"
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
            "• **Yellowing Leaves (Khaira / Zinc Deficiency):** Lower leaves turn yellow and bronze. Spray *0.5% Zinc Sulphate (ZnSO₄) + 1% Urea* (5 kg ZnSO₄ + 10 kg Urea in 1000 L water/ha).\n"
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

# Domain-Specific Broad Agricultural Knowledge
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


def answer_farming_doubt(query: str, user_name: str = "Farmer", history: list = None) -> dict:
    """
    Parses farmer query and returns customized agronomic advice,
    actionable tips, and follow-up suggestion chips.
    Guarantees unique, highly specific answers for every question.
    Maintains multi-turn context memory across conversation history.
    """
    cleaned_query = query.lower().strip()
    words = set(re.findall(r"\b\w+\b", cleaned_query))

    # 1. Check Conversational & Website Intents (Greetings, How to use, Identity, Accuracy)
    for conv in CONVERSATIONAL_INTENTS:
        for kw in conv["keywords"]:
            if re.search(r"\b" + re.escape(kw) + r"\b", cleaned_query):
                return {
                    "reply": f"### {conv['title']}\n\n{conv['reply']}",
                    "suggestions": conv["suggestions"]
                }

    # 2. Detect Crop (Direct name or Hindi/regional alias)
    detected_crop = detect_crop_in_query(cleaned_query)

    # If no crop in current query, check recent multi-turn conversation history
    if not detected_crop and history:
        for msg in reversed(history):
            prev_text = msg.get("content", "") or msg.get("message", "")
            prev_crop = detect_crop_in_query(prev_text)
            if prev_crop:
                detected_crop = prev_crop
                break

    # 3. Detect Query Sub-Intent
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

    # 4. If Crop + Sub-Intent matches detailed database
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

    # 5. If Crop is detected (General crop query)
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
            f"Hello {user_name}! Here is the scientific agronomic profile for **{info.get('icon', '🌱')} {detected_crop}**:\n\n"
            f"**Agronomic Standards:**\n"
            f"• **Category:** {info.get('category', 'Crop')}\n"
            f"• **Ideal Seasons:** {seasons}\n"
            f"• **Suitable Soils:** {soils}\n"
            f"• **Temperature Window:** {t_min}°C – {t_max}°C\n"
            f"• **Rainfall Requirement:** {r_min} mm – {r_max} mm\n"
            f"• **Typical Fertilizer Rate:** {fert_min} – {fert_max} kg/ha\n"
            f"• **Regional Benchmark Yield:** ~{info.get('avg_yield', 2.5)} tonnes/ha\n\n"
            f"**Expert Farming Recommendations:**\n"
            f"{tips}"
        )
        return {
            "reply": crop_reply,
            "suggestions": [
                f"Predict {detected_crop} yield for my acreage",
                f"Fertilizer dose for {detected_crop}",
                f"How to protect {detected_crop} from pests"
            ]
        }

    # 6. Check Broad Agronomic Topics (Fertilizers, Irrigation, Pests, Organic, Schemes, Yield)
    for topic in BROAD_TOPICS:
        for kw in topic["keywords"]:
            if re.search(r"\b" + re.escape(kw) + r"\b", cleaned_query):
                return {
                    "reply": f"Hello {user_name}! Here is the information on **{topic['title']}**:\n\n{topic['reply']}",
                    "suggestions": topic["suggestions"]
                }

    # 7. Contextual Fallback with Query-Aware Response
    query_display = query[:60] + ("..." if len(query) > 60 else "")
    fallback = (
        f"Hello {user_name}! 🌾\n\n"
        f"Regarding your question on: **\"{query_display}\"**\n\n"
        "Here are recommended agronomic steps:\n"
        "1. **Specific Crop Inquiries:** Try asking with a crop name (e.g., *'What fertilizer for wheat?'*, *'How to grow onions?'*, or *'How to control cotton bollworm?'*).\n"
        "2. **Crop Yield Predictions:** Visit the **[Predict Yield](/predict)** page to calculate expected harvest for your farm's acreage and climate.\n"
        "3. **District Level Weather/Pest Emergency:** Call the Ministry of Agriculture's toll-free **Kisan Call Center at 1800-180-1551** (6:00 AM to 10:00 PM in all Indian languages)."
    )

    return {
        "reply": fallback,
        "suggestions": [
            "How to use this website?",
            "What fertilizer to use for wheat?",
            "How to control bollworm in cotton?",
            "Government schemes for farmers"
        ]
    }
