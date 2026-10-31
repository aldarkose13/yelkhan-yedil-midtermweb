from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HuntLog, WantedCriminal
from app.schemas import HuntCreate, HuntOut, HuntUpdate

router = APIRouter(prefix="/api/hunts", tags=["hunts"])


def _get_hunt_or_404(db: Session, hunt_id: int) -> HuntLog:
    hunt = db.get(HuntLog, hunt_id)
    if hunt is None:
        raise HTTPException(404, "Hunt log not found")
    return hunt


@router.get("/", response_model=List[HuntOut])
def list_hunts(criminal_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(HuntLog)
    if criminal_id is not None:
        q = q.filter(HuntLog.criminal_id == criminal_id)
    return q.order_by(HuntLog.id.asc()).all()


@router.get("/{hunt_id}/", response_model=HuntOut)
def get_hunt(hunt_id: int, db: Session = Depends(get_db)):
    return _get_hunt_or_404(db, hunt_id)


@router.post("/", response_model=HuntOut, status_code=status.HTTP_201_CREATED)
def create_hunt(payload: HuntCreate, db: Session = Depends(get_db)):
    if db.get(WantedCriminal, payload.criminal_id) is None:
        raise HTTPException(404, "Criminal not found")
    hunt = HuntLog(**payload.model_dump())
    db.add(hunt)
    db.commit()
    db.refresh(hunt)
    return hunt


@router.patch("/{hunt_id}/", response_model=HuntOut)
def update_hunt(hunt_id: int, payload: HuntUpdate, db: Session = Depends(get_db)):
    hunt = _get_hunt_or_404(db, hunt_id)
    data = payload.model_dump(exclude_unset=True)
    if "success" in data and data["success"] is None:
        raise HTTPException(422, "success cannot be null")
    for field, value in data.items():
        setattr(hunt, field, value)
    db.commit()
    db.refresh(hunt)
    return hunt


@router.delete("/{hunt_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_hunt(hunt_id: int, db: Session = Depends(get_db)):
    hunt = _get_hunt_or_404(db, hunt_id)
    db.delete(hunt)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
