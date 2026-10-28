/**
 * Predict Page Logic - Farmer Yield Prediction & Advisory
 */

let currentAreaUnit = "ha"; // 'ha' or 'acre'

const PRESETS = {
  wheat_punjab: {
    farmer_name: "Ramesh Singh",
    state: "Punjab",
    district: "Ludhiana",
    crop: "Wheat",
    season: "Rabi",
    soil_type: "Alluvial",
    area_ha: 2.5,
    rainfall_mm: 520,
    temp_c: 19.5,
    fertilizer_kg: 130,
    pesticide_kg: 1.4,
    notes: "Ludhiana irrigated plains - certified HD-3086 seed",
  },
  rice_bengal: {
    farmer_name: "Subhash Mondal",
    state: "West Bengal",
    district: "Purba Bardhaman",
    crop: "Rice",
    season: "Kharif",
    soil_type: "Clayey",
    area_ha: 3.0,
    rainfall_mm: 1550,
    temp_c: 29.0,
    fertilizer_kg: 145,
    pesticide_kg: 2.2,
    notes: "Burdwan delta - Swarna variety with nursery transplanting",
  },
  cotton_maharashtra: {
    farmer_name: "Gajanan Patil",
    state: "Maharashtra",
    district: "Nagpur",
    crop: "Cotton",
    season: "Kharif",
    soil_type: "Black",
    area_ha: 4.0,
    rainfall_mm: 750,
    temp_c: 28.5,
    fertilizer_kg: 150,
    pesticide_kg: 2.8,
    notes: "Vidarbha deep black regur soil with drip lines",
  },
  sugarcane_up: {
    farmer_name: "Devendra Chaudhary",
    state: "Uttar Pradesh",
    district: "Muzaffarnagar",
    crop: "Sugarcane",
    season: "Whole Year",
    soil_type: "Alluvial",
    area_ha: 5.0,
    rainfall_mm: 1380,
    temp_c: 27.5,
    fertilizer_kg: 230,
    pesticide_kg: 3.2,
    notes: "Western UP sugar belt - Co-0238 ratoon crop",
  },
  tomato_karnataka: {
    farmer_name: "Manjunath Gowda",
    state: "Karnataka",
    district: "Kolar",
    crop: "Tomato",
    season: "Rabi",
    soil_type: "Red",
    area_ha: 1.5,
    rainfall_mm: 620,
    temp_c: 24.0,
    fertilizer_kg: 165,
    pesticide_kg: 2.5,
    notes: "Kolar horticultural belt - trellis staked cultivation",
  },
  onion_maharashtra: {
    farmer_name: "Suresh Shinde",
    state: "Maharashtra",
    district: "Nashik",
    crop: "Onion",
    season: "Rabi",
    soil_type: "Black",
    area_ha: 2.0,
    rainfall_mm: 550,
    temp_c: 22.0,
    fertilizer_kg: 140,
    pesticide_kg: 2.0,
    notes: "Nashik onion belt - high yield rabi crop with drip irrigation",
  },
  apple_kashmir: {
    farmer_name: "Bashir Ahmad",
    state: "Jammu and Kashmir",
    district: "Shopian",
    crop: "Apple",
    season: "Rabi",
    soil_type: "Sandy Loam",
    area_ha: 2.5,
    rainfall_mm: 850,
    temp_c: 15.0,
    fertilizer_kg: 160,
    pesticide_kg: 2.5,
    notes: "Shopian Kashmir orchard - Royal Delicious high density spur",
  },
};

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predict-form");
  const cropSelect = document.getElementById("crop");
  const unitHaBtn = document.getElementById("unit-ha");
  const unitAcreBtn = document.getElementById("unit-acre");
  const areaInput = document.getElementById("area");
  const areaLabelUnit = document.getElementById("area-label-unit");

  // Unit toggle handlers
  if (unitHaBtn && unitAcreBtn) {
    unitHaBtn.addEventListener("click", () => {
      if (currentAreaUnit === "acre") {
        const val = parseFloat(areaInput.value);
        if (!isNaN(val)) {
          areaInput.value = (val / 2.47105).toFixed(2);
        }
        currentAreaUnit = "ha";
        unitHaBtn.classList.add("active");
        unitAcreBtn.classList.remove("active");
        if (areaLabelUnit) areaLabelUnit.textContent = "(Hectares)";
      }
    });

    unitAcreBtn.addEventListener("click", () => {
      if (currentAreaUnit === "ha") {
        const val = parseFloat(areaInput.value);
        if (!isNaN(val)) {
          areaInput.value = (val * 2.47105).toFixed(2);
        }
        currentAreaUnit = "acre";
        unitAcreBtn.classList.add("active");
        unitHaBtn.classList.remove("active");
        if (areaLabelUnit) areaLabelUnit.textContent = "(Acres)";
      }
    });
  }

  // Preset Buttons
  document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const presetKey = e.target.getAttribute("data-preset");
      const preset = PRESETS[presetKey];
      if (preset) {
        applyPreset(preset);
        showToast(`Loaded realistic values for ${preset.crop} in ${preset.state}`, "info");
      }
    });
  });

  // Crop change auto-hint
  if (cropSelect) {
    cropSelect.addEventListener("change", async (e) => {
      const selectedCrop = e.target.value;
      if (!selectedCrop) return;
      try {
        const res = await fetch(`/api/crop-defaults/${encodeURIComponent(selectedCrop)}`);
        const data = await res.json();
        if (data.success && data.defaults) {
          const d = data.defaults;
          // Optionally populate default values if fields are empty
          const rain = document.getElementById("rainfall");
          const temp = document.getElementById("temperature");
          const fert = document.getElementById("fertilizer");
          if (!rain.value) rain.value = d.rainfall_mm;
          if (!temp.value) temp.value = d.temp_c;
          if (!fert.value) fert.value = d.fertilizer_kg;
        }
      } catch (err) {
        console.error("Error fetching crop defaults:", err);
      }
    });
  }

  // Load State-Districts Data from embedded JSON
  let stateDistrictsMap = {};
  const districtDataEl = document.getElementById("state-districts-data");
  if (districtDataEl) {
    try {
      stateDistrictsMap = JSON.parse(districtDataEl.textContent);
    } catch (e) {
      console.warn("Could not parse embedded district data:", e);
    }
  }

  // Helper to populate districts dropdown
  window.populateDistricts = function (state, selectedDistrict = null) {
    const districtSelect = document.getElementById("district");
    const countBadge = document.getElementById("district-count-badge");
    if (!districtSelect) return;

    districtSelect.innerHTML = "";
    const districts = stateDistrictsMap[state] || [];

    if (districts.length === 0) {
      const opt = document.createElement("option");
      opt.value = "";
      opt.textContent = "Select State First";
      districtSelect.appendChild(opt);
      if (countBadge) countBadge.style.display = "none";
      return;
    }

    const defaultOpt = document.createElement("option");
    defaultOpt.value = "";
    defaultOpt.disabled = true;
    defaultOpt.selected = !selectedDistrict;
    defaultOpt.textContent = `Choose ${state} District`;
    districtSelect.appendChild(defaultOpt);

    districts.forEach((d) => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = d;
      if (selectedDistrict && d.toLowerCase() === selectedDistrict.toLowerCase()) {
        opt.selected = true;
      }
      districtSelect.appendChild(opt);
    });

    if (countBadge) {
      countBadge.textContent = `${districts.length} Districts in ${state}`;
      countBadge.style.display = "inline-block";
    }

    // Auto-select first district if none pre-selected
    if (!selectedDistrict && districts.length > 0) {
      districtSelect.value = districts[0];
    }
  };

  // Query parameters support (e.g. from Location Map link)
  const urlParams = new URLSearchParams(window.location.search);
  const stateParam = urlParams.get("state");
  const districtParam = urlParams.get("district");
  const cropParam = urlParams.get("crop");
  if (stateParam) {
    const stateEl = document.getElementById("state");
    if (stateEl) {
      stateEl.value = stateParam;
      populateDistricts(stateParam, districtParam);
    }
  }
  if (cropParam) {
    const cropEl = document.getElementById("crop");
    if (cropEl) cropEl.value = cropParam;
  }

  // State, District & Season change: Auto-fetch weather data
  const stateSelect = document.getElementById("state");
  const districtSelect = document.getElementById("district");
  const seasonSelect = document.getElementById("season");

  if (stateSelect) {
    stateSelect.addEventListener("change", () => {
      populateDistricts(stateSelect.value);
      fetchWeatherForSelection();
    });
  }

  if (districtSelect) {
    districtSelect.addEventListener("change", () => {
      fetchWeatherForSelection();
    });
  }

  if (seasonSelect) {
    seasonSelect.addEventListener("change", () => {
      if (stateSelect && stateSelect.value) {
        fetchWeatherForSelection();
      }
    });
  }

  // Initial populate if state is pre-selected
  if (stateSelect && stateSelect.value) {
    populateDistricts(stateSelect.value, districtSelect ? districtSelect.value : null);
  }

  // Form Submission
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      await handlePredictionSubmit();
    });
  }
});

