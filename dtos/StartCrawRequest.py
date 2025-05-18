from pydantic import BaseModel, Field


class StartCrawRequest(BaseModel):
    url: str = Field(title="URL to scrape")
    links_to_follow: int = Field(gt=0, title="The first N link to follow")
