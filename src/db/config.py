from ..config import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://postgres:xPid1qfchaWiABuT@db.jstlaqnpqstdcpsfgymr.supabase.co:5432/postgres"

db.init_app(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.COlumn(db.String, nullable=False)
    

class Product(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
