from sqlalchemy import Column, Integer, String, DateTime
from orchestrator.schema_model.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    details = Column(String)
