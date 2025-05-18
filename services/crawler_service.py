import logging
from uuid import UUID

from fastapi.params import Depends

from constants import SCREENSHOTS_FOLDER
from db import get_session
from models import CrawlerProcess, ProcesStatus
from sqlmodel import Session, select

from spider import crawl

logger = logging.getLogger("server")


class CrawlerService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session: Session = session

    def update_crawler_status(self, crawler_process: CrawlerProcess, new_status: ProcesStatus):
        crawler_process.status = new_status
        self.session.add(crawler_process)
        self.session.commit()

    def find_crawler_process(self, uuid: UUID):
        query = select(CrawlerProcess).where(CrawlerProcess.uuid == uuid)
        return next(self.session.exec(query))

    def create_crawler_process(self, url, links_to_follow):
        crawler_process = CrawlerProcess(url=url, links_to_follow=links_to_follow)
        self.session.add(crawler_process)
        self.session.commit()
        self.session.refresh(crawler_process)
        return crawler_process


async def crawl_page(crawler_process: CrawlerProcess, crawler_service: CrawlerService):
    logger.info(f"Crawling page: {crawler_process.url} and first {crawler_process.links_to_follow} links")
    crawler_service.update_crawler_status(crawler_process, ProcesStatus.PROCESSING)
    try:
        await crawl(crawler_process.url, crawler_process.links_to_follow, crawler_process.uuid, SCREENSHOTS_FOLDER)
        crawler_service.update_crawler_status(crawler_process, ProcesStatus.FINISHED)
    except Exception as e:
        logger.error(e)
        crawler_service.update_crawler_status(crawler_process, ProcesStatus.ERROR)
