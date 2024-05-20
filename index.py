from fastapi import FastAPI
from endpoints.user import router
from endpoints.admin import adminRouter
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
# Secret key for signing the session cookie
SECRET_KEY = "ecommerce"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:3001","*"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

# Initialize session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.include_router(router)
app.include_router(adminRouter)
