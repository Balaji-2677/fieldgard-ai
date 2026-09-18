/**
 * Dashboard & Analytics Logic
 * Integrates Chart.js for data visualization and provides real-time table filtering.
 */

let cropChartInstance = null;
let scatterChartInstance = null;
let soilChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  initCharts();
  initAgriMap();
  initTableFilters();
});

async function initCharts() {
  try {
    const res = await fetch("/api/stats");
    const json = await res.json();
    if (!json.success || !json.stats) return;

    const stats = json.stats;

    // 1. Crop Yield Bar Chart
    const cropLabels = stats.crop_stats.map((c) => c.crop);
    const cropYields = stats.crop_stats.map((c) => c.avg_yield);
    const cropCounts = stats.crop_stats.map((c) => c.count);

    const ctxCrop = document.getElementById("cropYieldChart")?.getContext("2d");
    if (ctxCrop) {
      cropChartInstance = new Chart(ctxCrop, {
        type: "bar",
        data: {
          labels: cropLabels,
          datasets: [
            {
              label: "Avg Yield (Tonnes / Ha)",
              data: cropYields,
              backgroundColor: "rgba(30, 126, 52, 0.75)",
              borderColor: "rgba(30, 126, 52, 1)",
              borderWidth: 1.5,
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: true, position: "top" },
            tooltip: {
              callbacks: {
                footer: (tooltipItems) => {
                  const idx = tooltipItems[0].dataIndex;
                  return `Predictions: ${cropCounts[idx]}`;
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: "Tonnes per Hectare" },
            },
          },
        },
      });
    }

    // 2. Soil Doughnut Chart
    const soilLabels = stats.soil_stats.map((s) => s.soil);
    const soilCounts = stats.soil_stats.map((s) => s.count);

    const ctxSoil = document.getElementById("soilDoughnutChart")?.getContext("2d");
    if (ctxSoil) {
      soilChartInstance = new Chart(ctxSoil, {
        type: "doughnut",
        data: {
          labels: soilLabels,
          datasets: [
            {
              data: soilCounts,
              backgroundColor: [
                "#1e7e34",
                "#2b6cb0",
                "#d97706",
                "#805ad5",
                "#d69e2e",
                "#718096",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "right" },
          },
        },
      });
    }

    // 3. Rainfall vs Yield Scatter Chart
    const scatterPoints = stats.scatter_data.map((d) => ({
      x: d.x,
      y: d.y,
      crop: d.crop,
    }));

    const ctxScatter = document.getElementById("rainfallScatterChart")?.getContext("2d");
    if (ctxScatter) {
      scatterChartInstance = new Chart(ctxScatter, {
        type: "scatter",
        data: {
          datasets: [
            {
              label: "Rainfall vs Yield",
              data: scatterPoints,
              backgroundColor: "rgba(43, 108, 176, 0.7)",
              borderColor: "rgba(43, 108, 176, 1)",
              pointRadius: 6,
              pointHoverRadius: 8,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              callbacks: {
                label: (ctx) => {
                  const raw = ctx.raw;
                  return `${raw.crop}: ${raw.x}mm rain → ${raw.y} t/ha yield`;
                },
              },
            },
          },
          scales: {
            x: {
              title: { display: true, text: "Rainfall (mm)" },
            },
            y: {
              title: { display: true, text: "Predicted Yield (Tonnes/Ha)" },
            },
          },
        },
      });
    }
  } catch (err) {
    console.error("Failed to load charts data:", err);
  }
}

function initTableFilters() {
  const searchInput = document.getElementById("history-search");
  const cropFilter = document.getElementById("history-crop-filter");
  const rows = document.querySelectorAll(".history-row");

  function filterRows() {
    const q = (searchInput ? searchInput.value : "").toLowerCase().trim();
    const selectedCrop = (cropFilter ? cropFilter.value : "").toLowerCase().trim();

    rows.forEach((row) => {
      const text = row.textContent.toLowerCase();
      const rowCrop = (row.getAttribute("data-crop") || "").toLowerCase();

      const matchesSearch = !q || text.includes(q);
      const matchesCrop = !selectedCrop || selectedCrop === "all" || rowCrop === selectedCrop;

      if (matchesSearch && matchesCrop) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  }

  if (searchInput) searchInput.addEventListener("input", filterRows);
  if (cropFilter) cropFilter.addEventListener("change", filterRows);
}

async function deleteRecord(id) {
  if (!confirm(`Are you sure you want to delete prediction record #${id}?`)) return;

  try {
    const res = await fetch(`/api/delete/${id}`, { method: "POST" });
    const data = await res.json();
    if (data.success) {
      showToast(`Record #${id} deleted successfully.`, "info");
      const row = document.getElementById(`row-${id}`);
      if (row) row.remove();
    } else {
      showToast(data.error || "Failed to delete record", "error");
    }
  } catch (err) {
    showToast("Network error deleting record", "error");
  }
}

/**
 * Initialize Interactive Agricultural Map of India
 */
function initAgriMap() {
  const mapContainer = document.getElementById("agriMap");
  if (!mapContainer || typeof L === "undefined") return;

  // Center on India
  const map = L.map("agriMap").setView([22.5, 79.5], 5);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  const statesData = [
    // 28 States of India
    { name: "Andhra Pradesh", coords: [15.9129, 79.7400], crops: "Rice, Chilli, Tomato, Cotton, Mango", yieldAvg: "3.5 t/ha", rain: "950 mm", soil: "Alluvial / Red" },
    { name: "Arunachal Pradesh", coords: [28.2180, 94.7278], crops: "Rice, Maize, Ginger, Apple, Cardamom", yieldAvg: "2.3 t/ha", rain: "2500 mm", soil: "Red / Loamy" },
    { name: "Assam", coords: [26.2006, 92.9376], crops: "Tea, Rice, Jute, Mustard, Ginger", yieldAvg: "2.8 t/ha", rain: "2200 mm", soil: "Alluvial / Red" },
    { name: "Bihar", coords: [25.0961, 85.3131], crops: "Rice, Wheat, Maize, Potato, Jute", yieldAvg: "3.2 t/ha", rain: "1100 mm", soil: "Alluvial" },
    { name: "Chhattisgarh", coords: [21.2787, 81.8661], crops: "Rice, Maize, Soybean, Pulses", yieldAvg: "2.4 t/ha", rain: "1300 mm", soil: "Red / Clayey" },
    { name: "Goa", coords: [15.2993, 74.1240], crops: "Coconut, Rice, Rubber, Mango, Spices", yieldAvg: "3.1 t/ha", rain: "2800 mm", soil: "Laterite" },
    { name: "Gujarat", coords: [22.2587, 71.1924], crops: "Groundnut, Cotton, Wheat, Onion, Garlic", yieldAvg: "2.0 t/ha", rain: "650 mm", soil: "Sandy Loam / Black" },
    { name: "Haryana", coords: [29.0588, 76.0856], crops: "Wheat, Mustard, Rice, Sugarcane", yieldAvg: "3.7 t/ha", rain: "500 mm", soil: "Alluvial / Loam" },
    { name: "Himachal Pradesh", coords: [31.1048, 77.1734], crops: "Apple, Barley, Wheat, Maize, Tea", yieldAvg: "2.5 t/ha", rain: "1200 mm", soil: "Sandy Loam / Forest" },
    { name: "Jharkhand", coords: [23.6102, 85.2799], crops: "Rice, Maize, Pulses, Pigeon Pea", yieldAvg: "2.1 t/ha", rain: "1200 mm", soil: "Red / Sandy" },
    { name: "Karnataka", coords: [15.3173, 75.7139], crops: "Coffee, Maize, Cotton, Sugarcane, Sunflower", yieldAvg: "3.4 t/ha", rain: "750 mm", soil: "Red / Loam" },
    { name: "Kerala", coords: [10.8505, 76.2711], crops: "Coconut, Rubber, Tea, Coffee, Cardamom", yieldAvg: "2.9 t/ha", rain: "2700 mm", soil: "Laterite" },
    { name: "Madhya Pradesh", coords: [22.9734, 78.6569], crops: "Soybean, Wheat, Chickpea, Garlic, Mustard", yieldAvg: "2.1 t/ha", rain: "900 mm", soil: "Black / Mixed" },
    { name: "Maharashtra", coords: [19.7515, 75.7139], crops: "Cotton, Sugarcane, Soybean, Onion, Pulses", yieldAvg: "1.8 t/ha", rain: "850 mm", soil: "Black (Regur)" },
    { name: "Manipur", coords: [24.6637, 93.9063], crops: "Rice, Maize, Pulses, Ginger, Coffee", yieldAvg: "2.4 t/ha", rain: "1400 mm", soil: "Red / Clayey" },
    { name: "Meghalaya", coords: [25.4670, 91.3662], crops: "Ginger, Turmeric, Tea, Potato, Jute", yieldAvg: "2.6 t/ha", rain: "2600 mm", soil: "Laterite / Red" },
    { name: "Mizoram", coords: [23.1645, 92.9376], crops: "Ginger, Turmeric, Coffee, Rice", yieldAvg: "2.2 t/ha", rain: "2400 mm", soil: "Red / Loamy" },
    { name: "Nagaland", coords: [26.1584, 94.5624], crops: "Cardamom, Coffee, Ginger, Tea, Rice", yieldAvg: "2.3 t/ha", rain: "2000 mm", soil: "Red / Forest" },
    { name: "Odisha", coords: [20.9517, 85.0985], crops: "Rice, Turmeric, Groundnut, Jute, Coconut", yieldAvg: "2.6 t/ha", rain: "1450 mm", soil: "Alluvial / Red" },
    { name: "Punjab", coords: [31.1471, 75.3412], crops: "Wheat, Rice, Cotton, Sugarcane, Potato", yieldAvg: "3.8 t/ha", rain: "550 mm", soil: "Alluvial" },
    { name: "Rajasthan", coords: [27.0238, 74.2179], crops: "Mustard, Millets, Chickpea, Barley, Moong", yieldAvg: "1.5 t/ha", rain: "400 mm", soil: "Sandy Loam" },
    { name: "Sikkim", coords: [27.5330, 88.5122], crops: "Large Cardamom, Ginger, Tea, Maize", yieldAvg: "2.1 t/ha", rain: "2700 mm", soil: "Forest / Red" },
    { name: "Tamil Nadu", coords: [11.1271, 78.6569], crops: "Rice, Banana, Coconut, Sugarcane, Groundnut", yieldAvg: "3.6 t/ha", rain: "900 mm", soil: "Red / Clayey" },
    { name: "Telangana", coords: [18.1124, 79.0193], crops: "Cotton, Rice, Maize, Turmeric, Chilli", yieldAvg: "3.1 t/ha", rain: "900 mm", soil: "Black / Red" },
    { name: "Tripura", coords: [23.9408, 91.9882], crops: "Rubber, Tea, Rice, Jute, Coconut", yieldAvg: "2.7 t/ha", rain: "2100 mm", soil: "Alluvial / Red" },
    { name: "Uttar Pradesh", coords: [26.8467, 80.9462], crops: "Sugarcane, Wheat, Potato, Rice, Mango", yieldAvg: "3.9 t/ha", rain: "950 mm", soil: "Alluvial" },
    { name: "Uttarakhand", coords: [30.0668, 79.0193], crops: "Wheat, Rice, Apple, Sugarcane, Tea", yieldAvg: "2.8 t/ha", rain: "1400 mm", soil: "Alluvial / Mountain" },
    { name: "West Bengal", coords: [22.9868, 87.8550], crops: "Rice, Jute, Potato, Tea, Mango", yieldAvg: "3.6 t/ha", rain: "1550 mm", soil: "Clayey / Alluvial" },
    
    // 8 Union Territories
    { name: "Andaman and Nicobar Islands", coords: [11.7401, 92.6586], crops: "Coconut, Rubber, Banana, Rice", yieldAvg: "3.2 t/ha", rain: "2900 mm", soil: "Alluvial / Laterite" },
    { name: "Chandigarh", coords: [30.7333, 76.7794], crops: "Wheat, Maize, Horticulture", yieldAvg: "3.6 t/ha", rain: "600 mm", soil: "Alluvial" },
    { name: "Dadra and Nagar Haveli and Daman and Diu", coords: [20.1809, 73.0169], crops: "Rice, Sugarcane, Vegetables", yieldAvg: "2.8 t/ha", rain: "1800 mm", soil: "Black / Alluvial" },
    { name: "Delhi", coords: [28.7041, 77.1025], crops: "Wheat, Vegetables, Flowers, Mustard", yieldAvg: "3.5 t/ha", rain: "650 mm", soil: "Alluvial" },
    { name: "Jammu and Kashmir", coords: [33.7782, 76.5762], crops: "Apple, Saffron, Barley, Wheat", yieldAvg: "4.2 t/ha (Apple 12.8 t/ha)", rain: "800 mm", soil: "Alluvial / Clayey" },
    { name: "Ladakh", coords: [34.1526, 77.5771], crops: "Barley, Buckwheat, Apple, Wheat", yieldAvg: "2.1 t/ha", rain: "150 mm", soil: "Sandy / Cold Desert" },
    { name: "Lakshadweep", coords: [10.5667, 72.6417], crops: "Coconut, Coir & Lagoon Agri", yieldAvg: "11.5 t/ha", rain: "1600 mm", soil: "Coral / Sandy" },
    { name: "Puducherry", coords: [11.9416, 79.8083], crops: "Rice, Coconut, Sugarcane, Banana", yieldAvg: "3.4 t/ha", rain: "1300 mm", soil: "Coastal Alluvial" }
  ];

  statesData.forEach((st) => {
    const marker = L.circleMarker(st.coords, {
      radius: 8,
      fillColor: "#1e7e34",
      color: "#ffffff",
      weight: 2,
      opacity: 1,
      fillOpacity: 0.85,
    }).addTo(map);

    const popupHtml = `
      <div style="font-family: inherit; font-size: 0.88rem; min-width: 190px; line-height: 1.5;">
        <h4 style="margin: 0 0 6px; color: #1e7e34; font-size: 1.05rem;">🌾 ${st.name}</h4>
        <div><strong>Key Crops:</strong> ${st.crops}</div>
        <div><strong>Average Yield:</strong> ${st.yieldAvg}</div>
        <div><strong>Typical Rain:</strong> ${st.rain}</div>
        <div><strong>Dominant Soil:</strong> ${st.soil}</div>
        <div style="margin-top: 10px;">
          <a href="/predict?state=${encodeURIComponent(st.name)}" 
             style="background: #1e7e34; color: #fff; font-size: 0.8rem; font-weight: 600; padding: 5px 12px; display: inline-block; text-decoration: none; border-radius: 4px;">
            🌾 Predict for ${st.name} &rarr;
          </a>
        </div>
      </div>
    `;

    marker.bindPopup(popupHtml);
  });
}
