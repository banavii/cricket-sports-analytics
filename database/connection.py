from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database location
DATABASE_PATH = BASE_DIR / "data" / "cricket_analytics.db"

# Make sure the data folder exists
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# SQLite connection URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
)


# Enable SQLite foreign-key enforcement
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)