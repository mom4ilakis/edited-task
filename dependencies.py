from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from db import get_session
from services import CrawlerService

SessionDep = Annotated[Session, Depends(get_session)]

CrawlerServiceDep = Annotated[CrawlerService, Depends()]
