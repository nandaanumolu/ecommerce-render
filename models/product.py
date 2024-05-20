from pydantic import BaseModel

class ProductCreate(BaseModel):
    productName: str
    productDescription: str
    productCost: str
    productRating: str

class SearchBody(BaseModel):
    query:str