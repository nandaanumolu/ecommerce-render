from pydantic import BaseModel

class PromotionalCodeCreate(BaseModel):
    promoCode: str
    promoValidationdate: str
    promoWorth: int

class EmailBodyParticularUsers(BaseModel):
    EmailSubject:str
    CustomerEmails:list

class EmailBodyAllUsers(BaseModel):
    EmailSubject:str
    


class SMSBody(BaseModel):
    smsContent:str
    customerNumber:str