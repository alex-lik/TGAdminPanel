from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ChannelGroupCreate, ChannelGroupResponse
from database import get_db
import crud

router = APIRouter()

@router.post("/", response_model=ChannelGroupResponse)
def create_group(group: ChannelGroupCreate, db: Session = Depends(get_db)):
    return crud.create_channel_group(db, group)

@router.get("/", response_model=list[ChannelGroupResponse])
def get_groups(db: Session = Depends(get_db)):
    return crud.get_channel_groups(db)

@router.get("/{group_id}", response_model=ChannelGroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_channel_group(db, group_id)
    if not group:
        raise HTTPException(404)
    return group

@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    crud.delete_channel_group(db, group_id)
    return {"message": "Channel group deleted"}
