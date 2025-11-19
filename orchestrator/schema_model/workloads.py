from sqlalchemy import Column, Integer, String
from orchestrator.schema_model.base import Base

class Workload(Base):
    __tablename__ = "workloads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="Pending")
    description = Column(String)
