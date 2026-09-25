/* =========================================================
   DIGITAL LIFE — assessment logic
   No loading animation: submit -> real API call -> result.
   ========================================================= */

const API_URL = "https://social-media-impact-3.onrender.com";

const SECTION_IDS = ["sec-profile", "sec-habits", "sec-sleep", "sec-academic"];

const els = {
  navToggle: document.getElementById("navToggle"),
  mobileMenu: document.getElementById("mobileMenu"),
  form: document.getElementById("assessmentForm"),
  assessmentSection: document.getElementById("assessment"),
  resultSection: document.getElementById("result"),
  errorSection: document.getElementById("errorState"),
  resultClassification: document.getElementById("resultClassification"),
  resultMessage: document.getElementById("resultMessage"),
  resultVisual: document.getElementById("resultVisual"),
  insightsList: document.getElementById("insightsList"),
  restartBtn: document.getElementById("restartBtn"),
  retryBtn: document.getElementById("retryBtn"),
  progressDots: Array.from(document.querySelectorAll(".progress-dot")),
};

/* ---------------- Mobile nav ---------------- */

els.navToggle.addEventListener("click", () => {
  const isOpen = els.mobileMenu.classList.toggle("is-open");
  els.navToggle.setAttribute("aria-expanded", String(isOpen));
});

document.querySelectorAll(".mobile-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    els.mobileMenu.classList.remove("is-open");
    els.navToggle.setAttribute("aria-expanded", "false");
  });
});

/* ---------------- Slider live values ---------------- */

document.querySelectorAll('input[type="range"]').forEach((slider) => {
  const out = document.getElementById(`val-${slider.id}`);
  if (out) {
    slider.addEventListener("input", () => {
      out.textContent = slider.value;
    });
  }
});

/* ---------------- Section navigation ---------------- */

function showSection(targetId) {
  SECTION_IDS.forEach((id) => {
    document.getElementById(id).classList.toggle("is-active", id === targetId);
  });
  els.progressDots.forEach((dot) => {
    const active = dot.dataset.target === targetId;
    dot.classList.toggle("is-active", active);
    dot.setAttribute("aria-selected", String(active));
  });
  document.getElementById(targetId).scrollIntoView({ behavior: "smooth", block: "start" });
}

document.querySelectorAll("[data-next]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const currentSection = btn.closest(".form-section");
    if (!validateSection(currentSection)) return;
    showSection(btn.dataset.next);
  });
});

document.querySelectorAll("[data-prev]").forEach((btn) => {
  btn.addEventListener("click", () => {
    showSection(btn.dataset.prev);
  });
});

els.progressDots.forEach((dot) => {
  dot.addEventListener("click", () => showSection(dot.dataset.target));
});

/* ---------------- Validation ---------------- */

function fieldLabel(el) {
  const label = document.querySelector(`label[for="${el.id}"]`);
  return label ? label.textContent.trim() : el.name;
}

function setFieldError(name, message) {
  const errorEl = document.querySelector(`.field-error[data-for="${name}"]`);
  if (errorEl) errorEl.textContent = message || "";
}

function validateSection(sectionEl) {
  let valid = true;
  const inputs = sectionEl.querySelectorAll("input, select");
  const seenRadioGroups = new Set();

  inputs.forEach((input) => {
    if (input.type === "radio") {
      if (seenRadioGroups.has(input.name)) return;
      seenRadioGroups.add(input.name);
      const checked = sectionEl.querySelector(`input[name="${input.name}"]:checked`);
      if (!checked) {
        setFieldError(input.name, "Please choose one.");
        valid = false;
      } else {
        setFieldError(input.name, "");
      }
      return;
    }

    if (input.type === "range") {
      setFieldError(input.name, "");
      return;
    }

    if (!input.value || (input.hasAttribute("required") && input.value === "")) {
      setFieldError(input.name, `${fieldLabel(input)} is required.`);
      valid = false;
      return;
    }

    if (input.type === "number") {
      const num = parseFloat(input.value);
      const min = input.min !== "" ? parseFloat(input.min) : -Infinity;
      const max = input.max !== "" ? parseFloat(input.max) : Infinity;
      if (Number.isNaN(num) || num < min || num > max) {
        setFieldError(input.name, `Enter a value between ${input.min} and ${input.max}.`);
        valid = false;
        return;
      }
    }

    setFieldError(input.name, "");
  });

  return valid;
}

function validateForm() {
  let valid = true;
  SECTION_IDS.forEach((id) => {
    const section = document.getElementById(id);
    if (!validateSection(section)) valid = false;
  });
  return valid;
}

/* ---------------- Collect payload ---------------- */

