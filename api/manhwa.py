from flask import Blueprint, jsonify
from api.scrape import scrape_komik

manhwa_bp = Blueprint("manhwa", __name__)

@manhwa_bp.route("/manhwa")
def get_manhwa():
    return jsonify(scrape_komik("manhwa"))