/**
 * Automatically fetches and populates live & seasonal weather for selected State, District and Season
 */
async function fetchWeatherForSelection(stateOverride, seasonOverride, districtOverride) {
  const stateEl = document.getElementById("state");
  const districtEl = document.getElementById("district");
  const seasonEl = document.getElementById("season");
  const rainEl = document.getElementById("rainfall");
  const tempEl = document.getElementById("temperature");
  const syncBanner = document.getElementById("weather-sync-banner");
  const syncTitle = document.getElementById("weather-sync-title");
  const syncDesc = document.getElementById("weather-sync-desc");
  const syncIcon = document.getElementById("weather-sync-icon");
  const statusText = document.getElementById("weather-status-text");
  const rainBadge = document.getElementById("rain-auto-badge");
  const tempBadge = document.getElementById("temp-auto-badge");

  const state = stateOverride || (stateEl ? stateEl.value : "");
  const district = districtOverride || (districtEl ? districtEl.value : "");
  const season = seasonOverride || (seasonEl ? seasonEl.value : "");

  if (!state) return;

  const locDisplay = district ? `${district}, ${state}` : state;

  // Show syncing status
  if (statusText) statusText.textContent = "Syncing Weather...";
  if (syncDesc) syncDesc.textContent = `Connecting to satellite weather service for ${locDisplay}...`;

  try {
    const res = await fetch("/api/weather", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: state, district: district, season: season })
    });
    const data = await res.json();

    if (data.success) {
      // Auto-populate rainfall and temperature
      if (rainEl) {
        rainEl.value = data.rainfall_mm;
      }
      if (tempEl) {
        tempEl.value = data.temperature_c;
      }

      // Show auto-filled badges
      if (rainBadge) rainBadge.style.display = "inline-block";
      if (tempBadge) tempBadge.style.display = "inline-block";

      // Update Weather Card
      if (syncBanner) syncBanner.classList.add("synced");
      if (syncIcon) syncIcon.textContent = data.icon || "🌤️";
      const displayLoc = data.district ? `${data.district}, ${data.state}` : data.state;
      if (syncTitle) syncTitle.textContent = `Synced Weather for ${displayLoc} (${data.season || "Annual"})`;
      if (syncDesc) {
        syncDesc.innerHTML = `Auto-populated: <strong>${data.temperature_c}°C</strong> ambient temperature & <strong>${data.rainfall_mm} mm</strong> seasonal rainfall. Humidity: ${data.humidity_percent}%. Condition: <em>${data.condition}</em>.`;
      }
      if (statusText) statusText.textContent = "Live Weather Synced";

      showToast(`🌤️ Weather auto-synced for ${displayLoc}: ${data.temperature_c}°C & ${data.rainfall_mm} mm rain!`, "success");

      // Auto-fetch 7-Day Forecast & Spray Advisory
      loadSprayForecast(data.state, data.district);
    }
  } catch (err) {
    console.error("Error fetching weather:", err);
    if (statusText) statusText.textContent = "Offline Normals Ready";
  }
}

