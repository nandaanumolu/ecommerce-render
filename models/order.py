from pydantic import BaseModel

class createOrder(BaseModel):
    userId:int
    productIds:dict
    name: str
    mobileNumber : str
    pincode: str
    locality : str
    address: str
    city : str
    alternatePhonenumber: str
    amount:float
    currency:str
    # orderStatus:str
    # paymentId:str
    # Amount :str
    # promoCodeId :int

class editOrder(BaseModel):
    orderId:int
    orderStatus:str