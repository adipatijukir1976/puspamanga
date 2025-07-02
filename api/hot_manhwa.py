from flask import Blueprint, jsonify
from api.scrape import scrape_hot_bge

hot_manhwa_bp = Blueprint('hot_manhwa_bp', __name__, url_prefix="/api/hot")

@hot_manhwa_bp.route('/manhwa', methods=['GET'])
def hot_manhwa():
    data = scrape_hot_bge("manhwa")
    return jsonify(data)
