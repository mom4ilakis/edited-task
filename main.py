import logging
from logging.config import dictConfig
import uuid

import uvicorn
from fastapi import FastAPI, BackgroundTasks, Response, HTTPException

from constants import SCREENSHOTS_FOLDER
from dtos import IdResponse, StartCrawRequest
from logging_config import LOGGING_CONFIG
from models import ProcesStatus
from services import crawl_page, create_zip
from dependencies import CrawlerServiceDep

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("server")
app = FastAPI()

@app.get("/isalive")
async def is_alive():
    return {"is_alive": True}


@app.get("/screenshots/{screenshot_id}")
async def get_screenshots(screenshot_id: uuid.UUID, crawler_service: CrawlerServiceDep):
    crawler_process = crawler_service.find_crawler_process(screenshot_id)

    if crawler_process is None:
        raise HTTPException(status_code=404, detail="Screenshots not found!")

    if crawler_process.status in [ProcesStatus.QUEUED, ProcesStatus.PROCESSING]:
        raise HTTPException(status_code=400, detail="Screenshots are still generating!")

    if crawler_process.status == ProcesStatus.ERROR:
        raise HTTPException(status_code=422, detail="Screenshots couldn't be generated. Resubmit page for processing!")

    screenshots_folder = SCREENSHOTS_FOLDER / str(screenshot_id)

    buffer = create_zip(screenshots_folder)

    return Response(content=buffer.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": f"attachment; filename={screenshot_id}.zip"})


@app.post("/screenshots")
async def start_crawling(start_craw_request: StartCrawRequest, background_tasks: BackgroundTasks,
                         crawler_service: CrawlerServiceDep) -> IdResponse:
    crawler_process = crawler_service.create_crawler_process(start_craw_request.url, start_craw_request.links_to_follow)
    background_tasks.add_task(crawl_page, crawler_process, crawler_service)
    return IdResponse(id=crawler_process.uuid)


@app.get("/")
async def hello():
    return "WebScrapper 1.0.0"


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
