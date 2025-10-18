from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PostCreate, PostResponse
from database import get_db
import crud
from tasks import publish_post_task
from loguru import logger

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating post for group_id={post.group_id}, publish_now={post.publish_now}")
        db_post = crud.create_post(db, post)
        if post.publish_now:
            publish_post_task.delay(db_post.id)  # немедленная публикация через очередь Celery
        # если post.publish_now == False — публикацией займётся Celery Beat через schedule_published_posts
        logger.info(f"Post created with id={db_post.id}")
        return db_post
    except Exception as e:
        logger.error(f"Failed to create post: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create post: {str(e)}")

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    try:
        return crud.get_posts(db)
    except Exception as e:
        logger.error(f"Failed to get posts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get posts: {str(e)}")

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    try:
        post = crud.get_post(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get post {post_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get post: {str(e)}")

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_post(db, post_id)
        logger.info(f"Post {post_id} deleted")
        return {"message": "Post deleted"}
    except Exception as e:
        logger.error(f"Failed to delete post {post_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete post: {str(e)}")