function collectFormData() {
  const lateNight = document.querySelector('input[name="Late_Night_Usage"]:checked');

  return {
    Age: parseInt(document.getElementById("Age").value, 10),
    Gender: document.getElementById("Gender").value,
    Academic_Level: document.getElementById("Academic_Level").value,
    Primary_Platform: document.getElementById("Primary_Platform").value,
    Daily_Usage_Hours: parseFloat(document.getElementById("Daily_Usage_Hours").value),
    Weekend_Extra_Hours: parseFloat(document.getElementById("Weekend_Extra_Hours").value),
    Device_Type: document.getElementById("Device_Type").value,
    Sleep_Duration_Hours: parseFloat(document.getElementById("Sleep_Duration_Hours").value),
    Sleep_Quality_Score: parseInt(document.getElementById("Sleep_Quality_Score").value, 10),
    Late_Night_Usage: lateNight ? lateNight.value : "No",
    Social_Comparison_Frequency: document.getElementById("Social_Comparison_Frequency").value,
    Perceived_Stress_Score: parseFloat(document.getElementById("Perceived_Stress_Score").value),
    Mental_Health_Index: parseInt(document.getElementById("Mental_Health_Index").value, 10),
    Academic_Performance_GPA: parseFloat(document.getElementById("Academic_Performance_GPA").value),
  };
}

/* ---------------- Result content per classification ---------------- */

const RESULT_CONTENT = {
  Beneficial: {
    colorA: "#7ce8b0",
    colorB: "#63e6e2",
    message: "Your digital habits appear to be working well for you.",
    visual: () => `
      <svg viewBox="0 0 200 200" width="100%" height="100%">
        <circle cx="100" cy="100" r="70" fill="none" stroke="#7ce8b0" stroke-width="1" opacity="0.25"/>
        <circle cx="100" cy="100" r="52" fill="none" stroke="#7ce8b0" stroke-width="1.4" opacity="0.4"/>
        <polyline points="55,120 80,95 100,108 130,68 150,80" fill="none" stroke="#7ce8b0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="150" cy="80" r="5" fill="#7ce8b0"/>
        <circle cx="60" cy="60" r="2" fill="#63e6e2" opacity="0.8"/>
        <circle cx="145" cy="140" r="2.4" fill="#63e6e2" opacity="0.7"/>
      </svg>`,
  },
  Neutral: {
    colorA: "#b9a6ff",
    colorB: "#8ca3ff",
    message: "Your digital habits show a mixed pattern.",
    visual: () => `
      <svg viewBox="0 0 200 200" width="100%" height="100%">
        <line x1="60" y1="90" x2="140" y2="90" stroke="#b9a6ff" stroke-width="2.4" stroke-linecap="round"/>
        <line x1="100" y1="90" x2="100" y2="60" stroke="#b9a6ff" stroke-width="2.4" stroke-linecap="round"/>
        <circle cx="60" cy="100" r="14" fill="none" stroke="#b9a6ff" stroke-width="2.2"/>
        <circle cx="140" cy="100" r="14" fill="none" stroke="#b9a6ff" stroke-width="2.2"/>
        <circle cx="100" cy="54" r="4" fill="#b9a6ff"/>
        <line x1="100" y1="128" x2="100" y2="148" stroke="#8ca3ff" stroke-width="2" stroke-linecap="round"/>
      </svg>`,
  },
  Negative: {
    colorA: "#f5b377",
    colorB: "#f5d1a0",
    message: "Some of your digital habits may deserve a closer look.",
    visual: () => `
      <svg viewBox="0 0 200 200" width="100%" height="100%">
        <rect x="70" y="110" width="60" height="28" rx="8" fill="none" stroke="#f5b377" stroke-width="2"/>
        <circle cx="100" cy="124" r="2" fill="#f5b377"/>
        <path d="M60 90c6-8 10-14 10-14" stroke="#f5b377" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.5"/>
        <path d="M50 70a40 40 0 0 1 30-16" stroke="#f5b377" stroke-width="1.4" fill="none" stroke-linecap="round" opacity="0.35"/>
        <path d="M140 90c-6-8-10-14-10-14" stroke="#f5b377" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.5"/>
        <path d="M150 70a40 40 0 0 0-30-16" stroke="#f5b377" stroke-width="1.4" fill="none" stroke-linecap="round" opacity="0.35"/>
      </svg>`,
  },
};

/* ---------------- Insights ---------------- */

