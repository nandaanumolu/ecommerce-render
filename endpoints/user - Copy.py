from fastapi import APIRouter, HTTPException, Depends, Request,FastAPI
import razorpay
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from models.user import UserCreate
from models.cart import CartCreate,CartRemove,EditCart
from models.address import addAddress
from models.order import createOrder,editOrder
from sqlalchemy.orm import Session
from models.profileDetails import profileDetails
from models.product import SearchBody
from models.loginUser import UserLogin
from models.paymentVerification import PaymentVerify

from db.session import get_engine
from db.models.address_mapping import AddressMapping
from db.models.orders import Order,OrderItem
from db.models.user import User
from db.models.promocodes import PromoCodes
from db.models.product import Product
from db.models.cart import Cart
from db.models.address import Address

router = APIRouter()
load_dotenv()

@router.post("/signup")
def signup( request: Request,user: UserCreate, engine: Session = Depends(get_engine)):
    # Check if user with the given email already exists
    try:
        session = request.session
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            # Create a new user
            uId=User.generate_unique_id()
            hashedPassword=User.hash_password(user.password)
            createdUser = User(userId=uId,name=user.name,phoneNumber=user.phoneNumber,email=user.email, password=hashedPassword)
            with Session(engine) as session:
                session.add(createdUser)
                #session.add(some_other_object)
                session.commit()
                session.refresh(createdUser)
            
            session['user_email']=user.email
            validatedUser=getProfileDetails(uId,db)
            return validatedUser
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/login")
def login(user:UserLogin,db: Session = Depends(get_db)):
    try:
        DBuser=db.query(User).filter(User.email == user.email).first()
        userHashedPassword=DBuser.password
        validUserFlag=User.verify_password(user.password,userHashedPassword)
        if(validUserFlag):
            print("nanda anumolu")
            validatedUser=getProfileDetails(DBuser.userId,db)
            return {"validUser":validatedUser}
        else:
            return {"validUser":validUserFlag}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/getAllProducts")
async def get_all_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/searchResults")
async def get_all_products(search_query: SearchBody , db: Session = Depends(get_db)):
    try:
        if search_query.query:
            products = db.query(Product).filter(Product.productName.ilike(f"%{search_query.query}%")).all()
        else:
            products = db.query(Product).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/addToCart")
async def add_to_cart(cart: CartCreate, db: Session = Depends(get_db)):
    try:
        cId=Cart.generate_unique_id()
        addedCart=Cart(userId=cart.userId, productId=cart.productId, cartId=cId,quantity=1)
        db.add(addedCart)
        db.commit()
        db.refresh(addedCart)
        return {"message":"Added to cart successfully","cartId":cId}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/editCart")
async def edit_cart(cart:EditCart,db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.cartId == cart.cartId).first()
    cart_items.quantity=cart.quantity
    db.add(cart_items)
    db.commit()
    db.refresh(cart_items)
    return {"message":"successfully cart has been modified","cartId":cart_items.cartId}


@router.delete("/removeFromCart")
async def remove_from_cart(cart: CartRemove, db: Session = Depends(get_db)):
    try:
        cart_items = db.query(Cart).filter(Cart.cartId == cart.cartId).all()
        if not cart_items:
            raise HTTPException(status_code=404, detail="Cart items not found")

        for item in cart_items:
            db.delete(item)
        db.commit()
        
        return {"message": "Cart items removed successfully", "cartId": cart.cartId}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/editOrder")
