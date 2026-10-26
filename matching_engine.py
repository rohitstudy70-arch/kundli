"""
Vedic Kundali Matching Engine (Ashta Kuta - 36 Gun Milan System)
Calculates all 8 Kutas (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi)
along with Manglik compatibility analysis and Dosha Parihara exceptions.
"""

import os
import sys

# Ensure .venv site-packages (pyswisseph, tzdata) are accessible
venv_site_packages = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "Lib", "site-packages")
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

from kundli_engine import calculate_kundli, RASHIS, NAKSHATRAS

# ==========================================
# 1. VARNA (वर्ण - 1 Point)
# ==========================================
# Brahmin: Cancer(4), Scorpio(8), Pisces(12) [Water signs]
# Kshatriya: Aries(1), Leo(5), Sagittarius(9) [Fire signs]
# Vaishya: Taurus(2), Virgo(6), Capricorn(10) [Earth signs]
# Shudra: Gemini(3), Libra(7), Aquarius(11) [Air signs]
RASHI_VARNA = {
    4: (4, "ब्राह्मण"), 8: (4, "ब्राह्मण"), 12: (4, "ब्राह्मण"),
    1: (3, "क्षत्रिय"), 5: (3, "क्षत्रिय"), 9: (3, "क्षत्रिय"),
    2: (2, "वैश्य"), 6: (2, "वैश्य"), 10: (2, "वैश्य"),
    3: (1, "शूद्र"), 7: (1, "शूद्र"), 11: (1, "शूद्र"),
}

# ==========================================
# 2. VASHYA (वश्य - 2 Points)
# ==========================================
# 1=Chatushpada(Quadruped), 2=Manava/Dvipada(Human), 3=Jalachara(Water), 4=Vanachara(Wild/Lion), 5=Keeta(Insect/Scorpio)
RASHI_VASHYA = {
    1: "चतुष्पद", 2: "चतुष्पद", 3: "मानव", 4: "जलचर", 5: "वनचर",
    6: "मानव", 7: "मानव", 8: "कीट", 9: "मानव", 10: "जलचर",
    11: "मानव", 12: "जलचर"
}

VASHYA_SCORES = {
    ("चतुष्पद", "चतुष्पद"): 2,
    ("चतुष्पद", "मानव"): 1,
    ("चतुष्पद", "जलचर"): 1,
    ("चतुष्पद", "वनचर"): 0,
    ("चतुष्पद", "कीट"): 1,

    ("मानव", "मानव"): 2,
    ("मानव", "चतुष्पद"): 0.5,
    ("मानव", "जलचर"): 0.5,
    ("मानव", "वनचर"): 0,
    ("मानव", "कीट"): 1,

    ("जलचर", "जलचर"): 2,
    ("जलचर", "चतुष्पद"): 1,
    ("जलचर", "मानव"): 1,
    ("जलचर", "वनचर"): 0,
    ("जलचर", "कीट"): 1,

    ("वनचर", "वनचर"): 2,
    ("वनचर", "चतुष्पद"): 0,
    ("वनचर", "मानव"): 0,
    ("वनचर", "जलचर"): 0,
    ("वनचर", "कीट"): 0,

    ("कीट", "कीट"): 2,
    ("कीट", "चतुष्पद"): 1,
    ("कीट", "मानव"): 1,
    ("कीट", "जलचर"): 1,
    ("कीट", "वनचर"): 0,
}

# ==========================================
# 3. TARA (तारा - 3 Points)
# ==========================================
# 9 Taras: 1=Janma, 2=Sampat, 3=Vipat, 4=Kshema, 5=Pratyari, 6=Sadhak, 7=Vadha, 8=Mitra, 9=Parama Mitra
# Malefic Taras: 3, 5, 7

