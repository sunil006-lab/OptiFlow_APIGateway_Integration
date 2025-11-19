from sqlalchemy import create_engine, text

# Update with your actual DB path if different
engine = create_engine("sqlite:///./orchestrator.db")
with engine.connect() as connection:
    result = connection.execute(text("PRAGMA table_info(events);"))
    for row in result:
        print(row)
