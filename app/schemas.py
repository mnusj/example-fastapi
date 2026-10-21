from pydantic import BaseModel, conint
from datetime import datetime
from pydantic import EmailStr
from typing import Optional

class PostBase(BaseModel):
  title:str
  content:str
  published:bool = True
  
class PostCreate(PostBase):
  pass


class Post(BaseModel): #responnse model class
  title: str
  content:str
  published:bool = True
  created_at: datetime
  
  class config:
    from_attributes = True
    
    
    



class CreateUser(BaseModel):
  email: EmailStr
  password: str
  
class SignupResponse(BaseModel):
  id: int
  email: EmailStr 
  created_at: datetime
  
  class config:
    from_attributes = True
    
class UserLogin(BaseModel):
  email: EmailStr
  password: str
  
  
class Token(BaseModel):
  access_token: str
  token_type: str
  
  
class TokenData(BaseModel):
  id: Optional[str] = None
  
  
  
class Vote(BaseModel):
  post_id: int
  dir: conint(le=1)  # Ensure that dir is an integer less than or equal to 1