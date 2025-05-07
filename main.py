from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated
from send_email_request import send_email_request
from send_confirmation_email import send_confirmation_email
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from vars import smtp_sender_email

limiter = Limiter(key_func=get_remote_address, strategy="sliding-window-counter", enabled=True, default_limits=["10/minute"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
)

validation_str = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
class User_data(BaseModel):
    user_full_name: validation_str
    user_email: EmailStr
    user_phone: validation_str
    user_address: validation_str
    user_data: validation_str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_response = JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = jsonable_encoder({"Error": "Invalid data or missing fields"}),
    )
    return error_response

@app.post("/form-post", status_code=200)
async def form_post(request: Request, user_data: User_data):
    user_data_args = [user_data.user_full_name, user_data.user_email, user_data.user_phone, user_data.user_address, user_data.user_data]
    await send_email_request(smtp_sender_email, *user_data_args)
    await send_confirmation_email(user_data.user_email)
    return {"message": "Form data sent successfully!"}