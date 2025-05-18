from enum import IntEnum, unique
from datetime import datetime
import uuid as _uuid

from sqlmodel import SQLModel, Field


@unique
class ProcesStatus(IntEnum):
    ERROR = -1
    QUEUED = 0
    PROCESSING = 1
    FINISHED = 2


class CrawlerProcess(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: _uuid.UUID = Field(default_factory=_uuid.uuid4)
    url: str = Field()
    links_to_follow: int = Field(gt=0)
    status: int = Field(default=ProcesStatus.QUEUED.value)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
