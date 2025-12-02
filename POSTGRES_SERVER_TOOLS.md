# Postgres MCP Server Tools

This document lists the available tools in the PostgreSQL MCP Server (`postgres_server`). These tools are designed for database administration, schema exploration, and performance analysis.

## General Tools

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `execute_query` | Execute a raw SQL query and return the results. | `query` (str), `params` (list) |
| `list_tables` | List all tables in the specified schema. | `schema` (str) |
| `get_table_schema` | Get column definitions for a specific table. | `table_name` (str), `schema` (str) |
| `get_database_info` | Get general information (version, size, connection count). | None |

## Advanced Schema Exploration

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_foreign_keys` | Get foreign key constraints for a specific table. | `table_name` (str), `schema` (str) |
| `get_primary_keys` | Get primary key columns for a specific table. | `table_name` (str), `schema` (str) |
| `search_tables` | Fuzzy search for tables matching the search term. | `search_term` (str), `schema` (str) |

## Database Health & Stats

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_table_sizes` | Get the disk size of all tables in the schema. | `schema` (str) |
| `get_row_counts` | Get estimated row counts for all tables in the schema. | `schema` (str) |
| `get_active_connections` | Get current active connections to the database. | None |

## Query Analysis

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `explain_query` | Analyze a query plan without executing it (uses `EXPLAIN`). | `query` (str) |
| `validate_query` | Validate a SQL query syntax without executing it. | `query` (str) |
