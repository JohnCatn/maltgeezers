from app.api import bp
from flask import jsonify, request, url_for
from app.models import Tasting, Review
from app import db
from app.api.errors import bad_request
import json

@bp.route('/tasting/<int:id>', methods=['GET'])
def get_tasting(id):
    return jsonify(Tasting.query.get_or_404(id).to_dict())

@bp.route('/tastings', methods=['GET'])
def get_tastings():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Review.to_collection_dict(Tasting.query, page, per_page, 'api.get_tastings')
    return jsonify(data)

@bp.route('/tasting/<int:tasting_id>/reviews_chart', methods=['GET'])
def get_tasting_chart(tasting_id):
    data = Review.to_chart_dict_all(Review.query.filter_by(tasting_id=tasting_id))
    return jsonify(data)
