from flask import Blueprint, request
from models.products import Products
from controllers.users import s

from decorators.authorization_checker import role_required
from sqlalchemy import func

from cerberus import Validator
from validations.products_vallidation import add_products_schema

import cloudinary.uploader

from flask_jwt_extended import (get_jwt_identity)

products_routes = Blueprint('products_routes', __name__)

@products_routes.route('/products', methods=['GET'])
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
                    'nationality': row.nationality,
                    'size': row.size,
                    'created_at': row.created_at,
                    'updated_at': row.updated_at,
                }
            )

        return {'products': products}, 200
    
    except Exception as e:
        print(e)
        return {'message': 'Unexpected error'}, 500
    
@products_routes.route('/products/me', methods=['GET'])
@role_required('seller')
def get_user_products():
    try:
        current_user_id = get_jwt_identity()
        products_query = s.query(Products).filter(Products.user_id == current_user_id).all()
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
                    'nationality': row.nationality,
                    'size': row.size,
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
                'seller': product.users.username,
                'price': product.price,
                'image': product.image,
                'qty': product.qty,
                'description': product.description,
                'category': product.category,
                'location': product.location,
                'nationality': product.nationality,
                'size': product.size,
                'created_at': product.created_at,
                'updated_at': product.updated_at,}, 200
    
    except Exception as e:
        return {'message': 'Unexpected error'}, 500
    
@products_routes.route('/products', methods=['POST'])
@role_required('seller')
def create_product():
    current_user_id = get_jwt_identity()
    allowed_category = ['Import', 'Local']
    user_category = request.form.get('category')
    if user_category not in allowed_category:
        return {'message': 'Invalid category type (Import, Local)'}, 400

    v = Validator(add_products_schema)

    request_body = {
        'price': request.form.get('price', type=int),
        'qty': request.form.get('qty', type=int),
        'description': request.form.get('description'),
        'category': request.form.get('category'),
        'location': request.form.get('location'),
        'nationality': request.form.get('nationality'),
        'size': request.form.get('size', type=int)
    }

    if not v.validate(request_body):
        return {'message': 'Validation failed', 'errors': v.errors}, 400
    
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
        if (request.form.get('referral_code')):
            product = Products(
                user_id=current_user_id,
                image=image_url,
                price=request.form['price'],
                qty=request.form['qty'],
                description=request.form['description'],
                category=request.form['category'],
                location=request.form['location'],
                nationality=request.form['nationality'],
                size=request.form['size'],
                referral_code=request.form['referral_code']
            )
            s.add(product)
            s.commit()
            return {'message': 'Create product success'}, 200
            
        product = Products(
            user_id=current_user_id,
            image=image_url,
            price=request.form['price'],
            qty=request.form['qty'],
            description=request.form['description'],
            category=request.form['category'],
            location=request.form['location'],
            nationality=request.form['nationality'],
            size=request.form['size']
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

    allowed_category = ['Import', 'Local']
    current_user_id = get_jwt_identity()

    image_url = None

    if 'image' in request.files:
        image_file = request.files['image']
        try:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result['secure_url']
        except Exception as e:
            print(e)
            return {'message': 'Failed to upload image', 'error': str(e)}, 500
    elif 'image' in request.form:
        image_url = request.form['image']

    try:
        product = s.query(Products).filter(Products.id == id).first()

        if product == None:
            return {'message': 'product not found'}, 404
        
        if not product.user_id == current_user_id:
            return {'message': 'Unauthorized'}, 403

        if image_url:
            product.image = image_url
        if 'price' in request.form:
            product.price = request.form['price']
        if 'qty' in request.form:
            product.qty = request.form['qty']
        if 'description' in request.form:
            product.description = request.form['description']
        if 'category' in request.form:
            category = request.form['category']
            if category not in allowed_category:
                s.rollback()
                return {'message': 'Invalid category type (Import, Local)'}
            product.category = category
        if 'location' in request.form:
            product.location = request.form['location']
        if 'nationality' in request.form:
            product.nationality = request.form['nationality']
        if 'size' in request.form:
            product.size = request.form['size']
        if 'referral_code' in request.form:
            product.referral_code = request.form['referral_code']

        product.updated_at = func.now()
        s.commit()

    except Exception as e:  
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'Update product success'}, 200
    
