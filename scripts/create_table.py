from orchestrator.schema_model.base import Base
from orchestrator.schema_model.workloads import Workload
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./orchestrator.db")

Base.metadata.create_all(engine)
print("Database and workloads table created!")

