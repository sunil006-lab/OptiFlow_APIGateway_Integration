
import asyncio
import os
import sys
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure parent directory is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from orchestrator.db.database_query import async_session
from orchestrator.models.models import Workload, Node, MPod
from orchestrator.models import Event  # Assumes no circular import

# Helper to get async session context
def get_async_session() -> AsyncSession:
    return async_session()

# Controller CRUD operations
async def create_node(node_data):
    """Create a new node in the database."""
    async with get_async_session() as session:
        node = Node(**node_data.dict())
        session.add(node)
        await session.commit()
        await session.refresh(node)
        return node

async def get_all_nodes():
    """Fetch all registered nodes."""
    async with get_async_session() as session:
        result = await session.execute(select(Node))
        return result.scalars().all()

async def create_workload(workload_data):
    """Create a new workload entry."""
    async with get_async_session() as session:
        workload = Workload(**workload_data.dict())
        session.add(workload)
        await session.commit()
        await session.refresh(workload)
        return workload

async def get_all_workloads():
    """Retrieve all workloads."""
    async with get_async_session() as session:
        result = await session.execute(select(Workload))
        return result.scalars().all()

async def get_all_events():
    """Retrieve all events."""
    async with get_async_session() as session:
        result = await session.execute(select(Event))
        return result.scalars().all()


async def schedule_workloads():
    """Intelligently assign pending workloads to best-fit healthy nodes based on CPU and memory."""
    async with get_async_session() as session:
        workloads_result = await session.execute(
            select(Workload).where(Workload.status == "Pending")
        )
        workloads = workloads_result.scalars().all()

        nodes_result = await session.execute(
            select(Node).where(Node.status == "Healthy")
        )
        healthy_nodes = nodes_result.scalars().all()

        for workload in workloads:
            # Find best-fit node based on least remaining resources after assignment
            suitable_nodes = [
                node for node in healthy_nodes
                if node.available_cpu >= workload.cpu_request and
                   node.available_memory >= workload.memory_request
            ]

            if not suitable_nodes:
                logger.warning(f"No suitable node found for workload: {workload.name}")
                continue

            # Sort by best-fit (least remaining CPU after scheduling)
            best_node = sorted(
                suitable_nodes,
                key=lambda n: (n.available_cpu - workload.cpu_request) +
                              (n.available_memory - workload.memory_request)
            )[0]

            # Assign workload to best-fit node
            mpod = MPod(
                name=f"{workload.name}-mpod",
                node_id=best_node.id,
                workload_id=workload.id,
                status="Running",
                created_at=datetime.utcnow()
            )
            session.add(mpod)

            # Update node's available resources
            best_node.available_cpu -= workload.cpu_request
            best_node.available_memory -= workload.memory_request

            # Update workload status
            workload.status = "Running"

            logger.info(f"Scheduled '{workload.name}' to '{best_node.name}'")

        await session.commit()
        logger.info("All eligible workloads scheduled.")




async def controller_loop(interval=5):
    """Main loop for scheduling workloads periodically."""
    while True:
        try:
            await schedule_workloads()
        except Exception as e:
            logger.error(f"[Controller Error] {e}")
        await asyncio.sleep(interval)

async def create_mpod(mpod_data):
    """Manually create an MPod entry."""
    async with get_async_session() as session:
        mpod = MPod(**mpod_data.dict())
        session.add(mpod)
        await session.commit()
        await session.refresh(mpod)
        return mpod

async def get_all_mpods():
    """Retrieve all MPods."""
    async with get_async_session() as session:
        result = await session.execute(select(MPod))
        return result.scalars().all()
