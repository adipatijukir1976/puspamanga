from flask import Blueprint, jsonify
from api.scrape import scrape_paginated_bge

manhwa_bp = Blueprint("update_manhwa", __name__, url_prefix="/api/update")

@manhwa_bp.route("/manhwa")
def update_manhwa():
    data = scrape_paginated_bge("manhwa", pages=5)
    return jsonify(data)
