from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from orchestrator.schema_model.node import Node
#from orchestrator.schema_model.workloads import Workload
from orchestrator.schema_model.workloads import Workload


# Create async SQLite engine
DATABASE_URL = "sqlite+aiosqlite:///./orchestrator.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Async session generator
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Query Node table
async def query_nodes():
    async with async_session() as session:
        result = await session.execute(select(Node))
        nodes = result.scalars().all()
        for node in nodes:
            print(f"Node {node.id}: {node.name} - {node.status}")

# Query Workloads table
async def query_workloads():
    async with async_session() as session:
        result = await session.execute(select(Workload))
        workloads = result.scalars().all()
        for workload in workloads:
            print(f"Workload {workload.id}: {workload.name} - {workload.status}")

# Run both queries if executed directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(query_nodes())
    asyncio.run(query_workloads())
