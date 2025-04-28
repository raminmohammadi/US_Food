from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from db.database import Base, SessionLocal
import datetime

class APILog(Base):
    """
    SQLAlchemy model representing the API logs table.
    
    Stores:
    - Incoming request data (as JSON string)
    - Outgoing response data (as JSON string)
    - Timestamp of the API call
    """
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_data = Column(String, nullable=False)
    response_data = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Fixed: use utcnow (safer)

def create_tables():
    """
    Creates all tables defined by Base metadata.
    
    Typically called once on startup to ensure database schema is ready.
    """
    Base.metadata.create_all(bind=SessionLocal.kw["bind"])

def log_to_db(request_data: str, response_data: str):
    """
    Logs API request and response data into the database.

    Args:
        request_data (str): Serialized request JSON string.
        response_data (str): Serialized response JSON string.
    """
    db: Session = SessionLocal()

    try:
        log_entry = APILog(
            request_data=request_data,
            response_data=response_data
        )
        db.add(log_entry)
        db.commit()

    except Exception as e:
        print(f"Logging failed: {e}")
        db.rollback()  # Fixed typo: you wrote "do.rollback()" — should be db.rollback()

    finally:
        db.close()
