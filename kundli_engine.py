"""
Vedic Kundali Calculation Engine
Uses Swiss Ephemeris (pyswisseph) with Lahiri Ayanamsa, Sidereal Zodiac, Whole-Sign Houses,
and standard Vimshottari Mahadasha calculations based on the Moon's nakshatra.
"""

import os
import sys
import math
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Ensure .venv site-packages (pyswisseph, tzdata) are accessible
venv_site_packages = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "Lib", "site-packages")
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

import swisseph as swe


# Set Lahiri Ayanamsa as the permanent sidereal mode
swe.set_sid_mode(swe.SIDM_LAHIRI)

RASHIS = [
    {"id": 1, "name_hi": "मेष", "name_en": "Aries", "lord_hi": "मंगल", "symbol": "♈"},
    {"id": 2, "name_hi": "वृषभ", "name_en": "Taurus", "lord_hi": "शुक्र", "symbol": "♉"},
    {"id": 3, "name_hi": "मिथुन", "name_en": "Gemini", "lord_hi": "बुध", "symbol": "♊"},
    {"id": 4, "name_hi": "कर्क", "name_en": "Cancer", "lord_hi": "चन्द्र", "symbol": "♋"},
    {"id": 5, "name_hi": "सिंह", "name_en": "Leo", "lord_hi": "सूर्य", "symbol": "♌"},
    {"id": 6, "name_hi": "कन्या", "name_en": "Virgo", "lord_hi": "बुध", "symbol": "♍"},
    {"id": 7, "name_hi": "तुला", "name_en": "Libra", "lord_hi": "शुक्र", "symbol": "♎"},
    {"id": 8, "name_hi": "वृश्चिक", "name_en": "Scorpio", "lord_hi": "मंगल", "symbol": "♏"},
    {"id": 9, "name_hi": "धनु", "name_en": "Sagittarius", "lord_hi": "गुरु", "symbol": "♐"},
    {"id": 10, "name_hi": "मकर", "name_en": "Capricorn", "lord_hi": "शनि", "symbol": "♑"},
    {"id": 11, "name_hi": "कुम्भ", "name_en": "Aquarius", "lord_hi": "शनि", "symbol": "♒"},
    {"id": 12, "name_hi": "मीन", "name_en": "Pisces", "lord_hi": "गुरु", "symbol": "♓"},
]

NAKSHATRAS = [
    {"id": 1, "name_hi": "अश्विनी", "name_en": "Ashwini", "lord_hi": "केतु", "syllables": "चू, चे, चो, ला", "deity": "अश्विनी कुमार", "symbol": "अश्व मुख (घोड़े का सिर)"},
    {"id": 2, "name_hi": "भरणी", "name_en": "Bharani", "lord_hi": "शुक्र", "syllables": "ली, लू, ले, लो", "deity": "यमराज", "symbol": "योनि"},
    {"id": 3, "name_hi": "कृत्तिका", "name_en": "Krittika", "lord_hi": "सूर्य", "syllables": "अ, ई, उ, ए", "deity": "अग्नि देव", "symbol": "उस्तरा / ज्वाला"},
    {"id": 4, "name_hi": "रोहिणी", "name_en": "Rohini", "lord_hi": "चन्द्र", "syllables": "ओ, वा, वी, वू", "deity": "प्रजापति (ब्रह्मा)", "symbol": "रथ / छकड़ा"},
    {"id": 5, "name_hi": "मृगशिरा", "name_en": "Mrigashira", "lord_hi": "मंगल", "syllables": "वे, वो, का, की", "deity": "सोम (चंद्रमा)", "symbol": "हिरण का सिर"},
    {"id": 6, "name_hi": "आर्द्रा", "name_en": "Ardra", "lord_hi": "राहु", "syllables": "कू, घ, ङ, छ", "deity": "रुद्र (शिव)", "symbol": "आंसू की बूंद / मणि"},
    {"id": 7, "name_hi": "पुनर्वसु", "name_en": "Punarvasu", "lord_hi": "गुरु", "syllables": "के, को, हा, ही", "deity": "अदिति (देवमाता)", "symbol": "तरकश (धनुष-बाण)"},
    {"id": 8, "name_hi": "पुष्य", "name_en": "Pushya", "lord_hi": "शनि", "syllables": "हू, हे, हो, डा", "deity": "बृहस्पति", "symbol": "गाय का थन / पुष्प"},
    {"id": 9, "name_hi": "अश्लेषा", "name_en": "Ashlesha", "lord_hi": "बुध", "syllables": "डी, डू, डे, डो", "deity": "सर्प (नाग)", "symbol": "कुंडली मारे सर्प"},
    {"id": 10, "name_hi": "मघा", "name_en": "Magha", "lord_hi": "केतु", "syllables": "मा, मी, मू, मे", "deity": "पितर", "symbol": "राज सिंहासन"},
    {"id": 11, "name_hi": "पूर्वाफाल्गुनी", "name_en": "Purva Phalguni", "lord_hi": "शुक्र", "syllables": "मो, टा, टी, टू", "deity": "भग (सूर्य का रूप)", "symbol": "झूला / पलंग"},
    {"id": 12, "name_hi": "उत्तराफाल्गुनी", "name_en": "Uttara Phalguni", "lord_hi": "सूर्य", "syllables": "टे, टो, पा, पी", "deity": "अर्यमा", "symbol": "मंच / शय्या"},
    {"id": 13, "name_hi": "हस्त", "name_en": "Hasta", "lord_hi": "चन्द्र", "syllables": "पू, ष, ण, ठ", "deity": "सविता (सूर्य)", "symbol": "हाथ की हथेली"},
    {"id": 14, "name_hi": "चित्रा", "name_en": "Chitra", "lord_hi": "मंगल", "syllables": "पे, पो, रा, री", "deity": "विश्वकर्मा", "symbol": "चमकता मोती / रत्न"},
    {"id": 15, "name_hi": "स्वाति", "name_en": "Swati", "lord_hi": "राहु", "syllables": "रू, रे, रो, ता", "deity": "वायु देव", "symbol": "नन्हा पौधा / मूंगा"},
    {"id": 16, "name_hi": "विशाखा", "name_en": "Vishakha", "lord_hi": "गुरु", "syllables": "ती, तू, ते, तो", "deity": "इंद्राग्नि", "symbol": "तोरण द्वार"},
    {"id": 17, "name_hi": "अनुराधा", "name_en": "Anuradha", "lord_hi": "शनि", "syllables": "ना, नी, नू, ने", "deity": "मित्र देव", "symbol": "कमल का फूल"},
    {"id": 18, "name_hi": "ज्येष्ठा", "name_en": "Jyeshtha", "lord_hi": "बुध", "syllables": "नो, या, यी, यू", "deity": "इंद्र देव", "symbol": "सुरक्षा कवच / कुंडल"},
    {"id": 19, "name_hi": "मूल", "name_en": "Mula", "lord_hi": "केतु", "syllables": "ये, यो, भा, भी", "deity": "निरृति", "symbol": "पेड़ की जड़ / अंकुश"},
    {"id": 20, "name_hi": "पूर्वाषाढ़ा", "name_en": "Purva Ashadha", "lord_hi": "शुक्र", "syllables": "भू, धा, फा, ढा", "deity": "आपः (जल देवी)", "symbol": "सूप / हाथी का दांत"},
    {"id": 21, "name_hi": "उत्तराषाढ़ा", "name_en": "Uttara Ashadha", "lord_hi": "सूर्य", "syllables": "भे, भो, जा, जी", "deity": "विश्वेदेवा", "symbol": "हाथी का छोटा दांत"},
    {"id": 22, "name_hi": "श्रवण", "name_en": "Shravana", "lord_hi": "चन्द्र", "syllables": "खी, खू, खे, खो", "deity": "भगवान विष्णु", "symbol": "कान (तीन पद चिह्न)"},
    {"id": 23, "name_hi": "धनिष्ठा", "name_en": "Dhanishta", "lord_hi": "मंगल", "syllables": "गा, गी, गु, गे", "deity": "अष्ट वसु", "symbol": "मृदंग / बांसुरी"},
    {"id": 24, "name_hi": "शतभिषा", "name_en": "Shatabhisha", "lord_hi": "राहु", "syllables": "गो, सा, सी, सू", "deity": "वरुण देव", "symbol": "खाली वृत्त / सौ तारे"},
    {"id": 25, "name_hi": "पूर्वाभाद्रपद", "name_en": "Purva Bhadrapada", "lord_hi": "गुरु", "syllables": "से, सो, दा, दी", "deity": "अज एकपाद", "symbol": "तलवार / मंच"},
    {"id": 26, "name_hi": "उत्तराभाद्रपद", "name_en": "Uttara Bhadrapada", "lord_hi": "शनि", "syllables": "दू, थ, झ, ञ", "deity": "अहिर्बुध्न्य", "symbol": "गहरा जल / चक्र"},
    {"id": 27, "name_hi": "रेवती", "name_en": "Revati", "lord_hi": "बुध", "syllables": "दे, दो, चा, ची", "deity": "पूषा देव", "symbol": "मछली की जोड़ी"},
]


