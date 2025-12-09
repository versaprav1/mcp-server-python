# LLM API Reference - Integration Platform

This document provides all the knowledge an LLM needs to effectively use the Integration Platform REST API.

## Quick Reference

| Category | Base URL | Authentication |
|----------|----------|----------------|
| Local | `http://localhost:3000` | None (development) |
| Remote | Your ngrok URL | Bearer token (production) |

**Schema Parameter**: All endpoints require `{schema}` = `dev`, `prod`, or `test`

---

## Entity Hierarchy & Navigation

Understanding these relationships helps navigate the API:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CORE ENTITIES                            │
├─────────────────────────────────────────────────────────────────┤
│  System ──────► DataSource ──────► AzureTenant                  │
│     │                                                           │
│     └──► DataFlow ──────► Inventory (technical interface)       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     MICROSOFT AZURE                             │
├─────────────────────────────────────────────────────────────────┤
│  AzureTenant                                                    │
│     └──► AzureSubscription                                      │
│            └──► AzureResourceGroup                              │
│                                                                 │
│  ApiManagementService ──► API ──► Product                       │
│  StandardApp ──► LogicAppWorkflow ──► WorkflowVersion           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        SAP BTP                                  │
├─────────────────────────────────────────────────────────────────┤
│  CloudIntegrationPackage ──► Artefact ──► Runtime               │
│  ApiManagementProvider ──► Proxy ──► Product                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       SAP ABAP                                  │
├─────────────────────────────────────────────────────────────────┤
│  AbapDataSource ──► PartnerProfile                              │
│  AbapPort ──► RfcDestination                                    │
│  AbapSoapService ──► Binding                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Complete Endpoint Reference

### General Endpoints

#### GET `/{schema}/properties`
**Purpose**: Retrieve all configuration properties.  
**Use when**: You need system configuration settings or key-value pairs.  
**Response fields**: `id`, `name`, `value`, `description`, `created_at`, `updated_at`

```bash
GET /dev/properties
```

---

#### GET `/{schema}/property_types`
**Purpose**: List all available property type definitions.  
**Use when**: You need to understand what types of properties exist.  
**Response fields**: `id`, `type_name`, `description`, `created_at`

```bash
GET /dev/property_types
```

---

#### GET `/{schema}/metadata`
**Purpose**: Retrieve all system metadata entries.  
**Use when**: You need system-level metadata or configuration.  
**Response fields**: `id`, `key`, `value`, `category`, `created_at`, `updated_at`

```bash
GET /dev/metadata
```

---

### Core Relationship Endpoints

#### GET `/{schema}/relationships/datasources_to_tenants`
**Purpose**: Map all DataSources to their associated Azure Tenants.  
**Use when**: Understanding which datasources connect to which Azure tenants.  
**Response fields**: `datasource_id`, `datasource_name`, `datasource_type`, `tenant_id`, `tenant_name`, `tenant_id_guid`

```bash
GET /dev/relationships/datasources_to_tenants
```

---

#### GET `/{schema}/systems/{system_id}/datasources`
**Purpose**: Find all DataSources belonging to a specific System.  
**Use when**: You have a system_id and need its data sources.  
**Parameters**: `system_id` (path) - Unique identifier for the system  
**Response fields**: `id`, `name`, `datasource_type`, `connection_string`, `created_at`, `updated_at`

```bash
GET /dev/systems/sys-001/datasources
```

---

#### GET `/{schema}/dataflows/{dataflow_id}/systems`
**Purpose**: Get the sender and receiver Systems for a specific DataFlow.  
**Use when**: You need to understand the source and destination of a data flow.  
**Parameters**: `dataflow_id` (path) - Unique identifier for the dataflow  
**Response fields**: `dataflow_id`, `dataflow_name`, `sender_system_id`, `sender_system_name`, `sender_system_type`, `receiver_system_id`, `receiver_system_name`, `receiver_system_type`

```bash
GET /dev/dataflows/df-001/systems
```

---

#### GET `/{schema}/dataflows/{dataflow_id}/inventories`
**Purpose**: List all technical interfaces (Inventories) that compose a DataFlow.  
**Use when**: You need the technical implementation details of a data flow.  
**Parameters**: `dataflow_id` (path) - Unique identifier for the dataflow  
**Response fields**: `id`, `name`, `interface_type`, `endpoint_url`, `created_at`, `updated_at`

