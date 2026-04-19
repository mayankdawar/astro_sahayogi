"""Planet and aspect color maps for chart rendering and UI."""

PLANET_COLORS = {
    "Sun": "#b03a2e", "Su": "#b03a2e", "सूर्य": "#b03a2e",
    "Moon": "#21618c", "Mo": "#21618c", "चन्द्र": "#21618c", "Mon": "#21618c",
    "Mars": "#cb4335", "Ma": "#cb4335", "मंगल": "#cb4335", "Mar": "#cb4335",
    "Mercury": "#1e8449", "Me": "#1e8449", "बुध": "#1e8449", "Mer": "#1e8449",
    "Jupiter": "#d35400", "Ju": "#d35400", "गुरु": "#d35400", "Jup": "#d35400",
    "Venus": "#c71585", "Ve": "#c71585", "शुक्र": "#c71585", "Ven": "#c71585",
    "Saturn": "#2874a6", "Sa": "#2874a6", "शनि": "#2874a6", "Sat": "#2874a6",
    "Rahu": "#873600", "Ra": "#873600", "राहु": "#873600", "Rah": "#873600",
    "Ketu": "#873600", "Ke": "#873600", "केतु": "#873600", "Ket": "#873600",
    "Asc": "#d35400", "लग्न": "#d35400",
}

# Dasha tree lord colors (for colored significator display)
DASHA_LORD_COLORS = {
    "Ketu": "#8b4513", "Venus": "#e83e8c", "Sun": "#e74c3c",
    "Moon": "#2980b9", "Mars": "#c0392b", "Rahu": "#8e44ad",
    "Jupiter": "#f39c12", "Saturn": "#000080", "Mercury": "#27ae60",
}

# Aspect highlight colors
ASPECT_POSITIVE_FG = "#27ae60"
ASPECT_POSITIVE_BG = "#d5f5e3"
ASPECT_NEGATIVE_FG = "#c0392b"
ASPECT_NEGATIVE_BG = "#fadbd8"
ASPECT_NEUTRAL_FG = "#2c3e50"


def get_planet_color(name: str) -> str:
    for key, color in PLANET_COLORS.items():
        if key in name:
            return color
    return "#000000"
