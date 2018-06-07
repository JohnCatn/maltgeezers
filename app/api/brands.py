from app.api import bp
from flask import jsonify, request, url_for
from app.models import Brand
from app import db
from app.api.errors import bad_request
import json

@bp.route('/brands', methods=['GET'])
def get_brands():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Brand.to_collection_dict(Brand.query, page, per_page, 'api.get_brands')
    return jsonify(data)

@bp.route('/brandsautocomplete',methods=['POST','GET'])
def brandsautocomplete():
    result=''
    if request.method=='POST':
        query=request.form['q']
        data = Brand.to_collection_dict(Brand.query.filter(Brand.name.like("%"+query+"%")), 'api.brandsautocomplete')
        return jsonify(data)
    else:

        return "ooops"
