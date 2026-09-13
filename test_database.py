import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing from .env")

engine = create_engine(database_url)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        print("Database connection successful!")
        print("Result:", result.scalar())

except Exception as e:
    print("Database connection failed.")
    print("Error:", e)