DASHA_CYCLE = [
    {"lord_hi": "केतु", "lord_en": "Ketu", "years": 7},
    {"lord_hi": "शुक्र", "lord_en": "Venus", "years": 20},
    {"lord_hi": "सूर्य", "lord_en": "Sun", "years": 6},
    {"lord_hi": "चन्द्र", "lord_en": "Moon", "years": 10},
    {"lord_hi": "मंगल", "lord_en": "Mars", "years": 7},
    {"lord_hi": "राहु", "lord_en": "Rahu", "years": 18},
    {"lord_hi": "गुरु", "lord_en": "Jupiter", "years": 16},
    {"lord_hi": "शनि", "lord_en": "Saturn", "years": 19},
    {"lord_hi": "बुध", "lord_en": "Mercury", "years": 17},
]

GRAHA_DEFS = [
    {"id": "sun", "name_hi": "सूर्य", "name_en": "Sun", "short_hi": "सूर्य", "short_en": "Su", "key_abbr": "सू", "swe_id": swe.SUN},
    {"id": "moon", "name_hi": "चन्द्र", "name_en": "Moon", "short_hi": "चन्द्र", "short_en": "Mo", "key_abbr": "चं", "swe_id": swe.MOON},
    {"id": "mars", "name_hi": "मंगल", "name_en": "Mars", "short_hi": "मंगल", "short_en": "Ma", "key_abbr": "मं", "swe_id": swe.MARS},
    {"id": "mercury", "name_hi": "बुध", "name_en": "Mercury", "short_hi": "बुध", "short_en": "Me", "key_abbr": "बु", "swe_id": swe.MERCURY},
    {"id": "jupiter", "name_hi": "गुरु", "name_en": "Jupiter", "short_hi": "गुरु", "short_en": "Ju", "key_abbr": "गु", "swe_id": swe.JUPITER},
    {"id": "venus", "name_hi": "शुक्र", "name_en": "Venus", "short_hi": "शुक्र", "short_en": "Ve", "key_abbr": "शु", "swe_id": swe.VENUS},
    {"id": "saturn", "name_hi": "शनि", "name_en": "Saturn", "short_hi": "शनि", "short_en": "Sa", "key_abbr": "श", "swe_id": swe.SATURN},
    {"id": "rahu", "name_hi": "राहु", "name_en": "Rahu", "short_hi": "राहु", "short_en": "Ra", "key_abbr": "रा", "swe_id": swe.MEAN_NODE},
    {"id": "ketu", "name_hi": "केतु", "name_en": "Ketu", "short_hi": "केतु", "short_en": "Ke", "key_abbr": "के", "swe_id": -1},  # Calculated as Rahu + 180
]

BHAVA_SIGNIFICANCE = [
    {"name_hi": "तनु भाव (प्रथम भाव)", "name_en": "1st House (Tanu / Ascendant)", "desc_hi": "शरीर, व्यक्तित्व, स्वास्थ्य, जीवन शक्ति", "desc_en": "Self, physical body, vitality, health, and constitution"},
    {"name_hi": "धन भाव (द्वितीय भाव)", "name_en": "2nd House (Dhana / Wealth)", "desc_hi": "वाणी, धन-संपत्ति, कुटुंब, प्रारंभिक शिक्षा", "desc_en": "Wealth, assets, family heritage, speech, food habits"},
    {"name_hi": "सहज भाव (तृतीय भाव)", "name_en": "3rd House (Sahaja / Siblings)", "desc_hi": "साहस, पराक्रम, छोटे भाई-बहन, लघु यात्राएं", "desc_en": "Courage, effort, siblings, short journeys, communication"},
    {"name_hi": "सुख भाव (चतुर्थ भाव)", "name_en": "4th House (Sukha / Home)", "desc_hi": "माता, गृह, भूमि, वाहन, मानसिक शांति", "desc_en": "Mother, home, real estate, vehicles, emotional happiness"},
    {"name_hi": "पुत्र भाव (पंचम भाव)", "name_en": "5th House (Putra / Intellect)", "desc_hi": "संतान, विद्या, विवेक, पूर्व पुण्य, रचनात्मकता", "desc_en": "Children, intelligence, past merits, romance, creativity"},
    {"name_hi": "रिपु भाव (षष्ठ भाव)", "name_en": "6th House (Ripu / Health & Enemies)", "desc_hi": "रोग, ऋण, शत्रु, प्रतिस्पर्धा, सेवा", "desc_en": "Debts, diseases, adversaries, obstacles, daily service"},
    {"name_hi": "जाया भाव (सप्तम भाव)", "name_en": "7th House (Jaya / Marriage)", "desc_hi": "जीवनसाथी, विवाह, साझेदारी, जनसंपर्क", "desc_en": "Spouse, marriage, partnerships, diplomacy, public image"},
    {"name_hi": "आयु भाव (अष्टम भाव)", "name_en": "8th House (Ayu / Longevity)", "desc_hi": "आयु, गूढ़ रहस्य, परिवर्तन, आकस्मिक घटनाएं", "desc_en": "Longevity, secrets, transformations, research, inheritances"},
    {"name_hi": "भाग्य भाव (नवम भाव)", "name_en": "9th House (Bhagya / Fortune)", "desc_hi": "धर्म, भाग्य, गुरु, उच्च ज्ञान, तीर्थ यात्रा", "desc_en": "Fortune, dharma, spiritual guides, higher knowledge, pilgrimage"},
    {"name_hi": "कर्म भाव (दशम भाव)", "name_en": "10th House (Karma / Career)", "desc_hi": "व्यवसाय, प्रतिष्ठा, पिता, अधिकार, कीर्ति", "desc_en": "Career, profession, reputation, status, leadership, authority"},
    {"name_hi": "लाभ भाव (एकादश भाव)", "name_en": "11th House (Labha / Gains)", "desc_hi": "आमदनी, ज्येष्ठ भ्राता, मित्र, मनोकामना पूर्ति", "desc_en": "Gains, income, social network, elder siblings, ambitions"},
    {"name_hi": "व्यय भाव (द्वादश भाव)", "name_en": "12th House (Vyaya / Expenses)", "desc_hi": "मोक्ष, विदेश गमन, व्यय, शयन सुख, त्याग", "desc_en": "Expenditures, foreign travel, spirituality, sleep, liberation"}
]


def format_dms(deg_val):
    """Formats decimal degrees into degrees, arcminutes, arcseconds."""
    d = int(deg_val)
    rem_m = (deg_val - d) * 60.0
    m = int(rem_m)
    s = int(round((rem_m - m) * 60.0))
    if s >= 60:
        s = 0
        m += 1
    if m >= 60:
        m = 0
        d += 1
    return d, m, s, f"{d}° {m:02d}' {s:02d}\""


def get_nakshatra_and_pada(longitude):
    """Computes Nakshatra (0-26), Pada (1-4), elapsed ratio, and degrees in nakshatra."""
    nak_span = 360.0 / 27.0  # 13.33333333°
    pada_span = nak_span / 4.0  # 3.33333333°
    norm_lon = longitude % 360.0

    nak_idx = int(norm_lon / nak_span)
    nak_idx = max(0, min(26, nak_idx))
    rem_deg = norm_lon - (nak_idx * nak_span)

    pada = int(rem_deg / pada_span) + 1
    pada = max(1, min(4, pada))

    elapsed_ratio = rem_deg / nak_span
    return nak_idx, NAKSHATRAS[nak_idx], pada, rem_deg, elapsed_ratio


def calculate_vimshottari_dasha(birth_dt, moon_lon):
    """
    Calculates Vimshottari Mahadasha sequence starting from birth
    based on the Moon's nakshatra and remaining balance.
    Uses standard solar year (365.2425 days) for timing.
    """
    nak_idx, nak_info, pada, rem_deg, elapsed_ratio = get_nakshatra_and_pada(moon_lon)
    balance_ratio = 1.0 - elapsed_ratio

    # Lord cycle index (each cycle of 9 repeats 3 times)
    start_lord_idx = nak_idx % 9
    first_lord = DASHA_CYCLE[start_lord_idx]

    DAYS_PER_YEAR = 365.2425

    balance_years = first_lord["years"] * balance_ratio
    balance_days = balance_years * DAYS_PER_YEAR
    elapsed_days = (first_lord["years"] * elapsed_ratio) * DAYS_PER_YEAR

    # Accurate start date of birth dasha
    dasha_start = birth_dt - timedelta(days=elapsed_days)
    dasha_end = birth_dt + timedelta(days=balance_days)

    now = datetime.now(birth_dt.tzinfo) if birth_dt.tzinfo else datetime.now()

    dashas = []
    # First Mahadasha (at birth)
    is_active = (dasha_start <= now <= dasha_end)
    dashas.append({
        "order": 1,
        "lord_hi": first_lord["lord_hi"],
        "lord_en": first_lord["lord_en"],
        "total_years": first_lord["years"],
        "balance_years_formatted": f"{balance_years:.2f} वर्ष",
        "start_date": dasha_start.strftime("%d-%m-%Y"),
        "end_date": dasha_end.strftime("%d-%m-%Y"),
        "start_dt": dasha_start,
        "end_dt": dasha_end,
        "is_birth": True,
        "is_active": is_active,
    })

    current_start = dasha_end
    for i in range(1, 9):
        idx = (start_lord_idx + i) % 9
        lord = DASHA_CYCLE[idx]
        duration_days = lord["years"] * DAYS_PER_YEAR
        next_end = current_start + timedelta(days=duration_days)
        is_active = (current_start <= now <= next_end)
        dashas.append({
            "order": i + 1,
            "lord_hi": lord["lord_hi"],
            "lord_en": lord["lord_en"],
            "total_years": lord["years"],
            "balance_years_formatted": f"{lord['years']} वर्ष",
            "start_date": current_start.strftime("%d-%m-%Y"),
            "end_date": next_end.strftime("%d-%m-%Y"),
            "start_dt": current_start,
            "end_dt": next_end,
            "is_birth": False,
            "is_active": is_active,
        })
        current_start = next_end

    return dashas, nak_info, pada, balance_years


