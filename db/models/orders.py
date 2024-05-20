# app/db/models.py
import uuid
import bcrypt
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey,Float
from sqlalchemy.orm import relationship
#from sqlalchemy.orm import declarative_base

#ordersBase = declarative_base()
import sys
import os

# Add the path to the top-level directory of your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../' )))
from db.session import SessionLocal
from db.models.user import Base

db=SessionLocal()

class Order(Base):
    __tablename__ = "orders_table"
    orderId = Column(Integer, primary_key=True, index=True)
    userId=Column(Integer, ForeignKey('users_table.userId'))
    #OrderproductId=Column(Integer, ForeignKey('products_table.productId'))
    #addressMappingId=Column(Integer, ForeignKey('address_mapping_table.addressMappingId'))
    orderStatus=Column(String(100), nullable=True)
    paymentId=Column(String(255), nullable=True)
    Amount = Column(String(100), nullable=True)
    currency=Column(String(100), nullable=True)
    paymentStatus=Column(String(100), nullable=True)
    promoCodeId =Column(Integer, ForeignKey('promo_code_table.promoId'), nullable=True)
    

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = str(uuid.uuid4().int)[:6]  # Get the first 6 digits of a UUID
            if not db.query(Order).filter_by(orderId=unique_id).first():  # Check if ID is already in use
                return unique_id


class OrderItem(Base):
    __tablename__ = "order_items_table"
    orderItemId = Column(Integer, primary_key=True, index=True)
    orderId = Column(Integer, ForeignKey('orders_table.orderId'))
    productId = Column(Integer, ForeignKey('products_table.productId'))
    quantity = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    currency=Column(String(100), nullable=True)

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = str(uuid.uuid4().int)[:6]  # Get the first 6 digits of a UUID
            if not db.query(OrderItem).filter_by(orderItemId=unique_id).first():  # Check if ID is already in use
                return unique_id
            
