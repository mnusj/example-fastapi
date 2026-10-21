from typing import Optional
from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from sqlalchemy import select,delete,update
from .. import oauth2

router = APIRouter(
  tags=['Posts']
)

# using SQL alchemy
@router.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_new_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # 1. SQLAlchemy object create karo Pydantic data se
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)  # Assuming you have a relationship between Post and User models
    
    # 2. Database session mein add karo
    db.add(new_post)
    
    # 3. Database mein commit (save) karo
    db.commit()
    
    # 4. Refresh karo taaki generated 'id' aur 'created_at' mil jaye
    db.refresh(new_post)
    
    # 5. Saved data return karo
    return new_post

# it gives all post indside our database
@router.get("/getpost", response_model=list[schemas.Post])
def new_post(db: Session = Depends(get_db), limit: int = 1, skip: int = 0, search: Optional[str] = ""):
  statement = select(models.Post).where(models.Post.content.contains(search)).limit(limit)
  posts = db.scalars(statement).all()
  return posts

@router.get("/getpostbyid/{id}", response_model=schemas.Post)
def get_sp(id:int, db: Session = Depends(get_db)):
  statement = select(models.Post).where(models.Post.id == id)
  #execute the query
  post = db.scalar(statement)
  
  if post is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"post with id {id} was not found"
    )
  
  return post

@router.delete("/deletepostbyid/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  statement = select(models.Post).where(models.Post.id == id)
  post = db.scalar(statement)
  
  if not post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"post with id {id} was not found"
    )
  if post.owner_id != current_user.id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Not authorized to perform requested action"
    )
  
  db.delete(post)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
  
  
@router.put("/updatepost/{id}", response_model=schemas.Post)
def update_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  the_post = db.scalar(select(models.Post).where(models.Post.id == id))
  
  if not the_post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"post with id {id} was not found"
    )

  
  if the_post.owner_id != current_user.id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Not authorized to perform requested action"
    )

  # Pydantic v2: post.model_dump() | Pydantic v1: post.dict()
  for key, value in post.model_dump().items():
      setattr(the_post, key, value)

  db.commit()
  db.refresh(the_post)
  return the_post