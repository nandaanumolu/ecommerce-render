import sys
import os
# Add the path to the top-level directory of your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../' )))

# app/db/models.py
import uuid
from sqlalchemy import Column, Integer, ForeignKey,String
#from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

#addressBase = declarative_base()

from app.db.session import SessionLocal
from app.db.models.user import Base

db=SessionLocal()

class AddressMapping(Base):
    __tablename__ = "address_mapping_table"
    addressMappingId = Column(Integer, primary_key=True, index=True)
    addressId=Column(Integer, ForeignKey('address_table.addressId'))
    userId=Column(Integer, ForeignKey('users_table.userId'))

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = str(uuid.uuid4().int)[:6]  # Get the first 6 digits of a UUID
            if not db.query(AddressMapping).filter_by(addressMappingId=unique_id).first():  # Check if ID is already in use
                return unique_id
            
            