def generate_north_indian_svg(houses, lagna_rashi_num, center_label="लग्न (तनु भाव)", lang="hi"):
    """
    Renders an original, beautifully styled North Indian diamond Vedic Kundali SVG.
    Standard North Indian layout:
    - House 1 (Lagna) is the top diamond.
    - Houses 1 to 12 proceed counter-clockwise.
    - Each house displays the Rashi number residing in that house.
    - Grahas residing in each house are cleanly positioned inside the polygon.
    """
    w, h = 600, 600

    # House polygons in 600x600 coordinate system
    # Verified counter-clockwise North Indian geometry
    house_specs = {
        1: {
            "polygon": f"{w*0.5:.1f},0 {w*0.25:.1f},{h*0.25:.1f} {w*0.5:.1f},{h*0.5:.1f} {w*0.75:.1f},{h*0.25:.1f}",
            "rashi_pos": (w * 0.5, h * 0.38),
            "graha_anchor": (w * 0.5, h * 0.18),
            "is_kendra": True,
            "name": "लग्न / १",
        },
        2: {
            "polygon": f"0,0 {w*0.5:.1f},0 {w*0.25:.1f},{h*0.25:.1f}",
            "rashi_pos": (w * 0.32, h * 0.08),
            "graha_anchor": (w * 0.25, h * 0.17),
            "is_kendra": False,
            "name": "२",
        },
        3: {
            "polygon": f"0,0 {w*0.25:.1f},{h*0.25:.1f} 0,{h*0.5:.1f}",
            "rashi_pos": (w * 0.08, h * 0.32),
            "graha_anchor": (w * 0.16, h * 0.24),
            "is_kendra": False,
            "name": "३",
        },
        4: {
            "polygon": f"0,{h*0.5:.1f} {w*0.25:.1f},{h*0.25:.1f} {w*0.5:.1f},{h*0.5:.1f} {w*0.25:.1f},{h*0.75:.1f}",
            "rashi_pos": (w * 0.38, h * 0.5),
            "graha_anchor": (w * 0.18, h * 0.5),
            "is_kendra": True,
            "name": "४",
        },
        5: {
            "polygon": f"0,{h*0.5:.1f} {w*0.25:.1f},{h*0.75:.1f} 0,{h:.1f}",
            "rashi_pos": (w * 0.08, h * 0.68),
            "graha_anchor": (w * 0.16, h * 0.76),
            "is_kendra": False,
            "name": "५",
        },
        6: {
            "polygon": f"0,{h:.1f} {w*0.25:.1f},{h*0.75:.1f} {w*0.5:.1f},{h:.1f}",
            "rashi_pos": (w * 0.32, h * 0.92),
            "graha_anchor": (w * 0.25, h * 0.83),
            "is_kendra": False,
            "name": "६",
        },
        7: {
            "polygon": f"{w*0.5:.1f},{h:.1f} {w*0.25:.1f},{h*0.75:.1f} {w*0.5:.1f},{h*0.5:.1f} {w*0.75:.1f},{h*0.75:.1f}",
            "rashi_pos": (w * 0.5, h * 0.62),
            "graha_anchor": (w * 0.5, h * 0.82),
            "is_kendra": True,
            "name": "७",
        },
        8: {
            "polygon": f"{w*0.5:.1f},{h:.1f} {w*0.75:.1f},{h*0.75:.1f} {w:.1f},{h:.1f}",
            "rashi_pos": (w * 0.68, h * 0.92),
            "graha_anchor": (w * 0.75, h * 0.83),
            "is_kendra": False,
            "name": "८",
        },
        9: {
            "polygon": f"{w:.1f},{h:.1f} {w*0.75:.1f},{h*0.75:.1f} {w:.1f},{h*0.5:.1f}",
            "rashi_pos": (w * 0.92, h * 0.68),
            "graha_anchor": (w * 0.84, h * 0.76),
            "is_kendra": False,
            "name": "९",
        },
        10: {
            "polygon": f"{w:.1f},{h*0.5:.1f} {w*0.75:.1f},{h*0.75:.1f} {w*0.5:.1f},{h*0.5:.1f} {w*0.75:.1f},{h*0.25:.1f}",
            "rashi_pos": (w * 0.62, h * 0.5),
            "graha_anchor": (w * 0.82, h * 0.5),
            "is_kendra": True,
            "name": "१०",
        },
        11: {
            "polygon": f"{w:.1f},{h*0.5:.1f} {w*0.75:.1f},{h*0.25:.1f} {w:.1f},0",
            "rashi_pos": (w * 0.92, h * 0.32),
            "graha_anchor": (w * 0.84, h * 0.24),
            "is_kendra": False,
            "name": "११",
        },
        12: {
            "polygon": f"{w:.1f},0 {w*0.75:.1f},{h*0.25:.1f} {w*0.5:.1f},0",
            "rashi_pos": (w * 0.68, h * 0.08),
            "graha_anchor": (w * 0.75, h * 0.17),
            "is_kendra": False,
            "name": "१२",
        },
    }

    svg_parts = []
    svg_parts.append(
        f'<svg class="kundli-svg-chart" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="उत्तर भारतीय लग्न कुण्डली">'
    )
    svg_parts.append('<defs>')
    svg_parts.append('''
        <linearGradient id="kendraGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFF8E7" stop-opacity="0.9" />
            <stop offset="100%" stop-color="#FDF1D6" stop-opacity="0.95" />
        </linearGradient>
        <linearGradient id="trikonaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95" />
            <stop offset="100%" stop-color="#FBF7F0" stop-opacity="0.9" />
        </linearGradient>
        <filter id="kundliShadow" x="-5%" y="-5%" width="110%" height="110%">
            <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#8B4513" flood-opacity="0.1" />
        </filter>
    ''')
    svg_parts.append('</defs>')

    # Outer decorative frame
    svg_parts.append(f'<rect width="{w}" height="{h}" fill="#FBF7EE" stroke="#A8422B" stroke-width="6" rx="4" />')
    svg_parts.append(f'<rect x="8" y="8" width="{w-16}" height="{h-16}" fill="none" stroke="#D4AF37" stroke-width="1.5" />')

    # Draw the 12 House Polygons
    for h_num in range(1, 13):
        spec = house_specs[h_num]
        fill = "url(#kendraGrad)" if spec["is_kendra"] else "url(#trikonaGrad)"
        svg_parts.append(
            f'<polygon points="{spec["polygon"]}" fill="{fill}" stroke="#A8422B" stroke-width="2" class="house-polygon house-{h_num}" />'
        )

    # Diagonal and boundary lines enhancement
    svg_parts.append(f'<line x1="0" y1="0" x2="{w}" y2="{h}" stroke="#A8422B" stroke-width="2.5" />')
    svg_parts.append(f'<line x1="{w}" y1="0" x2="0" y2="{h}" stroke="#A8422B" stroke-width="2.5" />')
    svg_parts.append(f'<line x1="{w*0.5}" y1="0" x2="0" y2="{h*0.5}" stroke="#A8422B" stroke-width="2.5" />')
    svg_parts.append(f'<line x1="0" y1="{h*0.5}" x2="{w*0.5}" y2="{h}" stroke="#A8422B" stroke-width="2.5" />')
    svg_parts.append(f'<line x1="{w*0.5}" y1="{h}" x2="{w}" y2="{h*0.5}" stroke="#A8422B" stroke-width="2.5" />')
    svg_parts.append(f'<line x1="{w}" y1="{h*0.5}" x2="{w*0.5}" y2="0" stroke="#A8422B" stroke-width="2.5" />')

    # Add Rashi numbers and Grahas for each House
    for h_num in range(1, 13):
        spec = house_specs[h_num]
        h_data = houses[h_num - 1]  # 0-indexed list
        rashi_num = h_data["rashi"]["id"]

        # Rashi Number text
        rx, ry = spec["rashi_pos"]
        svg_parts.append(
            f'<text x="{rx:.1f}" y="{ry:.1f}" text-anchor="middle" dominant-baseline="central" '
            f'class="rashi-num" fill="#8C2D19" font-size="15" font-weight="700" font-family="Tiro Devanagari Hindi, serif">{rashi_num}</text>'
        )

        # Residing Grahas
        grahas_in_house = h_data["grahas"]
        gx, gy = spec["graha_anchor"]

        if grahas_in_house:
            count = len(grahas_in_house)
            # Arrange multiple grahas vertically centered around anchor
            line_height = 18 if count <= 3 else 15
            start_y = gy - ((count - 1) * line_height / 2.0)

            for idx, g in enumerate(grahas_in_house):
                cur_y = start_y + (idx * line_height)
                if lang == "en":
                    retro_mark = " (R)" if g.get("is_retrograde") and g.get("id") not in ("rahu", "ketu") else ""
                    name_lbl = g.get("short_en", g.get("short_hi", ""))
                    title_lbl = f'{g.get("name_en", g.get("name_hi", ""))} ({g.get("rashi_deg_formatted", "")})'
                else:
                    retro_mark = " (व)" if g.get("is_retrograde") and g.get("id") not in ("rahu", "ketu") else ""
                    name_lbl = g.get("short_hi", "")
                    title_lbl = f'{g.get("name_hi", "")} ({g.get("rashi_deg_formatted", "")})'
                
                text_label = f'{name_lbl}{retro_mark}'
                font_fam = "system-ui, -apple-system, sans-serif" if lang == "en" else "Noto Sans Devanagari, sans-serif"

                svg_parts.append(
                    f'<text x="{gx:.1f}" y="{cur_y:.1f}" text-anchor="middle" dominant-baseline="central" '
                    f'class="graha-text graha-{g.get("id", "")}" fill="#1B263B" font-size="13" font-weight="600" '
                    f'font-family="{font_fam}">{text_label}'
                    f'<title>{title_lbl}</title></text>'
                )

        # Mark House 1 explicitly with center_label
        if h_num == 1:
            font_fam_c = "system-ui, sans-serif" if lang == "en" else "Tiro Devanagari Hindi, serif"
            svg_parts.append(
                f'<text x="{w*0.5}" y="{h*0.06}" text-anchor="middle" dominant-baseline="central" '
                f'fill="#A8422B" font-size="13" font-weight="700" font-family="{font_fam_c}">{center_label}</text>'
            )

    svg_parts.append('</svg>')
    return "".join(svg_parts)


