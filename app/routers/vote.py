from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..schemas import Vote
from sqlalchemy.orm import Session
from ..database import get_db
from ..import models
from .. import oauth2



router = APIRouter(
    tags=['Votes'],
    prefix='/vote'
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    # Check if the user has already voted on this post
    existing_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id  # Assuming you have a way to get the current user's ID
    ).first()

    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted on this post")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not voted on this post")
        db.delete(existing_vote)
        db.commit()
        return {"message": "Vote removed successfully"}