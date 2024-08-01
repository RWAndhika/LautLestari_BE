from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.users import Users

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from flask_login import login_user

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
        return {'message': 'Fail to register'}, 500
    
    return {'message': 'Register user success'}, 200

@users_routes.route('/users/login', methods=['POST'])
def user_login():
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