from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MPod(Base):
    __tablename__ = "mpods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    node_id = Column(Integer, ForeignKey("nodes.id")) ##,nullable=False)
    workload_id = Column(Integer, ForeignKey("workloads.id"),nullable=False)
    status = Column(String)
    created_at = Column(DateTime)
