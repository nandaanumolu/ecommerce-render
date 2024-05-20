# app/db/models.py
import uuid
import bcrypt
from sqlalchemy import Column, Integer, String, LargeBinary, Float, Text
#from sqlalchemy.orm import declarative_base
from db.models.user import Base
#productBase = declarative_base()
import sys
import os

# Add the path to the top-level directory of your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../' )))
from db.session import SessionLocal

db=SessionLocal()

class Product(Base):
    __tablename__ = "products_table"
    productName = Column(String(100))
    productId = Column(Integer, primary_key=True, index=True)
    productDescription=Column('mediumtext_col', Text(length=16777215))
    productImage=Column(LargeBinary)
    productCost = Column(Float)
    productRating = Column(String(100))

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = int(str(uuid.uuid4().int)[:6])  # Get the first 6 digits of a UUID
            if not db.query(Product).filter_by(productId=unique_id).first():  # Check if ID is already in use
                return unique_id
            
