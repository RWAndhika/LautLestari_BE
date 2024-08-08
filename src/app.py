from flask import Flask
from dotenv import load_dotenv
from controllers.users import users_routes, s
from controllers.products import products_routes
from flask_cors import CORS  # Import Flask-CORS
from flask_login import LoginManager
from models.users import Users

import cloudinary
import os



load_dotenv()

app = Flask(__name__)

CORS(app)  # Enable CORS for the whole app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

app.register_blueprint(users_routes)
app.register_blueprint(products_routes)

if __name__ == "__main__":
    app.run(debug=True)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return s.query(Users).get(int(user_id))

@app.route('/')
def hello_world():
    return "Hello world!"