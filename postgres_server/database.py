"""
Database connection and session management for REST API.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import config

# Create database URL
DATABASE_URL = config.get_connection_string().replace("postgresql://", "postgresql+psycopg2://")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Use with FastAPI Depends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_schema_prefix(schema: str) -> str:
    """
    Get the schema prefix for table names.
    
    Args:
        schema: Schema name (dev, prod, test)
    
    Returns:
        Schema prefix string
    """
    valid_schemas = ["dev", "prod", "test"]
    if schema not in valid_schemas:
        raise ValueError(f"Invalid schema '{schema}'. Must be one of: {', '.join(valid_schemas)}")
    
    return schema
