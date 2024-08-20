from flask import Blueprint, request
from models.subscribe import Subscribe
from controllers.users import s

subscribe_routes = Blueprint('subscribe_routes', __name__)

@subscribe_routes.route('/subscribe', methods=['GET'])
def get_subscribers():
    try:
        subscribe_query = s.query(Subscribe).all()
        subscribe = []

        for row in subscribe_query:
            subscribe.append(
                {
                    'id': row.id,
                    'email': row.email
                }
            )

        return {'subscriber': subscribe}, 200
    
    except Exception as e:
        return {'message': 'Unexpected error'}, 500

@subscribe_routes.route('/subscribe', methods=['POST'])
def add_subscriber():
    try:        
        subscribe = Subscribe(
            email=request.form['email']
        )
        s.add(subscribe)
        s.commit()
    
    except Exception as e:
        s.rollback()
        print(e)
        return {'message': 'Unexpected error'}, 500

    return {'message': 'add subscriber success'}, 200
    
