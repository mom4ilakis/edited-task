import uuid

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: uuid.UUID