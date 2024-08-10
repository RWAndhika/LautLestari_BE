from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims.get('role') == 'seller' and role == 'seller':
                return func(*args, **kwargs)
            elif claims.get('role') == 'seller' and role == 'buyer':
                return func(*args, **kwargs)
            elif claims.get('role') == 'buyer' and role == 'buyer':
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "Unauthorized"}), 403

        return wrapper
    return decorator
