from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, DECIMAL
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.Numeric(precision=10, scale=2))  # Use Numeric for decimal