from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.users import Users

from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from flask_login import login_user

users_routes = Blueprint('users_routes', __name__)

Session = sessionmaker(connection)
s = Session()

@users_routes.route('/users', methods=['POST'])
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