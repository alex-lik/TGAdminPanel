# tasks.py
from celery_app import celery
from database import SessionLocal
from models import Post
from sender import send_to_publisher
from loguru import logger
from datetime import datetime, timezone

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def publish_post_task(self, post_id):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logger.error(f"Post {post_id} not found")
            return

        for content in post.contents:
            try:
                # Функция send_to_publisher должна быть синхронной, либо используй anyio.run() для async
                message_id = send_to_publisher.__wrapped__(  # используем __wrapped__ чтобы обойти async def
                    token=content.channel.bot_token,
                    chat_id=content.channel.channel_id,
                    parse_mode="HTML",
                    text=content.content,
                    image_path=getattr(content, "image_path", None),
                )
                content.message_id = message_id
            except Exception as e:
                logger.error(f"Failed to send to {content.channel_id}: {e}")
                raise self.retry(exc=e)

        post.status = "published"
        db.commit()
        logger.info(f"Published post {post_id}")
    finally:
        db.close()

@celery.task
def schedule_published_posts():
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        posts = db.query(Post).filter(Post.status == "scheduled", Post.publish_time <= now).all()
        for post in posts:
            publish_post_task.delay(post.id)
    finally:
        db.close()