/**
 * Auto-detects farmer's location via GPS and fetches hyper-local weather
 */
async function detectGPSWeather() {
  const gpsBtn = document.getElementById("btn-detect-gps");
  if (!navigator.geolocation) {
    showToast("Geolocation is not supported by your browser. Please select state from dropdown.", "error");
    return;
  }

  if (gpsBtn) {
    gpsBtn.classList.add("loading");
    gpsBtn.textContent = "📍 Detecting...";
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      const seasonEl = document.getElementById("season");
      const season = seasonEl ? seasonEl.value : "";

      try {
        const res = await fetch("/api/weather", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ lat: lat, lon: lon, season: season })
        });
        const data = await res.json();

        if (data.success) {
          // Select detected state and district in dropdown
          const stateEl = document.getElementById("state");
          if (stateEl && data.nearest_state) {
            stateEl.value = data.nearest_state;
            if (typeof populateDistricts === "function") {
              populateDistricts(data.nearest_state, data.nearest_district);
            }
          }

          // Populate weather
          document.getElementById("rainfall").value = data.rainfall_mm;
          document.getElementById("temperature").value = data.temperature_c;

          // Badges
          const rainBadge = document.getElementById("rain-auto-badge");
          const tempBadge = document.getElementById("temp-auto-badge");
          if (rainBadge) rainBadge.style.display = "inline-block";
          if (tempBadge) tempBadge.style.display = "inline-block";

          // Card
          const locName = data.nearest_district ? `${data.nearest_district}, ${data.nearest_state}` : data.nearest_state;
          const syncBanner = document.getElementById("weather-sync-banner");
          if (syncBanner) syncBanner.classList.add("synced");
          document.getElementById("weather-sync-icon").textContent = data.icon || "🌤️";
          document.getElementById("weather-sync-title").textContent = `GPS Detected: ${locName}`;
          document.getElementById("weather-sync-desc").innerHTML = `Coordinates (${lat.toFixed(2)}°, ${lon.toFixed(2)}°): <strong>${data.temperature_c}°C</strong> & <strong>${data.rainfall_mm} mm</strong> rainfall. Humidity: ${data.humidity_percent}%.`;
          document.getElementById("weather-status-text").textContent = "GPS Weather Synced";

          showToast(`📍 GPS Location detected near ${locName}! Weather auto-synced.`, "success");

          // Sync 7-day spray advisory for GPS location
          loadSprayForecast(data.nearest_state, data.nearest_district);
        }
      } catch (err) {
        console.error("GPS Weather Error:", err);
        showToast("Could not fetch weather for GPS coordinates.", "error");
      } finally {
        if (gpsBtn) {
          gpsBtn.classList.remove("loading");
          gpsBtn.textContent = "📍 Detect Location";
        }
      }
    },
    (err) => {
      console.warn("Geolocation denied or error:", err);
      if (gpsBtn) {
        gpsBtn.classList.remove("loading");
        gpsBtn.textContent = "📍 Detect Location";
      }
      showToast("Location access was not granted. Please select your State from the dropdown to auto-sync weather.", "info");
    },
    { timeout: 10000 }
  );
}

