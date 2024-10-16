from flask import Blueprint, request, jsonify
from models.carts import Carts
from models.products import Products
from models.users import Users
from controllers.users import s
from flask_jwt_extended import get_jwt_identity
from decorators.authorization_checker import role_required


carts_routes = Blueprint('carts_routes', __name__)

@carts_routes.route('/carts', methods=['POST'])
@role_required('buyer')
def add_to_cart():
    try:
        current_user_id = get_jwt_identity()
        user_id = current_user_id
        product_id = request.form.get('product_id')
        qty = request.form.get('qty', type=int)

        if not user_id or not product_id or not qty:
            return {'message': 'Missing parameter'}, 400
        
        try:
            qty = int(qty)
        except ValueError:
            return {'message': 'qty must be an integer'}, 400
        
        product = s.query(Products).filter(Products.id == product_id).first()
        product_price = int(qty) * int(product.price)
        product_description = product.description

        cart = s.query(Carts).filter(Carts.user_id == user_id, Carts.product_id == product_id).first()

        if cart:
            cart.qty += int(qty)
            cart.price = cart.qty * product_price
        else:
            new_cart = Carts(user_id=user_id, product_id=product_id, qty=int(qty), price=product_price, description=product_description)
            s.add(new_cart)

        s.commit()

        return {'message': 'Success add to cart'}, 200
        
    except Exception as e:
        s.rollback()
        return{'message': 'Fail to add to cart'}, 500

@carts_routes.route('/carts', methods=['GET'])
@role_required('buyer')
def get_cart():
    try:
        current_user_id = get_jwt_identity()
        cart_items_query = s.query(Carts).filter(Carts.user_id == current_user_id).all()
        cart_items = []

        for row in cart_items_query:
            product = s.query(Products).filter(Products.id == row.product_id).first()
            seller = s.query(Users).filter(Users.id == product.user_id).first()
            cart_items.append(
                {
                    'id': row.id,
                    'user_id': row.user_id,
                    'product_id': row.product_id,
                    'qty': row.qty,
                    'price': row.price,
                    'description': row.description,
                    'image': product.image,
                    'seller': seller.username,
                    'contact_phone': seller.phonenumber,
                }
            )

        return {'cart_items': cart_items}, 200
    
    except Exception as e:
        print(e)
        return {'message': 'Unexpected error'}, 500

@carts_routes.route('/carts/<product_id>', methods=['DELETE'])
@role_required('buyer')
def delete_cart(product_id):
    try:
        current_user_id = get_jwt_identity()
        cart_item = s.query(Carts).filter(Carts.user_id == current_user_id, Carts.product_id == product_id).first()

        if not cart_item:
            return {'message': 'Item not found'}, 404

        s.delete(cart_item)
        s.commit()

        return {'message': 'Item deleted successfully'}, 200

    except Exception as e:
        s.rollback() 
        print(e)
        return {'message': 'Unexpected error'}, 500