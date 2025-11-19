# orchestrator/models/core_models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String, nullable=False)
    capacity_cpu = Column(Float)
    status = Column(String)
    capacity_memory = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    mpods = relationship("MPod", back_populates="node")
    events = relationship("Event", back_populates="node")
    logs = relationship("Log", back_populates="node")
    scheduling_queues = relationship("SchedulingQueue", back_populates="node")

class Workload(Base):
    __tablename__ = 'workloads'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String)

    mpods = relationship("MPod", back_populates="workload")
    events = relationship("Event", back_populates="workload")
    logs = relationship("Log", back_populates="workload")
    scheduling_queues = relationship("SchedulingQueue", back_populates="workload")

class MPod(Base):
    __tablename__ = 'mpods'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    node_id = Column(Integer, ForeignKey('nodes.id'), index=True)
    workload_id = Column(Integer, ForeignKey('workloads.id'), index=True)
    status = Column(String, default="Running")
    image = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    node = relationship("Node", back_populates="mpods")
    workload = relationship("Workload", back_populates="mpods")
    logs = relationship("Log", back_populates="mpod")
    resource_metrics = relationship("ResourceMetric", back_populates="mpod")
    health_checks = relationship("HealthCheck", back_populates="mpod")
    gpu_metrics = relationship("GPUMetric", back_populates="mpod")
    events = relationship("Event", back_populates="mpod")

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    node_id = Column(Integer, ForeignKey('nodes.id'), nullable=True, index=True)
    workload_id = Column(Integer, ForeignKey('workloads.id'), nullable=True, index=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"), nullable=True, index=True)

    node = relationship("Node", back_populates="events")
    workload = relationship("Workload", back_populates="events")
    mpod = relationship("MPod", back_populates="events")

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"), index=True)
    log_level = Column(String)
    message = Column(String)
    timestamp = Column(DateTime)

    mpod = relationship("MPod", back_populates="logs")
    node = relationship("Node", back_populates="logs")
    workload = relationship("Workload", back_populates="logs")

class SchedulingQueue(Base):
    __tablename__ = "scheduling_queue"
    id = Column(Integer, primary_key=True)
    workload_id = Column(Integer, ForeignKey("workloads.id"), index=True)
    node_id = Column(Integer, ForeignKey("nodes.id"), index=True)
    scheduled_time = Column(DateTime)
    priority = Column(Integer)

    node = relationship("Node", back_populates="scheduling_queues")
    workload = relationship("Workload", back_populates="scheduling_queues")
