from app.api import bp
from flask import jsonify, request, url_for
from app.models import Review
from app import db
from app.api.errors import bad_request
import json

@bp.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    return jsonify(Review.query.get_or_404(id).to_dict())

@bp.route('/reviews', methods=['GET'])
def get_reviews():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Review.to_collection_dict(Review.query, page, per_page, 'api.get_reviews')
    return jsonify(data)
