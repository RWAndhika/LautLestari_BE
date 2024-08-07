from functools import wraps
from flask_login import current_user

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # role seller bisa akses semua 
            if current_user.is_authenticated and role == "seller" and current_user.role == "seller":
                return func(*args, **kwargs)
            elif current_user.is_authenticated and role == "seller" and current_user.role == "customer":
                return func(*args, **kwargs)
            # role yg akses customer
            elif current_user.is_authenticated and role == "customer" and current_user.role == "customer":
                return func(*args, **kwargs)
            # role yg akses customer, klo required seller dia gagal
            else:
                return {'message': 'Unauthorized'}, 401 
            

        return wrapper
    return decorator