function applyPreset(preset) {
  document.getElementById("farmer_name").value = preset.farmer_name || "";
  document.getElementById("state").value = preset.state;
  if (typeof populateDistricts === "function") {
    populateDistricts(preset.state, preset.district);
  }
  const districtEl = document.getElementById("district");
  if (districtEl && preset.district) {
    districtEl.value = preset.district;
  }
  document.getElementById("crop").value = preset.crop;
  document.getElementById("season").value = preset.season;
  document.getElementById("soil_type").value = preset.soil_type;

  const areaInput = document.getElementById("area");
  if (currentAreaUnit === "acre") {
    areaInput.value = (preset.area_ha * 2.47105).toFixed(2);
  } else {
    areaInput.value = preset.area_ha;
  }

  document.getElementById("rainfall").value = preset.rainfall_mm;
  document.getElementById("temperature").value = preset.temp_c;
  document.getElementById("fertilizer").value = preset.fertilizer_kg;
  document.getElementById("pesticide").value = preset.pesticide_kg;
  document.getElementById("notes").value = preset.notes || "";

  // Update weather sync status
  const syncBanner = document.getElementById("weather-sync-banner");
  if (syncBanner) {
    syncBanner.classList.add("synced");
    const syncIcon = document.getElementById("weather-sync-icon");
    const syncTitle = document.getElementById("weather-sync-title");
    const syncDesc = document.getElementById("weather-sync-desc");
    const statusText = document.getElementById("weather-status-text");
    const locDisplay = preset.district ? `${preset.district}, ${preset.state}` : preset.state;
    if (syncIcon) syncIcon.textContent = "🌤️";
    if (syncTitle) syncTitle.textContent = `Preset Weather for ${locDisplay} (${preset.season})`;
    if (syncDesc) syncDesc.innerHTML = `Loaded: <strong>${preset.temp_c}°C</strong> ambient temperature & <strong>${preset.rainfall_mm} mm</strong> seasonal rainfall.`;
    if (statusText) statusText.textContent = "Preset Synced";
  }
  const rainBadge = document.getElementById("rain-auto-badge");
  const tempBadge = document.getElementById("temp-auto-badge");
  if (rainBadge) rainBadge.style.display = "inline-block";
  if (tempBadge) tempBadge.style.display = "inline-block";

  // Auto-sync spray advisory for preset location
  loadSprayForecast(preset.state, preset.district);
}

