from flask import Blueprint, jsonify, request
from api.scrape import (
    scrape_hot_bge,
    scrape_paginated_bge,
    scrape_rekomendasi_bge
)

home_bp = Blueprint('home_bp', __name__, url_prefix="/api")

@home_bp.route('/home', methods=['GET'])
def home():
    base_url = request.host_url.rstrip('/')  # Hasilnya: https://yourdomain.com

    menu = [
        {
            "name": "Manga",
            "icon": f"{base_url}/static/icons/manga.png",
            "type": "manga"
        },
        {
            "name": "Manhua",
            "icon": f"{base_url}/static/icons/manhua.png",
            "type": "manhua"
        },
        {
            "name": "Manhwa",
            "icon": f"{base_url}/static/icons/manhwa.png",
            "type": "manhwa"
        }
    ]

    data = [
        {
            "title": "🆕 Update Manga",
            "items": scrape_paginated_bge("manga", pages=2)
        },
        {
            "title": "🆕 Update Manhua",
            "items": scrape_paginated_bge("manhua", pages=2)
        },
        {
            "title": "🆕 Update Manhwa",
            "items": scrape_paginated_bge("manhwa", pages=2)
        },
        {
            "title": "🎯 Rekomendasi Komik",
            "items": scrape_rekomendasi_bge()
        },
        {
            "title": "🔥 Hot Manga",
            "items": scrape_hot_bge("manga", pages=2)
        },
        {
            "title": "🔥 Hot Manhua",
            "items": scrape_hot_bge("manhua", pages=2)
        },
        {
            "title": "🔥 Hot Manhwa",
            "items": scrape_hot_bge("manhwa", pages=2)
        }
    ]

    return jsonify({
        "menu": menu,
        "sections": data
    })
    
