from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./orchestrator.db")
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS mpods"))
    print("Dropped mpods table if it existed.")