async def edit_order(Editorder: editOrder,db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.orderId == Editorder.orderId).first()
        if not order:
            raise HTTPException(status_code=404, detail="order not found")
        
        order.orderStatus=Editorder.orderStatus
        db.commit()
        db.refresh(order)
        
        return {"message": "successfully edited order", "cartId": Editorder.orderId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/getAllPromoCodes")
async def get_all_promocodes(db: Session = Depends(get_db)):
    try:
        promocodes = db.query(PromoCodes).all()
        return promocodes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.post("/addAddress")
async def add_address(address: addAddress, db: Session = Depends(get_db)):
    try:
        AId=Address.generate_unique_id()
        new_address = Address(name=address.name,
                                mobileNumber=address.mobileNumber,
                                pincode= address.pincode,
                                locality=address.locality,
                                address=address.address,
                                city=address.city,
                                alternatePhonenumber=address.alternatePhonenumber,
                                addressId=AId)
        uniqueAddressMappingId=AddressMapping.generate_unique_id()
        address_mapping=AddressMapping(
            addressId=AId,
            userId=address.userId,
            addressMappingId=uniqueAddressMappingId
        )
        db.add(address_mapping)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return {"message":"Added address successfully","addressId":AId,"addressMapping":address_mapping.addressMappingId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/createOrder")
async def createUserOrder(order:createOrder,db: Session = Depends(get_db)):
    load_dotenv()
    try:      
        oId=Order.generate_unique_id()
        new_order = Order(userId=order.userId,orderId=oId,orderStatus=None,
                          paymentId=None, Amount=None,promoCodeId=None,paymentStatus=None,currency=order.currency)
        
        AId=Address.generate_unique_id()
        new_address = Address(name=order.name,
                                mobileNumber=order.mobileNumber,
                                pincode= order.pincode,
                                locality=order.locality,
                                address=order.address,
                                city=order.city,
                                alternatePhonenumber=order.alternatePhonenumber,
                                addressId=AId)
        # new_order = Order(userId=order.userId,orderId=oId,addressMappingId=order.addressMappingId)
        db.add(new_order)
        db.add(new_address)
        db.commit()
        db.refresh(new_order)
        db.refresh(new_address)

        # amount=0
        # productDetails=[]
        for pid,quantity in order.productIds.items():
            oIId=OrderItem.generate_unique_id()
            product_cost=db.query(Product).filter(Product.productId == int(pid)).first()      
            if not product_cost:
                raise HTTPException(status_code=404, detail="product not found")
            
            #product_name=product_cost.productName
            new_order_item = OrderItem(orderId=oId,productId=pid,quantity=quantity,orderItemId=oIId,price=int(quantity)*product_cost.productCost)
            db.add(new_order_item)
            db.commit()
            db.refresh(new_order_item)  
            #amount=amount+(product_cost.productCost*int(quantity))
            #productDetails.append({product_name:new_order_item.price})
        #updating amount in the order

        edit_order_amount=db.query(Order).filter(Order.orderId == oId).first()
        if not edit_order_amount:
            raise HTTPException(status_code=404, detail="order not found")
        edit_order_amount.Amount=order.amount
        db.add(edit_order_amount)
        db.commit()
        db.refresh(edit_order_amount)
        
        razor_id=os.getenv("razor_id")
        razor_secret_id=os.getenv('razor_secret_id')
        client = razorpay.Client(auth=(razor_id, razor_secret_id))
        DATA = {
            "amount": order.amount,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        response=client.order.create(data=DATA)
        if not response:
            raise HTTPException(status_code=404, detail="Razorpay order not created")
        
        return {"message":"New order created successfully","orderId":oId,"Razorpay_orderId":response["id"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def getProfileDetails(userId: int, db: Session):
    try:
        userDetails=db.query(User).filter(User.userId == userId).first()
        userInfo={
            'Name':userDetails.name,
            'Email':userDetails.email,
            'Number':userDetails.phoneNumber,
            'userId':userDetails.userId
        }
        print("kowshik")
        orderDetails=db.query(Order).filter(Order.userId == userId).all()
        print("nanda",orderDetails)
        
        allOrders=[]
        for order in orderDetails:
            orderItems=db.query(OrderItem).filter(OrderItem.orderId==order.orderId).all()
            allItemsInOrder=[]
            for item in orderItems:
                product=db.query(Product).filter(Product.productId == item.productId).first()
                info={
                    "ProductName":product.productName,
                    "ProductImage":product.productImage,
                    "ProductPrice":product.productCost,
                    "ProductQunatity":item.quantity
                }
                allItemsInOrder.append(info)
            allOrders.append({order.orderId:{"items":allItemsInOrder,"orderAmount":order.Amount}})

        cartDetails=db.query(Cart).filter(Cart.userId == userId).all()
        cartInfo=[]
        for item in cartDetails:
            product=db.query(Product).filter(Product.productId == item.productId).first()
            info={
                "ProductName":product.productName,
                "ProductImage":product.productImage,
                "ProductQuantity":item.quantity,
                "ProductCost":item.quantity*product.productCost
                
            }
            cartInfo.append(info)
        addressDetails=db.query(AddressMapping).filter(AddressMapping.userId == userId).all()
        addressInfo=[]
        for address in addressDetails:
            userAddress=db.query(Address).filter(Address.addressId == address.addressId).first()
            address_dict={**userAddress.__dict__ ,'AddressMappingID':address.addressMappingId}
            addressInfo.append(address_dict )

        profileDetails={
            "userInfo":userInfo,
            "ordersInfo":allOrders,
            "cartInfo":cartInfo,
            "addressInfo":addressInfo
        }
        return profileDetails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/payment")
async def paymentVerification(razorpay:PaymentVerify,db: Session = Depends(get_db)):
    load_dotenv()
    razor_id=os.getenv("razor_id")
    razor_secret_id=os.getenv('razor_secret_id')
    client = razorpay.Client(auth=(razor_id, razor_secret_id))

    payment_status=client.utility.verify_payment_signature({
    'razorpay_order_id': razorpay.OrderId,
    'razorpay_payment_id': razorpay.paymentId,
    'razorpay_signature': razorpay.paymentSignature
    })
    edit_payment_status=db.query(Order).filter(Order.orderId == razorpay.OrderId).first()
    if not edit_payment_status:
        raise HTTPException(status_code=404, detail="order not found")
    
    edit_payment_status.paymentId=razorpay.paymentId
    edit_payment_status.paymentStatus=payment_status
    db.commit()
    db.refresh(edit_payment_status)

    return {"Order_id":razorpay.OrderId, "Payment_status":payment_status}




@router.post("/logout")
async def logout(request: Request):
    session = request.session
    session.clear()
    return {"message": "Logout successful"}