```bash
GET /dev/dataflows/df-001/inventories
```

---

### Microsoft Azure Endpoints

#### GET `/{schema}/azure/tenants/{tenant_id}/subscriptions`
**Purpose**: List all Azure Subscriptions within a specific Tenant.  
**Use when**: Drilling down from tenant level to subscription level.  
**Parameters**: `tenant_id` (path) - Unique identifier for the Azure tenant  
**Response fields**: `id`, `subscription_name`, `subscription_id_guid`, `status`, `created_at`, `updated_at`

```bash
GET /dev/azure/tenants/tenant-001/subscriptions
```

---

#### GET `/{schema}/azure/subscriptions/{subscription_id}/resource_groups`
**Purpose**: List all Resource Groups within a specific Subscription.  
**Use when**: Drilling down from subscription to resource group level.  
**Parameters**: `subscription_id` (path) - Unique identifier for the Azure subscription  
**Response fields**: `id`, `resource_group_name`, `location`, `created_at`, `updated_at`

```bash
GET /dev/azure/subscriptions/sub-001/resource_groups
```

---

#### GET `/{schema}/azure/api_management_services/{service_id}/apis`
**Purpose**: List all APIs managed by a specific API Management Service.  
**Use when**: Exploring APIs within an APIM instance.  
**Parameters**: `service_id` (path) - Unique identifier for the API Management service  
**Response fields**: `id`, `api_name`, `api_path`, `api_version`, `created_at`, `updated_at`

```bash
GET /dev/azure/api_management_services/apim-001/apis
```

---

#### GET `/{schema}/azure/api_management_apis/{api_id}/products`
**Purpose**: Find which Products include a specific API.  
**Use when**: Understanding API bundling and access control.  
**Parameters**: `api_id` (path) - Unique identifier for the API Management API  
**Response fields**: `id`, `product_name`, `description`, `requires_subscription`, `created_at`, `updated_at`

```bash
GET /dev/azure/api_management_apis/api-001/products
```

---

#### GET `/{schema}/azure/standard_apps/{app_id}/workflows`
**Purpose**: List all Workflows inside a specific Standard Logic App.  
**Use when**: Exploring workflow definitions within a Logic App.  
**Parameters**: `app_id` (path) - Unique identifier for the Standard App  
**Response fields**: `id`, `workflow_name`, `state`, `created_at`, `updated_at`

```bash
GET /dev/azure/standard_apps/app-001/workflows
```

---

#### GET `/{schema}/azure/logic_app_workflows/{workflow_id}/versions`
**Purpose**: Get all historical versions of a Logic App Workflow.  
**Use when**: Auditing changes or rolling back to a previous version.  
**Parameters**: `workflow_id` (path) - Unique identifier for the Logic App workflow  
**Response fields**: `id`, `version_number`, `definition`, `created_at`

```bash
GET /dev/azure/logic_app_workflows/wf-001/versions
```

---

### SAP BTP Endpoints

#### GET `/{schema}/btp/cloud_integration_packages/{package_id}/artefacts`
**Purpose**: List all integration Artefacts (iFlows, etc.) within a Package.  
**Use when**: Exploring contents of a CI/DS package.  
**Parameters**: `package_id` (path) - Unique identifier for the Cloud Integration package  
**Response fields**: `id`, `artefact_name`, `artefact_type`, `version`, `created_at`, `updated_at`

```bash
GET /dev/btp/cloud_integration_packages/pkg-001/artefacts
```

---

#### GET `/{schema}/btp/cloud_integration_artefacts/{artefact_id}/runtime`
**Purpose**: Get runtime status and deployment details for a specific Artefact.  
**Use when**: Checking if an iFlow is deployed and running correctly.  
**Parameters**: `artefact_id` (path) - Unique identifier for the Cloud Integration artefact  
**Response fields**: `id`, `artefact_id`, `artefact_name`, `status`, `deployment_status`, `last_deployed_at`, `error_message`, `updated_at`

```bash
GET /dev/btp/cloud_integration_artefacts/art-001/runtime
```

---

