from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChannelCreate(BaseModel):
    name: str
    channel_id: str
    bot_token: str
    language: str = ""

class ChannelResponse(ChannelCreate):
    id: int
    class Config:
        orm_mode = True

class ChannelGroupCreate(BaseModel):
    name: str

class ChannelGroupResponse(BaseModel):
    id: int
    name: str
    channels: List[ChannelResponse]
    class Config:
        orm_mode = True

class PostContentCreate(BaseModel):
    channel_id: int
    content: str

class PostCreate(BaseModel):
    group_id: int
    publish_time: datetime
    publish_now: bool = False
    contents: List[PostContentCreate]

class PostContentResponse(PostContentCreate):
    id: int
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    id: int
    group_id: int
    publish_time: datetime
    status: str
    created_at: datetime
    contents: List[PostContentResponse]
    class Config:
        orm_mode = True
