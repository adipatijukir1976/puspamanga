import requests
from bs4 import BeautifulSoup
import re
import time

# Manual cache
_cache = {}
_cache_timeout = 300  # detik

def cached_get(url):
    now = time.time()
    if url in _cache:
        data, timestamp = _cache[url]
        if now - timestamp < _cache_timeout:
            return data
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    _cache[url] = (response.text, now)
    return response.text

# 🔹 Untuk halaman utama daftar komik
def parse_komiku_list(html):
    soup = BeautifulSoup(html, "html.parser")
    komik_list = []

    for item in soup.select("div.ls4"):
        try:
            img_tag = item.select_one("img")
            title_tag = item.select_one("h4 a")
            genre_tags = item.select("span.ls4s")

            image = re.sub(r'\?resize=.*$', '', img_tag["src"]) if img_tag else ""
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = title_tag["href"] if title_tag else ""
            type_komik = genre_tags[0].get_text(strip=True) if len(genre_tags) > 0 else ""
            status = genre_tags[1].get_text(strip=True).replace("Status: ", "") if len(genre_tags) > 1 else ""
            genre = genre_tags[2].get_text(strip=True).replace("Genre: ", "") if len(genre_tags) > 2 else ""

            komik_list.append({
                "title": title,
                "link": link,
                "image": image,
                "type": type_komik,
                "status": status,
                "genre": genre
            })
        except Exception:
            continue

    return komik_list

def scrape_komik(tipe="manga"):
    url = f"https://komiku.org/daftar-komik/?tipe={tipe}"
    html = cached_get(url)
    return parse_komiku_list(html)

# 🔸 Untuk update terbaru <div class="bge">
def scrape_paginated_bge(tipe="manga", pages=5):
    results = []
    for page in range(1, pages + 1):
        url = f"https://api.komiku.org/manga/page/{page}/?orderby&tipe={tipe}"
        html = cached_get(url)
        soup = BeautifulSoup(html, "html.parser")

        for div in soup.select("div.bge"):
            try:
                link = div.select_one(".bgei a")["href"]
                title = div.select_one("h3").get_text(strip=True)
                thumbnail = re.sub(r'\?resize=.*$', '', div.select_one("img")["src"])
                type_genre = div.select_one(".tpe1_inf").get_text(strip=True).split(maxsplit=1)
                tipe_komik = type_genre[0]
                genre = type_genre[1] if len(type_genre) > 1 else ""
                desc = div.select_one("p").get_text(strip=True)
                chapter_awal = div.select("div.new1 a")[0]
                chapter_terbaru = div.select("div.new1 a")[1]

                results.append({
                    "title": title,
                    "type": tipe_komik,
                    "genre": genre,
                    "thumbnail": thumbnail,
                    "description": desc,
                    "link": link,
                    "chapter_awal": {
                        "title": chapter_awal.get_text(strip=True).replace("Awal: ", ""),
                        "url": chapter_awal["href"]
                    },
                    "chapter_terbaru": {
                        "title": chapter_terbaru.get_text(strip=True).replace("Terbaru: ", ""),
                        "url": chapter_terbaru["href"]
                    }
                })
            except Exception:
                continue

    return results
