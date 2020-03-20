from contextlib import contextmanager
from werkzeug.security import generate_password_hash

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
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

    # This is here for now, until separate rooms are implemented.
    with managed_session() as session:
        session.add_all([
            models.User(
                username='f1re',
                password=generate_password_hash('pw')
            ),
            models.Room(
                name='Main Room',
                invite_code='abc123',
                owner_id=1
            )
        ])
        u = session.query(models.User).first()
        u.joined_rooms.append(
            session.query(models.Room).first()
        )
