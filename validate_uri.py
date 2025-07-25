import os

from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env"))

uri = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

try:
    parsed = make_url(uri)
    print("✅ URI syntax is valid:")
    print(parsed)
except Exception as e:
    print("❌ URI is malformed:", e)
