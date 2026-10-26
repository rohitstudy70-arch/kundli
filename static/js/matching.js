/**
 * Kundali Matching JavaScript
 * Handles Groom and Bride Nominatim autocomplete, validation, and dynamic matching report.
 */

document.addEventListener("DOMContentLoaded", function () {
  const matchingForm = document.getElementById("matchingForm");
  const matchSubmitBtn = document.getElementById("matchSubmitBtn");
  const matchAlert = document.getElementById("matchAlert");
  const matchPrintBtn = document.getElementById("matchPrintBtn");

  // Setup Nominatim Autocomplete for both Groom and Bride
  setupPlaceAutocomplete("groom_place", "groomDropdown", "groomSpinner", "groom_lat", "groom_lon", "groom_tz");
  setupPlaceAutocomplete("bride_place", "brideDropdown", "brideSpinner", "bride_lat", "bride_lon", "bride_tz");

  function setupPlaceAutocomplete(inputId, dropdownId, spinnerId, latId, lonId, tzId) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(dropdownId);
    const spinner = document.getElementById(spinnerId);
    const latEl = document.getElementById(latId);
    const lonEl = document.getElementById(lonId);
    const tzEl = document.getElementById(tzId);

    if (!input || !dropdown) return;

    let timeout = null;

    input.addEventListener("input", function (e) {
      const q = e.target.value.trim();
      clearTimeout(timeout);
      if (q.length < 2) {
        dropdown.innerHTML = "";
        dropdown.classList.remove("active");
        return;
      }

      if (spinner) spinner.classList.add("active");

      timeout = setTimeout(() => {
        fetch(`/api/search-place?q=${encodeURIComponent(q)}`)
          .then((res) => res.json())
          .then((places) => {
            if (spinner) spinner.classList.remove("active");
            dropdown.innerHTML = "";
            if (!places || !places.length) {
              dropdown.classList.remove("active");
              return;
            }

            places.forEach((p) => {
              const item = document.createElement("div");
              item.className = "autocomplete-item";
              item.textContent = p.name;
              item.addEventListener("click", () => {
                input.value = p.name;
                latEl.value = p.lat;
                lonEl.value = p.lon;
                if (tzEl && p.timezone) tzEl.value = p.timezone;
                dropdown.innerHTML = "";
                dropdown.classList.remove("active");
              });
              dropdown.appendChild(item);
            });
            dropdown.classList.add("active");
          })
          .catch(() => {
            if (spinner) spinner.classList.remove("active");
            dropdown.classList.remove("active");
          });
      }, 350);
    });

    document.addEventListener("click", function (e) {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove("active");
      }
    });
  }

  // ==========================================
  // Form Submission
  // ==========================================
  if (matchingForm) {
    matchingForm.addEventListener("submit", function (e) {
      e.preventDefault();

      // Clear previous errors
      document.querySelectorAll(".field-error-msg").forEach((el) => {
        el.classList.remove("visible");
        el.textContent = "";
      });
      if (matchAlert) {
        matchAlert.style.display = "none";
        matchAlert.textContent = "";
      }

      // Collect Groom Data
      const groomData = {
        name: document.getElementById("groom_name").value.trim() || "वर",
        gender: "पुरुष",
        birth_date: document.getElementById("groom_birth_date").value.trim(),
        birth_time: document.getElementById("groom_birth_time").value.trim(),
        place_name: document.getElementById("groom_place").value.trim(),
        latitude: parseFloat(document.getElementById("groom_lat").value),
        longitude: parseFloat(document.getElementById("groom_lon").value),
        timezone: document.getElementById("groom_tz").value.trim() || "Asia/Kolkata",
      };

      // Collect Bride Data
      const brideData = {
        name: document.getElementById("bride_name").value.trim() || "वधू",
        gender: "महिला",
        birth_date: document.getElementById("bride_birth_date").value.trim(),
        birth_time: document.getElementById("bride_birth_time").value.trim(),
        place_name: document.getElementById("bride_place").value.trim(),
        latitude: parseFloat(document.getElementById("bride_lat").value),
        longitude: parseFloat(document.getElementById("bride_lon").value),
        timezone: document.getElementById("bride_tz").value.trim() || "Asia/Kolkata",
      };

      // Client validation
      let hasError = false;
      if (!groomData.birth_date) {
        showError("groom_birth_date_error", "कृपया वर की जन्म तिथि दर्ज करें।");
        hasError = true;
      }
      if (!groomData.birth_time) {
        showError("groom_birth_time_error", "कृपया वर का जन्म समय दर्ज करें।");
        hasError = true;
      }
      if (!groomData.place_name || isNaN(groomData.latitude)) {
        showError("groom_place_error", "कृपया वर का जन्म स्थान खोज सूची से चुनें।");
        hasError = true;
      }

      if (!brideData.birth_date) {
        showError("bride_birth_date_error", "कृपया वधू की जन्म तिथि दर्ज करें।");
        hasError = true;
      }
      if (!brideData.birth_time) {
        showError("bride_birth_time_error", "कृपया वधू का जन्म समय दर्ज करें।");
        hasError = true;
      }
      if (!brideData.place_name || isNaN(brideData.latitude)) {
        showError("bride_place_error", "कृपया वधू का जन्म स्थान खोज सूची से चुनें।");
        hasError = true;
      }

      if (hasError) return;

      // Loading state
      matchSubmitBtn.disabled = true;
      const originalText = matchSubmitBtn.innerHTML;
      matchSubmitBtn.innerHTML = `<span>⏳ अष्टकूट गुण मिलान गणना हो रही है...</span>`;

      fetch("/api/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ groom: groomData, bride: brideData }),
      })
        .then((res) => res.json())
        .then((response) => {
          matchSubmitBtn.disabled = false;
          matchSubmitBtn.innerHTML = originalText;

          if (!response.success) {
            if (matchAlert) {
              matchAlert.style.display = "block";
              matchAlert.textContent = response.message || "गणना में त्रुटि उत्पन्न हुई।";
            }
            return;
          }

          updateMatchingDOM(response.data);

          // Scroll to results
          const resultsSec = document.getElementById("matchingResultsContainer");
          if (resultsSec) {
            resultsSec.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        })
        .catch((err) => {
          matchSubmitBtn.disabled = false;
          matchSubmitBtn.innerHTML = originalText;
          if (matchAlert) {
            matchAlert.style.display = "block";
            matchAlert.textContent = "सर्वर से संपर्क करने में असमर्थ।";
          }
        });
    });
  }

  function showError(id, msg) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = msg;
      el.classList.add("visible");
    }
  }

  function updateMatchingDOM(data) {
    const match = data.match_result;
    const groomChart = data.groom_chart;
    const brideChart = data.bride_chart;

    // 1. Total Score & Verdict
    setText("res_total_score", match.total_score);
    const badge = document.getElementById("res_verdict_badge");
    if (badge) {
      badge.textContent = match.verdict_badge;
      badge.style.background = match.verdict_color;
    }
    setText("res_verdict_desc", match.verdict_desc);

    // Summary texts
    setText("res_groom_summary", `${match.summary.groom.name} | लग्न: ${match.summary.groom.lagna} | राशि: ${match.summary.groom.rashi} | ${match.summary.groom.nakshatra}`);
    setText("res_bride_summary", `${match.summary.bride.name} | लग्न: ${match.summary.bride.lagna} | राशि: ${match.summary.bride.rashi} | ${match.summary.bride.nakshatra}`);

    // Print Header
    setText("print_matching_title", `${match.summary.groom.name} एवं ${match.summary.bride.name} का कुंडली मिलान`);

    // 2. Manglik Analysis
    const mStatus = document.getElementById("res_manglik_status");
    if (mStatus) mStatus.textContent = match.manglik_analysis.status;
    setText("res_manglik_groom", `${match.manglik_analysis.groom.status} (मंगल भाव ${match.manglik_analysis.groom.mars_house})`);
    setText("res_manglik_bride", `${match.manglik_analysis.bride.status} (मंगल भाव ${match.manglik_analysis.bride.mars_house})`);
    setText("res_manglik_verdict", match.manglik_analysis.verdict);

    // 3. Ashta Kuta Table
    const tableBody = document.getElementById("kutaTableBody");
    if (tableBody && match.kutas) {
      tableBody.innerHTML = "";
      match.kutas.forEach((k) => {
        const row = document.createElement("tr");
        const color = k.obtained_points === k.max_points ? "#2E7D32" : (k.obtained_points > 0 ? "#C57B12" : "#C62828");
        row.innerHTML = `
          <td><strong>${k.name_hi}</strong></td>
          <td style="font-size: 0.85rem; color: var(--text-secondary);">${k.area}</td>
          <td>${k.max_points}</td>
          <td><strong style="color: ${color}; font-size: 1.05rem;">${k.obtained_points}</strong></td>
          <td>${k.groom_val}</td>
          <td>${k.bride_val}</td>
          <td style="font-size: 0.88rem;">${k.description}</td>
        `;
        tableBody.appendChild(row);
      });
    }

    // 4. Update SVG Charts
    const gContainer = document.getElementById("groomChartContainer");
    if (gContainer && groomChart.chart_svg) {
      gContainer.innerHTML = groomChart.chart_svg;
    }
    const bContainer = document.getElementById("brideChartContainer");
    if (bContainer && brideChart.chart_svg) {
      bContainer.innerHTML = brideChart.chart_svg;
    }
  }

  function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  // Print button
  if (matchPrintBtn) {
    matchPrintBtn.addEventListener("click", () => window.print());
  }

  // FAQ Accordion
  document.querySelectorAll(".faq-question").forEach((btn) => {
    btn.addEventListener("click", function () {
      const parent = this.parentElement;
      const isOpen = parent.classList.contains("open");
      document.querySelectorAll(".faq-item").forEach((item) => item.classList.remove("open"));
      if (!isOpen) parent.classList.add("open");
    });
  });
});
