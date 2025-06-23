from database import SessionLocal
from models import Post
from sender import send_to_publisher
from loguru import logger
from datetime import datetime, UTC

async def publish_post(post_id: int):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        for content in post.contents:
            message_id = await send_to_publisher(
                token=content.channel.bot_token,
                chat_id=content.channel.channel_id,
                parse_mode="HTML",
                text=content.content,
                image_path=getattr(content, "image_path", None),  
            )
            content.message_id = message_id
        post.status = "published"
        db.commit()
    finally:
        db.close()


