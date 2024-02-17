from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager = LoginManager(app) 
login_manager.login_view = "/login" 
login_manager.login_message_category = "info" 
login_manager.login_message = "You can not access this page. Please log in to access this page." 
login_manager.session_protection = 'strong'