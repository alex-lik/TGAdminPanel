from sqlalchemy.orm import Session
from models import ChannelGroup, Channel, Post, PostContent

def create_channel_group(db: Session, group_data):
    db_group = ChannelGroup(name=group_data.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_channel_groups(db: Session):
    return db.query(ChannelGroup).all()

def get_channel_group(db: Session, group_id: int):
    return db.query(ChannelGroup).filter(ChannelGroup.id == group_id).first()

def delete_channel_group(db: Session, group_id: int):
    group = db.query(ChannelGroup).filter(ChannelGroup.id == group_id).first()
    if group:
        db.delete(group)
        db.commit()

def add_channel(db: Session, group_id: int, channel_data):
    db_channel = Channel(group_id=group_id, **channel_data.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def delete_channel(db: Session, channel_id: int):
    ch = db.query(Channel).filter(Channel.id == channel_id).first()
    if ch:
        db.delete(ch)
        db.commit()

def create_post(db: Session, post_data):
    db_post = Post(
        group_id=post_data.group_id,
        publish_time=post_data.publish_time,
        status="published" if post_data.publish_now else "scheduled"
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    for c in post_data.contents:
        db_content = PostContent(
            post_id=db_post.id,
            channel_id=c.channel_id,
            content=c.content
        )
        db.add(db_content)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session):
    return db.query(Post).order_by(Post.created_at.desc()).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
