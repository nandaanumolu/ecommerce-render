from pydantic import BaseModel

class UserCreate(BaseModel):
    name:str
    phoneNumber:str
    email: str
    password: str
    
