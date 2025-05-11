from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime, timezone


class UTCBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @field_serializer("*")
    def serialize_datetime(self, value: any, _info):
        if isinstance(value, datetime):
            return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return value