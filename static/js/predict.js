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

    renderPredictionResult(data.analysis, payload);
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

function renderPredictionResult(analysis, inputData) {
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

        <div class="result-actions">
          <button class="btn btn-outline btn-sm" onclick="window.print()" style="flex: 1;">
            🖨️ Print Farmer Yield Card
          </button>
          <a href="/dashboard" class="btn btn-primary btn-sm" style="flex: 1;">
            📊 View History & Analytics
          </a>
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

