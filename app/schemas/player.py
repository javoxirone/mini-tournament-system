from datetime import datetime
from pydantic import ConfigDict

from app.schemas.common import UTCBaseModel


class PlayerInRequest(UTCBaseModel):
    name: str
    email: str

class PlayerInDBInput(UTCBaseModel):
    name: str
    email: str
    tournament_id: int


class PlayerInDBOutput(UTCBaseModel):
    id: int
    name: str
    email: str
    tournament_id: int
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)