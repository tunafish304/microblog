# validate_db.py

import os

from sqlalchemy import create_engine

from config import Config

# Optional: Masked logging for teaching/debug purposes
uri_preview = Config.SQLALCHEMY_DATABASE_URI.replace(os.getenv("DB_PASSWORD"), "***")
print(f"[DB URI Preview] {uri_preview}")

# Create SQLAlchemy engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Attempt connection
try:
    with engine.connect() as connection:
        print("[Success] Connected to the database.")
except Exception as e:
    print(f"[Error] Connection failed:\n{e}")
