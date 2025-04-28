from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Read the database connection URL from my .env config
DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine (connection to database)
# For SQLite, I need to pass "check_same_thread=False" (required by SQLite)
# Also enable "pool_pre_ping=True" to make sure dead connections are detected
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True
)

# Create a session factory
# This is what I'll use to open/close database sessions safely in my app
SessionLocal = sessionmaker(
    autocommit=False,    # I want manual commit/rollback to avoid accidental writes
    autoflush=False,     # I want to control when DB flush happens
    bind=engine          # Tie this session factory to the engine I just created
)

# Define the base class for all my database models
# (Every table model I create will inherit from this Base)
Base = declarative_base()
