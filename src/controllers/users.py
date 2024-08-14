from flask import Blueprint, request
from connectors.mysql_connector import connection
from models.users import Users
from models.blocklist import BLOCKLIST
from datetime import timedelta

from sqlalchemy.orm import sessionmaker

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from cerberus import Validator
from validations.users_validation import users_register_schema

users_routes = Blueprint("users_routes", __name__)

Session = sessionmaker(connection)
s = Session()


@users_routes.route("/users/register", methods=["POST"])
def register_user():
    allowed_role = ["seller", "buyer"]
    user_role = request.form.get("role")
    if user_role not in allowed_role:
        return {"message": "Invalid role type (seller, buyer)"}, 400

    v = Validator(users_register_schema)
    request_body = {
        "username": request.form.get("username"),
        "email": request.form.get("email"),
    }

    if not v.validate(request_body):
        return {"message": "Validation failed", "error": v.errors}, 409

    try:
        NewUser = Users(
            username=request.form["username"],
            email=request.form["email"],
            role=request.form["role"],
            phonenumber=request.form["phonenumber"],
        )
        NewUser.set_password(request.form["password"])

        s.add(NewUser)
        s.commit()
    except Exception as e:
        s.rollback()
        print(e)
        return {"message": "Fail to register"}, 500

    return {"message": "Register user success"}, 200


@users_routes.route("/users/login", methods=["POST"])
def user_login():

    try:
        email = request.form["email"]
        user = s.query(Users).filter(Users.email == email).first()

        if user == None:
            return {"message": "User not found"}, 403

        if not user.check_password(request.form["password"]):
            return {"message": "Invalid password"}, 403

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"email": user.email, "id": user.id, "role": user.role},
            fresh=timedelta(days=7),
        )

        return {"access_token": access_token, "message": "Login success"}, 200

    except Exception as e:
        s.rollback()
        return {"message": "Fail to login"}, 500


@users_routes.route("/users/me", methods=["GET"])
@jwt_required()
def info_user():
    current_user_id = get_jwt_identity()
    try:
        user = s.query(Users).filter(Users.id == current_user_id).first()
        if not user:
            return {"message": "User not found"}, 404

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "phonenumber": user.phonenumber,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }, 200
    except Exception as e:
        return {"message": "Unauthorized"}, 401


@users_routes.route("/users/me", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()
    try:
        user = s.query(Users).filter(Users.id == current_user_id).first()
        s.delete(user)
        s.commit()
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
    except Exception as e:
        s.rollback()
        return {"message": "Fail to delete user"}, 500

    return {"message": "Delete user success"}, 200


@users_routes.route("/users/logout", methods=["GET"])
@jwt_required()
def user_logout():

    try:
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User successfully logged out"}, 200
    except Exception as e:
        print(e)
        return {"message": "Failed to logout"}, 500
