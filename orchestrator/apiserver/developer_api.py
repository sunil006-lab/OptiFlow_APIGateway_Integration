import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Ensure the orchestrator module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from orchestrator.controller import controller

app = FastAPI(title="OptiFlow Developer API")

# Schemas
class Node(BaseModel):
    name: str
    status: str

class Workload(BaseModel):
    name: str
    type: str
    status: str
    node_id: Optional[int]  # node_id might be null if not assigned yet

class Event(BaseModel):
    type: str
    description: str
    source: str

class MPod(BaseModel):
    name: str
    node_id: int
    workload_id: int
    status: str
    class Config:
        orm_mode = True

# ------------------ NODES ------------------ #

@app.post("/nodes/")
async def add_node(node: Node):
    return await controller.create_node(node)

@app.get("/nodes/")
async def get_nodes():
    return await controller.get_all_nodes()

# ------------------ WORKLOADS ------------------ #

@app.post("/workloads/")
async def add_workload(workload: Workload):
    return await controller.create_workload(workload)

@app.get("/workloads/")
async def get_workloads():
    return await controller.get_all_workloads()

# ------------------ EVENTS ------------------ #

@app.get("/events/")
async def get_events():
    return await controller.get_all_events()

# ------------------ MPODS ------------------ #

@app.post("/mpods/")
async def add_mpod(mpod: MPod):
    return await controller.create_mpod(mpod)

@app.get("/mpods/")
async def get_mpods():
    return await controller.get_all_mpods()