function generateInsights(data) {
  const insights = [];

  if (data.Daily_Usage_Hours >= 6) {
    insights.push("Your daily screen time is on the higher side compared with a typical short-use pattern.");
  } else if (data.Daily_Usage_Hours <= 1.5) {
    insights.push("Your daily screen time is relatively light, which tends to leave more room for other things.");
  }

  if (data.Weekend_Extra_Hours >= 4) {
    insights.push("Your usage climbs noticeably on weekends — worth noticing if that time is coming from rest or plans with people.");
  }

  if (data.Sleep_Duration_Hours < 6) {
    insights.push("Your sleep duration is on the shorter side. A consistent sleep routine may be worth paying attention to.");
  }

  if (data.Sleep_Quality_Score <= 4) {
    insights.push("You rated your sleep quality fairly low — late-screen habits are a common, fixable factor there.");
  }

  if (data.Late_Night_Usage === "Yes") {
    insights.push("You mentioned using platforms late at night, which can quietly chip away at rest over time.");
  }

  if (data.Social_Comparison_Frequency === "Often" || data.Social_Comparison_Frequency === "Always") {
    insights.push("You compare yourself to others online fairly often — a pattern that's worth being gentle with yourself about.");
  }

  if (data.Perceived_Stress_Score >= 7) {
    insights.push("Your perceived stress is on the higher end right now.");
  }

  if (data.Mental_Health_Index <= 4) {
    insights.push("Your self-rated wellbeing is lower than you might want it to be — that's worth talking through with someone you trust.");
  }

  if (data.Academic_Performance_GPA < 5) {
    insights.push("Your academic performance suggests this might be a demanding stretch — habits and workload often move together.");
  }

  if (insights.length === 0) {
    insights.push("Nothing here stands out as a pattern to worry about — your habits look fairly balanced overall.");
  }

  return insights.slice(0, 4);
}

/* ---------------- Show / hide states ---------------- */

function showResult(classification, data) {
  const content = RESULT_CONTENT[classification] || RESULT_CONTENT.Neutral;

  els.resultSection.style.setProperty("--result-a", content.colorA);
  els.resultSection.style.setProperty("--result-b", content.colorB);

  els.resultClassification.textContent = classification;
  els.resultMessage.textContent = content.message;
  els.resultVisual.innerHTML = content.visual();

  els.insightsList.innerHTML = "";
  generateInsights(data).forEach((text) => {
    const li = document.createElement("li");
    li.textContent = text;
    els.insightsList.appendChild(li);
  });

  els.assessmentSection.hidden = true;
  els.errorSection.hidden = true;
  els.resultSection.hidden = false;
  els.resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function showError() {
  els.assessmentSection.hidden = true;
  els.resultSection.hidden = true;
  els.errorSection.hidden = false;
  els.errorSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetAssessment() {
  els.form.reset();
  document.querySelectorAll(".field-error").forEach((el) => (el.textContent = ""));
  document.querySelectorAll('input[type="range"]').forEach((slider) => {
    const out = document.getElementById(`val-${slider.id}`);
    if (out) out.textContent = slider.value;
  });
  showSection("sec-profile");
  els.resultSection.hidden = true;
  els.errorSection.hidden = true;
  els.assessmentSection.hidden = false;
  els.assessmentSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

els.restartBtn.addEventListener("click", resetAssessment);

els.retryBtn.addEventListener("click", () => {
  els.errorSection.hidden = true;
  els.assessmentSection.hidden = false;
  els.assessmentSection.scrollIntoView({ behavior: "smooth", block: "start" });
});

/* ---------------- Submission ---------------- */

async function submitAssessment(event) {
  event.preventDefault();

  console.log("1. Form submitted");

  if (!validateForm()) {
    console.log("Validation failed — staying on form");
    const firstInvalid = els.form.querySelector(".field-error:not(:empty)");
    if (firstInvalid) {
      const section = firstInvalid.closest(".form-section");
      if (section) showSection(section.id);
    }
    return;
  }

  const payload = collectFormData();
  console.log("2. Payload built:", payload);

  const submitBtn = els.form.querySelector(".submit-btn");
  submitBtn.disabled = true;

  try {
    console.log("3. Sending API request to", API_URL);

    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    console.log("4. Response received, status:", response.status);

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    const result = await response.json();
    console.log("5. JSON parsed:", result);

    const prediction = result.predicted_classification;
    console.log("6. Prediction:", prediction);

    if (!prediction || !RESULT_CONTENT[prediction]) {
      throw new Error("predicted_classification missing or unrecognized");
    }

    console.log("7. Rendering result, hiding form");
    showResult(prediction, payload);
    console.log("8. Result displayed");
  } catch (error) {
    console.error("Prediction error:", error);
    showError();
  } finally {
    submitBtn.disabled = false;
  }
}

els.form.addEventListener("submit", submitAssessment);

/* ---------------- Init ---------------- */

showSection("sec-profile");