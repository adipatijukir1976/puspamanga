from flask import Blueprint, jsonify
from api.scrape import scrape_rekomendasi_bge

rekomendasi_bp = Blueprint('rekomendasi_bp', __name__, url_prefix="/api")

@rekomendasi_bp.route('/rekomendasi', methods=['GET'])
def rekomendasi():
    data = scrape_rekomendasi_bge()
    return jsonify(data)
