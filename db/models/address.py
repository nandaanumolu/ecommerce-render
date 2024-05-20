# app/db/models.py
import uuid
from sqlalchemy import Column, Integer, String, Text
#from sqlalchemy.orm import declarative_base
from datetime import datetime
from db.models.user import Base
#ddressBase = declarative_base()
import sys
import os

# Add the path to the top-level directory of your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../' )))
from db.session import SessionLocal

db=SessionLocal()

class Address(Base):
    __tablename__ = "address_table"
    addressId = Column(Integer, primary_key=True, index=True)
    name=Column(String(255))
    mobileNumber = Column(String(100))
    pincode=Column(String(100))
    locality = Column(String(100))
    address=Column('mediumtext_col', Text(length=16777215))
    city = Column(String(255))
    alternatePhonenumber=Column(String(100))

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = int(str(uuid.uuid4().int)[:6])  # Get the first 6 digits of a UUID
            if not db.query(Address).filter_by(addressId=unique_id).first():  # Check if ID is already in use
                return unique_id
            
