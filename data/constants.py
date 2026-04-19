"""Astrological constants: zodiac signs, nakshatras, planets, sign properties, Vimshottari lords/years."""

import swisseph as swe

# Vimshottari dasha lords (in order) and their year durations
LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
YRS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

ZODIAC = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
HINDI_ZODIAC = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]

SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
DAY_LORDS = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]

NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
HINDI_NAKSHATRAS = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"]

# Default planet map (Rahu defaults to MEAN_NODE; toggled at runtime)
PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
    "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
    "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE,
}

HINDI_PLANETS = {
    "Sun": "सूर्य", "Moon": "चन्द्र", "Mars": "मंगल", "Mercury": "बुध",
    "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि", "Rahu": "राहु", "Ketu": "केतु",
}

ASPECT_RULES = {
    "Sun": [7], "Moon": [7], "Mercury": [7], "Venus": [7],
    "Mars": [4, 7, 8], "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10],
    "Rahu": [5, 7, 9], "Ketu": [5, 7, 9],
}

DEGREE_ASPECTS = {
    0: ("Conjunction", "Variable"), 30: ("Semi-Sextile", "Positive"),
    45: ("Semi-Square", "Negative"), 60: ("Sextile", "Positive"),
    90: ("Square", "Negative"), 120: ("Trine", "Positive"),
    135: ("Sesquisquare", "Negative"), 180: ("Opposition", "Negative"),
}

SIGN_PROPS = {
    1:  {"dir": "E/ESE6", "h_dir": "पूर्व/पूर्व-आग्नेय", "tatwa": "Fire", "h_tatwa": "अग्नि", "mob": "Movable", "h_mob": "चर", "gender": "M", "h_gender": "पु"},
    2:  {"dir": "WNW/NW", "h_dir": "पश्चिम-वायव्य/वायव्य", "tatwa": "Earth", "h_tatwa": "पृथ्वी", "mob": "Fixed", "h_mob": "स्थिर", "gender": "F", "h_gender": "स्त्री"},
    3:  {"dir": "NNW", "h_dir": "उत्तर-वायव्य", "tatwa": "Air", "h_tatwa": "वायु", "mob": "Dual", "h_mob": "द्विस्वभाव", "gender": "M", "h_gender": "पु"},
    4:  {"dir": "NNE", "h_dir": "उत्तर-ईशान", "tatwa": "Water", "h_tatwa": "जल", "mob": "Movable", "h_mob": "चर", "gender": "F", "h_gender": "स्त्री"},
    5:  {"dir": "ENE", "h_dir": "पूर्व-ईशान", "tatwa": "Fire", "h_tatwa": "अग्नि", "mob": "Fixed", "h_mob": "स्थिर", "gender": "M", "h_gender": "पु"},
    6:  {"dir": "N", "h_dir": "उत्तर", "tatwa": "Earth", "h_tatwa": "पृथ्वी", "mob": "Dual", "h_mob": "द्विस्वभाव", "gender": "F", "h_gender": "स्त्री"},
    7:  {"dir": "WSW", "h_dir": "पश्चिम-नैऋत्य", "tatwa": "Air", "h_tatwa": "वायु", "mob": "Movable", "h_mob": "चर", "gender": "M", "h_gender": "पु"},
    8:  {"dir": "SSW", "h_dir": "दक्षिण-नैऋत्य", "tatwa": "Water", "h_tatwa": "जल", "mob": "Fixed", "h_mob": "स्थिर", "gender": "F", "h_gender": "स्त्री"},
    9:  {"dir": "NE", "h_dir": "ईशान", "tatwa": "Fire", "h_tatwa": "अग्नि", "mob": "Dual", "h_mob": "द्विस्वभाव", "gender": "M", "h_gender": "पु"},
    10: {"dir": "SSE/S", "h_dir": "दक्षिण-आग्नेय/दक्षिण", "tatwa": "Earth", "h_tatwa": "पृथ्वी", "mob": "Movable", "h_mob": "चर", "gender": "F", "h_gender": "स्त्री"},
    11: {"dir": "W", "h_dir": "पश्चिम", "tatwa": "Air", "h_tatwa": "वायु", "mob": "Fixed", "h_mob": "स्थिर", "gender": "M", "h_gender": "पु"},
    12: {"dir": "ESE7/SE", "h_dir": "पूर्व-आग्नेय/आग्नेय", "tatwa": "Water", "h_tatwa": "जल", "mob": "Dual", "h_mob": "द्विस्वभाव", "gender": "F", "h_gender": "स्त्री"},
}

# Planet abbreviations for chart display
ENG_ABBR = {"Sun": "Sun", "Moon": "Mon", "Mars": "Mar", "Mercury": "Mer", "Jupiter": "Jup", "Venus": "Ven", "Saturn": "Sat", "Rahu": "Rah", "Ketu": "Ket"}
ENG_SHORT_ABBR = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke"}
HINDI_SHORT_ABBR = {"Sun": "सू", "Moon": "चं", "Mars": "मं", "Mercury": "बु", "Jupiter": "गु", "Venus": "शु", "Saturn": "श", "Rahu": "रा", "Ketu": "के"}

# Nadi planet order used in significator calculations
NADI_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

# Ayanamsa identifiers (used in Strategy pattern)
AYANAMSA_LAHIRI = "Chitrapaksha"
AYANAMSA_RAMAN = "Raman"
AYANAMSA_FAGAN = "Fagan"
AYANAMSA_KP_NEW = "K.P. (New)"
AYANAMSA_KP = "K.P."
AYANAMSA_WESTERN = "Western"
AYANAMSA_OPTIONS = [AYANAMSA_LAHIRI, AYANAMSA_RAMAN, AYANAMSA_FAGAN, AYANAMSA_KP_NEW, AYANAMSA_KP, AYANAMSA_WESTERN]

# Default aspect orb
DEFAULT_ORB = 3.0
