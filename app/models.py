from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class WantedCriminal(Base):
    __tablename__ = "wanted_criminals"
    __table_args__ = (
        CheckConstraint("difficulty BETWEEN 1 AND 10", name="ck_difficulty_range"),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)  # real name may be unknown
    nickname = Column(String(100), nullable=False)
    reward = Column(Numeric(14, 2), nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    last_known_location_note = Column(Text, nullable=True)
    difficulty = Column(Integer, nullable=False)
    armed = Column(Boolean, nullable=False, default=False)
    has_crew = Column(Boolean, nullable=False, default=False)
    escape_master = Column(Boolean, nullable=False, default=False)

    hunts = relationship(
        "HuntLog", back_populates="criminal", cascade="all, delete-orphan"
    )


class HuntLog(Base):
    __tablename__ = "hunt_logs"

    id = Column(Integer, primary_key=True, index=True)
    criminal_id = Column(
        Integer,
        ForeignKey("wanted_criminals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    success = Column(Boolean, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    criminal = relationship("WantedCriminal", back_populates="hunts")
