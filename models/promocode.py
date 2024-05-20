from pydantic import BaseModel

class PromotionalCodeCreate(BaseModel):
    promoCode: str
    promoValidationdate: str
    promoWorth: int

class EmailBody(BaseModel):
    EmailSubject:str
    customerEmails:list[str]

class SMSBody(BaseModel):
    smsContent:str
    customerNumber:str