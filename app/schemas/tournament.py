from datetime import datetime

from pydantic import BaseModel

class TournamentInDBInput(BaseModel):
    name: str
    max_players: int
    start_at: datetime

class TournamentInDBOutput(BaseModel):
    id: int
    name: str
    max_players: int
    start_at: datetime
    created_at: datetime