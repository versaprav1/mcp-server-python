# REST API Server Documentation

Complete guide for the FastAPI REST API server that provides all integration platform endpoints backed by PostgreSQL.

## Overview

The REST API server sits between your MCP server and PostgreSQL database:

```
MCP Client → MCP Server (port 8020) → REST API (port 3000) → PostgreSQL DB
```

## Quick Start

### 1. Set Up Database

#### Option A: Use Sample Schema

Run the sample schema to create all tables:

```bash
psql -h localhost -U your_username -d your_database -f sample_schema.sql
```

This creates:
- 3 schemas: `dev`, `prod`, `test`
- All required tables
- Sample data in `dev` schema

#### Option B: Use Your Existing Schema

If you have existing tables, ensure they match the expected structure or modify the queries in `rest_api_server.py`.

### 2. Configure Database Connection

Edit `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

### 3. Start the REST API Server

```bash
uv run rest_api_server.py
```

Or:

```bash
python rest_api_server.py
```

The server starts on **http://localhost:3000**

### 4. Test the API

Visit the interactive documentation:
- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

Test an endpoint:

```bash
curl http://localhost:3000/dev/properties
```

### 5. Start the MCP Server

In a new terminal:

```bash
uv run api_server.py
```

The MCP server (port 8020) will now call your REST API (port 3000).

---

## Complete Architecture

```
┌─────────────┐
│  MCP Client │
└──────┬──────┘
       │ MCP Protocol
       ▼
┌─────────────────┐
│   MCP Server    │  Port 8020
│ (api_server.py) │  20 MCP Tools
└──────┬──────────┘
       │ HTTP/REST
       ▼
┌──────────────────────┐
│   REST API Server    │  Port 3000
│(rest_api_server.py)  │  20 Endpoints
└──────┬───────────────┘
       │ SQL
       ▼
┌─────────────────┐
│   PostgreSQL    │  Port 5432
│    Database     │  dev/prod/test schemas
└─────────────────┘
```

---

## API Endpoints

### General Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{schema}/properties` | GET | List all properties |
| `/{schema}/property_types` | GET | List all property types |
| `/{schema}/metadata` | GET | List all metadata entries |

### Core Relationships

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{schema}/relationships/datasources_to_tenants` | GET | DataSources to Tenants relationships |
| `/{schema}/systems/{system_id}/datasources` | GET | DataSources for a system |
| `/{schema}/dataflows/{dataflow_id}/systems` | GET | Sender/receiver systems for a dataflow |
| `/{schema}/dataflows/{dataflow_id}/inventories` | GET | Technical interfaces for a dataflow |

### Azure Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{schema}/azure/tenants/{tenant_id}/subscriptions` | GET | Subscriptions in a tenant |
| `/{schema}/azure/subscriptions/{subscription_id}/resource_groups` | GET | Resource groups in a subscription |
| `/{schema}/azure/api_management_services/{service_id}/apis` | GET | APIs in API Management service |
| `/{schema}/azure/api_management_apis/{api_id}/products` | GET | Products for an API |
| `/{schema}/azure/standard_apps/{app_id}/workflows` | GET | Workflows in a Standard App |
| `/{schema}/azure/logic_app_workflows/{workflow_id}/versions` | GET | Workflow versions |

### SAP BTP Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{schema}/btp/cloud_integration_packages/{package_id}/artefacts` | GET | Artefacts in a package |
| `/{schema}/btp/cloud_integration_artefacts/{artefact_id}/runtime` | GET | Runtime status of an artefact |
| `/{schema}/btp/api_management_providers/{provider_id}/proxies` | GET | Proxies for a provider |
| `/{schema}/btp/api_management_proxies/{proxy_id}/products` | GET | Products for a proxy |

### SAP ABAP Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{schema}/abap/datasources/{datasource_id}/partner_profiles` | GET | Partner profiles for a datasource |
| `/{schema}/abap/ports/{port_id}/rfc_destinations` | GET | RFC destinations for a port |
| `/{schema}/abap/soap_services/{service_id}/bindings` | GET | Bindings for a SOAP service |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |

---

## Database Schema

The database uses **schema-based multi-tenancy** with three schemas:
- `dev` - Development environment
- `prod` - Production environment
- `test` - Testing environment

### Key Tables

**General Tables:**
- `properties` - Configuration properties
- `property_types` - Property type definitions
- `metadata` - System metadata

**Core Tables:**
- `systems` - Integration systems
- `datasources` - Data sources
- `dataflows` - Data flows between systems
- `inventories` - Technical interfaces

**Azure Tables:**
- `azure_tenants` - Azure tenants
- `azure_subscriptions` - Azure subscriptions
- `azure_resource_groups` - Resource groups
- `azure_api_management_services` - API Management services
- `azure_api_management_apis` - APIs
- `azure_api_management_products` - Products
- `azure_standard_apps` - Standard Apps
- `azure_logic_app_workflows` - Logic App workflows
- `azure_logic_app_workflow_versions` - Workflow versions

