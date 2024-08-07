from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.users import Users

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from flask_login import login_user, login_required, logout_user, current_user
# from decorators.authorization_checker import role_required

users_routes = Blueprint('users_routes', __name__)

Session = sessionmaker(connection)
s = Session()

@users_routes.route('/users/register', methods=['POST'])
def register_user():

    try:
        NewUser = Users(
            username=request.form['username'],
            email=request.form['email'],
            role=request.form['role'],
            phonenumber=request.form['phonenumber']
        )
        NewUser.set_password(request.form['password'])

        s.add(NewUser)
        s.commit()
    except Exception as e:
        s.rollback()
        print(e)
        return {'message': 'Fail to register'}, 500
    
    return {'message': 'Register user success'}, 200

@users_routes.route('/users/login', methods=['POST'])
def user_login():
    # input = request.get_json()
    # print(input)
    # try:
    #     user = s.query(Users).filter(Users.email == input.get("email")).first()
    #     if user == None:
    #         return {'message': 'User not found'}, 403
        
    #     if not user.check_password(input.get("password")):
    #         return {'message': 'Invalid password'}, 403
        
    #     login_user(user)
    #     session_id = request.cookies.get('session')
    #     return {
    #         'session_id': session_id,
    #         'message': 'Login success'
    #     }, 200
    
    # except Exception as e:
    #     print(e)
    #     s.rollback()
    #     return {'message': 'Fail to login'}, 500

    try:
        email = request.form['email']
        user = s.query(Users).filter(Users.email == email).first()

        if user == None:
            return {'message': 'User not found'}, 403

        if not user.check_password(request.form['password']):
            return {'message': 'Invalid password'}, 403
        
        login_user(user)
        session_id = request.cookies.get('session')
        return {
            'session_id': session_id,
            'message': 'Login success'
        }, 200
    
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to login'}, 500
    
@users_routes.route('/users/me', methods=['GET'])
@login_required
def info_user():
    try:
        return {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role,
            'phonenumber': current_user.phonenumber,
            'created_at': current_user.created_at,
            'updated_at': current_user.updated_at
        }, 200
    except Exception as e:
        return {'message': 'Unauthorized'}, 401
    
@users_routes.route('/users/me', methods=['DELETE'])
@login_required
def delete_user():
    try:
        user = s.query(Users).filter(Users.id == current_user.id).first()
        s.delete(user)
        s.commit()
        logout_user()
    except Exception as e:
        s.rollback()
        return {'message': 'Fail to delete user'}, 500
    
    return {'message': 'Delete user success'}, 200

@users_routes.route('/users/logout', methods=['GET'])
@login_required
def user_logout():
    logout_user()
    return {'message': 'Logout user success'}, 200