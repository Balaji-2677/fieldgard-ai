"""
Agricultural Market Intelligence & Financial Profit Engine
Provides official Government MSP (Minimum Support Price) benchmarks,
mandi trading prices, cultivation cost models, and net farmer profit calculations.
"""

# Official 2024-2026 Government MSP & Benchmark Mandi Wholesale Rates (INR per Quintal)
# 1 Tonne = 10 Quintals
CROP_MARKET_RATES = {
    "Wheat": {"msp_per_quintal": 2275, "avg_mandi_rate": 2450, "cost_per_ha": 32000},
    "Rice": {"msp_per_quintal": 2300, "avg_mandi_rate": 2550, "cost_per_ha": 35000},
    "Maize": {"msp_per_quintal": 2090, "avg_mandi_rate": 2200, "cost_per_ha": 28000},
    "Cotton": {"msp_per_quintal": 7121, "avg_mandi_rate": 7450, "cost_per_ha": 45000},
    "Sugarcane": {"msp_per_quintal": 340, "avg_mandi_rate": 375, "cost_per_ha": 65000},
    "Chickpea": {"msp_per_quintal": 5440, "avg_mandi_rate": 5850, "cost_per_ha": 25000},
    "Mustard": {"msp_per_quintal": 5650, "avg_mandi_rate": 5900, "cost_per_ha": 22000},
    "Millets": {"msp_per_quintal": 2500, "avg_mandi_rate": 2700, "cost_per_ha": 18000},
    "Pigeon Pea": {"msp_per_quintal": 7000, "avg_mandi_rate": 8200, "cost_per_ha": 26000},
    "Lentil": {"msp_per_quintal": 6425, "avg_mandi_rate": 6800, "cost_per_ha": 23000},
    "Moong": {"msp_per_quintal": 8558, "avg_mandi_rate": 8900, "cost_per_ha": 22000},
    "Urad": {"msp_per_quintal": 6950, "avg_mandi_rate": 7500, "cost_per_ha": 22000},
    "Groundnut": {"msp_per_quintal": 6377, "avg_mandi_rate": 6700, "cost_per_ha": 32000},
    "Potato": {"msp_per_quintal": 1200, "avg_mandi_rate": 1550, "cost_per_ha": 75000},
    "Tomato": {"msp_per_quintal": 1400, "avg_mandi_rate": 2100, "cost_per_ha": 85000},
    "Onion": {"msp_per_quintal": 1500, "avg_mandi_rate": 2300, "cost_per_ha": 60000},
    "Garlic": {"msp_per_quintal": 6000, "avg_mandi_rate": 9500, "cost_per_ha": 90000},
    "Turmeric": {"msp_per_quintal": 7500, "avg_mandi_rate": 11500, "cost_per_ha": 70000},
    "Ginger": {"msp_per_quintal": 6500, "avg_mandi_rate": 9000, "cost_per_ha": 85000},
    "Chilli": {"msp_per_quintal": 12000, "avg_mandi_rate": 16500, "cost_per_ha": 65000},
    "Barley": {"msp_per_quintal": 1850, "avg_mandi_rate": 2100, "cost_per_ha": 22000},
    "Jute": {"msp_per_quintal": 5050, "avg_mandi_rate": 5350, "cost_per_ha": 30000},
    "Tea": {"msp_per_quintal": 18000, "avg_mandi_rate": 24000, "cost_per_ha": 120000},
    "Coconut": {"msp_per_quintal": 3000, "avg_mandi_rate": 3800, "cost_per_ha": 40000},
    "Apple": {"msp_per_quintal": 6500, "avg_mandi_rate": 8500, "cost_per_ha": 95000},
    "Mango": {"msp_per_quintal": 3500, "avg_mandi_rate": 4800, "cost_per_ha": 45000},
    "Banana": {"msp_per_quintal": 1600, "avg_mandi_rate": 2200, "cost_per_ha": 80000},
    "Sunflower": {"msp_per_quintal": 6760, "avg_mandi_rate": 7100, "cost_per_ha": 25000},
    "Cardamom": {"msp_per_quintal": 95000, "avg_mandi_rate": 140000, "cost_per_ha": 150000},
    "Soybean": {"msp_per_quintal": 4892, "avg_mandi_rate": 5150, "cost_per_ha": 25000},
    "Tobacco": {"msp_per_quintal": 6500, "avg_mandi_rate": 7800, "cost_per_ha": 45000},
    "Coffee": {"msp_per_quintal": 18000, "avg_mandi_rate": 22000, "cost_per_ha": 85000}
}

