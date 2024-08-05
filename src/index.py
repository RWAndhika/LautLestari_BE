from flask import Flask
from dotenv import load_dotenv
from controllers.users import users_routes, s
from controllers.products import products_routes

from flask_login import LoginManager
from models.users import Users

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(users_routes)
app.register_blueprint(products_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return s.query(Users).get(int(user_id))

@app.route('/')
def hello_world():
    return "Hello world!"