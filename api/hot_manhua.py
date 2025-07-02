from flask import Blueprint, jsonify
from api.scrape import scrape_hot_bge

hot_manhua_bp = Blueprint('hot_manhua_bp', __name__, url_prefix="/api/hot")

@hot_manhua_bp.route('/manhua', methods=['GET'])
def hot_manhua():
    data = scrape_hot_bge("manhua")
    return jsonify(data)