# ==========================================
# 4. YONI (योनि - 4 Points)
# ==========================================
# 14 Yonis mapped to 27 Nakshatras (0-indexed nakshatra id 0-26)
NAKSHATRA_YONI = {
    0: "अश्व",   # Ashwini
    23: "अश्व",  # Shatabhisha
    1: "गज",    # Bharani
    26: "गज",   # Revati
    2: "मेष",   # Krittika
    7: "मेष",   # Pushya
    3: "सर्प",   # Rohini
    4: "सर्प",   # Mrigashira
    18: "श्वान", # Mula
    5: "श्वान",  # Ardra
    6: "मार्जार",# Punarvasu
    8: "मार्जार",# Ashlesha
    9: "मूषक",   # Magha
    10: "मूषक",  # Purva Phalguni
    11: "गौ",    # Uttara Phalguni
    25: "गौ",    # Uttara Bhadrapada
    12: "महिष",  # Hasta
    14: "महिष",  # Swati
    13: "व्याघ्र",# Chitra
    15: "व्याघ्र",# Vishakha
    16: "मृग",   # Anuradha
    17: "मृग",   # Jyeshtha
    19: "वानर",  # Purva Ashadha
    21: "वानर",  # Shravana
    20: "नकुल",  # Uttara Ashadha
    22: "सिंह",  # Dhanishta
    24: "सिंह",  # Purva Bhadrapada
}

# Inimical enemy pairs (0 points)
YONI_ENEMIES = {
    ("अश्व", "महिष"), ("महिष", "अश्व"),
    ("गज", "सिंह"), ("सिंह", "गज"),
    ("मेष", "वानर"), ("वानर", "मेष"),
    ("सर्प", "नकुल"), ("नकुल", "सर्प"),
    ("श्वान", "मृग"), ("मृग", "श्वान"),
    ("मार्जार", "मूषक"), ("मूषक", "मार्जार"),
    ("गौ", "व्याघ्र"), ("व्याघ्र", "गौ"),
}

# ==========================================
# 5. GRAHA MAITRI (ग्रहमैत्री - 5 Points)
# ==========================================
PLANET_FRIENDS = {
    "सूर्य": {"friends": ["चन्द्र", "मंगल", "गुरु"], "neutrals": ["बुध"], "enemies": ["शुक्र", "शनि"]},
    "चन्द्र": {"friends": ["सूर्य", "बुध"], "neutrals": ["मंगल", "गुरु", "शुक्र", "शनि"], "enemies": []},
    "मंगल": {"friends": ["सूर्य", "चन्द्र", "गुरु"], "neutrals": ["शुक्र", "शनि"], "enemies": ["बुध"]},
    "बुध": {"friends": ["सूर्य", "शुक्र"], "neutrals": ["मंगल", "गुरु", "शनि"], "enemies": ["चन्द्र"]},
    "गुरु": {"friends": ["सूर्य", "चन्द्र", "मंगल"], "neutrals": ["शनि"], "enemies": ["बुध", "शुक्र"]},
    "शुक्र": {"friends": ["बुध", "शनि"], "neutrals": ["मंगल", "गुरु"], "enemies": ["सूर्य", "चन्द्र"]},
    "शनि": {"friends": ["बुध", "शुक्र"], "neutrals": ["गुरु"], "enemies": ["सूर्य", "चन्द्र", "मंगल"]},
}

# ==========================================
# 6. GANA (गण - 6 Points)
# ==========================================
# Deva, Manushya, Rakshasa
NAKSHATRA_GANA = {
    0: "देव", 4: "देव", 6: "देव", 7: "देव", 12: "देव", 14: "देव", 16: "देव", 21: "देव", 26: "देव",
    1: "मनुष्य", 3: "मनुष्य", 5: "मनुष्य", 10: "मनुष्य", 11: "मनुष्य", 19: "मनुष्य", 20: "मनुष्य", 24: "मनुष्य", 25: "मनुष्य",
    2: "राक्षस", 8: "राक्षस", 9: "राक्षस", 13: "राक्षस", 15: "राक्षस", 17: "राक्षस", 18: "राक्षस", 22: "राक्षस", 23: "राक्षस"
}

# ==========================================
# 8. NADI (नाड़ी - 8 Points)
# ==========================================
# Adi (Vata), Madhya (Pitta), Antya (Kapha)
NAKSHATRA_NADI = {
    0: "आदि", 5: "आदि", 6: "आदि", 11: "आदि", 12: "आदि", 17: "आदि", 18: "आदि", 23: "आदि", 24: "आदि",
    1: "मध्य", 4: "मध्य", 7: "मध्य", 10: "मध्य", 13: "मध्य", 16: "मध्य", 19: "मध्य", 22: "मध्य", 25: "मध्य",
    2: "अंत्य", 3: "अंत्य", 8: "अंत्य", 9: "अंत्य", 14: "अंत्य", 15: "अंत्य", 20: "अंत्य", 21: "अंत्य", 26: "अंत्य"
}


