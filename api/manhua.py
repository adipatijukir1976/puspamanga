from flask import Blueprint, jsonify
from api.scrape import scrape_komik

manhua_bp = Blueprint("manhua", __name__, url_prefix="/api")

@manhua_bp.route("/manhua")
def get_manhua():
    return jsonify(scrape_komik("manhua"))
