from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from sqlalchemy import select,delete,update



router = APIRouter(
  tags=['Users']
)
# users Table routes:

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.SignupResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
  
  hashed_password = utils.hash(user.password)
  user.password = hashed_password
  
  new_user = models.User(**user.model_dump())
  
  db.add(new_user)
  db.commit()
  
  db.refresh(new_user)
  
  return new_user

@router.get("/users/{id}", response_model=schemas.SignupResponse)
def get_user(id: int, db: Session = Depends(get_db)):
  statement = select(models.User).where(models.User.id == id)
  user = db.scalar(statement)
  
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"user with id {id} was not found"
    )
    
  return user