"""
Extensions initialization for SQLAlchemy, Marshmallow and Flask-Mail.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail

db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
