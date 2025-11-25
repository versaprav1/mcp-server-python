"""
PostgreSQL MCP Server
A Model Context Protocol server that provides tools for interacting with PostgreSQL databases.
"""

import json
import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.server.fastmcp import FastMCP
from config import config

# Create MCP server
mcp = FastMCP("PostgreSQL Database Server", json_response=True)


def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**config.get_connection_params())
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Database connection failed: {str(e)}")


@mcp.tool()
def execute_query(query: str, params: list = None) -> dict:
    """
    Execute a SQL query and return the results.
    
    Args:
        query: SQL query to execute
        params: Optional list of parameters for parameterized queries
    
    Returns:
        Dictionary with 'rows' (list of results) and 'rowcount' (number of affected rows)
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Check if query returns results
        if cursor.description:
            rows = cursor.fetchall()
            # Convert RealDictRow to regular dict
            rows = [dict(row) for row in rows]
        else:
            rows = []
        
        rowcount = cursor.rowcount
        conn.commit()
        
        return {
            "success": True,
            "rows": rows,
            "rowcount": rowcount,
            "message": f"Query executed successfully. {rowcount} row(s) affected."
        }
    
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"Query execution failed: {str(e)}"
        }
    
    finally:
        if conn:
            cursor.close()
            conn.close()


@mcp.tool()
def list_tables(schema: str = "dev") -> dict:
    """
    List all tables in the specified schema.
    
    Args:
        schema: Database schema name (default: 'public')
    
    Returns:
        Dictionary with list of table names
    """
    query = """
        SELECT table_name, table_type
        FROM information_schema.tables
        WHERE table_schema = %s
        ORDER BY table_name;
    """
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, [schema])
        tables = [dict(row) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "schema": schema,
            "tables": tables,
            "count": len(tables)
        }
    
    except psycopg2.Error as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to list tables: {str(e)}"
        }
    
    finally:
        if conn:
            cursor.close()
            conn.close()


@mcp.tool()
def get_table_schema(table_name: str, schema: str = "dev") -> dict:
    """
    Get the schema information for a specific table.
    
    Args:
        table_name: Name of the table
        schema: Database schema name (default: 'public')
    
    Returns:
        Dictionary with column information including names, types, and constraints
    """
    query = """
        SELECT 
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position;
    """
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, [schema, table_name])
        columns = [dict(row) for row in cursor.fetchall()]
        
        if not columns:
            return {
                "success": False,
                "message": f"Table '{table_name}' not found in schema '{schema}'"
            }
        
        return {
            "success": True,
            "table_name": table_name,
            "schema": schema,
            "columns": columns,
            "column_count": len(columns)
        }
    
    except psycopg2.Error as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to get table schema: {str(e)}"
        }
    
    finally:
        if conn:
            cursor.close()
            conn.close()


@mcp.tool()
def get_database_info() -> dict:
    """
    Get general information about the database.
    
    Returns:
        Dictionary with database metadata including version, size, and connection info
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()['version']
        
        # Get database size
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as size;
        """)
        size = cursor.fetchone()['size']
        
        # Get current database name
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()['current_database']
        
        # Get number of tables
        cursor.execute("""
            SELECT COUNT(*) as table_count
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()['table_count']
        
        return {
            "success": True,
            "database_name": db_name,
            "version": version,
            "size": size,
            "table_count": table_count,
            "host": config.host,
            "port": config.port
        }
    
    except psycopg2.Error as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to get database info: {str(e)}"
        }
    
    finally:
        if conn:
            cursor.close()
            conn.close()


@mcp.resource("db://schema/{schema_name}")
def get_schema_resource(schema_name: str) -> str:
    """Get all tables in a schema as a resource."""
    result = list_tables(schema_name)
    return json.dumps(result, indent=2)


@mcp.resource("db://table/{table_name}")
def get_table_resource(table_name: str) -> str:
    """Get table schema as a resource."""
    result = get_table_schema(table_name)
    return json.dumps(result, indent=2)


# Run with streamable HTTP transport
if __name__ == "__main__":
    print("Starting PostgreSQL MCP Server...")
    print(f"Connecting to database: {config.database} at {config.host}:{config.port}")
    print("Server will run on http://localhost:8010")
    mcp.run(transport="streamable-http")
