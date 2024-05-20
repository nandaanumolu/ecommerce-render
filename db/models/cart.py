# app/db/models.py
import uuid
from sqlalchemy import Column, Integer, ForeignKey
#from sqlalchemy.orm import declarative_base


#cartBase = declarative_base()
import sys
import os

# Add the path to the top-level directory of your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../' )))
from db.session import SessionLocal
from db.models.user import Base

db=SessionLocal()

class Cart(Base):
    __tablename__ = "cart_table"
    cartId = Column(Integer, primary_key=True, index=True)
    userId=Column(Integer, ForeignKey('users_table.userId'))
    productId=Column(Integer, ForeignKey('products_table.productId'))
    quantity=Column(Integer)

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = str(uuid.uuid4().int)[:6]  # Get the first 6 digits of a UUID
            if not db.query(Cart).filter_by(cartId=unique_id).first():  # Check if ID is already in use
                return unique_id
            
