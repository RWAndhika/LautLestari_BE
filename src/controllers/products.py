from flask import Blueprint
from models.products import Products
from controllers.users import s

from flask_login import current_user, login_required

products_routes = Blueprint('products_routes', __name__)

@products_routes.route('/products', methods=['GET'])
@login_required
def get_products():
    try:
        products_query = s.query(Products).all()
        products = []

        for row in products_query:
            products.append(
                {
                    'id': row.id,
                    'user_id': row.user_id,
                    'price': row.price,
                    'qty': row.qty,
                    'description': row.description,
                    'category': row.category,
                    'location': row.location,
                    'created_at': row.created_at,
                    'updated_at': row.updated_at,
                }
            )

        return {'products': products}, 200
    
    except Exception as e:
        print(e)
        return {'message': 'Unexpected error'}, 500
    
@products_routes.route('/products/<id>', methods=['GET'])
@login_required
def get_product(id):
    try:
        product= s.query(Products).filter(Products.id == id).first()
        if product == None:
            return {'message': 'product not found'}, 404

        return {
                'id': product.id,
                'user_id': product.user_id,
                'price': product.price,
                'qty': product.qty,
                'description': product.description,
                'category': product.category,
                'location': product.location,
                'created_at': product.created_at,
                'updated_at': product.updated_at,}, 200
    
    except Exception as e:
        return {'message': 'Unexpected error'}, 500
    
