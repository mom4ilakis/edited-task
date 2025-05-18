from datetime import date, datetime
import uuid

from sqlmodel import SQLModel, Field


class CrawlerProcess(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=uuid.uuid4)
    url: str = Field()
    links_to_follow: int = Field(gt=0)
    status: str = Field(default="Queued")
    created_at: date = Field(default_factory=datetime.now)
    updated_at: date = Field(default_factory=datetime.now)
