"""
Path: tests/SYS_WATCHDOG/test_database.py
Description: Tests for SQLAlchemy ORM and DB operations.
Version: 2.1.0
Sub_System: SYS_WATCHDOG
System: JERICHO_SYSTEM
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.SYS_WATCHDOG.src.database import Base, Log


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test.db"
    url = f"sqlite:///{db_file}"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return engine, Session


def test_log_insert(temp_db):
    engine, SessionLocal = temp_db
    session = SessionLocal()
    entry = Log(event_type="TEST", message="DB test")
    session.add(entry)
    session.commit()
    rows = session.query(Log).all()
    assert len(rows) == 1
    assert rows[0].event_type == "TEST"
    session.close()
