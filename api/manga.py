from flask import Blueprint, jsonify
from api.scrape import scrape_komik

manga_bp = Blueprint("manga", __name__, url_prefix="/api")

@manga_bp.route("/manga")
def get_manga():
    return jsonify(scrape_komik("manga"))
