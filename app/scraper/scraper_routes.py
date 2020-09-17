from http import HTTPStatus
from flask import Blueprint, request
from app.scraper.scraper_service import ScraperService

bp = Blueprint("standings", __name__, url_prefix="/standings")


@bp.route("/update", methods=["POST"])
def update_standings():
    content = request.json  # content contains url
    if not content:
        return "Bad request. Expecting JSON.", HTTPStatus.BAD_REQUEST
    result = ScraperService.update_standing_new_table(content=content)
    if isinstance(result, str):
        return result, HTTPStatus.BAD_REQUEST
    if result:
        return "Success!"
