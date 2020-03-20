from contextlib import contextmanager

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


@contextmanager
def managed_session():
    session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=engine
        )
    )
    try:
        yield session
        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.remove()


def init_db():
    from frost.server.database import models  # NOQA: F401
    Base.metadata.create_all(bind=engine)
