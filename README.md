# MCP Server Collection

A collection of Model Context Protocol (MCP) servers for database and API integration.

## Servers

### 1. PostgreSQL MCP Server (`postgres_server.py`)
Provides tools for interacting with PostgreSQL databases.

### 2. Integration Platform API Server (`api_server.py`)
Provides 20 tools for interacting with your integration platform API covering Azure, SAP BTP, and SAP ABAP endpoints.

---

## PostgreSQL Server

### Features

- **Execute SQL Queries**: Run any SQL query and get results in JSON format
- **List Tables**: View all tables in a database schema
- **Inspect Table Schema**: Get detailed column information for any table
- **Database Info**: Retrieve database metadata and statistics
- **HTTP Transport**: Accessible via HTTP for easy integration
- **Ngrok Support**: Expose your local server publicly for remote access

## Setup

### 1. Install Dependencies

```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

Copy the example environment file and add your database credentials:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL connection details:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

### 3. Run the Server Locally

```bash
uv run postgres_server.py
```

Or:
```bash
python postgres_server.py
```

The server will start on `http://localhost:8000`

### 4. Expose with Ngrok (Optional)

To make your server accessible from the internet:

**First, install and configure ngrok:**
1. Download from https://ngrok.com/download
2. Sign up and get your auth token
3. Run: `ngrok authtoken YOUR_AUTH_TOKEN`

**Then start the server with ngrok:**

```bash
python start_with_ngrok.py
```

This will:
- Start the MCP server on port 8000
- Create an ngrok tunnel
- Display the public URL for remote access

## Available Tools

### `execute_query`
Execute SQL queries and get results.

**Parameters:**
- `query` (string): SQL query to execute
- `params` (list, optional): Parameters for parameterized queries

**Example:**
```json
{
  "query": "SELECT * FROM users WHERE age > $1",
  "params": [18]
}
```

### `list_tables`
List all tables in a schema.

**Parameters:**
- `schema` (string, default: "public"): Database schema name

### `get_table_schema`
Get detailed schema information for a table.

**Parameters:**
- `table_name` (string): Name of the table
- `schema` (string, default: "public"): Database schema name

### `get_database_info`
Get general database information including version, size, and table count.

**No parameters required.**

## Resources

The server also provides MCP resources:

- `db://schema/{schema_name}` - Get all tables in a schema
- `db://table/{table_name}` - Get table schema information

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use read-only database users** when possible
3. **Validate queries** before execution in production
4. **Use ngrok authentication** for public exposure
5. **Consider IP whitelisting** for production deployments

## Testing

Test the connection:

```bash
python -c "from config import config; import psycopg2; conn = psycopg2.connect(**config.get_connection_params()); print('✓ Connected successfully!'); conn.close()"
```

## Troubleshooting

### Connection Failed
- Verify database credentials in `.env`
- Check if PostgreSQL is running
- Ensure firewall allows connections on the database port

### Ngrok Issues
- Verify ngrok is installed: `ngrok version`
- Check if you've authenticated: `ngrok authtoken YOUR_TOKEN`
- Ensure port 8000 is not already in use

---

## Integration Platform API Server

### Features

- **20 MCP Tools** covering all integration platform endpoints
- **General Endpoints**: Properties, Property Types, Metadata
- **Core Relationships**: Systems, DataFlows, DataSources
- **Azure Resources**: Tenants, Subscriptions, API Management, Logic Apps
- **SAP BTP**: Cloud Integration, API Management
- **SAP ABAP**: Partner Profiles, RFC Destinations, SOAP Services
- **Multiple Auth Methods**: Bearer token, API key, Basic auth
- **Ngrok Support**: Expose your API server publicly

### Setup

#### 1. Configure API Connection

Edit `.env` file with your API details:

```env
API_BASE_URL=http://your-api-url.com
API_AUTH_METHOD=bearer
API_BEARER_TOKEN=your_token_here
```

#### 2. Run the API Server

```bash
uv run api_server.py
```

Or:
```bash
python api_server.py
```

The server will start on `http://localhost:8020`

#### 3. Expose with Ngrok (Optional)

```bash
python start_api_with_ngrok.py
```

### Documentation

See [API_TOOLS.md](API_TOOLS.md) for complete documentation of all 20 API tools with examples.

### Quick Example

```json
{
  "tool": "get_properties",
  "arguments": {
    "schema": "dev"
  }
}
```

---

## License

MIT
