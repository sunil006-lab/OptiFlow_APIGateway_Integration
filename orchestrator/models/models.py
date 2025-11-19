# orchestrator/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()
# schema 1
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
    events = relationship("Event", back_populates="node")  # Link to events
# schema 2
class Workload(Base):
    __tablename__ = 'workloads'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    mpods = relationship("MPod", back_populates="workload")
    events = relationship("Event", back_populates="workload")  # Link to events
# schema 3
class MPod(Base):
    __tablename__ = 'mpods'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    node_id = Column(Integer, ForeignKey('nodes.id'))
    workload_id = Column(Integer, ForeignKey('workloads.id'))
    status = Column(String, default="Running")
    image = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    node = relationship("Node", back_populates="mpods")
    workload = relationship("Workload", back_populates="mpods")
# schema 4
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    node_id = Column(Integer, ForeignKey('nodes.id'), nullable=True)
    workload_id = Column(Integer, ForeignKey('workloads.id'), nullable=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"), nullable=True)
    node = relationship("Node", back_populates="events")
    workload = relationship("Workload", back_populates="events")
# schema 5
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"))
    log_level = Column(String)
    message = Column(String)
    timestamp = Column(DateTime)
    node = relationship("Node", back_populates="logs")
    workload = relationship("Workload", back_populates="logs")
# schema 6    
class SchedulingQueue(Base):
    __tablename__ = "scheduling_queue"
    id = Column(Integer, primary_key=True)
    workload_id = Column(Integer, ForeignKey("workloads.id"))
    node_id = Column(Integer, ForeignKey("nodes.id"))
    scheduled_time = Column(DateTime)
    priority = Column(Integer)
    node = relationship("Node", back_populates="scheduling_queues")
    workload = relationship("Workload", back_populates="scheduling_queues")
# schema 7
class Registry(Base):
    __tablename__ = "registry"
    id = Column(Integer, primary_key=True)
    image_name = Column(String)
    repo_url = Column(String)
    checksum = Column(String)
    last_updated = Column(DateTime)
# schema 8
class ResourceMetric(Base):
    __tablename__ = "resource_metrics"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"))
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    timestamp = Column(DateTime)
    
# schema 9
class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"))
    check_type = Column(String)
    status = Column(String)
    checked_at = Column(DateTime)
# schema 10
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String)
    token = Column(String)
# schema 11
class GPUMetric(Base):
    __tablename__ = "gpu_metrics"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"))
    gpu_utilization = Column(Float)
    gpu_memory_usage = Column(Float)
    gpu_temperature = Column(Float)
    timestamp = Column(DateTime)
    
# schema 12
class SecurityToken(Base):
    __tablename__ = "security_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String)
    expiry_time = Column(DateTime)
    issued_at = Column(DateTime)
    scope = Column(String)

