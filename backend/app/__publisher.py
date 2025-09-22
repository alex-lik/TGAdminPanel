from database import SessionLocal
from models import Post
from sender import send_to_publisher
from loguru import logger

def publish_post(post_id: int):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logger.error(f"Post {post_id} not found")
            return

        for content in post.contents:
            try:
                message_id = send_to_publisher(
                    token=content.channel.bot_token,
                    chat_id=content.channel.channel_id,
                    parse_mode="HTML",
                    text=content.content,
                    image_path=getattr(content, "image_path", None),
                )
                content.message_id = message_id
            except Exception as e:
                logger.error(f"Failed to send to {content.channel_id}: {e}")
                raise  # Для ретрая задачи

        post.status = "published"
        db.commit()
        logger.info(f"Published post {post_id}")
    finally:
        db.close()
