# orchestrator/models/support_models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from .core_models import Base

class Registry(Base):
    __tablename__ = "registry"
    id = Column(Integer, primary_key=True)
    image_name = Column(String)
    repo_url = Column(String)
    checksum = Column(String)
    last_updated = Column(DateTime)

class ResourceMetric(Base):
    __tablename__ = "resource_metrics"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"), index=True)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    timestamp = Column(DateTime)

    mpod = relationship("MPod", back_populates="resource_metrics")

class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"), index=True)
    check_type = Column(String)
    status = Column(String)
    checked_at = Column(DateTime)

    mpod = relationship("MPod", back_populates="health_checks")

class GPUMetric(Base):
    __tablename__ = "gpu_metrics"
    id = Column(Integer, primary_key=True)
    mpod_id = Column(Integer, ForeignKey("mpods.id"), index=True)
    gpu_utilization = Column(Float)
    gpu_memory_usage = Column(Float)
    gpu_temperature = Column(Float)
    timestamp = Column(DateTime)

    mpod = relationship("MPod", back_populates="gpu_metrics")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String)
    token = Column(String)

    security_tokens = relationship("SecurityToken", back_populates="user")

class SecurityToken(Base):
    __tablename__ = "security_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    token = Column(String)
    expiry_time = Column(DateTime)
    issued_at = Column(DateTime)
    scope = Column(String)

    user = relationship("User", back_populates="security_tokens")
