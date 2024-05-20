from pydantic import BaseModel

class CartCreate(BaseModel):
    userId: int
    productId: int

class CartRemove(BaseModel):
    cartId:int

class EditCart(BaseModel):
    cartId:int
    quantity:int
    userId:int