#### GET `/{schema}/btp/api_management_providers/{provider_id}/proxies`
**Purpose**: List all API Proxies associated with a specific API Provider.  
**Use when**: Exploring APIs exposed through BTP API Management.  
**Parameters**: `provider_id` (path) - Unique identifier for the API Management provider  
**Response fields**: `id`, `proxy_name`, `proxy_endpoint`, `created_at`, `updated_at`

```bash
GET /dev/btp/api_management_providers/prov-001/proxies
```

---

#### GET `/{schema}/btp/api_management_proxies/{proxy_id}/products`
**Purpose**: Find which Products include a specific API Proxy.  
**Use when**: Understanding proxy bundling and access control.  
**Parameters**: `proxy_id` (path) - Unique identifier for the API Management proxy  
**Response fields**: `id`, `product_name`, `description`, `created_at`, `updated_at`

```bash
GET /dev/btp/api_management_proxies/proxy-001/products
```

---

### SAP ABAP Endpoints

#### GET `/{schema}/abap/datasources/{datasource_id}/partner_profiles`
**Purpose**: List all Partner Profiles (iDoc partners) for a specific DataSource.  
**Use when**: Exploring EDI/iDoc partner configurations.  
**Parameters**: `datasource_id` (path) - Unique identifier for the ABAP datasource  
**Response fields**: `id`, `partner_number`, `partner_type`, `description`, `created_at`, `updated_at`

```bash
GET /dev/abap/datasources/ds-001/partner_profiles
```

---

#### GET `/{schema}/abap/ports/{port_id}/rfc_destinations`
**Purpose**: Get RFC Destinations associated with a specific ABAP Port.  
**Use when**: Understanding outbound connections from an ABAP system.  
**Parameters**: `port_id` (path) - Unique identifier for the ABAP port  
**Response fields**: `id`, `destination_name`, `connection_type`, `target_host`, `created_at`, `updated_at`

```bash
GET /dev/abap/ports/port-001/rfc_destinations
```

---

#### GET `/{schema}/abap/soap_services/{service_id}/bindings`
**Purpose**: List all Bindings (endpoints) for a specific ABAP SOAP Service.  
**Use when**: Finding service endpoints for SOAP integration.  
**Parameters**: `service_id` (path) - Unique identifier for the ABAP SOAP service  
**Response fields**: `id`, `binding_name`, `endpoint_url`, `binding_type`, `created_at`, `updated_at`

```bash
GET /dev/abap/soap_services/soap-001/bindings
```

---

### Utility Endpoints

#### GET `/`
**Purpose**: Get API information and status.  
**Use when**: Initial connection check or discovery.  
**Response fields**: `name`, `version`, `status`, `endpoints`, `documentation`

```bash
GET /
```

---

#### GET `/health`
**Purpose**: Health check including database connectivity.  
**Use when**: Verifying the API and database are operational.  
**Response fields**: `status`, `database`

```bash
GET /health
```

---

## Common Workflows

### 1. Explore Azure Infrastructure
```
1. GET /dev/azure/tenants/{tenant_id}/subscriptions
2. For each subscription: GET /dev/azure/subscriptions/{id}/resource_groups
```

### 2. Analyze a DataFlow
```
1. GET /dev/dataflows/{dataflow_id}/systems     → Get sender/receiver
2. GET /dev/dataflows/{dataflow_id}/inventories → Get technical interfaces
```

### 3. Check BTP Integration Status
```
1. GET /dev/btp/cloud_integration_packages/{pkg}/artefacts → List iFlows
2. GET /dev/btp/cloud_integration_artefacts/{id}/runtime   → Check deployment
```

### 4. Map System Connections
```
1. GET /dev/relationships/datasources_to_tenants → Full mapping
2. GET /dev/systems/{system_id}/datasources      → Specific system
```

---

## Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Process response |
| 400 | Invalid schema | Use `dev`, `prod`, or `test` |
| 404 | Resource not found | Verify ID exists |
| 500 | Database error | Check connectivity |
| 503 | Service unavailable | API or DB down |

---

## OpenAPI Specification

For programmatic access to the complete API schema:
- **Swagger UI**: `{base_url}/docs`
- **ReDoc**: `{base_url}/redoc`
- **OpenAPI JSON**: `{base_url}/openapi.json`
