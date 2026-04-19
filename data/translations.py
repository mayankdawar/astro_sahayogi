"""Internationalization: English/Hindi UI translations and helper functions."""

from astro_sahayogi.data.constants import ZODIAC, HINDI_ZODIAC, NAKSHATRAS, HINDI_NAKSHATRAS, HINDI_PLANETS

# Master UI translation dictionary (English -> Hindi)
UI_TRANS = {
    "Planetary Positions": "ग्रह स्थिति",
    "Cusp Positions": "भाव स्थिति",
    "Nadi Significators": "नाड़ी कारक",
    "Vimshottari Dasha (5 Levels)": "विंशोत्तरी दशा (5 स्तर)",
    "Live Ruling Planets (RP)": "तात्कालिक शासक ग्रह (RP)",
    "Planet": "ग्रह", "Sign": "राशि", "Degree": "अंश",
    "Nakshatra": "नक्षत्र", "Star Lord": " नक्षत्र स्वा.",
    "Sub Lord": "उप स्वा.", "S-Sub": "उप-उप",
    "Star": "नक्षत्र", "Sub": "उप", "S-Sub Lord": "उप-उप स्वा.",
    "House": "भाव", "P-Signifs": "ग्रह कारक",
    "St-Signifs": "नक्षत्र कारक", "Sb-Signifs": "उप कारक",
    "In Sign": "राशि में", "Dasha Lord": "दशा स्वामी",
    "Start Date": "आरंभ तिथि", "End Date": "अंत तिथि",
    "Sign L": "राशि स्वा.", "Star L": "नक्षत्र स्वा.",
    "Sub L": "उप स्वा.", "Day Lord": "दिन स्वामी",
    "Lagna": "लग्न", "Moon": "चन्द्र",
    "Time:": "समय:", "Balance:": "शेष दशा:",
    "Planetary & Cusp Positions": "ग्रह और भाव स्थिति",
    "Revolve to House:": "भाव चक्र:", "Language:": "भाषा:",
    "Options ⚙️": "विकल्प ⚙️", "1-Page Report 📄": "1-पेज रिपोर्ट 📄",
    "Degree Hits ⧉": "डिग्री दृष्टि ⧉",
    "Forward Check 🔎": "आगे की जाँच 🔎",
    "EXIT": "बाहर जाएँ", "⏸ Pause": "⏸ रोकें",
    "▶ Resume": "▶ फिर से शुरू करें",
    "Year": "वर्ष", "Month": "माह", "Week": "सप्ताह",
    "Day": "दिन", "Hour": "घंटा", "10 Min": "10 मिनट",
    "1 Min": "1 मिनट", "1 Sec": "1 सेकंड",
    "Source Planet": "मूल ग्रह", "Target Planet": "लक्षित ग्रह",
    "Aspect Type": "दृष्टि प्रकार", "Exact Diff": "सटीक अंतर",
    "Nature": "प्रकृति", "Target House": "लक्षित भाव",
    "Degree Hits (Planet to Planet)": "डिग्री दृष्टि (ग्रह से ग्रह)",
    "Degree Hits (Planet to House)": "डिग्री दृष्टि (ग्रह से भाव)",
    "Lagna Chart": "लग्न कुण्डली", "Bhava Chalit": "भाव चलित",
    "Native Name": "जातक का नाम", "Date of Birth": "जन्म तिथि",
    "Time of Birth": "जन्म समय", "Place": "स्थान",
    "Coordinates": "निर्देशांक", "Chart Mode": "कुण्डली प्रकार",
    "Dasha Balance": "दशा शेष",
    "KP ASTROLOGY MASTER REPORT DETAILS": "केपी एस्ट्रोलॉजी मास्टर रिपोर्ट विवरण",
    "Positive": "सकारात्मक", "Negative": "नकारात्मक",
    "Neutral": "तटस्थ", "Variable": "पर परिवर्तनशील",
    "Conjunction": "युति", "Semi-Sextile": "अर्ध-षष्टक",
    "Semi-Square": "अर्ध-केन्द्र", "Sextile": "षष्टक",
    "Square": "केन्द्र", "Trine": "त्रिकोण",
    "Quincunx": "षडाष्टक", "Opposition": "समसप्तक",
    "Natal Chart Time:": "जन्म कुण्डली समय:",
    "Horary": "प्रश्न कुण्डली",
    "Progression Time:": "गोचर समय:",
    "Planet 1": "ग्रह 1", "Planet 2": "ग्रह 2",
    "Name:": "नाम:", "DOB:": "जन्म तिथि:",
    "Mode:": "प्रकार:", "Rotated to House:": "भाव चक्र:",
    "Balance of Dasha:": "शेष दशा:",
    "Active Mahadasha:": "सक्रिय महादशा:",
    "--- PLANETARY POSITIONS ---": "--- ग्रह स्थिति ---",
    "--- NIRAYANA CUSPS ---": "--- निरयण भाव ---",
    "--- NADI SIGNIFICATORS ---": "--- नाड़ी कारक ---",
    "--- DEGREE HITS (PLANET TO PLANET) ---": "--- डिग्री दृष्टि (ग्रह से ग्रह) ---",
    "--- DEGREE HITS (PLANET TO HOUSE) ---": "--- डिग्री दृष्टि (ग्रह से भाव) ---",
    "Astro Vastu": "एस्ट्रो वास्तु",
    "Direction": "दिशा", "Zodiac": "राशि", "Lord": "स्वामी",
    "Tatwa": "तत्व", "Mobility": "स्वभाव",
    "Sign No": "राशि क्र.",
    "Properties": "गुण",
    "Planet to Cusp Aspects": "ग्रह से भाव दृष्टि",
    "Planet to Planet Aspects": "ग्रह से ग्रह दृष्टि",
    "House to House Aspects": "भाव से भाव दृष्टि",
    "FROM": "से (ग्रह)", "DIR 1": "दिशा 1",
    "TO": "तक (ग्रह)", "DIR 2": "दिशा 2",
    "ASP": "दृष्टि अंश",
    "Transit": "गोचर",
    "Natal": "जन्म",
    "Vimshottari Dasha (Current & 3 Levels)": "विंशोत्तरी दशा (वर्तमान और 3 स्तर)",
    "Planets To House Aspect": "ग्रह से भाव दृष्टि",
    "House to House Aspects (Medical)": "भाव से भाव दृष्टि (चिकित्सा)",
    "Set Transit": "गोचर सेट करें",
    "Set Horary": "प्रश्न सेट करें",
    "Latitude:": "अक्षांश:",
    "Longitude:": "देशांतर:",
    "Timezone:": "काल क्षेत्र:",
    "Horary #:": "प्रश्न संख्या:",
    "Place:": "स्थान:",
    "Vastu module: use dashboard tools for detailed mapping.":
        "वास्तु विवरण: डैशबोर्ड उपकरणों से पूर्ण मानचित्रण करें।",
}


class I18n:
    """Internationalization helper: thread-safe, standalone (no UI dependency)."""

    def __init__(self, language: str = "English"):
        self._language = language

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, value: str):
        self._language = value

    @property
    def is_hindi(self) -> bool:
        return self._language == "Hindi"

    def t(self, text: str) -> str:
        if self._language == "Hindi":
            return UI_TRANS.get(text, text)
        return text

    def tr_p(self, planet: str) -> str:
        if self._language == "Hindi":
            return HINDI_PLANETS.get(planet, planet)
        return planet

    def tr_z(self, idx: int) -> str:
        if self._language == "Hindi":
            return HINDI_ZODIAC[idx]
        return ZODIAC[idx]

    def tr_n(self, idx: int) -> str:
        if self._language == "Hindi":
            return HINDI_NAKSHATRAS[idx]
        return NAKSHATRAS[idx]