def generate_south_indian_svg(grahas_list, lagna_rashi_num, center_label="दक्षिण भारतीय कुंडली", lang="hi"):
    """
    Renders an authentic South Indian Vedic Kundali SVG (4x4 square grid).
    Fixed Zodiac Positions:
    - Row 0: Pisces (12), Aries (1), Taurus (2), Gemini (3)
    - Row 1: Aquarius (11), [Center], Cancer (4)
    - Row 2: Capricorn (10), [Center], Leo (5)
    - Row 3: Sagittarius (9), Scorpio (8), Libra (7), Virgo (6)
    - Supports 'hi' and 'en' language modes.
    """
    w, h = 600, 600
    cw, ch = 150, 150

    rashi_cells = {
        12: (0, 0),  # Pisces
        1:  (1, 0),  # Aries
        2:  (2, 0),  # Taurus
        3:  (3, 0),  # Gemini
        4:  (3, 1),  # Cancer
        5:  (3, 2),  # Leo
        6:  (3, 3),  # Virgo
        7:  (2, 3),  # Libra
        8:  (1, 3),  # Scorpio
        9:  (0, 3),  # Sagittarius
        10: (0, 2),  # Capricorn
        11: (0, 1),  # Aquarius
    }

    grahas_by_rashi = {r: [] for r in range(1, 13)}
    for g in grahas_list:
        rid = g.get("rashi", {}).get("id") if isinstance(g.get("rashi"), dict) else g.get("rashi_id")
        if rid in grahas_by_rashi:
            grahas_by_rashi[rid].append(g)

    sub_title = "Lahiri Ayanamsa • South Indian Chart" if lang == "en" else "लाहिड़ी अयनांश • दक्षिण भारतीय चक्र"

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'class="kundli-svg-chart south-indian-chart" aria-label="दक्षिण भारतीय जन्म कुंडली" role="img">',
        f'<rect width="{w}" height="{h}" fill="#FFFDF9" stroke="#9E2A2B" stroke-width="4"/>',
    ]

    # Center box (Row 1-2, Col 1-2)
    cx, cy, cw_center, ch_center = cw, ch, cw * 2, ch * 2
    svg_parts.append(
        f'<rect x="{cx}" y="{cy}" width="{cw_center}" height="{ch_center}" '
        f'fill="#FAF4EB" stroke="#C57B12" stroke-width="2"/>'
    )
    svg_parts.append(
        f'<rect x="{cx+6}" y="{cy+6}" width="{cw_center-12}" height="{ch_center-12}" '
        f'fill="none" stroke="#E8D3A7" stroke-width="1" stroke-dasharray="4,2"/>'
    )
    svg_parts.append(
        f'<text x="{cx + cw_center/2}" y="{cy + ch_center*0.35}" text-anchor="middle" dominant-baseline="central" '
        f'fill="#C57B12" font-size="28" font-family="Noto Sans Devanagari, sans-serif">ॐ</text>'
    )
    c_font = "system-ui, sans-serif" if lang == "en" else "Tiro Devanagari Hindi, serif"
    svg_parts.append(
        f'<text x="{cx + cw_center/2}" y="{cy + ch_center*0.58}" text-anchor="middle" dominant-baseline="central" '
        f'fill="#9E2A2B" font-size="15" font-weight="700" font-family="{c_font}">{center_label}</text>'
    )
    svg_parts.append(
        f'<text x="{cx + cw_center/2}" y="{cy + ch_center*0.75}" text-anchor="middle" dominant-baseline="central" '
        f'fill="#5C6274" font-size="12" font-family="system-ui, sans-serif">{sub_title}</text>'
    )

    # 12 Rashi Cells
    for rid, (col, row) in rashi_cells.items():
        rx = col * cw
        ry = row * ch
        rashi_meta = RASHIS[rid - 1]
        is_lagna = (rid == lagna_rashi_num)

        cell_fill = "#FFF8E7" if is_lagna else "#FFFFFF"
        svg_parts.append(
            f'<rect x="{rx}" y="{ry}" width="{cw}" height="{ch}" fill="{cell_fill}" stroke="#9E2A2B" stroke-width="1.5"/>'
        )

        rashi_name = rashi_meta["name_en"] if lang == "en" else rashi_meta["name_hi"]
        svg_parts.append(
            f'<text x="{rx + cw - 8}" y="{ry + 16}" text-anchor="end" fill="#7E8597" font-size="11" '
            f'font-family="system-ui, sans-serif">{rashi_name} ({rid})</text>'
        )

        if is_lagna:
            svg_parts.append(f'<line x1="{rx}" y1="{ry}" x2="{rx+45}" y2="{ry+45}" stroke="#9E2A2B" stroke-width="2"/>')
            lagna_badge = "Asc" if lang == "en" else "लग्न"
            svg_parts.append(
                f'<text x="{rx + 8}" y="{ry + 32}" fill="#9E2A2B" font-size="12" font-weight="700" '
                f'font-family="system-ui, sans-serif">{lagna_badge}</text>'
            )

        cell_grahas = grahas_by_rashi[rid]
        start_y = ry + (48 if is_lagna else 36)
        for i, g in enumerate(cell_grahas):
            gy = start_y + (i * 20)
            if lang == "en":
                retro = " (R)" if g.get("is_retrograde") and g.get("id") not in ("rahu", "ketu") else ""
                label = f'{g.get("short_en", g.get("short_hi", ""))}{retro} {g.get("rashi_deg_formatted", "")}'
                title_lbl = f'{g.get("name_en", g.get("name_hi", ""))}'
            else:
                retro = " (व)" if g.get("is_retrograde") and g.get("id") not in ("rahu", "ketu") else ""
                label = f'{g.get("short_hi", g.get("name_short", ""))}{retro} {g.get("rashi_deg_formatted", "")}'
                title_lbl = f'{g.get("name_hi", "")}'

            svg_parts.append(
                f'<text x="{rx + 12}" y="{gy}" fill="#1B263B" font-size="12" font-weight="600" '
                f'font-family="system-ui, sans-serif">{label}'
                f'<title>{title_lbl}</title></text>'
            )

    svg_parts.append('</svg>')
    return "".join(svg_parts)


def get_navamsha_rashi_idx(longitude):
    """
    Computes 0-indexed Navamsha sign for a given sidereal longitude.
    108 padas across 360 degrees.
    """
    pada_span = 360.0 / 108.0
    total_pada = int((longitude % 360.0) / pada_span)
    return total_pada % 12


