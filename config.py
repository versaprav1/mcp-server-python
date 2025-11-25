"""
Configuration management for PostgreSQL MCP Server.
Loads database credentials from environment variables or .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig:
    """Database configuration with environment variable support."""
    
    def __init__(self):
        # Check if full DATABASE_URL is provided
        self.database_url = os.getenv("DATABASE_URL")
        
        # Individual connection parameters
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME", "postgres")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "")
    
    def get_connection_params(self):
        """Get connection parameters as a dictionary."""
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password": self.password,
        }
    
    def get_connection_string(self):
        """Get connection string for PostgreSQL."""
        if self.database_url:
            return self.database_url
        
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# Global config instance
config = DatabaseConfig()
