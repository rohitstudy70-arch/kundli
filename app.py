"""
Flask Web Application for Vedic Kundali (Janam Kundali)
Provides clean REST API endpoints, SEO sitemap/robots, about/privacy pages,
and renders single-page responsive mobile-first frontend.
"""

import os
import sys

# Ensure .venv site-packages (pyswisseph, tzdata, etc.) are always loaded
venv_site_packages = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "Lib", "site-packages")
if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

from datetime import datetime

from flask import Flask, render_template, request, jsonify, Response
import urllib.parse
import urllib.request
import json

from kundli_engine import calculate_kundli, calculate_sade_sati_status, calculate_daily_panchang
from matching_engine import calculate_ashta_kuta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


# Default sample chart data for initial page load
DEFAULT_CHART_PARAMS = {
    "name": "रोहित कुमार",
    "gender": "पुरुष",
    "birth_date": "1995-05-15",
    "birth_time": "10:30:00",
    "place_name": "नई दिल्ली, भारत (New Delhi, India)",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata",
}


@app.route("/")
@app.route("/api/index")
def index():
    """Serves the single-page Hindi Kundali application."""
    initial_data = None
    try:
        initial_data = calculate_kundli(
            birth_date_str=DEFAULT_CHART_PARAMS["birth_date"],
            birth_time_str=DEFAULT_CHART_PARAMS["birth_time"],
            tz_name=DEFAULT_CHART_PARAMS["timezone"],
            lat=DEFAULT_CHART_PARAMS["latitude"],
            lon=DEFAULT_CHART_PARAMS["longitude"],
            name=DEFAULT_CHART_PARAMS["name"],
            gender=DEFAULT_CHART_PARAMS["gender"],
        )
        initial_data["place_name"] = DEFAULT_CHART_PARAMS["place_name"]
    except Exception as e:
        app.logger.error(f"Error computing initial chart: {e}")

    return render_template(
        "index.html",
        defaults=DEFAULT_CHART_PARAMS,
        initial_chart=initial_data
    )


DEFAULT_GROOM_PARAMS = {
    "name": "राहुल शर्मा",
    "gender": "पुरुष",
    "birth_date": "1994-04-12",
    "birth_time": "14:20:00",
    "place_name": "नई दिल्ली, भारत",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata",
}

DEFAULT_BRIDE_PARAMS = {
    "name": "पूजा वर्मा",
    "gender": "महिला",
    "birth_date": "1996-08-18",
    "birth_time": "09:30:00",
    "place_name": "जयपुर, राजस्थान, भारत",
    "latitude": 26.9124,
    "longitude": 75.7873,
    "timezone": "Asia/Kolkata",
}


@app.route("/matching")
def matching():
    """Serves the Vedic Kundali Matching (36 Gun Milan) page."""
    try:
        groom_chart = calculate_kundli(
            birth_date_str=DEFAULT_GROOM_PARAMS["birth_date"],
            birth_time_str=DEFAULT_GROOM_PARAMS["birth_time"],
            tz_name=DEFAULT_GROOM_PARAMS["timezone"],
            lat=DEFAULT_GROOM_PARAMS["latitude"],
            lon=DEFAULT_GROOM_PARAMS["longitude"],
            name=DEFAULT_GROOM_PARAMS["name"],
            gender=DEFAULT_GROOM_PARAMS["gender"]
        )
        groom_chart["user_info"]["place_name"] = DEFAULT_GROOM_PARAMS["place_name"]

        bride_chart = calculate_kundli(
            birth_date_str=DEFAULT_BRIDE_PARAMS["birth_date"],
            birth_time_str=DEFAULT_BRIDE_PARAMS["birth_time"],
            tz_name=DEFAULT_BRIDE_PARAMS["timezone"],
            lat=DEFAULT_BRIDE_PARAMS["latitude"],
            lon=DEFAULT_BRIDE_PARAMS["longitude"],
            name=DEFAULT_BRIDE_PARAMS["name"],
            gender=DEFAULT_BRIDE_PARAMS["gender"]
        )
        bride_chart["user_info"]["place_name"] = DEFAULT_BRIDE_PARAMS["place_name"]

        match_res = calculate_ashta_kuta(groom_chart, bride_chart)

        return render_template(
            "matching.html",
            defaults_groom=DEFAULT_GROOM_PARAMS,
            defaults_bride=DEFAULT_BRIDE_PARAMS,
            initial_match=match_res,
            initial_groom_svg=groom_chart["chart_svg"],
            initial_bride_svg=bride_chart["chart_svg"]
        )
    except Exception as e:
        app.logger.error(f"Error computing initial matching: {e}")
        return render_template(
            "matching.html",
            defaults_groom=DEFAULT_GROOM_PARAMS,
            defaults_bride=DEFAULT_BRIDE_PARAMS,
            initial_match=None,
            initial_groom_svg="",
            initial_bride_svg=""
        )


