from flask import Blueprint, jsonify
from api.scrape import scrape_hot_bge

hot_manga_bp = Blueprint('hot_manga_bp', __name__, url_prefix="/api/hot")

@hot_manga_bp.route('/manga', methods=['GET'])
def hot_manga():
    data = scrape_hot_bge("manga")
    return jsonify(data)
