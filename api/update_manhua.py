from flask import Blueprint, jsonify
from api.scrape import scrape_paginated_bge

update_manhua_bp = Blueprint("update_manhua", __name__, url_prefix="/api/update")

@manhua_bp.route("/manhua")
def update_manhua():
    data = scrape_paginated_bge("manhua", pages=5)
    return jsonify(data)
