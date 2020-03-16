from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    raise NotImplementedError

    from .models import main_models  # NOQA: F401
    Base.metadata.create_all(bind=engine)
