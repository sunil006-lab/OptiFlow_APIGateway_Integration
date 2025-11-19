import asyncio
import sys
import os

# Add orchestrator to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.schema_model.workloads import Workloads  # Import from schema_model
from orchestrator.db.database import engine
from orchestrator.schema_model.node import Base  # import from schema_model
from orchestrator.schema_model import node, workloads
from orchestrator.schema_model.base import Base



# Ensure that Workloads and Node models are included in the metadata
async def init_schema_models():
    async with engine.begin() as conn:
        # Create tables for both Node and Workloads
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_schema_models())