@app.route("/api/match", methods=["POST"])
def api_match():
    """Calculates Ashta Kuta 36 Gun Milan and Manglik compatibility."""
    req_data = request.get_json(silent=True) or {}
    groom = req_data.get("groom", {})
    bride = req_data.get("bride", {})

    # Validation
    for p_name, partner in [("वर (Groom)", groom), ("वधू (Bride)", bride)]:
        if not partner.get("birth_date"):
            return jsonify({"success": False, "message": f"कृपया {p_name} की जन्म तिथि दर्ज करें।"}), 400
        if not partner.get("birth_time"):
            return jsonify({"success": False, "message": f"कृपया {p_name} का जन्म समय दर्ज करें।"}), 400
        try:
            float(partner.get("latitude"))
            float(partner.get("longitude"))
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": f"कृपया {p_name} का स्थान खोज सूची से चुनें ताकि अक्षांश/देशांतर भरे जा सकें।"}), 400

    try:
        groom_chart = calculate_kundli(
            birth_date_str=groom["birth_date"],
            birth_time_str=groom["birth_time"],
            tz_name=groom.get("timezone", "Asia/Kolkata"),
            lat=float(groom["latitude"]),
            lon=float(groom["longitude"]),
            name=groom.get("name", "वर"),
            gender="पुरुष"
        )
        groom_chart["user_info"]["place_name"] = groom.get("place_name", "")

        bride_chart = calculate_kundli(
            birth_date_str=bride["birth_date"],
            birth_time_str=bride["birth_time"],
            tz_name=bride.get("timezone", "Asia/Kolkata"),
            lat=float(bride["latitude"]),
            lon=float(bride["longitude"]),
            name=bride.get("name", "वधू"),
            gender="महिला"
        )
        bride_chart["user_info"]["place_name"] = bride.get("place_name", "")

        match_res = calculate_ashta_kuta(groom_chart, bride_chart)

        return jsonify({
            "success": True,
            "data": {
                "match_result": match_res,
                "groom_chart": groom_chart,
                "bride_chart": bride_chart
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"मिलान गणना में त्रुटि: {str(e)}"}), 400


@app.route("/lagna-calculator")
def lagna_calculator():
    """Renders Lagna Calculator page."""
    params = {
        "name": request.args.get("name", DEFAULT_CHART_PARAMS["name"]),
        "birth_date": request.args.get("birth_date", DEFAULT_CHART_PARAMS["birth_date"]),
        "birth_time": request.args.get("birth_time", DEFAULT_CHART_PARAMS["birth_time"]),
        "place_name": request.args.get("place_name", DEFAULT_CHART_PARAMS["place_name"]),
        "latitude": float(request.args.get("latitude", DEFAULT_CHART_PARAMS["latitude"])),
        "longitude": float(request.args.get("longitude", DEFAULT_CHART_PARAMS["longitude"])),
        "timezone": request.args.get("timezone", DEFAULT_CHART_PARAMS["timezone"]),
    }
    try:
        result = calculate_kundli(
            birth_date_str=params["birth_date"],
            birth_time_str=params["birth_time"],
            tz_name=params["timezone"],
            lat=params["latitude"],
            lon=params["longitude"],
            name=params["name"],
            gender="पुरुष"
        )
    except Exception as e:
        app.logger.error(f"Error computing lagna: {e}")
        result = None

    return render_template("lagna_calculator.html", params=params, result=result)


@app.route("/vimshottari-dasha")
def vimshottari_dasha():
    """Renders Vimshottari Mahadasha timeline page."""
    params = {
        "name": request.args.get("name", DEFAULT_CHART_PARAMS["name"]),
        "birth_date": request.args.get("birth_date", DEFAULT_CHART_PARAMS["birth_date"]),
        "birth_time": request.args.get("birth_time", DEFAULT_CHART_PARAMS["birth_time"]),
        "place_name": request.args.get("place_name", DEFAULT_CHART_PARAMS["place_name"]),
        "latitude": float(request.args.get("latitude", DEFAULT_CHART_PARAMS["latitude"])),
        "longitude": float(request.args.get("longitude", DEFAULT_CHART_PARAMS["longitude"])),
        "timezone": request.args.get("timezone", DEFAULT_CHART_PARAMS["timezone"]),
    }
    try:
        result = calculate_kundli(
            birth_date_str=params["birth_date"],
            birth_time_str=params["birth_time"],
            tz_name=params["timezone"],
            lat=params["latitude"],
            lon=params["longitude"],
            name=params["name"],
            gender="पुरुष"
        )
    except Exception as e:
        app.logger.error(f"Error computing dasha: {e}")
        result = None

    return render_template("vimshottari_dasha.html", params=params, result=result)


@app.route("/nakshatra-calculator")
def nakshatra_calculator():
    """Renders Nakshatra finder page."""
    params = {
        "name": request.args.get("name", DEFAULT_CHART_PARAMS["name"]),
        "birth_date": request.args.get("birth_date", DEFAULT_CHART_PARAMS["birth_date"]),
        "birth_time": request.args.get("birth_time", DEFAULT_CHART_PARAMS["birth_time"]),
        "place_name": request.args.get("place_name", DEFAULT_CHART_PARAMS["place_name"]),
        "latitude": float(request.args.get("latitude", DEFAULT_CHART_PARAMS["latitude"])),
        "longitude": float(request.args.get("longitude", DEFAULT_CHART_PARAMS["longitude"])),
        "timezone": request.args.get("timezone", DEFAULT_CHART_PARAMS["timezone"]),
    }
    try:
        result = calculate_kundli(
            birth_date_str=params["birth_date"],
            birth_time_str=params["birth_time"],
            tz_name=params["timezone"],
            lat=params["latitude"],
            lon=params["longitude"],
            name=params["name"],
            gender="पुरुष"
        )
    except Exception as e:
        app.logger.error(f"Error computing nakshatra: {e}")
        result = None

    return render_template("nakshatra_calculator.html", params=params, result=result)


@app.route("/manglik-dosh")
def manglik_dosh():
    """Renders Manglik Dosh and classical Parihara analysis page."""
    return render_template("manglik_dosh.html")


@app.route("/sade-sati")
def sade_sati():
    """Renders Shani Sade Sati and Dhaiya calculator page."""
    return render_template("sade_sati.html")


@app.route("/panchang")
def panchang():
    """Renders daily Vedic Panchang page."""
    return render_template("panchang.html")


@app.route("/api/sade-sati", methods=["GET"])
def api_sade_sati():
    """Calculates Sade Sati & Dhaiya status for a given Moon rashi ID (1-12)."""
    try:
        moon_rashi_id = int(request.args.get("moon_rashi_id", 1))
        moon_rashi_id = max(1, min(12, moon_rashi_id))
        status = calculate_sade_sati_status(moon_rashi_id)
        return jsonify({"success": True, "data": status})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/panchang", methods=["GET"])
def api_panchang():
    """Calculates complete Vedic Panchang for date, lat, lon and timezone."""
    try:
        date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
        lat = float(request.args.get("lat", 28.6139))
        lon = float(request.args.get("lon", 77.2090))
        tz_name = request.args.get("tz", "Asia/Kolkata")
        res = calculate_daily_panchang(date_str, tz_name, lat, lon)
        return jsonify({"success": True, "data": res})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/about")
def about():
    """Renders the About page in pure original Hindi."""
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    """Renders the Privacy Policy page in pure original Hindi."""
    return render_template("privacy.html")


@app.route("/robots.txt")
def robots_txt():
    """Returns robots.txt for search engine crawlers."""
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Sitemap: http://127.0.0.1:5000/sitemap.xml\n"
    )
    return Response(content, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    """Returns XML sitemap for SEO discovery."""
    today = datetime.now().strftime("%Y-%m-%d")
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://127.0.0.1:5000/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/matching</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.95</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/lagna-calculator</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.90</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/vimshottari-dasha</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.90</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/nakshatra-calculator</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.90</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/manglik-dosh</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/sade-sati</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/panchang</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/about</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.60</priority>
  </url>
  <url>
    <loc>http://127.0.0.1:5000/privacy</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.50</priority>
  </url>
</urlset>"""
    return Response(xml_content, mimetype="application/xml")



@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    """
    Computes Vedic Kundali, Planetary positions, North Indian SVG chart,
    and Vimshottari Mahadasha sequence.
    """
    req_data = request.get_json(silent=True)
    if not req_data:
        req_data = request.form.to_dict()

    name = req_data.get("name", "").strip() or "जातक"
    gender = req_data.get("gender", "पुरुष").strip()
    birth_date = req_data.get("birth_date", "").strip()
    birth_time = req_data.get("birth_time", "").strip()
    place_name = req_data.get("place_name", "").strip() or "अज्ञात स्थान"
    lat_val = req_data.get("latitude")
    lon_val = req_data.get("longitude")
    timezone = req_data.get("timezone", "").strip() or "Asia/Kolkata"

    # Friendly Hindi Validations
    if not birth_date:
        return jsonify({
            "success": False,
            "error_field": "birth_date",
            "message": "कृपया जन्म तिथि चुनें (उदा. 15-05-1995)।"
        }), 400

    if not birth_time:
        return jsonify({
            "success": False,
            "error_field": "birth_time",
            "message": "कृपया जन्म समय दर्ज करें (उदा. 10:30 पूर्वाह्न/अपराह्न)।"
        }), 400

    try:
        lat = float(lat_val)
        lon = float(lon_val)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "error_field": "place_name",
            "message": "कृपया जन्म स्थान खोज सूची से चुनें ताकि सही अक्षांश और देशांतर स्वतः भरे जा सकें।"
        }), 400

    if not (-90.0 <= lat <= 90.0):
        return jsonify({
            "success": False,
            "error_field": "latitude",
            "message": "अक्षांश का मान -90° और +90° के मध्य होना चाहिए।"
        }), 400

    if not (-180.0 <= lon <= 180.0):
        return jsonify({
            "success": False,
            "error_field": "longitude",
            "message": "देशांतर का मान -180° और +180° के मध्य होना चाहिए।"
        }), 400

    try:
        result = calculate_kundli(
            birth_date_str=birth_date,
            birth_time_str=birth_time,
            tz_name=timezone,
            lat=lat,
            lon=lon,
            name=name,
            gender=gender,
        )
        result["user_info"]["place_name"] = place_name
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"गणना में त्रुटि: {str(exc)}"
        }), 400


@app.route("/api/search-place", methods=["GET"])
def api_search_place():
    """
    Proxies search queries to OpenStreetMap Nominatim with debounced rate compliance
    and custom descriptive User-Agent header.
    """
    query = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return jsonify([])

    encoded_q = urllib.parse.quote(query)
    nominatim_url = (
        f"https://nominatim.openstreetmap.org/search?"
        f"format=json&q={encoded_q}&limit=6&accept-language=hi,en&addressdetails=1"
    )

    req = urllib.request.Request(
        nominatim_url,
        headers={
            "User-Agent": "VedicKundaliApp/1.0 (Hindi Vedic Kundali Application; contact: rohit@kundli.local)"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                raw_data = json.loads(response.read().decode("utf-8"))
                places = []
                for item in raw_data:
                    display_name = item.get("display_name", "")
                    lat = float(item.get("lat", 0))
                    lon = float(item.get("lon", 0))
                    country_code = item.get("address", {}).get("country_code", "").lower()
                    
                    tz_suggest = "Asia/Kolkata" if country_code == "in" else "Asia/Kolkata"

                    places.append({
                        "name": display_name,
                        "lat": lat,
                        "lon": lon,
                        "timezone": tz_suggest,
                        "country_code": country_code
                    })
                return jsonify(places)
    except Exception as e:
        app.logger.warning(f"Nominatim lookup error: {e}")
        return jsonify([])

    return jsonify([])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
