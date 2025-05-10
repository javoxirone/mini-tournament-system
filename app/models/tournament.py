from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, relationship
from app.db import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False, unique=True)
    max_players = mapped_column(Integer, nullable=False)
    start_at = mapped_column(DateTime, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    players = relationship("Player", back_populates="tournament")