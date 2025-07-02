from flask import Blueprint, jsonify
from api.scrape import scrape_paginated_bge

update_manga_bp = Blueprint("update_manga", __name__, url_prefix="/api/update")

@update_manga_bp.route("/manga")
def update_manga():
    data = scrape_paginated_bge("manga", pages=5)
    return jsonify(data)
