# import os
# from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# load_dotenv()

# host = os.getenv("POSTGRES_SERVER")
# port = os.getenv("POSTGRES_PORT")
# dbname = os.getenv("POSTGRES_DB")
# user = os.getenv("POSTGRES_USER")
# password = os.getenv("POSTGRES_PASSWORD")

# # DATABASE CONNECTION STRING/URI
# # [dialect]://[user]:[password]@[host]:[port]/[dbname]

# # PostgreSQL connection string/URI
# POSTGRES_DATABASE_URI = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"

# Create a database engine
engine = create_engine(str(settings.POSTGRES_DATABASE_URI), echo=True)

# Initialize a `Session` factory with specified configurations
SessionLocal = sessionmaker(bind=engine, autoflush=True, autocommit=False)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db    # FastAPI calls your path operations with this session
    finally:
        db.close()

# Base class for sqlalchemy models - Python classes that are mapped to the actual database schemas/tables
class Base(DeclarativeBase):
    pass