from flask import Flask
import os
from dotenv import load_dotenv
from .prompts import prompts
from .routes.routes import routes

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.register_blueprint(prompts)
app.register_blueprint(routes)