from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import WantedCriminal
from app.schemas import CriminalOut

router = APIRouter(prefix="/api/criminals", tags=["criminals"])

SORT_FIELDS = {
    "reward": WantedCriminal.reward.asc(),
    "-reward": WantedCriminal.reward.desc(),
}


@router.get("/", response_model=List[CriminalOut])
def list_criminals(
    min_reward: Optional[float] = Query(None, ge=0),
    max_reward: Optional[float] = Query(None, ge=0),
    armed: Optional[bool] = None,
    has_crew: Optional[bool] = None,
    escape_master: Optional[bool] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if min_reward is not None and max_reward is not None and min_reward > max_reward:
        raise HTTPException(400, "min_reward cannot be greater than max_reward")
    if sort is not None and sort not in SORT_FIELDS:
        raise HTTPException(400, "sort must be one of: reward, -reward")

    q = db.query(WantedCriminal)
    if min_reward is not None:
        q = q.filter(WantedCriminal.reward >= min_reward)
    if max_reward is not None:
        q = q.filter(WantedCriminal.reward <= max_reward)
    if armed is not None:
        q = q.filter(WantedCriminal.armed == armed)
    if has_crew is not None:
        q = q.filter(WantedCriminal.has_crew == has_crew)
    if escape_master is not None:
        q = q.filter(WantedCriminal.escape_master == escape_master)

    q = q.order_by(SORT_FIELDS[sort] if sort else WantedCriminal.id.asc())
    return q.all()


@router.get("/{criminal_id}/", response_model=CriminalOut)
def get_criminal(criminal_id: int, db: Session = Depends(get_db)):
    criminal = db.get(WantedCriminal, criminal_id)
    if criminal is None:
        raise HTTPException(404, "Criminal not found")
    return criminal
