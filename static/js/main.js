/**
 * Main Application Utilities
 */

document.addEventListener("DOMContentLoaded", () => {
  // Mobile Nav Toggle
  const mobileToggle = document.querySelector(".mobile-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener("click", () => {
      navMenu.classList.toggle("open");
    });
  }
});

/**
 * Display a toast notification
 * @param {string} message 
 * @param {'success'|'error'|'info'} type 
 */
function showToast(message, type = "info") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${type === "success" ? "✅" : type === "error" ? "❌" : "ℹ️"}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(20px)";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

/**
 * Auto-Rotating Farmer Hero Slideshow
 */
document.addEventListener("DOMContentLoaded", () => {
  const slideshow = document.getElementById("heroSlideshow");
  const slides = document.querySelectorAll(".hero-slide");
  const dots = document.querySelectorAll(".slide-dot");
  const badgeText = document.getElementById("heroBadgeText");

  if (!slideshow || slides.length === 0) return;

  let currentIndex = 0;
  let slideTimer = null;
  const slideInterval = 3800; // 3.8 seconds per slide

  function showSlide(index) {
    if (index >= slides.length) index = 0;
    if (index < 0) index = slides.length - 1;

    slides.forEach((slide, i) => {
      if (i === index) {
        slide.classList.add("active");
      } else {
        slide.classList.remove("active");
      }
    });

    dots.forEach((dot, i) => {
      if (i === index) {
        dot.classList.add("active");
      } else {
        dot.classList.remove("active");
      }
    });

    if (badgeText && slides[index]) {
      const badgeData = slides[index].getAttribute("data-badge");
      if (badgeData) {
        badgeText.textContent = badgeData;
      }
    }

    currentIndex = index;
  }

  window.gotoHeroSlide = function(index) {
    showSlide(index);
    restartTimer();
  };

  function nextSlide() {
    showSlide((currentIndex + 1) % slides.length);
  }

  function startTimer() {
    if (!slideTimer) {
      slideTimer = setInterval(nextSlide, slideInterval);
    }
  }

  function stopTimer() {
    if (slideTimer) {
      clearInterval(slideTimer);
      slideTimer = null;
    }
  }

  function restartTimer() {
    stopTimer();
    startTimer();
  }

  // Pause when hovered, resume on mouse leave
  slideshow.addEventListener("mouseenter", stopTimer);
  slideshow.addEventListener("mouseleave", startTimer);

  // Start auto-rotation
  startTimer();
});

/**
 * Multi-Language Switcher for Indian Regional Languages
 */
function changeWebsiteLanguage(langCode) {
  if (!langCode) return;
  localStorage.setItem("cropyield_selected_lang", langCode);

  // Set Google Translate cookie
  const domain = window.location.hostname;
  document.cookie = `googtrans=/en/${langCode}; path=/;`;
  if (domain && domain !== "localhost" && domain !== "127.0.0.1") {
    document.cookie = `googtrans=/en/${langCode}; domain=.${domain}; path=/;`;
  }

  // Trigger select inside Google Translate widget
  const googleCombo = document.querySelector(".goog-te-combo");
  if (googleCombo) {
    googleCombo.value = langCode;
    googleCombo.dispatchEvent(new Event("change"));
  } else {
    // Reload if widget has not yet initialized
    window.location.reload();
  }

  // Show friendly toast feedback
  const langNames = {
    en: "English",
    hi: "हिन्दी (Hindi)",
    te: "తెలుగు (Telugu)",
    ta: "தமிழ் (Tamil)",
    kn: "ಕನ್ನಡ (Kannada)",
    ml: "മലയാളം (Malayalam)",
    mr: "मराठी (Marathi)",
    gu: "ગુજરાતી (Gujarati)",
    bn: "বাংলা (Bengali)",
    pa: "ਪੰਜਾਬੀ (Punjabi)",
    or: "ଓଡ଼ିଆ (Odia)",
    as: "অসমীয়া (Assamese)",
    ur: "اردو (Urdu)"
  };
  if (typeof showToast === "function") {
    showToast(`🌐 Language switched to ${langNames[langCode] || langCode}`, "success");
  }
}

// Restore saved language on page load
document.addEventListener("DOMContentLoaded", () => {
  const savedLang = localStorage.getItem("cropyield_selected_lang");
  const langSelect = document.getElementById("languageSelect");
  if (savedLang && langSelect) {
    langSelect.value = savedLang;
  }
});

