from flask import Blueprint, request
from models.confirmations import Confirmations
from models.products import Products
from models.carts import Carts
from models.users import Users
from controllers.users import s

from decorators.authorization_checker import role_required
from sqlalchemy import func

from flask_jwt_extended import get_jwt_identity

confirmations_routes = Blueprint('confirmations_routes', __name__)
   
@confirmations_routes.route('/confirmations/me', methods=['GET'])
@role_required('seller')
def get_user_confirmations():
    try:
        current_user_id = get_jwt_identity()
        confirmations_query = s.query(Confirmations).filter(Confirmations.user_id == current_user_id).all()
        confirmations = []

        for confirmation in confirmations_query:
            confirmations.append(
                {
                    'id': confirmation.id,
                    'user_id': confirmation.user_id,
                    'buyer': confirmation.buyer,
                    'description': confirmation.description,
                    'product_id': confirmation.product_id,
                    'qty': confirmation.qty,
                    'created_at': confirmation.created_at,
                    'is_confirm': confirmation.is_confirm
                }
            )

        return {'confirmations': confirmations}, 200
    
    except Exception as e:
        print(e)
        return {'message': 'Unexpected error'}, 500
    
@confirmations_routes.route('/confirmations/<id>', methods=['GET'])
@role_required('seller')
def get_confirmation(id):
    try:
        confirmation= s.query(Confirmations).filter(Confirmations.id == id).first()
        if confirmation == None:
            return {'message': 'confirmation not found'}, 404

        return {
                'id': confirmation.id,
                    'user_id': confirmation.user_id,
                    'buyer': confirmation.buyer,
                    'description': confirmation.description,
                    'product_id': confirmation.product_id,
                    'qty': confirmation.qty,
                    'created_at': confirmation.created_at,
                    'is_confirm': confirmation.is_confirm }, 200
    
    except Exception as e:
        return {'message': 'Unexpected error'}, 500
    
@confirmations_routes.route('/confirmations', methods=['POST'])
@role_required('buyer')
def create_confirmation():
    current_user_id = get_jwt_identity()
        
    try:
        product_id = request.form['product_id']
        product = s.query(Products).filter(Products.id == product_id).first()
        if not product:
            return {'message': 'product not found'}, 404
        
        product_user_id = product.user_id
        product_total_price = product.price * request.form.get('qty', type=int)
        product_description = product.description
        
        buyer = s.query(Users).filter(Users.id == current_user_id).first()

        if not buyer:
            return {'message': 'user not found'}, 404
        
        buyer_username = buyer.username

        if (request.form.get('referral_code')):
            referral_code = request.form.get('referral_code')
            if product.referral_code == referral_code:
                product_total_price = (product_total_price * 80)//100

        confirmation = Confirmations(
            user_id=product_user_id,
            buyer=buyer_username,
            product_id=product_id,
            price=product_total_price,
            qty=request.form['qty'],
            description=product_description,
            is_confirm=0
        )
        s.add(confirmation)

        cart = s.query(Carts).filter(Carts.id == request.form.get('cart_id')).first()
        if cart == None:
            s.rollback()
            return {'message': 'Cart Not Found'}, 404
        
        s.delete(cart)
        s.commit()
    
    except Exception as e:
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'Create confirmation success'}, 200

@confirmations_routes.route('/confirmations/<id>', methods=['DELETE'])
@role_required('seller')
def delete_confirmation(id):
    try:
        confirmation = s.query(Confirmations).filter(Confirmations.id == id).first()
        s.delete(confirmation)
        s.commit()

    except Exception as e:
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'Delete confirmation success'}, 200

@confirmations_routes.route('/confirmations/<id>', methods=['PUT'])
@role_required('seller')
def update_confirmation(id):
    current_user_id = get_jwt_identity()

    try:
        confirmation = s.query(Confirmations).filter(Confirmations.id == id).first()

        if confirmation == None:
            return {'message': 'Confirmation not found'}, 404
        
        if not confirmation.user_id == current_user_id:
            return {'message': 'Unauthorized'}, 403
        
        product = s.query(Products).filter(Products.id == confirmation.product_id).first()

        product.qty -= int(confirmation.qty)

        confirmation.is_confirm = 1
        confirmation.updated_at = func.now()
        s.commit()

    except Exception as e:  
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'Update confirmation success'}, 200
    
