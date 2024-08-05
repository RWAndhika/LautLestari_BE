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
        result = s.execute(products_query)
        products = []

        for row in result.scalars():
            products.append(
                {
                    'id': row.id,
                    'user_id': row.user_id,
                    'price': row.price,
                    'description': row.description,
                    'category': row.category,
                    'location': row.location,
                    'created_at': row.created_at,
                    'updated_at': row.updated_at,
                }
            )

        return {'products': products}, 200
    
    except Exception as e:
        return {'message': 'Unexpected error'}, 500
    

        