import io
import os
import uuid
import zipfile
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, BackgroundTasks, Response, HTTPException
from sqlmodel import Session, select

from dtos import IdResponse, StartCrawRequest
from models.crawler_process import CrawlerProcess, ProcesStatus
from setup_db import get_session
from spider import craw

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]
SCREENSHOTS_FOLDER = Path(os.environ.get("SCREENSHOTS_FOLDER", "screenshots"))


async def craw_page(crawler_process: CrawlerProcess, session: Session):
    crawler_process.status = ProcesStatus.PROCESSING
    session.add(crawler_process)
    session.commit()
    try:
        await craw(crawler_process.url, crawler_process.links_to_follow, crawler_process.uuid, SCREENSHOTS_FOLDER)
        crawler_process.status = ProcesStatus.FINISHED
        session.add(crawler_process)
        session.commit()
    except Exception as e:
        print(e)
        crawler_process.status = ProcesStatus.ERROR
        session.add(crawler_process)
        session.commit()


@app.get("/isalive")
async def is_alive():
    return {"is_alive": True}


@app.get("/screenshots/{screenshot_id}")
async def get_screenshots(screenshot_id: uuid.UUID, session: SessionDep):
    query = select(CrawlerProcess).where(CrawlerProcess.uuid == screenshot_id)
    crawler_process = next(session.exec(query))

    if crawler_process is None:
        raise HTTPException(status_code=404, detail="Screenshots not found!")

    if crawler_process.status in [ProcesStatus.QUEUED, ProcesStatus.PROCESSING]:
        raise HTTPException(status_code=400, detail="Screenshots are still generating!")

    if crawler_process.status == ProcesStatus.ERROR:
        raise HTTPException(status_code=422, detail="Screenshots couldn't be generated. Resubmit page for processing!")

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        screenshots_folder = SCREENSHOTS_FOLDER / str(screenshot_id)
        for file_path in screenshots_folder.iterdir():
            zip_file.write(file_path, arcname=file_path.name)

    return Response(content=buffer.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": f"attachment; filename={screenshot_id}.zip"})


@app.post("/screenshots")
async def start_crawling(start_craw_request: StartCrawRequest, background_tasks: BackgroundTasks,
                         session: SessionDep) -> IdResponse:
    crawler_process = CrawlerProcess(url=start_craw_request.url, links_to_follow=start_craw_request.links_to_follow)
    session.add(crawler_process)
    session.commit()
    session.refresh(crawler_process)
    background_tasks.add_task(craw_page, crawler_process, session)
    return IdResponse(id=crawler_process.uuid)


@app.get("/")
async def hello():
    return "WebScrapper 1.0.0"


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
