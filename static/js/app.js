/**
 * Vedic Janam Kundali Frontend Application
 * Handles OpenStreetMap Nominatim autocomplete, client-side validation,
 * bilingual translation (हिन्दी ⇄ English), AJAX calculations, dynamic DOM updating, and print layouts.
 */

const I18N = {
  hi: {
    brand_title: "वैदिक जन्म कुंडली",
    site_title: "सटीक वैदिक जन्म कुंडली (Janam Kundali)",
    site_tagline: "लाहिड़ी अयनांश, सम्पूर्ण राशि भाव एवं विंशोत्तरी महादशा चक्र पर आधारित प्रामाणिक जन्म पत्रिका",
    nav_kundli: "📜 जन्म कुंडली (Kundli)",
    nav_matching: "💍 कुंडली मिलान (Matching)",
    nav_lagna: "🌅 लग्न (Lagna)",
    nav_dasha: "⌛ महादशा (Dasha)",
    nav_nakshatra: "✨ नक्षत्र (Nakshatra)",
    nav_manglik: "🔥 मांगलिक दोष",
    nav_sade_sati: "🪐 साढ़े साती",
    nav_panchang: "📅 पंचांग (Panchang)",
    bc_home: "होम",
    bc_astro: "ज्योतिष",
    bc_current: "जन्म कुंडली हिंदी में",
    form_title: "अपना जन्म विवरण डालें",
    lbl_name: "नाम (Name)*",
    ph_name: "आपका नाम (उदा. रोहित शर्मा)",
    lbl_gender: "लिंग (Gender)*",
    lbl_male: "पुरुष",
    lbl_female: "महिला",
    lbl_other: "अन्य",
    lbl_dob: "जन्म तिथि (Date of Birth)*",
    lbl_tob: "जन्म समय (Birth Time)*",
    lbl_pob: "जन्म स्थान (Birth Place)*",
    ph_pob: "उदा. नई दिल्ली, मुंबई, जयपुर, वाराणसी...",
    pob_help: "स्थान का नाम टाइप करें और सूची से चुनें (अक्षांश व देशांतर स्वतः भरे जाएंगे)।",
    btn_submit: "कुंडली प्राप्त करें (Get Kundali)",
    btn_submitting: "वैदिक गणना प्रगति पर है...",
    report_title: "विस्तृत जन्म पत्रिका रिपोर्ट",
    btn_print: "प्रिंट / PDF सहेजें",
    tab_charts: "कुंडली चक्र",
    tab_avakhada: "अवकहड़ा चक्र",
    tab_planets: "ग्रह स्थिति",
    tab_houses: "भाव विचार",
    tab_dasha: "विंशोत्तरी दशा",
    tab_doshas: "दोष एवं योग",
    chart_d1: "लग्न कुंडली (D1)",
    chart_d9: "नवमांश कुंडली (D9)",
    chart_chandra: "चंद्र कुंडली (Chandra)",
    chart_south: "दक्षिण भारतीय (South)",
    tbl_planet: "ग्रह (Planet)",
    tbl_motion: "गति",
    tbl_sign: "राशि (Sign)",
    tbl_deg: "अंश कला विकला (DMS)",
    tbl_nak: "नक्षत्र (पद)",
    tbl_house: "भाव (House)",
    tbl_avastha: "अवस्था (Avastha)",
    tbl_dignity: "स्थिति (Dignity)",
    th_lord: "महादशा स्वामी",
    th_start: "प्रारंभ तिथि",
    th_end: "समाप्ति तिथि",
    th_dur: "अवधि (वर्ष)",
    th_status: "स्थिति",
    active_badge: "वर्तमान सक्रिय",
    birth_badge: "जन्म कालीन",
    none_text: "कोई नहीं (रिक्त)",
    lord_label: "भावेश (स्वामी):",
    planets_in_house: "स्थित ग्रह:",
    house_prefix: "भाव",
  },
  en: {
    brand_title: "Vedic Kundali",
    site_title: "Vedic Janam Kundali (Birth Chart)",
    site_tagline: "Authentic Vedic Birth Chart with Lahiri Ayanamsa, 12 Houses & Vimshottari Mahadasha",
    nav_kundli: "📜 Kundli (Birth Chart)",
    nav_matching: "💍 Kundli Matching",
    nav_lagna: "🌅 Lagna (Ascendant)",
    nav_dasha: "⌛ Vimshottari Dasha",
    nav_nakshatra: "✨ Nakshatra Finder",
    nav_manglik: "🔥 Manglik Dosha",
    nav_sade_sati: "🪐 Sade Sati Report",
    nav_panchang: "📅 Vedic Panchang",
    bc_home: "Home",
    bc_astro: "Astrology",
    bc_current: "Vedic Birth Chart (Kundli)",
    form_title: "Enter Birth Details",
    lbl_name: "Full Name*",
    ph_name: "Enter your name (e.g. Rohit Sharma)",
    lbl_gender: "Gender*",
    lbl_male: "Male",
    lbl_female: "Female",
    lbl_other: "Other",
    lbl_dob: "Date of Birth*",
    lbl_tob: "Time of Birth*",
    lbl_pob: "Place of Birth*",
    ph_pob: "e.g. New Delhi, Mumbai, Varanasi, London...",
    pob_help: "Type city name and select from list (Latitude & Longitude will auto-fill).",
    btn_submit: "Generate Kundli / Birth Chart",
    btn_submitting: "Calculating Vedic Positions...",
    report_title: "Comprehensive Vedic Kundli Report",
    btn_print: "Print / Save PDF",
    tab_charts: "Kundali Charts",
    tab_avakhada: "Avakhada Chakra",
    tab_planets: "Planetary Positions",
    tab_houses: "12 Houses Analysis",
    tab_dasha: "Vimshottari Dasha",
    tab_doshas: "Doshas & Yogas",
    chart_d1: "Lagna Chart (D1)",
    chart_d9: "Navamsha (D9)",
    chart_chandra: "Moon Chart (Chandra)",
    chart_south: "South Indian Chart",
    tbl_planet: "Planet",
    tbl_motion: "Motion",
    tbl_sign: "Sign (Rashi)",
    tbl_deg: "Degree (DMS)",
    tbl_nak: "Nakshatra (Pada)",
    tbl_house: "House",
    tbl_avastha: "Avastha (State)",
    tbl_dignity: "Dignity",
    th_lord: "Mahadasha Lord",
    th_start: "Start Date",
    th_end: "End Date",
    th_dur: "Duration (Yrs)",
    th_status: "Status",
    active_badge: "Currently Active",
    birth_badge: "Active at Birth",
    none_text: "None (Empty)",
    lord_label: "House Lord:",
    planets_in_house: "Residing Planets:",
    house_prefix: "House",
  }
};

