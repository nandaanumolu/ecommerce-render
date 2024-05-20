from fastapi import APIRouter, HTTPException, Depends,FastAPI, UploadFile
from sqlalchemy.orm import Session
from db.models.product import Product
from fastapi import Form

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

from db.models.promocodes import PromoCodes
from models.product import ProductCreate
from models.promocode import PromotionalCodeCreate,EmailBody,SMSBody

from db.session import get_db,get_engine
adminRouter = APIRouter()

# Pydantic model for product creation request
engine=get_engine()

# Function to add product
def add_product(db, product: Product, image: bytes):
    db.add(product)
    db.commit()
    db.refresh(product)
    product.productImage = image
    return product

# FastAPI endpoint to add product
@adminRouter.post("/products")
async def create_product(productName:str=Form(...),
    productDescription:str=Form(...),
    productCost:str=Form(...),
    productRating:str=Form(...), productImage: UploadFile = UploadFile(...) ):
    with Session(engine) as db:
        try:
            productId=Product.generate_unique_id()
            # Read image file
            image_bytes = await productImage.read()
            # Create product instance
            new_product = Product(productName=productName,
                                productDescription=productDescription,
                                productCost=productCost,
                                productRating=productRating, 
                                productId=productId,
                                productImage=image_bytes)
            # Add product to database
            #created_product = add_product(db, new_product, image_bytes)
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            return {"message": "Product added successfully", "product_id": new_product.productId}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

@adminRouter.post("/promotional-codes")
async def create_promotional_code(promo_data: PromotionalCodeCreate):
    with Session(engine) as db:
        try:
            promoId=PromoCodes.generate_unique_id()
            new_promo = PromoCodes(**promo_data.dict(),promoId=promoId)
            db.add(new_promo)
            db.commit()
            db.refresh(new_promo)
            return {"message": "Promotional code added successfully", "promo_id": new_promo.promoId}
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

def send_email(subject, recipient_email):

    html_file_path = "email_content/index.html"
    # Set SendGrid API key
    api_key = os.environ.get('SENDGRID')

    # Initialize SendGrid client
    sg = SendGridAPIClient(api_key)

    # Read HTML file content
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Create Mail object
    message = Mail(
        from_email='nandakishore087@gmail.com',
        to_emails=recipient_email,
        subject=subject,
        html_content=html_content
    )

    # Send message
    try:
        response = sg.send(message)
        return True
    except Exception as e:
        return False

@adminRouter.post("/sendEmail")
async def sendEmailAlert(emailDetails:EmailBody):
    try:
        send_email(emailDetails.EmailSubject, emailDetails.customerEmail)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@adminRouter.post("/sendSMS")
async def sendSMSAlert(smsDetails:SMSBody):
    try:
        account_sid= os.environ.get('SMS_ACCOUNT_SID')
        auth_token= os.environ.get('SMS_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
    from_='+14142468721',
    body=smsDetails.smsContent,
    to=smsDetails.customerNumber
        )
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))