import logging
import os

from sqlmodel import SQLModel, create_engine, Session

from constants import DB_FILE_FOLDER

from models import CrawlerProcess

DB_FILE_FOLDER.mkdir(parents=True, exist_ok=True)

sqlite_file_name = DB_FILE_FOLDER / "database.db"



sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=os.environ.get("DEBUG", False))


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    logger = logging.getLogger("db")
    logger.info("Syncing DB and models!")
    create_db_and_tables()


if __name__ == '__main__':
    main()
