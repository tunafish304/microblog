import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Load env vars using anchored path
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

uri = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

try:
    engine = create_engine(uri)
    with engine.connect() as connection:
        print("✅ Connection to database established.")
except SQLAlchemyError as e:
    print("❌ Failed to connect to database.")
    print("Error details:", e)
