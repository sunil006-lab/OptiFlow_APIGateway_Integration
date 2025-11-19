# orchestrator/apiserver/developer_api.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import os
from sqlalchemy import text

DATABASE_URL = "sqlite+aiosqlite:///./orchestrator.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

app = FastAPI(title="OptiFlow Developer API")

# DB Models
class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

class Workload(Base):
    __tablename__ = "workloads"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    description = Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    details = Column(String)

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

# --- NODE Routes ---
@app.post("/nodes/")
async def add_node(name: str, status: str, db: AsyncSession = Depends(get_db)):
    node = Node(name=name, status=status)
    db.add(node)
    await db.commit()
    await db.refresh(node)
    return node

@app.get("/nodes/")
async def get_nodes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM nodes"))
    return result.mappings().all()

# --- WORKLOAD Routes ---
@app.post("/workloads/")
async def add_workload(type: str, description: str = "", db: AsyncSession = Depends(get_db)):
    workload = Workload(type=type, description=description)
    db.add(workload)
    await db.commit()
    await db.refresh(workload)
    return workload

@app.get("/workloads/")
async def get_workloads(db: AsyncSession = Depends(get_db)):
    #result = await db.execute("""SELECT * FROM workloads""")
    result = await db.execute(text("SELECT * FROM workloads"))
    return result.mappings().all()

# --- EVENT Routes ---
@app.post("/events/")
async def add_event(event_type: str, details: str = "", db: AsyncSession = Depends(get_db)):
    event = Event(event_type=event_type, details=details)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

@app.get("/events/")
async def get_events(db: AsyncSession = Depends(get_db)):
    #result = await db.execute("""SELECT * FROM events""")
    result = await db.execute(text("SELECT * FROM events"))
    return result.mappings().all()
