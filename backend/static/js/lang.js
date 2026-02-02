console.log("✅ lang.js loaded");

let currentLang = localStorage.getItem("lang") || "en";

const translations = {
  en: {
    welcomeTitle: "Your Smart Farming Assistant",
    welcomeDesc: "Integrated guidance and market links for efficient cultivation.",
    navIcon1: "Diagnosis",
    navText1: "Detect Diseases",
    navIcon2: "Guidance",
    navText2: "Crop Roadmap",
    navIcon3: "Market",
    navText3: "Nearby Shops",
    navIcon4: "Support",
    navText4: "Contact / Help",
    toggleBtn: "తెలుగు"
  },
  te: {
    welcomeTitle: "మీ స్మార్ట్ వ్యవసాయ సహాయకుడు",
    welcomeDesc: "సమర్థవంతమైన సాగు కోసం మార్గదర్శనం మరియు మార్కెట్ లింకులు.",
    navIcon1: "పరిశీలన",
    navText1: "వ్యాధులను గుర్తించండి",
    navIcon2: "మార్గదర్శనం",
    navText2: "పంట ప్రణాళిక",
    navIcon3: "మార్కెట్",
    navText3: "దగ్గరలోని దుకాణాలు",
    navIcon4: "సహాయం",
    navText4: "సంప్రదించండి / హెల్ప్",
    toggleBtn: "English"
  }
};

function setLanguage(lang) {
  for (let id in translations[lang]) {
    if (id === "toggleBtn") continue;

    const el = document.getElementById(id);
    if (el) el.innerText = translations[lang][id];
  }

  const btn = document.getElementById("langToggle");
  if (btn) btn.innerText = translations[lang].toggleBtn;

  currentLang = lang;
  localStorage.setItem("lang", lang);
}

function toggleLanguage() {
  setLanguage(currentLang === "en" ? "te" : "en");
}

document.addEventListener("DOMContentLoaded", () => {
  setLanguage(currentLang);

  const btn = document.getElementById("langToggle");
  if (btn) btn.addEventListener("click", toggleLanguage);
});
