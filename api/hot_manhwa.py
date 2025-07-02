from flask import Blueprint, jsonify
from api.scrape import scrape_paginated_bge

hot_manwa_bp = Blueprint('hot_manwa_bp', __name__, url_prefix="/api/hot")

@hot_manwa_bp.route('/manwa', methods=['GET'])
def hot_manwa():
    data = scrape_paginated_bge("manhwa")
    return jsonify(data)
