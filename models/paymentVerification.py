from pydantic import BaseModel

class PaymentVerify(BaseModel):
    OrderId:int
    razorpayOrderId:str
    paymentId:str
    paymentSignature:str
