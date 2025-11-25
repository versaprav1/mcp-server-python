# Integration Platform API Tools

Complete documentation for all 20 MCP tools that interact with your integration platform API.

## Quick Start

### 1. Configure API Connection

Edit your `.env` file:

```env
API_BASE_URL=http://your-api-url.com
API_AUTH_METHOD=bearer
API_BEARER_TOKEN=your_token_here
```

### 2. Start the API Server

```bash
uv run api_server.py
```

The server runs on `http://localhost:8020`

---

## Tool Categories

- **General Endpoints**: 3 tools for properties, property types, and metadata
- **Core Relationships**: 4 tools for systems, dataflows, and datasources
- **Azure**: 6 tools for Azure resources and relationships
- **SAP BTP**: 4 tools for SAP Business Technology Platform
- **SAP ABAP**: 3 tools for SAP ABAP integration points

---

## General Endpoints

### `get_properties`

Retrieves all properties from the database.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`

**Example:**
```json
{
  "tool": "get_properties",
  "arguments": {
    "schema": "dev"
  }
}
```

---

### `get_property_types`

Retrieves all available property types.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`

**Example:**
```json
{
  "tool": "get_property_types",
  "arguments": {
    "schema": "dev"
  }
}
```

---

### `get_metadata`

Retrieves all metadata entries.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`

**Example:**
```json
{
  "tool": "get_metadata",
  "arguments": {
    "schema": "prod"
  }
}
```

---

## Core & High-Level Relationship Endpoints

### `get_datasources_to_tenants`

Shows relationships between DataSources and AzureTenants.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`

**Example:**
```json
{
  "tool": "get_datasources_to_tenants",
  "arguments": {
    "schema": "dev"
  }
}
```

---

### `get_system_datasources`

Retrieves all datasources belonging to a specific system.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `system_id` (string): Unique identifier for the system

**Example:**
```json
{
  "tool": "get_system_datasources",
  "arguments": {
    "schema": "dev",
    "system_id": "sys-12345"
  }
}
```

---

### `get_dataflow_systems`

Gets sender and receiver systems for a dataflow.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `dataflow_id` (string): Unique identifier for the dataflow

**Example:**
```json
{
  "tool": "get_dataflow_systems",
  "arguments": {
    "schema": "dev",
    "dataflow_id": "df-67890"
  }
}
```

---

### `get_dataflow_inventories`

Retrieves technical interfaces (inventories) for a dataflow.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `dataflow_id` (string): Unique identifier for the dataflow

**Example:**
```json
{
  "tool": "get_dataflow_inventories",
  "arguments": {
    "schema": "dev",
    "dataflow_id": "df-67890"
  }
}
```

---

## Microsoft Azure Relationship Endpoints

### `get_azure_tenant_subscriptions`

Lists all subscriptions within an Azure tenant.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `tenant_id` (string): Azure tenant ID

**Example:**
```json
{
  "tool": "get_azure_tenant_subscriptions",
  "arguments": {
    "schema": "dev",
    "tenant_id": "tenant-abc123"
  }
}
```

---

### `get_azure_subscription_resource_groups`

Lists all resource groups in a subscription.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `subscription_id` (string): Azure subscription ID

**Example:**
```json
{
  "tool": "get_azure_subscription_resource_groups",
  "arguments": {
    "schema": "dev",
    "subscription_id": "sub-xyz789"
  }
}
```

---

### `get_azure_api_management_service_apis`

Lists all APIs in an API Management service.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `service_id` (string): API Management service ID

**Example:**
```json
{
  "tool": "get_azure_api_management_service_apis",
  "arguments": {
    "schema": "dev",
    "service_id": "apim-service-001"
  }
}
```

---

### `get_azure_api_management_api_products`

Lists products that an API belongs to.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `api_id` (string): API Management API ID

**Example:**
```json
{
  "tool": "get_azure_api_management_api_products",
  "arguments": {
    "schema": "dev",
    "api_id": "api-12345"
  }
}
```

---

### `get_azure_standard_app_workflows`

Lists all workflows in a Standard App.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `app_id` (string): Standard App ID

**Example:**
```json
{
  "tool": "get_azure_standard_app_workflows",
  "arguments": {
    "schema": "dev",
    "app_id": "app-standard-001"
  }
}
```

---

### `get_azure_logic_app_workflow_versions`

Lists all versions of a Logic App workflow.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `workflow_id` (string): Logic App workflow ID

