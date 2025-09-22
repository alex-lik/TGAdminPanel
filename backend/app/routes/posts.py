from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import PostCreate, PostResponse
from database import get_db
import crud
from tasks import publish_post_task

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    print(post)
    db_post = crud.create_post(db, post)
    if post.publish_now:
        publish_post_task.delay(db_post.id)  # немедленная публикация через очередь Celery
    # если post.publish_now == False — публикацией займётся Celery Beat через schedule_published_posts
    return db_post

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    crud.delete_post(db, post_id)
    return {"message": "Post deleted"}