DEFAULT_RATE = {"msp_per_quintal": 2500, "avg_mandi_rate": 2800, "cost_per_ha": 30000}


def get_crop_market_rate(crop_name: str) -> dict:
    """Returns MSP, Mandi price, and cultivation cost per hectare for a specific crop."""
    return CROP_MARKET_RATES.get(crop_name, DEFAULT_RATE)


def calculate_crop_financials(crop_name: str, predicted_yield_t_ha: float, area_ha: float) -> dict:
    """
    Computes complete financial projections for the farmer:
    - Gross Revenue at Govt MSP (₹)
    - Gross Revenue at Mandi Market Price (₹)
    - Total Estimated Cultivation Cost (₹)
    - Net Profit in Rupees (₹)
    - Profit per Acre (₹/acre)
    - Return on Investment (ROI %)
    """
    rate_info = CROP_MARKET_RATES.get(crop_name, DEFAULT_RATE)
    
    # 1 Tonne = 10 Quintals
    total_tonnes = float(predicted_yield_t_ha) * float(area_ha)
    total_quintals = total_tonnes * 10.0
    area_acres = float(area_ha) * 2.47105

    msp_rate = rate_info["msp_per_quintal"]
    mandi_rate = rate_info["avg_mandi_rate"]
    cost_per_ha = rate_info["cost_per_ha"]

    gross_revenue_msp = round(total_quintals * msp_rate)
    gross_revenue_mandi = round(total_quintals * mandi_rate)
    
    total_cost = round(cost_per_ha * float(area_ha))
    
    # Net profit based on prevailing mandi rate
    net_profit = round(gross_revenue_mandi - total_cost)
    net_profit_msp = round(gross_revenue_msp - total_cost)
    profit_per_acre = round(net_profit / area_acres) if area_acres > 0 else 0
    profit_per_ha = round(net_profit / float(area_ha)) if float(area_ha) > 0 else 0

    # Return on Investment
    roi_percent = round((net_profit / total_cost) * 100, 1) if total_cost > 0 else 0.0

    profit_rating = "Highly Profitable 🌟" if roi_percent >= 80 else "Profitable ✅" if roi_percent >= 25 else "Marginal / Low ⚠️"

    return {
        "crop": crop_name,
        "area_ha": round(float(area_ha), 2),
        "area_acres": round(area_acres, 2),
        "total_tonnes": round(total_tonnes, 2),
        "total_quintals": round(total_quintals, 1),
        "msp_rate_quintal": msp_rate,
        "mandi_rate_quintal": mandi_rate,
        "gross_revenue_msp": gross_revenue_msp,
        "gross_revenue_mandi": gross_revenue_mandi,
        "total_cost": total_cost,
        "net_profit": net_profit,
        "net_profit_msp": net_profit_msp,
        "profit_per_acre": profit_per_acre,
        "profit_per_ha": profit_per_ha,
        "roi_percent": roi_percent,
        "profit_rating": profit_rating,
        "formatted_net_profit": f"₹{net_profit:,.0f}",
        "formatted_gross_revenue": f"₹{gross_revenue_mandi:,.0f}",
        "formatted_total_cost": f"₹{total_cost:,.0f}",
        "formatted_profit_per_acre": f"₹{profit_per_acre:,.0f}/acre"
    }
