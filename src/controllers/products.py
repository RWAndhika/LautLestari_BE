from flask import Blueprint, request
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
        print(result)
        products = []

        if products is None:
            return {"products": "[]"}, 200

        for row in result.scalars():
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
    
@products_routes.route('/products', methods=['POST'])
@login_required
def create_product():
    try:
        product = Products(
            user_id=current_user.id,
            # image=request.form['image'],
            price=request.form['price'],
            qty=request.form['qty'],
            description=request.form['description'],
            category=request.form['category'],
            location=request.form['location'],
        )
        s.add(product)
        s.commit()
    
    except Exception as e:
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'Create product success'}, 200

@products_routes.route('/products/<id>', methods=['DELETE'])
@login_required
def delete_product(id):
    try:
        product = s.query(Products).filter(Products.id == id).first()
        s.delete(product)
        s.commit()

    except Exception as e:
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'Delete product success'}, 200

@products_routes.route('/products/<id>', methods=['PUT'])
@login_required
def update_product(id):
    try:
        product = s.query(Products).filter(Products.id == id).first()
        # product.image = request.form['image']
        product.price = request.form['price']
        product.qty = request.form['qty']
        product.description = request.form['description']
        product.category = request.form['category']
        product.location = request.form['location']
        s.commit()

    except Exception as e:  
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'Update product success'}, 200
    
