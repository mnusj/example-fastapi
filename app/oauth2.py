from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from . import database, models, schemas
from .config import settings  # Import settings here

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # the endpoint of the login

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict): # access-token gonna have a payload  so whatever data we want to provide in the token we provide that as data:dict
  to_encode = data.copy() # we do not want to change the data so we just copy it, now to_encode is the data we will encode in the token
  
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire}) # it is also a dictionary and we provided this in the to_encode data 
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # calling jwt to encode the data....we pass (to_encode the dictionary to encode in the token, secret key, algorithm = hs256)
  
  return encoded_jwt # then we returned the encoded key

def verify_access_token(token: str, credential_exception):
  try: # without try except block if the user sent a invalid token it will crash with an unhadeled error 500 
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # here we decode the token we took from the user by passing the token the secret key and ago and then decode it using jwt.decode function
    id: str = payload.get("user_id") # we just extracted the data the user gave to us in the  payload, you can see it in auth.py 
    
    if id is None:
      raise credential_exception
    
    token_data = schemas.TokenData(id=str(id)) # to verify the provided data is valid and we alidate it through the schema from schemas.py
    
  except JWTError:
    raise credential_exception
  
  return token_data
  
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
  credential_exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credential", headers={"WWW-Authenticate": "Bearer"})
  
  token = verify_access_token(token, credential_exception)
  
  statement = select(models.User).where(models.User.id == int(token.id))
  
  user = db.scalar(statement)
  
  
  return user