# Purpose: set up SQLAlchemy engine and a session factory for PostgreSQL

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config import Config  # loads .env

# Create engine once for the service
engine = create_engine(
    Config.DATABASE_URL,
    pool_pre_ping=True,       # drop dead connections
    pool_size=5,
    max_overflow=5,
    future=True,
)

# Session factory (we’ll use short-lived sessions per request)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)