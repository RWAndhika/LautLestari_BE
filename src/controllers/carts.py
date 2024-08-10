from flask import Blueprint, request, jsonify
from models.carts import Carts
from controllers.users import s

from decorators.authorization_checker import role_required


carts_routes = Blueprint('carts_routes', __name__)


# menambahkan item ke cart
@carts_routes.route('/carts', methods=['POST'])
@role_required('buyer')
def add_to_cart():
    try:
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        qty = request.form['qty']

        if not user_id or not product_id or not qty:
            return {'message': 'Missing parameter'}, 400

        # cek apakah sudah ada di keranjang
        cart = s.query(Carts).filter(Carts.user_id == user_id, Carts.product_id == product_id).first()

        if cart:
            cart.qty = cart.qty + int(qty)
        else:
            new_cart = Carts(user_id=user_id, product_id=product_id, qty=int(qty))
            s.add(new_cart)

        s.commit()

        return {'message': 'Success add to cart'}, 200
        
    except Exception as e:
        s.rollback()
        return{'message': 'Fail to add to cart'}, 500


# mendapatkan item dari cart
@carts_routes.route('/carts/<user_id>', methods=['GET'])
@role_required('buyer')
def get_cart(user_id):
    try:
        cart_items_query = s.query(Carts).filter(Carts.user_id == user_id).all()
        cart_items = []

        for row in cart_items_query:
            cart_items.append(
                {
                    'id': row.id,
                    'user_id': row.user_id,
                    'product_id': row.product_id,
                    'qty': row.qty
                }
            )

        return {'cart_items': cart_items}, 200
    
    except Exception as e:
        print(e)
        return {'message': 'Unexpected error'}, 500


# menghapus item dari cart
@carts_routes.route('/carts/<user_id>/<product_id>', methods=['DELETE'])
@role_required('buyer')
def delete_cart(user_id, product_id):
    try:
        cart_item = s.query(Carts).filter(Carts.user_id == user_id, Carts.product_id == product_id).first()

        if not cart_item:
            return jsonify({'message': 'Item not found'}), 404

        s.delete(cart_item)
        s.commit()

        return jsonify({'message': 'Item deleted successfully'}), 200

    except Exception as e:
        s.rollback() 
        print(e)
        return jsonify({'message': 'Unexpected error'}), 500