**Example:**
```json
{
  "tool": "get_azure_logic_app_workflow_versions",
  "arguments": {
    "schema": "dev",
    "workflow_id": "workflow-abc"
  }
}
```

---

## SAP BTP Relationship Endpoints

### `get_btp_cloud_integration_package_artefacts`

Lists all artefacts (like iFlows) in a Cloud Integration package.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `package_id` (string): Cloud Integration package ID

**Example:**
```json
{
  "tool": "get_btp_cloud_integration_package_artefacts",
  "arguments": {
    "schema": "dev",
    "package_id": "pkg-integration-001"
  }
}
```

---

### `get_btp_cloud_integration_artefact_runtime`

Shows runtime status for a deployed artefact.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `artefact_id` (string): Cloud Integration artefact ID

**Example:**
```json
{
  "tool": "get_btp_cloud_integration_artefact_runtime",
  "arguments": {
    "schema": "dev",
    "artefact_id": "iflow-12345"
  }
}
```

---

### `get_btp_api_management_provider_proxies`

Lists API proxies for a provider.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `provider_id` (string): API Management provider ID

**Example:**
```json
{
  "tool": "get_btp_api_management_provider_proxies",
  "arguments": {
    "schema": "dev",
    "provider_id": "provider-001"
  }
}
```

---

### `get_btp_api_management_proxy_products`

Lists products that include a specific proxy.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `proxy_id` (string): API Management proxy ID

**Example:**
```json
{
  "tool": "get_btp_api_management_proxy_products",
  "arguments": {
    "schema": "dev",
    "proxy_id": "proxy-abc123"
  }
}
```

---

## SAP ABAP Relationship Endpoints

### `get_abap_datasource_partner_profiles`

Lists partner profiles (e.g., iDoc partners) for a datasource.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `datasource_id` (string): ABAP datasource ID

**Example:**
```json
{
  "tool": "get_abap_datasource_partner_profiles",
  "arguments": {
    "schema": "dev",
    "datasource_id": "ds-sap-001"
  }
}
```

---

### `get_abap_port_rfc_destinations`

Shows RFC destinations for an ABAP port.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `port_id` (string): ABAP port ID

**Example:**
```json
{
  "tool": "get_abap_port_rfc_destinations",
  "arguments": {
    "schema": "dev",
    "port_id": "port-rfc-001"
  }
}
```

---

### `get_abap_soap_service_bindings`

Lists bindings (endpoints) for a SOAP service.

**Parameters:**
- `schema` (string): Database schema - `dev`, `prod`, or `test`
- `service_id` (string): ABAP SOAP service ID

**Example:**
```json
{
  "tool": "get_abap_soap_service_bindings",
  "arguments": {
    "schema": "dev",
    "service_id": "soap-service-001"
  }
}
```

---

## Response Format

All tools return a consistent response format:

### Success Response

```json
{
  "success": true,
  "status_code": 200,
  "data": {
    // API response data
  }
}
```

### Error Response

```json
{
  "success": false,
  "status_code": 404,
  "error": "HTTP Error message",
  "error_detail": "Detailed error information"
}
```

---

## Error Handling

The tools handle various error scenarios:

- **Invalid Schema**: Returns error if schema is not `dev`, `prod`, or `test`
- **Connection Errors**: Returns error if API is unreachable
- **Authentication Errors**: Returns 401/403 status codes
- **Not Found**: Returns 404 when resource doesn't exist
- **Timeout**: Returns error if request exceeds configured timeout

---

## Authentication

Configure authentication in `.env`:

### Bearer Token (Recommended)

```env
API_AUTH_METHOD=bearer
API_BEARER_TOKEN=your_token_here
```

### API Key

```env
API_AUTH_METHOD=api_key
API_KEY=your_api_key_here
```

### Basic Authentication

```env
API_AUTH_METHOD=basic
API_BASIC_USERNAME=your_username
API_BASIC_PASSWORD=your_password
```

### No Authentication

```env
API_AUTH_METHOD=none
```

---

## Testing

Test a tool manually:

```bash
curl -X POST http://localhost:8020/tools/get_properties \
  -H "Content-Type: application/json" \
  -d '{"schema": "dev"}'
```

---

## Troubleshooting

### Connection Refused

- Check if your API is running
- Verify `API_BASE_URL` in `.env`
- Check network connectivity

### Authentication Failed

- Verify your token/credentials in `.env`
- Check token expiration
- Ensure correct `API_AUTH_METHOD`

### Invalid Schema Error

- Schema must be exactly: `dev`, `prod`, or `test`
- Check for typos or extra spaces
