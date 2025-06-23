from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ChannelGroup(Base):
    __tablename__ = "channel_groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    channels = relationship("Channel", back_populates="group", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="group", cascade="all, delete-orphan")

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("channel_groups.id"))
    name = Column(String, nullable=False)
    channel_id = Column(String, nullable=False)
    bot_token = Column(String, nullable=False)
    language = Column(String, nullable=True)
    group = relationship("ChannelGroup", back_populates="channels")
    post_contents = relationship("PostContent", back_populates="channel")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("channel_groups.id"))
    publish_time = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)
    group = relationship("ChannelGroup", back_populates="posts")
    contents = relationship("PostContent", back_populates="post", cascade="all, delete-orphan")

class PostContent(Base):
    __tablename__ = "post_contents"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    channel_id = Column(Integer, ForeignKey("channels.id"))
    content = Column(Text, nullable=False)
    post = relationship("Post", back_populates="contents")
    channel = relationship("Channel", back_populates="post_contents")
    message_id = Column(Integer, nullable=True)  # ID сообщения в отправщике
    image_path = Column(String, nullable=True)
