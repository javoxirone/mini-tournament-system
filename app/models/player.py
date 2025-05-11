from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import mapped_column, relationship
from app.db import Base


class Player(Base):
    __tablename__ = "players"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False)
    tournament_id = mapped_column(ForeignKey("tournaments.id"), nullable=False)
    registered_at = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("email", "tournament_id", name="unique_player_per_tournament"),
    )

    tournament = relationship("Tournament", back_populates="players")