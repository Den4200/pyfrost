from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=engine
    )
)
Base = declarative_base()


def init_db():
    from frost.server.database import models  # NOQA: F401
    Base.metadata.create_all(bind=engine)
