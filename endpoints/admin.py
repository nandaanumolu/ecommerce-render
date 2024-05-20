from fastapi import APIRouter, HTTPException, Depends,FastAPI, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker 

from db.models.product import Product
from fastapi import Form

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

from db.models.promocodes import PromoCodes
from db.models.user import User

from models.product import ProductCreate
from models.promocode import PromotionalCodeCreate,EmailBody,SMSBody

from db.session import get_db,get_engine
adminRouter = APIRouter()

# Pydantic model for product creation request
engine=get_engine()
Session = sessionmaker(bind=engine) 


# FastAPI endpoint to add product
@adminRouter.post("/products")
async def create_product(productName:str=Form(...),
    productDescription:str=Form(...),
    productCost:str=Form(...),
    productRating:str=Form(...), productImage: UploadFile = UploadFile(...) ):
    db = Session()
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
    #with Session(engine) as db:
    db = Session()
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

def send_email(subject, recipient_emails):
    html_file_path = "email_content/index.html"
    # Set SendGrid API key
    api_key = os.environ.get('SENDGRID')
    if not api_key:
        raise ValueError("SendGrid API key is not set in the environment variables.")
    # Initialize SendGrid client
    sg = SendGridAPIClient(api_key)
    # Read HTML file content
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    # Create Mail object
    message = Mail(
        from_email='nandakishore087@gmail.com',
        to_emails=recipient_emails,
        subject=subject,
        html_content=html_content
    )
    # Send message
    try:
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    

@adminRouter.post("/sendEmail")
async def sendEmailAlert(emailDetails:EmailBody):
    try:
        for email in emailDetails.customerEmails:
            success = send_email(emailDetails.EmailSubject, email)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to send email to {email}.")
        return {"message": "Emails sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@adminRouter.post("/sendEmail")
async def sendEmailAlertToAll(emailDetails:EmailBody):
    db = Session()
    #with Session(engine) as db:
    try:
        user=db.query(User).all()
        for email in user.email:
                success = send_email(emailDetails.EmailSubject, email)
        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to send email to {email}.")  
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Emails sent successfully"}



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