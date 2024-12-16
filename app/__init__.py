from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap5(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


from app import routes, models, forms

with app.app_context():
    db.create_all()