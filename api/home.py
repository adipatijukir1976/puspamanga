import logging
from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
import time

logging.basicConfig(level=logging.INFO)

home_bp = Blueprint("home", __name__, url_prefix="/api")

# In-memory cache
_cache = {}
CACHE_TTL = 300

@home_bp.route("/home", methods=["GET"])
def home():
    now = time.time()

    if "data" in _cache and now - _cache["timestamp"] < CACHE_TTL:
        logging.info("🟡 Serve from cache")
        return jsonify(_cache["data"])

    try:
        url = "https://komiku.org"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        logging.error(f"🔴 Error: {e}")
        if "data" in _cache:
            return jsonify(_cache["data"])
        return jsonify({"error": "Failed to fetch from komiku.org"}), 503

    def extract_ls2(section_id):
        section = soup.find("section", id=section_id)
        result = []
        if not section:
            return result
        for idx, article in enumerate(section.find_all("article", class_="ls2")):
            title_tag = article.find("h3")
            title = title_tag.get_text(strip=True) if title_tag else f"No Title {idx}"
            link = title_tag.a["href"] if title_tag and title_tag.a else ""
            genre = article.find("span", class_="ls2t")
            chapter = article.find("a", class_="ls2l")
            image = article.find("img")
            rank = article.find("span", class_="svg hot")
            thumbnail = (image.get("data-src") or image.get("src") or "").split("?")[0] if image else ""
            result.append({
                "title": title,
                "link": link,
                "genre": genre.get_text(strip=True) if genre else "",
                "latest_chapter": chapter.get_text(strip=True) if chapter else "",
                "chapter_link": chapter["href"] if chapter else "",
                "thumbnail": thumbnail,
                "rank": rank.get_text(strip=True) if rank else None
            })
        return result

    def extract_terbaru():
        section = soup.find("section", id="Terbaru")
        result = []
        if not section:
            return result
        for idx, article in enumerate(section.find_all("article", class_="ls8")):
            title_tag = article.find("h3")
            title = title_tag.get_text(strip=True) if title_tag else f"No Title {idx}"
            link = title_tag.a["href"] if title_tag and title_tag.a else ""
            up_label = article.find("div", class_="ls84")
            image = article.find("img")
            thumbnail = (image.get("data-src") or image.get("src") or "").split("?")[0] if image else ""
            result.append({
                "title": title,
                "link": link,
                "up_info": up_label.get_text(strip=True) if up_label else "",
                "thumbnail": thumbnail
            })
        return result

    data = {
        "sections": [
            {"title": "Terbaru", "data": extract_terbaru()},
            {"title": "Rekomendasi", "data": extract_ls2("Rekomendasi_Komik")},
            {"title": "Manga Populer", "data": extract_ls2("Komik_Hot_Manga")},
            {"title": "Manhwa Populer", "data": extract_ls2("Komik_Hot_Manhwa")},
            {"title": "Manhua Populer", "data": extract_ls2("Komik_Hot_Manhua")}
        ]
    }

    _cache["data"] = data
    _cache["timestamp"] = now
    logging.info("🟢 New data scraped")

    return jsonify(data)