async function handlePredictionSubmit() {
  const submitBtn = document.getElementById("predict-submit-btn");
  const crop = document.getElementById("crop").value;
  const state = document.getElementById("state").value;
  const district = (document.getElementById("district")?.value || "").trim();
  const season = document.getElementById("season").value;
  const soil_type = document.getElementById("soil_type").value;
  const rawRain = document.getElementById("rainfall").value.trim();
  const rawTemp = document.getElementById("temperature").value.trim();
  const rawAreaVal = document.getElementById("area").value.trim();
  const rawFert = document.getElementById("fertilizer").value.trim();
  const rawPest = document.getElementById("pesticide").value.trim();

  // Test 2: Check for missing or empty mandatory fields
  if (!crop || !state || !season || !soil_type || !rawRain || !rawTemp || !rawAreaVal) {
    showToast("Please enter all required information.", "error");
    return;
  }

  const rainfall_mm = parseFloat(rawRain);
  const temp_c = parseFloat(rawTemp);
  const rawArea = parseFloat(rawAreaVal);
  const fertilizer_kg = parseFloat(rawFert) || 120;
  const pesticide_kg = parseFloat(rawPest) || 1.5;

  // Test 3: Validate negative or out-of-range inputs
  if (rainfall_mm < 0) {
    showToast("Invalid input: Rainfall cannot be negative.", "error");
    return;
  }

  if (rawArea <= 0 || isNaN(rawArea)) {
    showToast("Invalid input: Farm area must be greater than zero.", "error");
    return;
  }

  if (temp_c < -15 || temp_c > 65 || isNaN(temp_c)) {
    showToast("Invalid input: Temperature must be between -15°C and 65°C.", "error");
    return;
  }

  if (fertilizer_kg < 0 || pesticide_kg < 0) {
    showToast("Invalid input: Fertilizer and pesticide amounts cannot be negative.", "error");
    return;
  }

  if (pesticide_kg > 25) {
    showToast("Invalid input: Pesticide usage cannot exceed 25 kg/ha.", "error");
    return;
  }

  // Convert area to Hectares for ML model if entered in acres
  const areaInHa = currentAreaUnit === "acre" ? rawArea / 2.47105 : rawArea;

  const payload = {
    farmer_name: document.getElementById("farmer_name").value.trim(),
    state: state,
    district: district,
    crop: crop,
    season: season,
    soil_type: soil_type,
    area_ha: areaInHa,
    rainfall_mm: rainfall_mm,
    temp_c: temp_c,
    fertilizer_kg: fertilizer_kg,
    pesticide_kg: pesticide_kg,
    notes: document.getElementById("notes").value.trim(),
  };

  // Test 4: Slow internet / Loading State
  const originalBtnText = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span>⏳</span> Predicting...`;

  const resultContainer = document.getElementById("result-container");
  if (resultContainer) {
    resultContainer.innerHTML = `
      <div class="result-placeholder" style="border-color: var(--primary); background: #f0fdf4;">
        <div class="result-placeholder-icon">⏳</div>
        <h3 style="color: var(--primary-dark); font-size: 1.25rem;">Predicting...</h3>
        <p style="color: var(--gray-medium); font-size: 0.9rem; max-width: 320px; margin: 8px auto 0;">
          Evaluating agro-climatic conditions and soil chemistry through the ML model. Please wait...
        </p>
      </div>
    `;
  }

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!data.success) {
      throw new Error(data.error || "Failed to calculate prediction");
    }

    renderPredictionResult(data.analysis, payload, data.financials);
    showToast(`🌾 Predicted Yield: ${data.predicted_yield_t_ha} tonnes/hectare`, "success");

    // Smooth scroll to result on mobile
    if (window.innerWidth < 900 && resultContainer) {
      resultContainer.scrollIntoView({ behavior: "smooth" });
    }
  } catch (err) {
    showToast(err.message, "error");
    console.error(err);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalBtnText;
  }
}

function renderPredictionResult(analysis, inputData, financials) {
  const container = document.getElementById("result-container");
  if (!container) return;

  const advisoriesHtml = analysis.advisories
    .map((adv) => {
      const icon = adv.type === "positive" ? "✅" : adv.type === "alert" ? "⚠️" : "ℹ️";
      return `
      <div class="advisory-item">
        <span>${icon}</span>
        <div>
          <strong>${adv.title}:</strong> ${adv.text}
        </div>
      </div>
    `;
    })
    .join("");

  const tipsHtml = analysis.expert_tips
    .map((tip) => `<li><span>💡</span> <span>${tip}</span></li>`)
    .join("");

  const whatsappUrl = generateWhatsAppShareLink(analysis, inputData, financials);

  container.innerHTML = `
    <div class="result-card">
      <div class="result-header">
        <div class="result-badge">
          <span class="badge ${analysis.badge_class}">
            ${analysis.status_icon} ${analysis.status}
          </span>
        </div>
        <div class="result-crop-icon">${analysis.icon}</div>
        <div class="result-crop-name">${analysis.crop}</div>
        <div style="font-size: 0.85rem; opacity: 0.9;">${analysis.category} &bull; ${inputData.season} Season &bull; ${inputData.district ? inputData.district + ', ' : ''}${inputData.state}</div>

        <div class="result-main-yield">
          <div class="yield-number">${analysis.predicted_yield_t_ha}</div>
          <div class="yield-unit">Tonnes / Hectare</div>
          <div class="yield-alt-unit">&asymp; ${analysis.predicted_yield_q_acre} Quintals / Acre</div>
        </div>
      </div>

      <div class="result-body">
        <div class="metrics-summary-grid">
          <div class="metric-box">
            <div class="metric-box-val">${analysis.total_production_tonnes} T</div>
            <div class="metric-box-lbl">Total Farm Output (${analysis.area_ha} Ha / ${analysis.area_acres} Acres)</div>
          </div>
          <div class="metric-box">
            <div class="metric-box-val">${analysis.benchmark_yield_t_ha} T/Ha</div>
            <div class="metric-box-lbl">Regional Benchmark (${analysis.ratio_vs_benchmark}% of standard)</div>
          </div>
        </div>

        <!-- Financial Profit & Revenue ROI Card -->
        ${renderFinancialsHtml(financials)}

        ${renderCropSuggestionHtml(analysis.suggested_alternative_crop, analysis, inputData)}

        <div style="margin-bottom: 16px; font-size: 0.9rem; color: #374151;">
          <strong>Farm Summary:</strong> ${analysis.summary}
        </div>

        <div class="advisory-box">
          <h4 style="margin-bottom: 8px; font-size: 0.95rem; color: #92400e;">
            🌾 Field & Climate Suitability Analysis
          </h4>
          ${advisoriesHtml}
        </div>

        <div style="margin-top: 16px;">
          <h4 style="font-size: 0.95rem; color: #1e7e34; margin-bottom: 6px;">
            🧑‍🌾 Agronomist Recommendations
          </h4>
          <ul class="tips-list">
            ${tipsHtml}
          </ul>
        </div>

        <!-- 1-Click WhatsApp Share & Action Buttons -->
        <div class="result-actions" style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;">
          <a href="${whatsappUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp" style="background: #25D366; color: #ffffff; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px 16px; font-size: 0.96rem; text-decoration: none; border-radius: 8px; box-shadow: 0 4px 14px rgba(37, 211, 102, 0.4); border: none;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
              <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
            </svg>
            <span>📲 Share Farm Yield & Profit on WhatsApp</span>
          </a>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-outline btn-sm" onclick="window.print()" style="flex: 1;">
              🖨️ Print Farmer Yield Card
            </button>
            <a href="/dashboard" class="btn btn-primary btn-sm" style="flex: 1;">
              📊 View History & Analytics
            </a>
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderCropSuggestionHtml(sug, analysis, inputData) {
  if (!sug) return "";

  const gainText = sug.yield_diff_percent > 0
    ? `+${sug.yield_diff_percent}% Yield Gain`
    : `Higher Regional Fit`;

  const locationDisplay = inputData.district ? `${inputData.district}, ${inputData.state}` : inputData.state;

  return `
    <div class="crop-suggestion-card" style="margin-bottom: 20px; background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 2px solid #f59e0b; border-radius: var(--radius-md); padding: 18px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
        <div style="display: flex; align-items: center; gap: 6px;">
          <span style="font-size: 1.3rem;">💡</span>
          <span style="font-size: 0.8rem; font-weight: 800; color: #92400e; text-transform: uppercase; letter-spacing: 0.5px;">
            Yield Optimization Suggestion for ${locationDisplay}
          </span>
        </div>
        <span style="background: #15803d; color: #fff; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: var(--radius-full);">
          ${gainText}
        </span>
      </div>

      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        <div style="font-size: 2.2rem; line-height: 1;">${sug.icon}</div>
        <div>
          <h4 style="font-size: 1.15rem; font-weight: 800; color: #78350f; margin: 0;">
            Recommend Switching to <span style="color: #166534; text-decoration: underline;">${sug.crop}</span>
          </h4>
          <div style="font-size: 0.82rem; color: #92400e;">
            Expected harvest: <strong>${sug.expected_yield_t_ha} tonnes/ha</strong> (vs current ${analysis.predicted_yield_t_ha} t/ha for ${analysis.crop})
          </div>
        </div>
      </div>

      <p style="font-size: 0.88rem; color: #451a03; line-height: 1.5; margin-bottom: 14px; background: rgba(255,255,255,0.7); padding: 10px 12px; border-radius: var(--radius-sm); border: 1px solid #fde68a;">
        ${sug.reason}
      </p>

      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 14px;">
        <span style="background: #fff; border: 1px solid #fde68a; color: #78350f; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 12px;">📍 ${sug.why_state}</span>
        <span style="background: #fff; border: 1px solid #fde68a; color: #78350f; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 12px;">🌱 ${sug.why_soil}</span>
        <span style="background: #fff; border: 1px solid #fde68a; color: #78350f; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 12px;">🌦️ ${sug.why_climate}</span>
      </div>

      <button type="button" class="btn btn-primary btn-sm" onclick="switchToSuggestedCrop('${sug.crop}')" style="width: 100%; font-weight: 700; background: #15803d; border-color: #166534; padding: 9px; font-size: 0.9rem; display: flex; align-items: center; justify-content: center; gap: 6px; box-shadow: 0 2px 6px rgba(21, 128, 61, 0.3);">
        <span>🔄</span> Switch Crop to ${sug.crop} & Simulate Forecast (${sug.expected_yield_t_ha} t/ha)
      </button>
    </div>
  `;
}

function switchToSuggestedCrop(cropName) {
  const cropSelect = document.getElementById("crop");
  if (cropSelect) {
    cropSelect.value = cropName;
    cropSelect.style.borderColor = "#22c55e";
    cropSelect.style.boxShadow = "0 0 0 4px rgba(34, 197, 94, 0.3)";
    setTimeout(() => {
      cropSelect.style.borderColor = "";
      cropSelect.style.boxShadow = "";
    }, 2000);

    showToast(`🔄 Switched crop to ${cropName}! Recalculating forecast...`, "success");

    // Automatically trigger prediction submit with the new crop
    setTimeout(() => {
      handlePredictionSubmit();
    }, 350);
  }
}

/* ==========================================================================
   💰 Financial Profit & Revenue ROI Engine
   ========================================================================== */

function renderFinancialsHtml(fin) {
  if (!fin) return "";
  const isProfit = fin.net_profit >= 0;
  const profitColor = isProfit ? "#15803d" : "#b91c1c";
  const bgGrad = isProfit ? "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)" : "linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)";
  const borderCol = isProfit ? "#86efac" : "#fca5a5";

  return `
    <div class="financial-profit-card" style="margin-bottom: 20px; background: ${bgGrad}; border: 1.5px solid ${borderCol}; border-radius: var(--radius-md); padding: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid rgba(0,0,0,0.08); padding-bottom: 10px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 1.4rem;">💰</span>
          <span style="font-weight: 800; font-size: 0.95rem; color: #166534; text-transform: uppercase; letter-spacing: 0.5px;">
            Financial Profit & Revenue ROI Forecast
          </span>
        </div>
        <span style="background: ${profitColor}; color: white; font-weight: 700; font-size: 0.75rem; padding: 3px 10px; border-radius: 12px;">
          ${fin.profit_rating}
        </span>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 14px;">
        <div style="background: white; border-radius: 8px; padding: 10px 12px; border: 1px solid rgba(0,0,0,0.06);">
          <div style="font-size: 0.72rem; color: #6b7280; text-transform: uppercase; font-weight: 600;">Gross Mandi Revenue</div>
          <div style="font-size: 1.15rem; font-weight: 800; color: #1f2937;">${fin.formatted_gross_revenue}</div>
          <div style="font-size: 0.7rem; color: #9ca3af;">@ ₹${fin.mandi_rate_quintal}/qtl</div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 10px 12px; border: 1px solid rgba(0,0,0,0.06);">
          <div style="font-size: 0.72rem; color: #6b7280; text-transform: uppercase; font-weight: 600;">Total Input Cost</div>
          <div style="font-size: 1.15rem; font-weight: 800; color: #dc2626;">${fin.formatted_total_cost}</div>
          <div style="font-size: 0.7rem; color: #9ca3af;">Seed, Fert, Labor</div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 10px 12px; border: 1px solid rgba(0,0,0,0.06);">
          <div style="font-size: 0.72rem; color: #6b7280; text-transform: uppercase; font-weight: 600;">Net Farmer Profit</div>
          <div style="font-size: 1.25rem; font-weight: 800; color: ${profitColor};">${fin.formatted_net_profit}</div>
          <div style="font-size: 0.7rem; color: #15803d; font-weight: 600;">${fin.formatted_profit_per_acre}</div>
        </div>
        <div style="background: white; border-radius: 8px; padding: 10px 12px; border: 1px solid rgba(0,0,0,0.06);">
          <div style="font-size: 0.72rem; color: #6b7280; text-transform: uppercase; font-weight: 600;">Return on Capital (ROI)</div>
          <div style="font-size: 1.25rem; font-weight: 800; color: #2563eb;">${fin.roi_percent}%</div>
          <div style="font-size: 0.7rem; color: #6b7280;">Govt MSP: ₹${fin.msp_rate_quintal}/qtl</div>
        </div>
      </div>

      <div style="font-size: 0.78rem; color: #4b5563; background: rgba(255,255,255,0.85); padding: 8px 12px; border-radius: 6px;">
        🏛️ <strong>MSP Safety Net:</strong> Assured ₹${fin.gross_revenue_msp.toLocaleString('en-IN')} revenue at Government MSP (₹${fin.msp_rate_quintal}/quintal) ensures guaranteed floor returns.
      </div>
    </div>
  `;
}

/* ==========================================================================
   📲 1-Click WhatsApp Share Generator
   ========================================================================== */

function generateWhatsAppShareLink(analysis, inputData, financials) {
  const farmer = inputData.farmer_name || "Farmer";
  const loc = inputData.district ? `${inputData.district}, ${inputData.state}` : inputData.state;
  const profitStr = financials ? `💰 *Estimated Net Profit:* ${financials.formatted_net_profit} (${financials.formatted_profit_per_acre}, ROI: ${financials.roi_percent}%)\n💵 *Gross Mandi Revenue:* ${financials.formatted_gross_revenue}\n` : "";
  const tip = analysis.expert_tips && analysis.expert_tips.length > 0 ? analysis.expert_tips[0] : "Maintain balanced soil nutrition.";

  const text = 
`🌾 *Crop Yield & Farm Profit Advisory - CropYield AI*
👨‍🌾 *Farmer:* ${farmer}
📍 *Location:* ${loc}
🌱 *Crop:* ${analysis.crop} (${inputData.season} Season)
📊 *Estimated Yield:* ${analysis.predicted_yield_t_ha} Tonnes/Ha (~ ${analysis.predicted_yield_q_acre} Quintals/Acre)
🚜 *Total Harvest:* ${analysis.total_production_tonnes} Tonnes (${inputData.area_ha} Ha)
${profitStr}✨ *Status:* ${analysis.status} (${analysis.ratio_vs_benchmark}% of regional benchmark)
💡 *Agronomist Tip:* ${tip}

📲 Calculated on CropYield AI Platform (Govt ICAR Calibrated)
Check your farm yield: https://cropyieldai.in`;

  return `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
}

/* ==========================================================================
   🌦️ 7-Day Meteorological Weather Forecast & Spray Advisory Widget
   ========================================================================== */

async function loadSprayForecast(state, district) {
  const container = document.getElementById("spray-forecast-container");
  if (!container || !state) return;

  try {
    const res = await fetch(`/api/spray-forecast?state=${encodeURIComponent(state)}&district=${encodeURIComponent(district || "")}`);
    const data = await res.json();
    if (data.success) {
      renderSprayAdvisoryWidget(data);
    }
  } catch (err) {
    console.error("Error loading spray forecast:", err);
  }
}

function renderSprayAdvisoryWidget(data) {
  const container = document.getElementById("spray-forecast-container");
  if (!container) return;

  const adv = data.spray_advisory;
  const badgeClass = adv.badge_color === "success" ? "background: #dcfce7; color: #166534; border: 1px solid #86efac;" : adv.badge_color === "warning" ? "background: #fef3c7; color: #92400e; border: 1px solid #fde68a;" : "background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;";

  const dayCardsHtml = (data.forecast_days || []).map((day) => {
    const tagBg = day.spray_class === "success" ? "#dcfce7" : day.spray_class === "warning" ? "#fef3c7" : "#fee2e2";
    const tagColor = day.spray_class === "success" ? "#166534" : day.spray_class === "warning" ? "#92400e" : "#991b1b";

    return `
      <div style="flex: 1; min-width: 85px; background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px 6px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size: 0.75rem; font-weight: 700; color: #374151;">${day.day_name}</div>
        <div style="font-size: 1.3rem; margin: 2px 0;">${day.icon}</div>
        <div style="font-size: 0.78rem; font-weight: 700; color: #111827;">${day.temp_max}° / ${day.temp_min}°</div>
        <div style="font-size: 0.68rem; color: #0284c7;">🌧️ ${day.precipitation_sum}mm</div>
        <div style="font-size: 0.68rem; color: #6b7280;">💨 ${day.windspeed_max}km/h</div>
        <div style="margin-top: 4px; font-size: 0.62rem; font-weight: 700; background: ${tagBg}; color: ${tagColor}; padding: 2px 4px; border-radius: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          ${day.spray_status}
        </div>
      </div>
    `;
  }).join("");

  const reasonsHtml = (adv.reasons || []).map(r => `<li>${r}</li>`).join("");

  container.innerHTML = `
    <div style="background: #ffffff; border: 1.5px solid #0284c7; border-radius: var(--radius-md); padding: 16px; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.1);">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 1.3rem;">🌦️</span>
          <div>
            <span style="font-weight: 800; font-size: 0.92rem; color: #0369a1; text-transform: uppercase;">
              7-Day Weather & Spray Advisory
            </span>
            <span style="font-size: 0.78rem; color: #6b7280; margin-left: 6px;">(${data.location})</span>
          </div>
        </div>
        <span style="font-weight: 800; font-size: 0.75rem; padding: 4px 10px; border-radius: 12px; ${badgeClass}">
          ${adv.status}
        </span>
      </div>

      <!-- Spray status headline & timing -->
      <div style="background: #f8fafc; border-left: 4px solid #0284c7; padding: 10px 12px; border-radius: 0 6px 6px 0; margin-bottom: 12px;">
        <div style="font-size: 0.88rem; font-weight: 700; color: #0f172a;">
          ${adv.headline}
        </div>
        <div style="font-size: 0.8rem; color: #475569; margin-top: 3px;">
          ⏰ <strong>Recommended Spray Hours:</strong> ${adv.best_window}
        </div>
        <ul style="font-size: 0.78rem; color: #64748b; margin: 6px 0 0 16px; padding: 0;">
          ${reasonsHtml}
        </ul>
      </div>

      <!-- 7-Day Daily Forecast Cards Strip -->
      <div style="display: flex; gap: 6px; overflow-x: auto; padding-bottom: 4px;">
        ${dayCardsHtml}
      </div>
    </div>
  `;
  container.style.display = "block";
}