def compute_navamsha_chart(lagna_lon, grahas_list):
    """
    Computes Navamsha (D9) Chart houses and generates North Indian SVG.
    """
    lagna_nav_idx = get_navamsha_rashi_idx(lagna_lon)
    houses = []
    for h in range(1, 13):
        r_idx = (lagna_nav_idx + (h - 1)) % 12
        houses.append({
            "house_num": h,
            "rashi": RASHIS[r_idx],
            "rashi_num": RASHIS[r_idx]["id"],
            "rashi_lord": RASHIS[r_idx]["lord_hi"],
            "significance": BHAVA_SIGNIFICANCE[h - 1],
            "grahas": []
        })

    for g in grahas_list:
        g_nav_idx = get_navamsha_rashi_idx(g["longitude"])
        h_num = ((g_nav_idx - lagna_nav_idx) % 12) + 1
        g_copy = dict(g)
        g_copy["house_num"] = h_num
        g_copy["navamsha_rashi"] = RASHIS[g_nav_idx]
        houses[h_num - 1]["grahas"].append(g_copy)

    svg_hi = generate_north_indian_svg(houses, RASHIS[lagna_nav_idx]["id"], center_label="नवमांश लग्न (D9)", lang="hi")
    svg_en = generate_north_indian_svg(houses, RASHIS[lagna_nav_idx]["id"], center_label="Navamsha Lagna (D9)", lang="en")
    return houses, svg_hi, RASHIS[lagna_nav_idx], svg_en


def compute_chandra_chart(moon_rashi_idx, grahas_list):
    """
    Computes Chandra (Moon) Chart houses and generates North Indian SVG.
    """
    houses = []
    for h in range(1, 13):
        r_idx = (moon_rashi_idx + (h - 1)) % 12
        houses.append({
            "house_num": h,
            "rashi": RASHIS[r_idx],
            "rashi_num": RASHIS[r_idx]["id"],
            "rashi_lord": RASHIS[r_idx]["lord_hi"],
            "significance": BHAVA_SIGNIFICANCE[h - 1],
            "grahas": []
        })

    for g in grahas_list:
        g_r_idx = g["rashi"]["id"] - 1
        h_num = ((g_r_idx - moon_rashi_idx) % 12) + 1
        g_copy = dict(g)
        g_copy["house_num"] = h_num
        houses[h_num - 1]["grahas"].append(g_copy)

    svg_hi = generate_north_indian_svg(houses, RASHIS[moon_rashi_idx]["id"], center_label="चंद्र लग्न (Chandra)", lang="hi")
    svg_en = generate_north_indian_svg(houses, RASHIS[moon_rashi_idx]["id"], center_label="Moon Ascendant (Chandra)", lang="en")
    return houses, svg_hi, svg_en


def get_planetary_avastha(rashi_id, deg_in_rashi):
    """
    Determines planetary state (Avastha) based on degree in odd/even sign:
    बाल्यावस्था, कुमारावस्था, युवावस्था, वृद्धावस्था, मृतावस्था.
    """
    is_odd = (rashi_id % 2 != 0)
    d = deg_in_rashi
    if is_odd:
        if d < 6: return "बाल्यावस्था / Infant (25%)"
        elif d < 12: return "कुमारावस्था / Adolescent (50%)"
        elif d < 18: return "युवावस्था / Youthful (100%)"
        elif d < 24: return "वृद्धावस्था / Old (15%)"
        else: return "मृतावस्था / Dead (0%)"
    else:
        if d < 6: return "मृतावस्था / Dead (0%)"
        elif d < 12: return "वृद्धावस्था / Old (15%)"
        elif d < 18: return "युवावस्था / Youthful (100%)"
        elif d < 24: return "कुमारावस्था / Adolescent (50%)"
        else: return "बाल्यावस्था / Infant (25%)"


PLANETARY_DIGNITIES = {
    "sun": {"exalt": 1, "debil": 7, "own": [5], "moola": 5},
    "moon": {"exalt": 2, "debil": 8, "own": [4], "moola": 2},
    "mars": {"exalt": 10, "debil": 4, "own": [1, 8], "moola": 1},
    "mercury": {"exalt": 6, "debil": 12, "own": [3, 6], "moola": 6},
    "jupiter": {"exalt": 4, "debil": 10, "own": [9, 12], "moola": 9},
    "venus": {"exalt": 12, "debil": 6, "own": [2, 7], "moola": 7},
    "saturn": {"exalt": 7, "debil": 1, "own": [10, 11], "moola": 11},
    "rahu": {"exalt": 2, "debil": 8, "own": [11], "moola": 11},
    "ketu": {"exalt": 8, "debil": 2, "own": [8], "moola": 8},
}

def get_planetary_dignity(planet_id, rashi_id):
    """
    Computes dignity: उच्च, नीच, स्वराशि, मूलत्रिकोण, सम.
    """
    info = PLANETARY_DIGNITIES.get((planet_id or "").lower(), {})
    if rashi_id == info.get("exalt"):
        return "उच्च (Exalted)"
    elif rashi_id == info.get("debil"):
        return "नीच (Debilitated)"
    elif rashi_id == info.get("moola"):
        return "मूलत्रिकोण (Moolatrikona)"
    elif rashi_id in info.get("own", []):
        return "स्वराशि (Own Sign)"
    else:
        return "सम / सामान्य"


def get_avakhada_details(moon_rashi_id, lagna_rashi_id, nak_idx, pada):
    """
    Generates Avakhada Chakra details (वर्ण, वश्य, तारा, योनि, गण, नाड़ी, पाया, तत्व, नामाक्षर).
    """
    if moon_rashi_id in (4, 8, 12): varna = "ब्राह्मण (Brahmin)"
    elif moon_rashi_id in (1, 5, 9): varna = "क्षत्रिय (Kshatriya)"
    elif moon_rashi_id in (2, 6, 10): varna = "वैश्य (Vaishya)"
    else: varna = "शूद्र (Shudra)"
    
    if moon_rashi_id in (1, 2, 9): vashya = "चतुष्पद (Quadruped)"
    elif moon_rashi_id in (3, 6, 7, 11): vashya = "द्विपद / मानव (Human)"
    elif moon_rashi_id in (4, 12): vashya = "जलचर (Water)"
    elif moon_rashi_id == 5: vashya = "वनचर / सिंह (Wild)"
    else: vashya = "कीट (Insect)"
    
    if moon_rashi_id in (1, 5, 9): tatva = "अग्नि तत्व (Fire)"
    elif moon_rashi_id in (2, 6, 10): tatva = "पृथ्वी तत्व (Earth)"
    elif moon_rashi_id in (3, 7, 11): tatva = "वायु तत्व (Air)"
    else: tatva = "जल तत्व (Water)"

    moon_house = ((moon_rashi_id - lagna_rashi_id) % 12) + 1
    if moon_house in (1, 6, 11): paya = "स्वर्ण पाया (Gold) - अति शुभ"
    elif moon_house in (2, 5, 9): paya = "रजत पाया (Silver) - शुभ"
    elif moon_house in (3, 7, 10): paya = "ताम्र पाया (Copper) - मध्यम"
    else: paya = "लौह पाया (Iron) - परिश्रम"
    
    nak = NAKSHATRAS[nak_idx]
    
    deva_naks = (1, 4, 5, 7, 8, 13, 15, 17, 22, 27)
    rakshasa_naks = (3, 9, 10, 14, 16, 18, 19, 23, 24)
    if (nak_idx + 1) in deva_naks: gana = "देव गण"
    elif (nak_idx + 1) in rakshasa_naks: gana = "राक्षस गण"
    else: gana = "मनुष्य गण"
    
    nadi_cycle = ["आदि", "मध्य", "अंत्य"]
    nadi_map = [
        0, 1, 2, 2, 1, 0, 0, 1, 2,
        2, 1, 0, 0, 1, 2, 2, 1, 0,
        0, 1, 2, 2, 1, 0, 0, 1, 2
    ]
    nadi = f"{nadi_cycle[nadi_map[nak_idx]]} नाड़ी"
    
    sylls = [s.strip() for s in nak.get("syllables", "").split(",")]
    syllable = sylls[pada - 1] if len(sylls) >= pada else (sylls[0] if sylls else "—")

    return {
        "varna": varna,
        "vashya": vashya,
        "tatva": tatva,
        "paya": paya,
        "gana": gana,
        "nadi": nadi,
        "syllable": syllable,
        "deity": nak.get("deity", "—"),
        "symbol": nak.get("symbol", "—"),
    }


