"""Run once to add new columns to existing database."""
from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN level VARCHAR DEFAULT 'intermediate'"))
        conn.commit()
        print("Added 'level' column to users table.")
    except Exception:
        print("Column 'level' already exists - skipping.")
print("Migration complete.")
