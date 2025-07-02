from flask import Blueprint, jsonify
from api.scrape import scrape_paginated_bge

hot_manga_bp = Blueprint('hot_manga_bp', __name__, url_prefix="/api/hot")

@hot_manga_bp.route('/manga', methods=['GET'])
def hot_manga():
    data = scrape_paginated_bge("manga")
    return jsonify(data)
