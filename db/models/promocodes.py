# app/db/models.py
import uuid
from sqlalchemy import Column, Integer, String, DateTime
#from sqlalchemy.orm import declarative_base
from datetime import datetime
#promocodeBase = declarative_base()

import sys
import os

# Add the path to the top-level directory of your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../' )))
from db.session import SessionLocal
from db.models.user import Base

db=SessionLocal()

class PromoCodes(Base):
    __tablename__ = "promo_code_table"
    promoId = Column(Integer, primary_key=True, index=True)
    promoCode=Column(String(100))
    promoValidationdate = Column(DateTime, default=datetime.now)
    promoWorth=Column(String(100))

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = str(uuid.uuid4().int)[:6]  # Get the first 6 digits of a UUID
            if not db.query(PromoCodes).filter_by(promoId=unique_id).first():  # Check if ID is already in use
                return unique_id
            
