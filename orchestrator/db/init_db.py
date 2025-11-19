import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from orchestrator.db.database import engine
from orchestrator.models.core_models import Base  # Base defined in core_models
from orchestrator.models import core_models, support_models  # Ensure model classes are imported

# Import SQLAlchemy ORM models (not Pydantic schemas)
# from orchestrator.schema_model.node import Node
#from orchestrator.schema_model.workloads import Workloads  # Confirm this is ORM model
# from orchestrator.schema_model.events import Event
#from orchestrator.schema_model.mpods import MPod  # ORM model

#async def init_models(engine: AsyncEngine):
    #async with engine.begin() as conn:
        # Create tables for all models
        #await conn.run_sync(Node.metadata.create_all)
        #await conn.run_sync(Workloads.metadata.create_all)
        #await conn.run_sync(Event.metadata.create_all)
        #await conn.run_sync(MPod.metadata.create_all)
        #await conn.run_sync(Base.metadata.create_all)

engine = create_async_engine("sqlite+aiosqlite:///./orchestrator.db", echo=True)


async def init_models(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models(engine))
    print("All tables created successfully!")
