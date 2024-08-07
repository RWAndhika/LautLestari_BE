from flask import Blueprint, request
from models.products import Products
from controllers.users import s

from flask_login import current_user
from decorators.authorization_checker import role_required

from cerberus import Validator
from validations.products_vallidation import add_products_schema

import cloudinary.uploader


products_routes = Blueprint('products_routes', __name__)

@products_routes.route('/products', methods=['GET'])

@role_required('buyer')
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
                    'image': row.image,
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
@role_required('buyer')
def get_product(id):
    try:
        product= s.query(Products).filter(Products.id == id).first()
        if product == None:
            return {'message': 'product not found'}, 404

        return {
                'id': product.id,
                'user_id': product.user_id,
                'price': product.price,
                'image': product.image,
                'qty': product.qty,
                'description': product.description,
                'category': product.category,
                'location': product.location,
                'created_at': product.created_at,
                'updated_at': product.updated_at,}, 200
    
    except Exception as e:
        return {'message': 'Unexpected error'}, 500
    
@products_routes.route('/products', methods=['POST'])
@role_required('seller')
def create_product():


    v = Validator(add_products_schema)

    request_body = {
        'price': request.form.get('price', type=int),
        'qty': request.form.get('qty', type=int),
        'description': request.form.get('description'),
        'category': request.form.get('category'),
        'location': request.form.get('location')
    }

    if not v.validate(request_body):
        return {'message': 'Validation failed', 'errors': v.errors}, 400
    
    # Upload image to cloudinary
    image_file = request.files.get('image')
    if image_file:
        try:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result['secure_url']
        except Exception as e:
            print(e)
            return {'message': 'Failed to upload image', 'error': str(e)}, 500
    else:
        return {'message': 'No image file provided'}, 400
    
    try:
        product = Products(
            user_id=current_user.id,
            image=image_url,
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
@role_required('seller')
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
@role_required('seller')
def update_product(id):
    try:
        product = s.query(Products).filter(Products.id == id).first()
        product.image = request.form['image']
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
    