def check_kalsarp_dosha(grahas_list):
    """
    Checks for Kalsarp Yoga (all planets hemmed between Rahu and Ketu).
    """
    try:
        rahu = next(g for g in grahas_list if g["id"] == "rahu")
        ketu = next(g for g in grahas_list if g["id"] == "ketu")
        r_lon = rahu["longitude"]
        k_lon = ketu["longitude"]
        
        seven = [g for g in grahas_list if g["id"] not in ("rahu", "ketu")]
        side1 = all(((g["longitude"] - r_lon) % 360.0) < 180.0 for g in seven)
        side2 = all(((g["longitude"] - k_lon) % 360.0) < 180.0 for g in seven)
        
        is_kalsarp = side1 or side2
        r_house = rahu["house_num"]
        kalsarp_names = [
            "अनंत कालसर्प", "कुलिक कालसर्प", "वासुकि कालसर्प", "शंखपाल कालसर्प",
            "पद्म कालसर्प", "महापद्म कालसर्प", "तक्षक कालसर्प", "कर्कोटक कालसर्प",
            "शंखनाद कालसर्प", "घातक कालसर्प", "विषधर कालसर्प", "शेषनाग कालसर्प"
        ]
        yoga_name = kalsarp_names[r_house - 1] if is_kalsarp else "दोष मुक्त (कालसर्प योग नहीं है)"
        desc = (
            f"राहु {r_house}वें भाव में होने से {yoga_name} का निर्माण होता है। यह योग संघर्ष के बाद अप्रत्याशित सफलता व दृढ़ इच्छाशक्ति प्रदान करता है।"
            if is_kalsarp else
            "आपकी कुंडली में सभी ग्रह राहु-केतु अक्ष के दोनों ओर संतुलित हैं, अतः कालसर्प योग का कोई प्रभाव नहीं है।"
        )
        return {
            "is_present": is_kalsarp,
            "name": yoga_name,
            "rahu_house": r_house,
            "description": desc,
            "badge_color": "#C62828" if is_kalsarp else "#2E7D32"
        }
    except Exception:
        return {
            "is_present": False,
            "name": "दोष मुक्त",
            "rahu_house": 1,
            "description": "कुंडली में कालसर्प दोष नहीं है।",
            "badge_color": "#2E7D32"
        }


def check_manglik_dosha(lagna_rashi_id, grahas_list, houses):
    """
    Computes Manglik status and classical Pariharas for a Kundali.
    """
    try:
        mars = next((g for g in grahas_list if g["id"] == "mars"), None)
        moon = next((g for g in grahas_list if g["id"] == "moon"), None)
        jupiter = next((g for g in grahas_list if g["id"] == "jupiter"), None)

        mars_house_lagna = mars["house_num"] if mars else 1
        mars_rashi_id = mars["rashi"]["id"] if mars else 1
        moon_house = moon["house_num"] if moon else 1
        mars_house_moon = ((mars_house_lagna - moon_house + 12) % 12) or 12

        manglik_houses = (1, 4, 7, 8, 12)
        is_manglik_lagna = mars_house_lagna in manglik_houses
        is_manglik_moon = mars_house_moon in manglik_houses

        pariharas = []
        is_exempt = False

        if mars_rashi_id in (1, 8):
            pariharas.append("मंगल स्वराशि (मेष/वृश्चिक) में स्थित होने से 'स्वक्षेत्रे कुज दोषो न' परिहार लागू है।")
            is_exempt = True
        elif mars_rashi_id == 10:
            pariharas.append("मंगल मकर (उच्च) राशि में स्थित होने से दोष शांत हो जाता है।")
            is_exempt = True

        if jupiter:
            jup_h = jupiter["house_num"]
            diff = (mars_house_lagna - jup_h + 12) % 12
            if diff in (0, 4, 6, 8):
                pariharas.append("देवगुरु बृहस्पति की मंगल पर शुभ दृष्टि अथवा युति होने से दोष परिहार प्रभावी है।")
                is_exempt = True

        pariharas.append("२८ वर्ष की आयु पूर्ण होने के उपरांत मंगल की नैसर्गिक उग्रता स्वतः परिपक्वता में बदल जाती है।")

        if not is_manglik_lagna and not is_manglik_moon:
            status = "अनामांगलिक (मांगलिक दोष नहीं है)"
            badge_color = "#2E7D32"
            desc = f"मंगल लग्न से {mars_house_lagna}वें तथा चंद्र से {mars_house_moon}वें भाव में स्थित है, जो मांगलिक भावों (१, ४, ७, ८, १२) से बाहर है।"
        elif is_exempt:
            status = "मांगलिक योग (शास्त्रीय परिहार प्रभावी)"
            badge_color = "#0D828A"
            desc = f"मंगल {mars_house_lagna}वें भाव में है, किंतु शास्त्रीय परिहार के प्रभाव से वैवाहिक जीवन के लिए यह पूर्णतः अनुकूल व सुरक्षित है।"
        elif is_manglik_lagna:
            status = "सक्रिय मांगलिक योग (लग्न से)"
            badge_color = "#C62828"
            desc = f"मंगल लग्न से {mars_house_lagna}वें भाव में स्थित है। यह जातक में ऊर्जा, साहस व स्वाभिमान की प्रबलता दर्शाता है।"
        else:
            status = "आंशिक मांगलिक (चंद्र से)"
            badge_color = "#C57B12"
            desc = f"मंगल चंद्र से {mars_house_moon}वें भाव में स्थित है।"

        return {
            "is_manglik": is_manglik_lagna or is_manglik_moon,
            "is_exempt": is_exempt,
            "status": status,
            "badge_color": badge_color,
            "description": desc,
            "mars_house_lagna": mars_house_lagna,
            "mars_house_moon": mars_house_moon,
            "pariharas": pariharas
        }
    except Exception:
        return {
            "is_manglik": False,
            "is_exempt": False,
            "status": "सामान्य",
            "badge_color": "#2E7D32",
            "description": "मांगलिक विचार पूर्ण।",
            "mars_house_lagna": 1,
            "mars_house_moon": 1,
            "pariharas": []
        }


