import requests
from bs4 import BeautifulSoup
import re
import time

# Cache manual dengan timeout (opsional)
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
