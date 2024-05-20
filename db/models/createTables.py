from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from user import Base as userBase
from product import Base as productBase
#from product import Base 
from promocodes import Base as promocodeBase
from address import Base as addressBase
from cart import Base as cartBase
from orders import Base as ordersBase
from address_mapping import Base as addressMappingBase

import urllib.parse
import os
from dotenv import load_dotenv
import pymysql
load_dotenv()


# username="postgres"
# password=os.getenv("DB_PASSWORD")
# encoded_password = urllib.parse.quote(password, safe='')
# DATABASE_URL = f"postgresql://{username}:{encoded_password}"+"@localhost:5432/ecommerce"
# engine = create_engine(DATABASE_URL)

DATABASE_URL = "mysql+mysqlconnector://u540836934_root:Nandakishore#1901@srv1111.hstgr.io:3306/u540836934_testEcommerce"
engine = create_engine(DATABASE_URL)

userBase.metadata.create_all(engine)
productBase.metadata.create_all(engine)
promocodeBase.metadata.create_all(engine)
addressBase.metadata.create_all(engine)

#addressMappingBase.metadata.create_all(engine)
cartBase.metadata.create_all(engine)
ordersBase.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Create a session
session = Session()