def calculate_ashta_kuta(groom_data, bride_data):
    """
    Computes all 8 Kutas (36 Guns) for marriage matching between Groom and Bride.
    """
    groom_moon = next(g for g in groom_data["grahas"] if g["id"] == "moon")
    bride_moon = next(g for g in bride_data["grahas"] if g["id"] == "moon")

    g_rashi_id = groom_moon["rashi"]["id"]      # 1 to 12
    b_rashi_id = bride_moon["rashi"]["id"]      # 1 to 12

    g_nak_idx = groom_moon["nakshatra_num"] - 1 # 0 to 26
    b_nak_idx = bride_moon["nakshatra_num"] - 1 # 0 to 26

    g_pada = groom_moon["pada"]
    b_pada = bride_moon["pada"]

    g_lord = groom_moon["rashi"]["lord_hi"]
    b_lord = bride_moon["rashi"]["lord_hi"]

    kutas = []

    # ----------------------------------------------------
    # 1. VARNA (वर्ण - 1 अंक)
    # ----------------------------------------------------
    g_v_score, g_v_name = RASHI_VARNA[g_rashi_id]
    b_v_score, b_v_name = RASHI_VARNA[b_rashi_id]
    if g_v_score >= b_v_score:
        varna_pts = 1
        varna_desc = f"वर का वर्ण ({g_v_name}) वधू के वर्ण ({b_v_name}) के अनुकूल है।"
    else:
        varna_pts = 0
        varna_desc = f"वर का वर्ण ({g_v_name}) वधू के वर्ण ({b_v_name}) से भिन्न होने से ० अंक प्राप्त।"

    kutas.append({
        "name_hi": "वर्ण (Varna)",
        "area": "कार्य प्रवृत्ति व आध्यात्मिक अनुकूलता",
        "max_points": 1,
        "obtained_points": varna_pts,
        "groom_val": g_v_name,
        "bride_val": b_v_name,
        "description": varna_desc
    })

    # ----------------------------------------------------
    # 2. VASHYA (वश्य - 2 अंक)
    # ----------------------------------------------------
    g_vashya = RASHI_VASHYA[g_rashi_id]
    b_vashya = RASHI_VASHYA[b_rashi_id]
    vashya_pts = VASHYA_SCORES.get((g_vashya, b_vashya), 0)
    if vashya_pts == 2:
        vashya_desc = f"वर ({g_vashya}) और वधू ({b_vashya}) में पूर्ण पारस्परिक आकर्षण व वश्यता है।"
    elif vashya_pts > 0:
        vashya_desc = f"वर ({g_vashya}) और वधू ({b_vashya}) में सामान्य सामंजस्य है।"
    else:
        vashya_desc = f"वर ({g_vashya}) और वधू ({b_vashya}) में वश्यता का अभाव है।"

    kutas.append({
        "name_hi": "वश्य (Vashya)",
        "area": "पारस्परिक प्रभाव व मानसिक आकर्षण",
        "max_points": 2,
        "obtained_points": vashya_pts,
        "groom_val": g_vashya,
        "bride_val": b_vashya,
        "description": vashya_desc
    })

    # ----------------------------------------------------
    # 3. TARA (तारा - 3 अंक)
    # ----------------------------------------------------
    # Count nakshatra distance mod 9
    d_g_to_b = ((b_nak_idx - g_nak_idx) % 27 + 1)
    tara_b = d_g_to_b % 9
    if tara_b == 0: tara_b = 9

    d_b_to_g = ((g_nak_idx - b_nak_idx) % 27 + 1)
    tara_g = d_b_to_g % 9
    if tara_g == 0: tara_g = 9

    malefic_taras = {3, 5, 7}
    g_good = tara_g not in malefic_taras
    b_good = tara_b not in malefic_taras

    if g_good and b_good:
        tara_pts = 3
        tara_desc = "दोनों की ताराएं शुभ हैं (भाग्य व आयु के लिए उत्तम)।"
    elif g_good or b_good:
        tara_pts = 1.5
        tara_desc = "एक पक्ष की तारा शुभ और दूसरे पक्ष की सामान्य होने से मध्यम अंक प्राप्त।"
    else:
        tara_pts = 0
        tara_desc = "दोनों पक्षों में तारा प्रतिकूल होने से शून्य अंक।"

    kutas.append({
        "name_hi": "तारा (Tara / Dina)",
        "area": "स्वास्थ्य, भाग्य व दीर्घायु",
        "max_points": 3,
        "obtained_points": tara_pts,
        "groom_val": f"तारा {tara_g}",
        "bride_val": f"तारा {tara_b}",
        "description": tara_desc
    })

    # ----------------------------------------------------
    # 4. YONI (योनि - 4 अंक)
    # ----------------------------------------------------
    g_yoni = NAKSHATRA_YONI.get(g_nak_idx, "अश्व")
    b_yoni = NAKSHATRA_YONI.get(b_nak_idx, "अश्व")

    if g_yoni == b_yoni:
        yoni_pts = 4
        yoni_desc = f"दोनों की एक ही योनि ({g_yoni}) है। शारीरिक व मानसिक सामंजस्य अति उत्तम।"
    elif (g_yoni, b_yoni) in YONI_ENEMIES:
        yoni_pts = 0
        yoni_desc = f"{g_yoni} और {b_yoni} में स्वाभाविक शत्रुता (योनि वैर) है।"
    else:
        yoni_pts = 2
        yoni_desc = f"{g_yoni} और {b_yoni} योनि में परस्पर सामान्य सामंजस्य है।"

    kutas.append({
        "name_hi": "योनि (Yoni)",
        "area": "दाम्पत्य सुख व शारीरिक अनुकूलता",
        "max_points": 4,
        "obtained_points": yoni_pts,
        "groom_val": g_yoni,
        "bride_val": b_yoni,
        "description": yoni_desc
    })

    # ----------------------------------------------------
    # 5. GRAHA MAITRI (ग्रहमैत्री - 5 अंक)
    # ----------------------------------------------------
    if g_lord == b_lord:
        maitri_pts = 5
        maitri_desc = f"दोनों राशियों के स्वामी एक ही ग्रह ({g_lord}) हैं। परम मित्रता।"
    else:
        g_view = "friend" if b_lord in PLANET_FRIENDS[g_lord]["friends"] else ("neutral" if b_lord in PLANET_FRIENDS[g_lord]["neutrals"] else "enemy")
        b_view = "friend" if g_lord in PLANET_FRIENDS[b_lord]["friends"] else ("neutral" if g_lord in PLANET_FRIENDS[b_lord]["neutrals"] else "enemy")

        if g_view == "friend" and b_view == "friend":
            maitri_pts = 5
            maitri_desc = f"{g_lord} और {b_lord} परस्पर परम मित्र हैं।"
        elif (g_view == "friend" and b_view == "neutral") or (b_view == "friend" and g_view == "neutral"):
            maitri_pts = 4
            maitri_desc = f"{g_lord} और {b_lord} में मित्रता व समभाव है।"
        elif g_view == "neutral" and b_view == "neutral":
            maitri_pts = 3
            maitri_desc = f"{g_lord} और {b_lord} दोनों सम हैं।"
        elif (g_view == "friend" and b_view == "enemy") or (b_view == "friend" and g_view == "enemy"):
            maitri_pts = 1
            maitri_desc = f"{g_lord} और {b_lord} में एकतरफ़ा मित्रता व विरोध है।"
        else:
            maitri_pts = 0
            maitri_desc = f"{g_lord} और {b_lord} में स्वाभाविक शत्रुता है।"

    kutas.append({
        "name_hi": "ग्रहमैत्री (Graha Maitri)",
        "area": "मानसिक समझ, मित्रता व बौद्धिक तालमेल",
        "max_points": 5,
        "obtained_points": maitri_pts,
        "groom_val": f"{g_lord} (राशि {groom_moon['rashi']['name_hi']})",
        "bride_val": f"{b_lord} (राशि {bride_moon['rashi']['name_hi']})",
        "description": maitri_desc
    })

    # ----------------------------------------------------
    # 6. GANA (गण - 6 अंक)
    # ----------------------------------------------------
    g_gana = NAKSHATRA_GANA.get(g_nak_idx, "मनुष्य")
    b_gana = NAKSHATRA_GANA.get(b_nak_idx, "मनुष्य")

    if g_gana == b_gana:
        gana_pts = 6
        gana_desc = f"दोनों का समान गण ({g_gana}) है। स्वभाव व सोच में पूर्ण समरसता।"
    elif (g_gana == "देव" and b_gana == "मनुष्य") or (g_gana == "मनुष्य" and b_gana == "देव"):
        gana_pts = 5
        gana_desc = "देव और मनुष्य गण का मिलान अत्यंत उत्तम व ग्राह्य माना जाता है।"
    elif g_gana == "देव" and b_gana == "राक्षस":
        gana_pts = 1
        gana_desc = "देव और राक्षस गण में स्वभाव भेद रहता है।"
    else:
        gana_pts = 0
        gana_desc = f"वर ({g_gana}) और वधू ({b_gana}) में गण दोष है (स्वभाव में भिन्नता)।"

    kutas.append({
        "name_hi": "गण (Gana)",
        "area": "स्वभाव, आचरण व जीवनशैली",
        "max_points": 6,
        "obtained_points": gana_pts,
        "groom_val": g_gana,
        "bride_val": b_gana,
        "description": gana_desc
    })

    # ----------------------------------------------------
    # 7. BHAKOOT (भकूट - 7 अंक)
    # ----------------------------------------------------
    diff_rashi = ((b_rashi_id - g_rashi_id) % 12) + 1
    # Dosha distances: 2/12 (द्विर्द्वादश), 6/8 (षडाष्टक), 9/5 (नवम-पंचम)
    is_bhakoot_dosha = diff_rashi in (2, 12, 6, 8, 5, 9)

    # Bhakoot Parihara (Exceptions):
    # Same lord (Mesha-Vrischika, Vrishabha-Tula) or friendly lords
    has_bhakoot_parihara = False
    if is_bhakoot_dosha:
        if g_lord == b_lord:
            has_bhakoot_parihara = True
        elif b_lord in PLANET_FRIENDS[g_lord]["friends"] and g_lord in PLANET_FRIENDS[b_lord]["friends"]:
            has_bhakoot_parihara = True

    if not is_bhakoot_dosha or has_bhakoot_parihara:
        bhakoot_pts = 7
        if has_bhakoot_parihara:
            bhakoot_desc = "राशि स्वामियों की मित्रता/समानता के कारण भकूट दोष परिहार होकर पूरे ७ अंक प्राप्त।"
        else:
            bhakoot_desc = "दोनों की राशियों में शुभ संबंध (१/७, ३/११ या ४/१०) है।"
    else:
        bhakoot_pts = 0
        bhakoot_desc = f"राशियों में {diff_rashi} भाव का अंतर होने से भकूट दोष बनता है।"

    kutas.append({
        "name_hi": "भकूट (Bhakoot)",
        "area": "परिवार वृद्धि, सुख-समृद्धि व प्रेम",
        "max_points": 7,
        "obtained_points": bhakoot_pts,
        "groom_val": f"{groom_moon['rashi']['name_hi']} ({g_rashi_id})",
        "bride_val": f"{bride_moon['rashi']['name_hi']} ({b_rashi_id})",
        "description": bhakoot_desc
    })

    # ----------------------------------------------------
    # 8. NADI (नाड़ी - 8 अंक)
    # ----------------------------------------------------
    g_nadi = NAKSHATRA_NADI.get(g_nak_idx, "मध्य")
    b_nadi = NAKSHATRA_NADI.get(b_nak_idx, "मध्य")

    is_nadi_dosha = (g_nadi == b_nadi)
    has_nadi_parihara = False

    if is_nadi_dosha:
        # Classical Nadi Parihar rules:
        # 1. Different Rashi, same Nakshatra (e.g. Kritika 1 in Aries, Kritika 2 in Taurus)
        # 2. Same Rashi, different Nakshatra
        # 3. Same Lord
        if g_rashi_id != b_rashi_id and g_nak_idx == b_nak_idx:
            has_nadi_parihara = True
        elif g_rashi_id == b_rashi_id and g_nak_idx != b_nak_idx:
            has_nadi_parihara = True
        elif g_lord == b_lord:
            has_nadi_parihara = True

    if not is_nadi_dosha or has_nadi_parihara:
        nadi_pts = 8
        if has_nadi_parihara:
            nadi_desc = f"समान नाड़ी ({g_nadi}) होते हुए भी नक्षत्र/राशि भिन्नता से नाड़ी दोष परिहार लागू (८ अंक)।"
        else:
            nadi_desc = f"वर ({g_nadi}) और वधू ({b_nadi}) की भिन्न नाड़ी होने से उत्तम आनुवंशिक व स्वास्थ्य अनुकूलता।"
    else:
        nadi_pts = 0
        nadi_desc = f"दोनों की एक ही नाड़ी ({g_nadi}) होने से नाड़ी दोष माना जाता है।"

    kutas.append({
        "name_hi": "नाड़ी (Nadi)",
        "area": "आनुवंशिकी, संतान स्वास्थ्य व जीवन शक्ति",
        "max_points": 8,
        "obtained_points": nadi_pts,
        "groom_val": g_nadi,
        "bride_val": b_nadi,
        "description": nadi_desc
    })

    # Total Score
    total_score = sum(k["obtained_points"] for k in kutas)

    # Compatibility Verdict
    if total_score >= 28:
        verdict_badge = "अति उत्तम मिलान (Excellent)"
        verdict_desc = "३६ में से २८ या अधिक गुण मिलना अत्यंत शुभ और सौभाग्यवर्धक माना जाता है।"
        verdict_color = "#2E7D32"
    elif total_score >= 18:
        verdict_badge = "उत्तम / ग्राह्य मिलान (Good & Approved)"
        verdict_desc = "१८ से २७ गुण वैवाहिक जीवन के लिए शुभ और सुखद माने जाते हैं।"
        verdict_color = "#C57B12"
    else:
        verdict_badge = "मध्यम / विचारणीय मिलान (Average)"
        verdict_desc = "१८ से कम गुण होने पर अन्य ग्रहों, गुरु-शुक्र की दृष्टि एवं व्यक्तिगत कुंडलियों का परीक्षण अनुशंसित है।"
        verdict_color = "#C62828"

    # ----------------------------------------------------
    # MANGLIK ANALYSIS (मांगलिक साम्य)
    # ----------------------------------------------------
    g_mars = next(g for g in groom_data["grahas"] if g["id"] == "mars")
    b_mars = next(g for g in bride_data["grahas"] if g["id"] == "mars")

    manglik_houses = {1, 4, 7, 8, 12}
    g_is_manglik = g_mars["house_num"] in manglik_houses
    b_is_manglik = b_mars["house_num"] in manglik_houses

    if g_is_manglik and b_is_manglik:
        manglik_verdict = "दोनों कुंडलियां मांगलिक हैं—मंगल का परस्पर साम्य (दोष निरस्तीकरण) है।"
        manglik_status = "मांगलिक साम्य (उत्तम)"
    elif not g_is_manglik and not b_is_manglik:
        manglik_verdict = "दोनों कुंडलियां सामान्य (अ-मांगलिक) हैं—कोई प्रतिकूलता नहीं।"
        manglik_status = "सामान्य (अनुकूल)"
    elif g_is_manglik and not b_is_manglik:
        manglik_verdict = f"वर मांगलिक (मंगल भाव {g_mars['house_num']}) हैं, जबकि वधू सामान्य हैं।"
        manglik_status = "आंशिक मांगलिक (संतुलन आवश्यक)"
    else:
        manglik_verdict = f"वधू मांगलिक (मंगल भाव {b_mars['house_num']}) हैं, जबकि वर सामान्य हैं।"
        manglik_status = "आंशिक मांगलिक (संतुलन आवश्यक)"

    return {
        "kutas": kutas,
        "total_score": round(total_score, 1),
        "max_score": 36,
        "score_percentage": round((total_score / 36.0) * 100, 1),
        "verdict_badge": verdict_badge,
        "verdict_desc": verdict_desc,
        "verdict_color": verdict_color,
        "manglik_analysis": {
            "groom": {"is_manglik": g_is_manglik, "mars_house": g_mars["house_num"], "status": "मांगलिक" if g_is_manglik else "सामान्य"},
            "bride": {"is_manglik": b_is_manglik, "mars_house": b_mars["house_num"], "status": "मांगलिक" if b_is_manglik else "सामान्य"},
            "verdict": manglik_verdict,
            "status": manglik_status
        },
        "summary": {
            "groom": {
                "name": groom_data["user_info"]["name"],
                "rashi": groom_moon["rashi"]["name_hi"],
                "nakshatra": f"{groom_moon['nakshatra']['name_hi']} (चरण {g_pada})",
                "lagna": groom_data["lagna"]["rashi"]["name_hi"],
            },
            "bride": {
                "name": bride_data["user_info"]["name"],
                "rashi": bride_moon["rashi"]["name_hi"],
                "nakshatra": f"{bride_moon['nakshatra']['name_hi']} (चरण {b_pada})",
                "lagna": bride_data["lagna"]["rashi"]["name_hi"],
            }
        }
    }
