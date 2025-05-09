from datetime import datetime

from pydantic import BaseModel

class PlayerInDBInput(BaseModel):
    name: str
    email: str
    tournament_id: int

class PlayerInDBOutput(BaseModel):
    id: int
    name: str
    email: str
    tournament_id: int
    registered_at: datetime