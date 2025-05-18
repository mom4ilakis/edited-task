from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from sqlmodel import Session

from dtos.StartCrawRequest import StartCrawRequest
from models.crawler_process import CrawlerProcess
from setup_db import get_session

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/isalive")
async def is_alive():
    return {"is_alive": True}


@app.get("/screenshots/{screenshot_id}")
async def get_screenshots(screenshot_id: str):
    return []


@app.post("/screenshots")
async def start_crawling(start_craw_request: StartCrawRequest, session: SessionDep):
    crawler_process = CrawlerProcess(url=start_craw_request.url, links_to_follow=start_craw_request.links_to_follow)
    session.add(crawler_process)
    session.commit()
    session.refresh(crawler_process)

    return {"id": crawler_process.uuid}


@app.get("/")
async def hello():
    return "WebScrapper 1.0.0"


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
