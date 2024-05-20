# app/db/models.py
import uuid
import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import sys
import os

# Add the path to the top-level directory of your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../' )))
from db.session import SessionLocal

Base = declarative_base()

db=SessionLocal()
class User(Base):
    __tablename__ = "users_table"
    name = Column(String(100))
    userId = Column(Integer, primary_key=True, index=True)
    phoneNumber=Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))

    @staticmethod
    def generate_unique_id():
        """
        Generate a 6-digit unique ID
        """
        while True:
            unique_id = str(uuid.uuid4().int)[:6]  # Get the first 6 digits of a UUID
            if not db.query(User).filter_by(userId=unique_id).first():  # Check if ID is already in use
                return unique_id
            
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using bcrypt
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a password using bcrypt
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

