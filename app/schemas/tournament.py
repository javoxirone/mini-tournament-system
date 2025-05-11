from datetime import datetime
from pydantic import BaseModel, ConfigDict, computed_field

from app.schemas.common import UTCBaseModel
from app.services.player import get_players_count_by_tournament


class TournamentInDBInput(UTCBaseModel):
    name: str
    max_players: int
    start_at: datetime


class TournamentInDBOutput(UTCBaseModel):
    id: int
    name: str
    max_players: int
    start_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def registered_players(self) -> int:
        players_count = get_players_count_by_tournament(self.id)
        return players_count