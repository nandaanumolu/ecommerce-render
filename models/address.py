from pydantic import BaseModel

class addAddress(BaseModel):
    name: str
    mobileNumber : str
    pincode: str
    locality : str
    address: str
    city : str
    alternatePhonenumber: str
    userId:int