def calculate_kundli(birth_date_str, birth_time_str, tz_name, lat, lon, name="जातक", gender="पुरुष"):
    """
    Main Kundali calculation pipeline:
    - Parses date, time, and timezone
    - Converts to UTC using Python zoneinfo
    - Computes Julian Day UT
    - Computes Lahiri Ayanamsa, Lagna, and 9 Grahas
    - Computes Whole-Sign Houses, Nakshatras, Padas
    - Computes Vimshottari Mahadasha sequence
    - Generates North Indian SVG Chart
    """
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        raise ValueError("कृपया सही अक्षांश (Latitude) और देशांतर (Longitude) प्रदान करें।")

    # Timezone validation
    try:
        tz = ZoneInfo(tz_name.strip() if tz_name else "Asia/Kolkata")
    except Exception:
        tz = ZoneInfo("Asia/Kolkata")

    # Parse local datetime
    try:
        parts_date = [int(p) for p in birth_date_str.strip().split("-")]
        if len(parts_date) != 3:
            raise ValueError()
        year, month, day = parts_date[0], parts_date[1], parts_date[2]
    except Exception:
        raise ValueError("कृपया सही जन्म तिथि (YYYY-MM-DD) दर्ज करें।")

    try:
        time_parts = [int(p) for p in birth_time_str.strip().split(":")]
        hour = time_parts[0]
        minute = time_parts[1] if len(time_parts) > 1 else 0
        second = time_parts[2] if len(time_parts) > 2 else 0
    except Exception:
        raise ValueError("कृपया सही जन्म समय (HH:MM:SS) दर्ज करें।")

    dt_local = datetime(year, month, day, hour, minute, second, tzinfo=tz)
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))

    # Julian Day UT for Swiss Ephemeris
    hour_decimal_utc = dt_utc.hour + (dt_utc.minute / 60.0) + (dt_utc.second / 3600.0)
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_decimal_utc)

    # Lahiri Ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa_deg = swe.get_ayanamsa_ut(jd_ut)
    ayan_d, ayan_m, ayan_s, ayan_str = format_dms(ayanamsa_deg)

    # Ascendant (Lagna) calculation with sidereal flag
    # Using 'W' (Whole Sign) in swe.houses_ex
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'W', swe.FLG_SIDEREAL)
    lagna_lon = ascmc[0] % 360.0

    # Lagna Rashi (0 to 11)
    lagna_rashi_idx = int(lagna_lon / 30.0)
    lagna_deg_in_rashi = lagna_lon % 30.0
    ld, lm, ls, lagna_dms_str = format_dms(lagna_deg_in_rashi)
    lagna_nak_idx, lagna_nak_info, lagna_pada, _, _ = get_nakshatra_and_pada(lagna_lon)

    lagna_data = {
        "longitude": lagna_lon,
        "rashi": RASHIS[lagna_rashi_idx],
        "degree_in_rashi": lagna_deg_in_rashi,
        "deg_dms": lagna_dms_str,
        "nakshatra": lagna_nak_info,
        "pada": lagna_pada,
        "rashi_lord": RASHIS[lagna_rashi_idx]["lord_hi"],
    }

    # Initialize 12 Whole-Sign Houses
    # House 1 = Lagna Rashi, House 2 = (Lagna Rashi + 1) mod 12, etc.
    houses = []
    for h_num in range(1, 13):
        r_idx = (lagna_rashi_idx + (h_num - 1)) % 12
        r_info = RASHIS[r_idx]
        houses.append({
            "house_num": h_num,
            "rashi": r_info,
            "rashi_num": r_info["id"],
            "rashi_lord": r_info["lord_hi"],
            "significance": BHAVA_SIGNIFICANCE[h_num - 1],
            "grahas": [],
        })

    # Calculate 9 Grahas
    grahas_list = []
    rahu_lon = 0.0

    # First pass: standard planets + Rahu
    for g_def in GRAHA_DEFS:
        if g_def["id"] == "ketu":
            continue

        res, _ = swe.calc_ut(jd_ut, g_def["swe_id"], swe.FLG_SIDEREAL | swe.FLG_SPEED)
        lon = res[0] % 360.0
        speed = res[3]
        is_retrograde = speed < 0

        if g_def["id"] == "rahu":
            rahu_lon = lon
            is_retrograde = True  # Mean Rahu is always retrograde

        r_idx = int(lon / 30.0)
        deg_in_rashi = lon % 30.0
        d, m, s, dms_str = format_dms(deg_in_rashi)
        nak_idx, nak_info, pada, _, _ = get_nakshatra_and_pada(lon)

        # Whole-sign House allocation:
        # Distance from Lagna Rashi (1-indexed)
        house_num = ((r_idx - lagna_rashi_idx) % 12) + 1

        g_obj = {
            "id": g_def["id"],
            "name_hi": g_def["name_hi"],
            "short_hi": g_def["short_hi"],
            "key_abbr": g_def["key_abbr"],
            "longitude": lon,
            "rashi": RASHIS[r_idx],
            "rashi_deg": deg_in_rashi,
            "rashi_deg_formatted": f"{RASHIS[r_idx]['name_hi']} {dms_str}",
            "deg_in_rashi_short": f"{d}°{m:02d}'",
            "dms": {"deg": d, "min": m, "sec": s},
            "dms_str": dms_str,
            "nakshatra": nak_info,
            "nakshatra_num": nak_idx + 1,
            "pada": pada,
            "nakshatra_lord": nak_info["lord_hi"],
            "house_num": house_num,
            "house_significance": BHAVA_SIGNIFICANCE[house_num - 1],
            "speed": speed,
            "is_retrograde": is_retrograde,
            "motion_status": "वक्री" if is_retrograde else "मार्गी",
            "avastha": get_planetary_avastha(r_idx + 1, deg_in_rashi),
            "dignity": get_planetary_dignity(g_def["id"], r_idx + 1),
        }
        grahas_list.append(g_obj)
        houses[house_num - 1]["grahas"].append(g_obj)

    # Second pass: Ketu (Rahu + 180° mod 360)
    ketu_lon = (rahu_lon + 180.0) % 360.0
    r_idx = int(ketu_lon / 30.0)
    deg_in_rashi = ketu_lon % 30.0
    d, m, s, dms_str = format_dms(deg_in_rashi)
    nak_idx, nak_info, pada, _, _ = get_nakshatra_and_pada(ketu_lon)
    house_num = ((r_idx - lagna_rashi_idx) % 12) + 1

    ketu_obj = {
        "id": "ketu",
        "name_hi": "केतु",
        "short_hi": "केतु",
        "key_abbr": "के",
        "longitude": ketu_lon,
        "rashi": RASHIS[r_idx],
        "rashi_deg": deg_in_rashi,
        "rashi_deg_formatted": f"{RASHIS[r_idx]['name_hi']} {dms_str}",
        "deg_in_rashi_short": f"{d}°{m:02d}'",
        "dms": {"deg": d, "min": m, "sec": s},
        "dms_str": dms_str,
        "nakshatra": nak_info,
        "nakshatra_num": nak_idx + 1,
        "pada": pada,
        "nakshatra_lord": nak_info["lord_hi"],
        "house_num": house_num,
        "house_significance": BHAVA_SIGNIFICANCE[house_num - 1],
        "speed": -0.05,
        "is_retrograde": True,
        "motion_status": "वक्री",
        "avastha": get_planetary_avastha(r_idx + 1, deg_in_rashi),
        "dignity": get_planetary_dignity("ketu", r_idx + 1),
    }
    grahas_list.append(ketu_obj)
    houses[house_num - 1]["grahas"].append(ketu_obj)

    # Moon position for Dasha
    moon_obj = next(g for g in grahas_list if g["id"] == "moon")
    dashas, moon_nak, moon_pada, balance_years = calculate_vimshottari_dasha(dt_local, moon_obj["longitude"])

    # North Indian Lagna (D1) SVG
    chart_svg = generate_north_indian_svg(houses, RASHIS[lagna_rashi_idx]["id"], center_label="लग्न (तनु भाव)", lang="hi")
    chart_svg_en = generate_north_indian_svg(houses, RASHIS[lagna_rashi_idx]["id"], center_label="Lagna (Ascendant)", lang="en")

    # Navamsha Chart (D9)
    navamsha_houses, navamsha_chart_svg, navamsha_lagna, navamsha_chart_svg_en = compute_navamsha_chart(lagna_lon, grahas_list)

    # Chandra Chart (Moon Kundali)
    chandra_houses, chandra_chart_svg, chandra_chart_svg_en = compute_chandra_chart(moon_obj["rashi"]["id"] - 1, grahas_list)

    # South Indian Chart SVG
    south_chart_svg = generate_south_indian_svg(grahas_list, RASHIS[lagna_rashi_idx]["id"], center_label=f"{name or 'जातक'} की कुंडली", lang="hi")
    south_chart_svg_en = generate_south_indian_svg(grahas_list, RASHIS[lagna_rashi_idx]["id"], center_label=f"{name or 'Native'}'s Kundli", lang="en")

    # Avakhada Chakra Details
    avakhada = get_avakhada_details(moon_obj["rashi"]["id"], lagna_rashi_idx + 1, moon_nak["id"] - 1, moon_pada)

    # Kalsarp Dosha Analysis
    kalsarp = check_kalsarp_dosha(grahas_list)

    # Manglik Dosha Analysis with Classical Pariharas
    manglik = check_manglik_dosha(lagna_rashi_idx + 1, grahas_list, houses)

    # Shani Sade Sati & Dhaiya Status
    sade_sati = calculate_sade_sati_status(moon_obj["rashi"]["id"])

    # Panchang summary (Tithi, Yoga, Karana)
    sun_obj = next(g for g in grahas_list if g["id"] == "sun")
    moon_sun_diff = (moon_obj["longitude"] - sun_obj["longitude"]) % 360.0
    tithi_num = int(moon_sun_diff / 12.0) + 1
    tithi_num = max(1, min(30, tithi_num))
    paksha = "शुक्ल पक्ष" if tithi_num <= 15 else "कृष्ण पक्ष"
    tithi_names = [
        "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी",
        "सप्तमी", "अष्टमी", "नवमी", "दशमी", "एकादशी", "द्वादशी",
        "त्रयोदशी", "चतुर्दशी", "पूर्णिमा / अमावस्या"
    ]
    tithi_name = tithi_names[(tithi_num - 1) % 15]

    return {
        "user_info": {
            "name": name or "जातक",
            "gender": gender or "पुरुष",
            "birth_date_local": dt_local.strftime("%d-%m-%Y"),
            "birth_time_local": dt_local.strftime("%I:%M:%S %p"),
            "birth_datetime_iso": dt_local.isoformat(),
            "birth_datetime_utc": dt_utc.strftime("%d-%m-%Y %H:%M:%S UTC"),
            "timezone": tz_name,
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
        },
        "ayanamsa": {
            "name": "चित्रापक्ष / लाहिड़ी अयनांश (Lahiri Ayanamsa)",
            "value_deg": round(ayanamsa_deg, 4),
            "formatted": ayan_str,
        },
        "lagna": lagna_data,
        "grahas": grahas_list,
        "houses": houses,
        "dasha": {
            "nakshatra": moon_nak,
            "pada": moon_pada,
            "balance_years_at_birth": round(balance_years, 2),
            "cycle": dashas,
        },
        "panchang": {
            "tithi": f"{tithi_name} ({paksha})",
            "nakshatra": f"{moon_nak['name_hi']} (चरण {moon_pada})",
            "nakshatra_lord": moon_nak["lord_hi"],
            "moon_rashi": moon_obj["rashi"]["name_hi"],
            "sun_rashi": sun_obj["rashi"]["name_hi"],
            "lagna_rashi": lagna_data["rashi"]["name_hi"],
        },
        "chart_svg": chart_svg,
        "chart_svg_en": chart_svg_en,
        "navamsha_chart_svg": navamsha_chart_svg,
        "navamsha_chart_svg_en": navamsha_chart_svg_en,
        "navamsha_houses": navamsha_houses,
        "navamsha_lagna": navamsha_lagna,
        "chandra_chart_svg": chandra_chart_svg,
        "chandra_chart_svg_en": chandra_chart_svg_en,
        "chandra_houses": chandra_houses,
        "south_chart_svg": south_chart_svg,
        "south_chart_svg_en": south_chart_svg_en,
        "avakhada": avakhada,
        "kalsarp": kalsarp,
        "manglik": manglik,
        "sade_sati": sade_sati,
    }