**SAP BTP Tables:**
- `btp_cloud_integration_packages` - CI packages
- `btp_cloud_integration_artefacts` - CI artefacts
- `btp_cloud_integration_artefact_runtime` - Runtime status
- `btp_api_management_providers` - API providers
- `btp_api_management_proxies` - API proxies
- `btp_api_management_products` - Products

**SAP ABAP Tables:**
- `abap_datasources` - ABAP datasources
- `abap_partner_profiles` - Partner profiles
- `abap_ports` - ABAP ports
- `abap_rfc_destinations` - RFC destinations
- `abap_soap_services` - SOAP services
- `abap_soap_service_bindings` - Service bindings

---

## Example Usage

### 1. Get All Properties (Dev Schema)

```bash
curl http://localhost:3000/dev/properties
```

Response:
```json
[
  {
    "id": 1,
    "name": "max_connections",
    "value": "100",
    "description": "Maximum number of concurrent connections",
    "created_at": "2025-11-25T10:00:00",
    "updated_at": "2025-11-25T10:00:00"
  }
]
```

### 2. Get DataSources for a System

```bash
curl http://localhost:3000/dev/systems/sys-001/datasources
```

### 3. Get Azure Tenant Subscriptions

```bash
curl http://localhost:3000/dev/azure/tenants/tenant-001/subscriptions
```

### 4. Check API Health

```bash
curl http://localhost:3000/health
```

---

## Testing the Complete Flow

### 1. Start All Services

**Terminal 1 - REST API:**
```bash
uv run rest_api_server.py
```

**Terminal 2 - MCP Server:**
```bash
uv run api_server.py
```

### 2. Call MCP Tool

The MCP tool will call the REST API, which queries PostgreSQL:

```json
{
  "tool": "get_properties",
  "arguments": {
    "schema": "dev"
  }
}
```

Flow:
1. MCP Server receives tool call
2. Makes HTTP GET to `http://localhost:3000/dev/properties`
3. REST API queries PostgreSQL: `SELECT * FROM dev.properties`
4. Returns data through the chain

---

## Customization

### Adding New Endpoints

1. Add route in `rest_api_server.py`:

```python
@app.get("/{schema}/your_new_endpoint")
def get_your_data(
    schema: str = Path(...),
    db: Session = Depends(get_db)
):
    validate_schema(schema)
    query = f"SELECT * FROM {schema}.your_table"
    return execute_query(db, query)
```

2. Add corresponding MCP tool in `api_server.py`

3. Update documentation

### Modifying Database Queries

Edit the SQL queries in `rest_api_server.py` to match your schema:

```python
query = f"""
    SELECT your_columns
    FROM {schema}.your_table
    WHERE your_condition
"""
```

---

## Production Deployment

### Security Considerations

1. **Add Authentication:**

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/{schema}/properties")
def get_properties(
    schema: str,
    credentials: HTTPBearer = Depends(security),
    db: Session = Depends(get_db)
):
    # Validate token
    # ...
```

2. **Configure CORS:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

3. **Use Environment Variables:**
- Never hardcode credentials
- Use `.env` for all configuration

4. **Enable HTTPS:**
- Use reverse proxy (nginx, Caddy)
- Get SSL certificates

### Performance Optimization

1. **Connection Pooling:**
Already configured in `database.py`:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

2. **Add Caching:**
```bash
pip install fastapi-cache2
```

3. **Add Indexes:**
See `sample_schema.sql` for index examples

---

## Troubleshooting

### REST API Won't Start

**Error: Port 3000 already in use**
```bash
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process or use different port
uvicorn rest_api_server:app --port 3001
```

**Error: Database connection failed**
- Check PostgreSQL is running
- Verify credentials in `.env`
- Test connection: `psql -h localhost -U username -d database`

### MCP Server Can't Reach REST API

**Error: Connection refused**
- Ensure REST API is running on port 3000
- Check `API_BASE_URL` in `.env` is `http://localhost:3000`
- Verify firewall settings

### No Data Returned

**Empty arrays returned**
- Check if tables exist: `\dt dev.*` in psql
- Verify sample data was inserted
- Check schema name (dev/prod/test)

---

## Development Tips

### Auto-Reload

Both servers support auto-reload:

```bash
# REST API
uvicorn rest_api_server:app --reload --port 3000

# MCP Server
# Already has auto-reload in FastMCP
```

### Interactive API Documentation

FastAPI provides automatic interactive docs:
- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

### Database Migrations

For production, use Alembic:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

## Summary

You now have a complete 3-tier architecture:

1. **MCP Server** - Protocol layer with 20 tools
2. **REST API** - HTTP layer with 20 endpoints
3. **PostgreSQL** - Data layer with multi-schema support

All components are production-ready and fully documented!
