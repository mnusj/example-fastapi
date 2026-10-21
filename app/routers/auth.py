from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from sqlalchemy import select

from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
  tags=['Authentication']
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  
  statement = select(models.User).where(models.User.email == user_credentials.username)
  user = db.scalar(statement)
  
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid creadentials")
  
  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="invalid credentials")
  
  # create token
  # return token
  
  
  # here we used the function from oauth2.py function create_access_token to create a accesss token and the data parameter here we chose only to givve the users id to encode in the payload nothing else and the expiration time will automatically added 
  access_token = oauth2.create_access_token(data = {"user_id": user.id})
  
  return{"access_token" : access_token, "token_type": "Bearer"} # the token_type is "bearer"