let currentLang = localStorage.getItem("site_lang") || "hi";

document.addEventListener("DOMContentLoaded", function () {
  const kundliForm = document.getElementById("kundliForm");
  const placeInput = document.getElementById("place_name");
  const placeDropdown = document.getElementById("placeDropdown");
  const placeSpinner = document.getElementById("placeSpinner");
  const latInput = document.getElementById("latitude");
  const lonInput = document.getElementById("longitude");
  const tzInput = document.getElementById("timezone");
  const submitBtn = document.getElementById("submitBtn");
  const formAlert = document.getElementById("formAlert");
  const printBtn = document.getElementById("printBtn");

  let searchTimeout = null;
  let currentPlaces = [];

  // ==========================================
  // Language Switcher Initialization
  // ==========================================
  function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem("site_lang", lang);
    document.documentElement.lang = lang;

    // Toggle button active class
    document.querySelectorAll("[data-set-lang]").forEach((b) => {
      if (b.getAttribute("data-set-lang") === lang) {
        b.classList.add("active");
      } else {
        b.classList.remove("active");
      }
    });

    // Translate DOM elements
    const dict = I18N[lang] || I18N["hi"];
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });

    // Update input placeholders
    if (placeInput && dict["ph_pob"]) {
      placeInput.placeholder = dict["ph_pob"];
    }
    const nameInput = document.getElementById("name");
    if (nameInput && dict["ph_name"]) {
      nameInput.placeholder = dict["ph_name"];
    }

    // Re-render chart and reports with new language
    const activeChartBtn = document.querySelector(".chart-switch-btn.active");
    const activeChartType = activeChartBtn ? activeChartBtn.getAttribute("data-chart") : "d1";
    renderChart(activeChartType);

    if (currentKundliData) {
      updateDOMWithKundliData(currentKundliData);
    }
  }

  // Hook up language toggle buttons
  document.querySelectorAll("[data-set-lang]").forEach((btn) => {
    btn.addEventListener("click", function () {
      const selectedLang = this.getAttribute("data-set-lang");
      setLanguage(selectedLang);
    });
  });

  // Apply saved language on load
  if (currentLang !== "hi") {
    setLanguage(currentLang);
  }

  // Mobile Navbar Hamburger Toggle
  const navToggle = document.getElementById("navbarToggle");
  const navMenu = document.getElementById("navbarMenu");
  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      navMenu.classList.toggle("show");
    });
    navMenu.querySelectorAll(".navbar-link").forEach((link) => {
      link.addEventListener("click", () => navMenu.classList.remove("show"));
    });
  }

  // ==========================================
  // OpenStreetMap Nominatim Place Search
  // ==========================================
  if (placeInput) {
    placeInput.addEventListener("input", function (e) {
      const query = e.target.value.trim();
      clearTimeout(searchTimeout);

      if (query.length < 2) {
        hidePlaceDropdown();
        return;
      }

      showSpinner(true);
      searchTimeout = setTimeout(() => {
        fetchPlaces(query);
      }, 350);
    });

    document.addEventListener("click", function (e) {
      if (!placeInput.contains(e.target) && !placeDropdown.contains(e.target)) {
        hidePlaceDropdown();
      }
    });

    placeInput.addEventListener("keydown", function (e) {
      const items = placeDropdown.querySelectorAll(".autocomplete-item");
      if (!items.length) return;

      let activeIndex = -1;
      items.forEach((item, idx) => {
        if (item.classList.contains("highlighted")) activeIndex = idx;
      });

      if (e.key === "ArrowDown") {
        e.preventDefault();
        const next = (activeIndex + 1) % items.length;
        highlightItem(items, next);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        const prev = (activeIndex - 1 + items.length) % items.length;
        highlightItem(items, prev);
      } else if (e.key === "Enter" && activeIndex >= 0) {
        e.preventDefault();
        selectPlace(currentPlaces[activeIndex]);
      }
    });
  }

  function fetchPlaces(query) {
    fetch(`/api/search-place?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => {
        showSpinner(false);
        if (data && data.length) {
          renderPlaces(data);
        } else {
          fallbackNominatim(query);
        }
      })
      .catch((err) => {
        console.warn("Proxy search failed, trying fallback Nominatim:", err);
        fallbackNominatim(query);
      });
  }

  function fallbackNominatim(query) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
      query
    )}&limit=6&accept-language=hi,en`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        showSpinner(false);
        const mapped = data.map((item) => ({
          name: item.display_name,
          lat: parseFloat(item.lat),
          lon: parseFloat(item.lon),
          timezone: "Asia/Kolkata",
        }));
        renderPlaces(mapped);
      })
      .catch(() => {
        showSpinner(false);
        hidePlaceDropdown();
      });
  }

  function renderPlaces(places) {
    currentPlaces = places;
    placeDropdown.innerHTML = "";

    if (!places.length) {
      hidePlaceDropdown();
      return;
    }

    places.forEach((place) => {
      const item = document.createElement("div");
      item.className = "autocomplete-item";
      item.textContent = place.name;
      item.addEventListener("click", () => selectPlace(place));
      placeDropdown.appendChild(item);
    });

    placeDropdown.classList.add("active");
  }

  function selectPlace(place) {
    placeInput.value = place.name;
    latInput.value = place.lat;
    lonInput.value = place.lon;
    if (tzInput && place.timezone) {
      tzInput.value = place.timezone;
    }
    clearFieldError("place_name");
    hidePlaceDropdown();
  }

  function highlightItem(items, index) {
    items.forEach((item, idx) => {
      if (idx === index) {
        item.classList.add("highlighted");
        item.scrollIntoView({ block: "nearest" });
      } else {
        item.classList.remove("highlighted");
      }
    });
  }

  function hidePlaceDropdown() {
    if (placeDropdown) {
      placeDropdown.classList.remove("active");
      placeDropdown.innerHTML = "";
    }
  }

  function showSpinner(show) {
    if (placeSpinner) {
      placeSpinner.style.display = show ? "inline-block" : "none";
    }
  }

  // ==========================================
  // Friendly Validation System
  // ==========================================
  function setFieldError(fieldId, message) {
    const errorEl = document.getElementById(`${fieldId}_error`);
    const inputEl = document.getElementById(fieldId);
    if (errorEl) {
      errorEl.textContent = message;
      errorEl.style.display = "block";
    }
    if (inputEl) {
      inputEl.classList.add("input-error");
      inputEl.setAttribute("aria-invalid", "true");
    }
  }

  function clearFieldError(fieldId) {
    const errorEl = document.getElementById(`${fieldId}_error`);
    const inputEl = document.getElementById(fieldId);
    if (errorEl) {
      errorEl.textContent = "";
      errorEl.style.display = "none";
    }
    if (inputEl) {
      inputEl.classList.remove("input-error");
      inputEl.removeAttribute("aria-invalid");
    }
  }

  function clearAllErrors() {
    ["name", "birth_date", "birth_time", "place_name"].forEach((id) => clearFieldError(id));
    if (formAlert) {
      formAlert.style.display = "none";
      formAlert.textContent = "";
    }
  }

  // Input event clear errors
  ["name", "birth_date", "birth_time", "place_name"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", () => clearFieldError(id));
    }
  });

  // ==========================================
  // Print Handler
  // ==========================================
  if (printBtn) {
    printBtn.addEventListener("click", function () {
      window.print();
    });
  }

  // ==========================================
  // Form Submit & AJAX Calculation
  // ==========================================
  if (kundliForm) {
    kundliForm.addEventListener("submit", function (e) {
      e.preventDefault();
      clearAllErrors();

      const name = document.getElementById("name").value.trim();
      const gender = (document.querySelector('input[name="gender"]:checked') || {}).value || "पुरुष";
      const birthDate = document.getElementById("birth_date").value;
      const birthTime = document.getElementById("birth_time").value;
      const placeName = placeInput.value.trim();
      const lat = parseFloat(latInput.value);
      const lon = parseFloat(lonInput.value);
      const tz = tzInput ? tzInput.value : "Asia/Kolkata";

      let hasError = false;

      if (!name) {
        setFieldError("name", currentLang === "en" ? "Please enter your name." : "कृपया अपना नाम भरें (उदा. राहुल वर्मा)।");
        hasError = true;
      }

      if (!birthDate) {
        setFieldError("birth_date", currentLang === "en" ? "Please choose your date of birth." : "कृपया जन्म तिथि चुनें (उदा. 15-05-1995)।");
        hasError = true;
      }

      if (!birthTime) {
        setFieldError("birth_time", currentLang === "en" ? "Please enter your birth time." : "कृपया जन्म समय दर्ज करें (उदा. 10:30 पूर्वाह्न/अपराह्न)।");
        hasError = true;
      }

      if (!placeName || isNaN(lat) || isNaN(lon)) {
        setFieldError("place_name", currentLang === "en" ? "Please search and pick a birth city from suggestions." : "कृपया स्थान का नाम खोजें और सूची में से चयन करें ताकि सटीक अक्षांश/देशांतर भरे जा सकें।");
        hasError = true;
      }

      if (hasError) return;

      submitBtn.disabled = true;
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.innerHTML = `<span>⏳ ${I18N[currentLang].btn_submitting}</span>`;

      const payload = {
        name: name,
        gender: gender,
        birth_date: birthDate,
        birth_time: birthTime,
        place_name: placeName,
        latitude: lat,
        longitude: lon,
        timezone: tz,
      };

      fetch("/api/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((res) => res.json())
        .then((response) => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;

          if (!response.success) {
            if (response.error_field) {
              setFieldError(response.error_field, response.message);
            } else if (formAlert) {
              formAlert.style.display = "block";
              formAlert.textContent = response.message || "गणना में त्रुटि उत्पन्न हुई।";
            }
            return;
          }

          updateDOMWithKundliData(response.data);

          const chartSection = document.getElementById("kundliResultsContainer");
          if (chartSection) {
            chartSection.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        })
        .catch((err) => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
          if (formAlert) {
            formAlert.style.display = "block";
            formAlert.textContent = currentLang === "en" ? "Unable to connect to calculation engine. Please retry." : "सर्वर से संपर्क करने में असमर्थ। कृपया पुनः प्रयास करें।";
          }
          console.error("Calculation fetch error:", err);
        });
    });
  }

  // ==========================================
  // In-Memory Chart Cache & Tab Switching
  // ==========================================
  let currentKundliData = window.INITIAL_KUNDLI_DATA || null;

  // Report Tab Switching
  document.querySelectorAll(".report-tab-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const tabId = this.getAttribute("data-tab");
      document.querySelectorAll(".report-tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".report-tab-panel").forEach((p) => p.classList.remove("active"));
      this.classList.add("active");
      const targetPanel = document.getElementById(tabId);
      if (targetPanel) targetPanel.classList.add("active");
    });
  });

  // Chart Switcher (D1, D9, Chandra, South)
  document.querySelectorAll(".chart-switch-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const chartType = this.getAttribute("data-chart");
      document.querySelectorAll(".chart-switch-btn").forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
      renderChart(chartType);
    });
  });

  function renderChart(type) {
    const container = document.getElementById("kundliSvgContainer");
    if (!container || !currentKundliData) return;
    const isEn = (currentLang === "en");

    if (type === "d1") {
      container.innerHTML = (isEn && currentKundliData.chart_svg_en) ? currentKundliData.chart_svg_en : (currentKundliData.chart_svg || "");
    } else if (type === "d9") {
      container.innerHTML = (isEn && currentKundliData.navamsha_chart_svg_en) ? currentKundliData.navamsha_chart_svg_en : (currentKundliData.navamsha_chart_svg || "");
    } else if (type === "chandra") {
      container.innerHTML = (isEn && currentKundliData.chandra_chart_svg_en) ? currentKundliData.chandra_chart_svg_en : (currentKundliData.chandra_chart_svg || "");
    } else if (type === "south") {
      container.innerHTML = (isEn && currentKundliData.south_chart_svg_en) ? currentKundliData.south_chart_svg_en : (currentKundliData.south_chart_svg || "");
    }
  }

  // ==========================================
  // Update DOM with Complete Kundali Data
  // ==========================================
  function updateDOMWithKundliData(data) {
    currentKundliData = data;
    const isEn = (currentLang === "en");
    const dict = I18N[currentLang] || I18N["hi"];

    // 1. Render active SVG
    const activeChartBtn = document.querySelector(".chart-switch-btn.active");
    const activeChartType = activeChartBtn ? activeChartBtn.getAttribute("data-chart") : "d1";
    renderChart(activeChartType);

    // 2. Update Quick Details
    const rashiName = isEn ? (data.lagna.rashi.name_en || data.lagna.rashi.name_hi) : data.lagna.rashi.name_hi;
    updateText("val_lagna", `${rashiName} (${data.lagna.deg_dms})`);
    updateText("val_moon_rashi", data.panchang.moon_rashi);
    updateText("val_nakshatra", data.panchang.nakshatra);
    updateText("val_ayanamsa", data.ayanamsa.formatted);

    // 3. Update Avakhada Chakra & Natal Panchang
    if (data.avakhada) {
      updateText("val_varna", data.avakhada.varna);
      updateText("val_vashya", data.avakhada.vashya);
      updateText("val_tatva", data.avakhada.tatva);
      updateText("val_paya", data.avakhada.paya);
      updateText("val_gana", data.avakhada.gana);
      updateText("val_nadi", data.avakhada.nadi);
      updateText("val_syllable", data.avakhada.syllable);
      updateText("val_deity", data.avakhada.deity);
      updateText("val_symbol", data.avakhada.symbol);
    }

    updateText("val_user_name_2", data.user_info.name);
    updateText("val_birth_datetime_2", `${data.user_info.birth_date_local}, ${data.user_info.birth_time_local}`);
    updateText("val_place_name_2", data.user_info.place_name || placeInput.value);
    updateText("val_tithi_2", data.panchang.tithi);
    updateText("val_nakshatra_2", data.panchang.nakshatra);
    updateText("val_nakshatra_lord_2", data.panchang.nakshatra_lord);
    updateText("val_sun_rashi_2", data.panchang.sun_rashi);
    updateText("val_moon_rashi_2", data.panchang.moon_rashi);

    // 4. Update Print Header Details
    updateText("print_user_name", isEn ? `${data.user_info.name}'s Janam Kundali` : `${data.user_info.name} की जन्म कुंडली`);
    updateText("print_birth_details", `${data.user_info.birth_date_local} | ${data.user_info.birth_time_local} | ${data.user_info.place_name || placeInput.value}`);
    updateText("print_lagna_details", `Lagna: ${rashiName} (${data.lagna.deg_dms}) | Nakshatra: ${data.panchang.nakshatra} | Ayanamsa: ${data.ayanamsa.formatted}`);

    // 5. Update Graha Sthiti & Avasthas Table
    const grahaTableBody = document.getElementById("grahaTableBody");
    if (grahaTableBody && data.grahas) {
      grahaTableBody.innerHTML = "";
      data.grahas.forEach((g) => {
        const row = document.createElement("tr");
        const gName = isEn ? (g.name_en || g.name_hi) : g.name_hi;
        const rName = isEn ? (g.rashi.name_en || g.rashi.name_hi) : g.rashi.name_hi;
        const nakName = isEn ? (g.nakshatra.name_en || g.nakshatra.name_hi) : g.nakshatra.name_hi;
        const houseLabel = isEn ? `House ${g.house_num}` : `भाव ${g.house_num}`;

        let retroBadge;
        if (g.is_retrograde) {
          retroBadge = `<span class="badge badge-retro">${isEn ? "Retro" : "वक्री"}</span>`;
        } else {
          retroBadge = `<span class="badge badge-direct">${isEn ? "Direct" : "मार्गी"}</span>`;
        }

        row.innerHTML = `
          <td><strong>${gName}</strong></td>
          <td>${retroBadge}</td>
          <td>${g.rashi.symbol || ""} ${rName} (${g.rashi.id})</td>
          <td>${g.dms_str}</td>
          <td>${nakName} (${g.pada})</td>
          <td><strong>${houseLabel}</strong></td>
          <td><span style="font-size: 0.88rem;">${g.avastha || "—"}</span></td>
          <td><strong>${g.dignity || "—"}</strong></td>
        `;
        grahaTableBody.appendChild(row);
      });
    }

    // 6. Update 12 Houses Grid
    const housesGrid = document.getElementById("housesGridContainer");
    if (housesGrid && data.houses) {
      housesGrid.innerHTML = "";
      data.houses.forEach((h) => {
        const card = document.createElement("div");
        card.className = "house-item-card";

        let houseTitle = `${dict.house_prefix} ${h.house_num}`;
        let houseDesc = "";
        if (h.significance) {
          if (typeof h.significance === "object") {
            houseTitle = isEn ? (h.significance.name_en || h.significance.name_hi) : h.significance.name_hi;
            houseDesc = isEn ? (h.significance.desc_en || h.significance.desc_hi) : h.significance.desc_hi;
          } else {
            houseTitle = h.significance;
          }
        }

        const rashiSign = isEn ? (h.rashi.name_en || h.rashi.name_hi) : h.rashi.name_hi;
        const lordName = isEn ? (h.rashi.lord_en || h.rashi_lord) : h.rashi_lord;

        let grahaHtml = `<span style="color: var(--text-muted);">${dict.none_text}</span>`;
        if (h.grahas && h.grahas.length) {
          grahaHtml = h.grahas
            .map((g) => {
              const retro = g.is_retrograde && g.id !== "rahu" && g.id !== "ketu" ? (isEn ? " (R)" : " (व)") : "";
              const gAbbr = isEn ? (g.short_en || g.short_hi) : g.short_hi;
              return `<span style="display: inline-block; background: var(--bg-card-alt); border: 1px solid var(--gold-border); padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 600; margin-right: 4px; font-size: 0.85rem;">${gAbbr}${retro}</span>`;
            })
            .join("");
        }

        card.innerHTML = `
          <div class="house-item-header">
            <span class="house-item-title">${houseTitle}</span>
            <span class="house-rashi-badge">${rashiSign} (${h.rashi.id})</span>
          </div>
          <div style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 0.4rem;">
            ${dict.lord_label} <strong>${lordName}</strong>
          </div>
          <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">
            <strong>${dict.planets_in_house}</strong> ${grahaHtml}
          </div>
          <p style="font-size: 0.85rem; color: var(--text-secondary); margin: 0; line-height: 1.5;">
            ${houseDesc}
          </p>
        `;
        housesGrid.appendChild(card);
      });
    }

    // 7. Update Vimshottari Dasha Table
    const dashaTableBody = document.getElementById("dashaTableBody");
    if (dashaTableBody && data.dasha && data.dasha.cycle) {
      updateText("dasha_nak_val", data.panchang.nakshatra);
      updateText("dasha_bal_val", data.dasha.balance_years_at_birth);
      dashaTableBody.innerHTML = "";
      data.dasha.cycle.forEach((d) => {
        const row = document.createElement("tr");
        if (d.is_active) row.className = "active-dasha-row";

        const statusBadge = d.is_active
          ? `<span class="badge badge-active">${dict.active_badge}</span>`
          : (d.is_birth ? `<span class="badge" style="background:#E2D9CC;color:#4A4036">${dict.birth_badge}</span>` : `—`);

        const dLord = isEn ? `${d.lord_en} (${d.lord_hi})` : `${d.lord_hi} (${d.lord_en})`;

        row.innerHTML = `
          <td><strong>${dLord}</strong></td>
          <td>${d.balance_years_formatted}</td>
          <td>${d.start_date}</td>
          <td>${d.end_date}</td>
          <td>${statusBadge}</td>
        `;
        dashaTableBody.appendChild(row);
      });
    }

    // 8. Update Dosha & Yoga Section
    if (data.manglik) {
      const mBadge = document.getElementById("manglikBadge");
      if (mBadge) {
        mBadge.className = data.manglik.is_manglik ? "dosha-badge badge-danger" : "dosha-badge badge-success";
        mBadge.style.backgroundColor = data.manglik.is_manglik ? "#C62828" : "#2E7D32";
        mBadge.textContent = data.manglik.is_manglik ? (isEn ? "Manglik Dosha Present" : "मांगलिक दोष उपस्थित") : (isEn ? "No Manglik Dosha" : "मांगलिक दोष मुक्त");
      }
      updateText("manglikDetails", data.manglik.details);
      updateText("manglikCancellation", data.manglik.cancellation_reasons || (isEn ? "No cancellation applicable." : "कोई परिहार लागू नहीं।"));
    }

    if (data.kalsarp) {
      const kBadge = document.getElementById("kalsarpBadge");
      if (kBadge) {
        kBadge.className = data.kalsarp.has_dosha ? "dosha-badge badge-warning" : "dosha-badge badge-success";
        kBadge.style.backgroundColor = data.kalsarp.has_dosha ? "#C57B12" : "#2E7D32";
        kBadge.textContent = data.kalsarp.has_dosha ? (data.kalsarp.yoga_name || (isEn ? "Kalsarp Present" : "कालसर्प योग उपस्थित")) : (isEn ? "No Kalsarp Yoga" : "कालसर्प योग मुक्त");
      }
      updateText("kalsarpDesc", data.kalsarp.description);
    }

    if (data.sade_sati) {
      const sBadge = document.getElementById("sadeSatiBadge");
      if (sBadge) {
        sBadge.className = data.sade_sati.has_sade_sati ? "dosha-badge badge-warning" : "dosha-badge badge-success";
        sBadge.style.backgroundColor = data.sade_sati.has_sade_sati ? "#1B263B" : "#2E7D32";
        sBadge.textContent = data.sade_sati.status;
      }
      updateText("sadeSatiDesc", data.sade_sati.description);
      updateText("sadeSatiTransit", data.sade_sati.current_saturn_transit);
    }
  }

  function updateText(elementId, text) {
    const el = document.getElementById(elementId);
    if (el && text !== undefined && text !== null) {
      el.textContent = text;
    }
  }

  // Pre-load initial chart into memory
  if (window.INITIAL_KUNDLI_DATA) {
    updateDOMWithKundliData(window.INITIAL_KUNDLI_DATA);
  }
});
