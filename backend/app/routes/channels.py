from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ChannelCreate, ChannelResponse
from database import get_db
import crud

router = APIRouter()

@router.post("/{group_id}/channels/", response_model=ChannelResponse)
def add_channel(group_id: int, channel: ChannelCreate, db: Session = Depends(get_db)):
    return crud.add_channel(db, group_id, channel)

@router.delete("/{channel_id}")
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    crud.delete_channel(db, channel_id)
    return {"message": "Channel deleted"}
