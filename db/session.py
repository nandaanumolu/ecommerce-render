from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv()

# username="postgres"
# password=os.getenv("DB_PASSWORD")
# encoded_password = urllib.parse.quote(password, safe='')
# DATABASE_URL = f"postgresql://{username}:{encoded_password}"+"@localhost:5432/ecommerce"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# host="localhost",
# user="root",
# password="Gmk@2324",
# database_name="ecommerce"
# port = '3306'
# connection_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database_name}"
# # Create the engine
# engine = create_engine(connection_url)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DATABASE_URL = "mysql+mysqlconnector://u540836934_root:Nandakishore#1901@srv1111.hstgr.io:3306/u540836934_testEcommerce"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_engine():
    return engine