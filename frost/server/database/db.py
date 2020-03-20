from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session  # NOQA: F401


engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
"""The SQLAlchemy engine."""

Base = declarative_base()
"""The base model."""


@contextmanager
def managed_session() -> 'Session':
    """A context manager for thread-safe database access. \
    Automatically commits if no errors occur, else it is rolled back. \
    Session is removed after use.

    :yield: An SQLAlchemy scoped_session
    :rtype: :class:`sqlalchemy.orm.Session`
    """
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


def init_db() -> None:
    """Initlializes a database and creates the pre-defined modules.
    """
    from werkzeug.security import generate_password_hash
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