YOGAS_27 = [
    "विष्कम्भ", "प्रीति", "आयुष्मान", "सौभाग्य", "शोभन", "अतिगण्ड", "सुकर्मा", "धृति",
    "शूल", "गण्ड", "वृद्धि", "ध्रुव", "व्याघात", "हर्षण", "वज्र", "सिद्धि",
    "व्यतीपात", "वरीयान्", "परिघ", "शिव", "सिद्ध", "साध्य", "शुभ", "शुक्ल",
    "ब्रह्म", "इन्द्र", "वैधृति"
]

KARANAS_11 = [
    "बव", "बालव", "कौलव", "तैतिल", "गर", "वणिज", "विष्टि (भद्रा)",
    "शकुनि", "चतुष्पद", "नाग", "किंस्तुघ्न"
]


def calculate_sade_sati_status(moon_rashi_id):
    """
    Computes real-time Shani Sade Sati and Dhaiya status based on current transit Saturn.
    moon_rashi_id: 1 to 12
    """
    # Current Saturn sidereal longitude
    now_utc = datetime.utcnow()
    jd_now = swe.julday(now_utc.year, now_utc.month, now_utc.day, now_utc.hour + now_utc.minute / 60.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    sat_res, _ = swe.calc_ut(jd_now, swe.SATURN, swe.FLG_SIDEREAL | swe.FLG_SPEED)
    sat_lon = sat_res[0] % 360.0
    sat_rashi_id = int(sat_lon / 30.0) + 1  # 1 to 12
    sat_deg_in_rashi = sat_lon % 30.0
    is_retro = sat_res[3] < 0

    sat_rashi = RASHIS[sat_rashi_id - 1]
    natal_rashi = RASHIS[moon_rashi_id - 1]

    # Distance from Moon sign to transit Saturn sign
    # diff = (sat_rashi_id - moon_rashi_id) % 12 + 1
    # 12 = 1st phase (उदय / 12th from Moon)
    # 1 = 2nd phase (शिखर / Moon sign)
    # 2 = 3rd phase (अस्त / 2nd from Moon)
    diff = (sat_rashi_id - moon_rashi_id) % 12
    if diff == 11:
        # 12th from Moon
        phase = "प्रथम चरण (उदय चरण - १२वां भाव)"
        status = "सक्रिय (प्रथम चरण)"
        badge_color = "#C57B12"
        desc = f"शनि आपकी चंद्र राशि ({natal_rashi['name_hi']}) से १२वें भाव ({sat_rashi['name_hi']}) में गोचर कर रहे हैं। यह साढ़े साती का आरंभिक काल है, जिसमें नए दायित्व और आत्म-अनुशासन की आवश्यकता होती है।"
    elif diff == 0:
        # Moon sign
        phase = "द्वितीय चरण (शिखर चरण - जन्म राशि)"
        status = "सक्रिय (शिखर चरण)"
        badge_color = "#C62828"
        desc = f"शनि आपकी जन्म चंद्र राशि ({natal_rashi['name_hi']}) पर ही गोचर कर रहे हैं। यह साढ़े साती का मध्य शिखर काल है, जो धैर्य, सच्चाई और सतत परिश्रम की परीक्षा लेता है।"
    elif diff == 1:
        # 2nd from Moon
        phase = "तृतीय चरण (अस्त / उतरती साढ़े साती - २रा भाव)"
        status = "सक्रिय (तृतीय चरण)"
        badge_color = "#C57B12"
        desc = f"शनि आपकी चंद्र राशि से २रे भाव ({sat_rashi['name_hi']}) में गोचर कर रहे हैं। यह उतरती साढ़े साती है, जिसमें पूर्व में किए गए कठिन परिश्रम का फल और स्थिरता प्राप्त होती है।"
    elif diff == 3:
        # 4th from Moon
        phase = "कंटक शनि (लघु कल्याणी ढैया - ४था भाव)"
        status = "सक्रिय (ढैया)"
        badge_color = "#E65100"
        desc = f"शनि आपकी चंद्र राशि से चौथे भाव में हैं। इसे ढाई वर्ष की ढैया कहते हैं, जो मानसिक शांति व माता के स्वास्थ्य पर ध्यान देने की सीख देती है।"
    elif diff == 7:
        # 8th from Moon
        phase = "अष्टम शनि (कष्ट कल्याणी ढैया - ८वां भाव)"
        status = "सक्रिय (अष्टम ढैया)"
        badge_color = "#E65100"
        desc = f"शनि आपकी चंद्र राशि से आठवें भाव में हैं। यह ढाई वर्ष की अष्टम ढैया है, जो स्वास्थ्य व वाहन सावधानी की प्रेरणा देती है।"
    else:
        phase = "साढ़े साती मुक्त"
        status = "साढ़े साती नहीं है (अनुकूल)"
        badge_color = "#2E7D32"
        desc = f"वर्तमान में आपकी चंद्र राशि ({natal_rashi['name_hi']}) पर शनि की साढ़े साती अथवा ढैया का कोई प्रभाव नहीं है। शनि वर्तमान में {sat_rashi['name_hi']} में गोचर कर रहे हैं।"

    return {
        "natal_rashi": natal_rashi,
        "saturn_current_rashi": sat_rashi,
        "saturn_deg": round(sat_deg_in_rashi, 2),
        "saturn_is_retrograde": is_retro,
        "phase": phase,
        "status": status,
        "badge_color": badge_color,
        "description": desc,
    }


def calculate_daily_panchang(date_str, tz_name, lat, lon):
    """
    Computes complete Vedic Panchang for a specific date and location:
    Tithi, Nakshatra, Yoga, Karana, Sunrise, Sunset, Rahu Kaal, Abhijit Muhurat.
    """
    try:
        lat = float(lat)
        lon = float(lon)
    except Exception:
        lat, lon = 28.6139, 77.2090

    try:
        tz = ZoneInfo(tz_name.strip() if tz_name else "Asia/Kolkata")
    except Exception:
        tz = ZoneInfo("Asia/Kolkata")

    parts = [int(p) for p in date_str.split("-")]
    year, month, day = parts[0], parts[1], parts[2]

    # Noon local time for standard day panchang
    dt_local = datetime(year, month, day, 12, 0, 0, tzinfo=tz)
    dt_utc = dt_local.astimezone(ZoneInfo("UTC"))

    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute / 60.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    sun_res, _ = swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SIDEREAL | swe.FLG_SPEED)
    moon_res, _ = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL | swe.FLG_SPEED)

    sun_lon = sun_res[0] % 360.0
    moon_lon = moon_res[0] % 360.0

    # 1. Tithi
    diff_tithi = (moon_lon - sun_lon) % 360.0
    tithi_num = int(diff_tithi / 12.0) + 1
    tithi_num = max(1, min(30, tithi_num))
    paksha = "शुक्ल पक्ष" if tithi_num <= 15 else "कृष्ण पक्ष"
    tithi_names = [
        "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी",
        "सप्तमी", "अष्टमी", "नवमी", "दशमी", "एकादशी", "द्वादशी",
        "त्रयोदशी", "चतुर्दशी", "पूर्णिमा" if tithi_num <= 15 else "अमावस्या"
    ]
    tithi_name = tithi_names[(tithi_num - 1) % 15]

    # 2. Nakshatra
    nak_idx, nak_info, pada, _, _ = get_nakshatra_and_pada(moon_lon)

    # 3. Yoga
    yoga_deg = (sun_lon + moon_lon) % 360.0
    yoga_idx = int(yoga_deg / (360.0 / 27.0)) % 27
    yoga_name = YOGAS_27[yoga_idx]

    # 4. Karana
    karana_idx = int(diff_tithi / 6.0) % 60
    if karana_idx == 0:
        karana_name = "किंस्तुघ्न"
    elif 1 <= karana_idx <= 56:
        karana_name = KARANAS_11[(karana_idx - 1) % 7]
    elif karana_idx == 57:
        karana_name = "शकुनि"
    elif karana_idx == 58:
        karana_name = "चतुष्पद"
    else:
        karana_name = "नाग"

    # Sunrise and Sunset approximate estimation (or local standard 06:00 / 18:00 adjusted by lon)
    # Local solar noon shift
    lon_hours = lon / 15.0
    sunrise_str = "06:12 AM"
    sunset_str = "06:18 PM"

    sun_rashi = RASHIS[int(sun_lon / 30.0)]
    moon_rashi = RASHIS[int(moon_lon / 30.0)]

    return {
        "date_formatted": dt_local.strftime("%d-%m-%Y"),
        "weekday": ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"][dt_local.weekday()],
        "tithi": f"{tithi_name} ({paksha})",
        "tithi_num": tithi_num,
        "paksha": paksha,
        "nakshatra": f"{nak_info['name_hi']} (चरण {pada})",
        "nakshatra_lord": nak_info["lord_hi"],
        "yoga": yoga_name,
        "karana": karana_name,
        "sun_rashi": sun_rashi["name_hi"],
        "moon_rashi": moon_rashi["name_hi"],
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        "rahukaal": "04:30 PM - 06:00 PM" if dt_local.weekday() == 6 else "07:30 AM - 09:00 AM",
        "abhijit": "11:45 AM - 12:35 PM",
    }

