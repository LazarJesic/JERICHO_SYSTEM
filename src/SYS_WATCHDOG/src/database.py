"""
Path: src/SYS_WATCHDOG/src/database.py
Description: SQLAlchemy ORM and database helpers.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

from .config_loader import load_env

Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)
    message = Column(String)


def _get_engine():
    env = load_env()
    url = env.get('DB_URL') or 'sqlite:///watchdog.db'
    return create_engine(url)

engine = _get_engine()
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
