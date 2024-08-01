from flask import Flask
from dotenv import load_dotenv
from controllers.users import users_routes, s

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(users_routes)

@app.route('/')
def hello_world():
    return "Hello world!"