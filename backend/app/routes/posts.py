from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from schemas import PostCreate, PostResponse
from database import get_db
import crud
from publisher import publish_post
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, UTC

router = APIRouter()
scheduler = AsyncIOScheduler()
scheduler.start()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_post = crud.create_post(db, post)
    if post.publish_now:
        background_tasks.add_task(publish_post, db_post.id)
    else:
        scheduler.add_job(
            publish_post,
            DateTrigger(run_date=post.publish_time),
            args=[db_post.id],
            id=f"post_{db_post.id}"
        )
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
