from flask import Blueprint, jsonify
from api.scrape import (
    scrape_hot_bge,
    scrape_paginated_bge,
    scrape_rekomendasi_bge
)

home_bp = Blueprint('home_bp', __name__, url_prefix="/api")

@home_bp.route('/home', methods=['GET'])
def home():
    data = [
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
        },
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
        }
    ]

    menu = [
        {
            "name": "Manga",
            "icon": "https://yourdomain.com/static/icons/manga.png",
            "type": "manga"
        },
        {
            "name": "Manhua",
            "icon": "https://yourdomain.com/static/icons/manhua.png",
            "type": "manhua"
        },
        {
            "name": "Manhwa",
            "icon": "https://yourdomain.com/static/icons/manhwa.png",
            "type": "manhwa"
        }
    ]

    return jsonify({
        "menu": menu,
        "sections": data
    })
    
