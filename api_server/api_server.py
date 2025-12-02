"""
Integration Platform API MCP Server
A Model Context Protocol server that provides tools for interacting with the integration platform API.
Covers General, Core Relationships, Azure, SAP BTP, and SAP ABAP endpoints.
"""

from mcp.server.fastmcp import FastMCP
from .api_client import APIClient
from .api_config import api_config

# Create MCP server
mcp = FastMCP("Integration Platform API Server", json_response=True, port=8020)

# Initialize API client
client = APIClient()


# ============================================================================
# GENERAL ENDPOINTS
# ============================================================================

@mcp.tool()
def get_properties(schema: str) -> dict:
    """
    Retrieves a list of all Properties from the database.
    
    Args:
        schema: Database schema (dev, prod, or test)
    
    Returns:
        Dictionary with list of properties
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/properties")


@mcp.tool()
def get_property_types(schema: str) -> dict:
    """
    Retrieves a list of all available PropertyTypes.
    
    Args:
        schema: Database schema (dev, prod, or test)
    
    Returns:
        Dictionary with list of property types
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/property_types")


@mcp.tool()
def get_metadata(schema: str) -> dict:
    """
    Retrieves a list of all Metadata entries from the database.
    
    Args:
        schema: Database schema (dev, prod, or test)
    
    Returns:
        Dictionary with list of metadata entries
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/metadata")


# ============================================================================
# CORE & HIGH-LEVEL RELATIONSHIP ENDPOINTS
# ============================================================================

@mcp.tool()
def get_datasources_to_tenants(schema: str) -> dict:
    """
    Retrieves all DataSources and their associated AzureTenants relationships.
    
    Args:
        schema: Database schema (dev, prod, or test)
    
    Returns:
        Dictionary with datasources to tenants relationships
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/relationships/datasources_to_tenants")


@mcp.tool()
def get_system_datasources(schema: str, system_id: str) -> dict:
    """
    Retrieves all DataSources that belong to a specific System.
    
    Args:
        schema: Database schema (dev, prod, or test)
        system_id: Unique identifier for the system
    
    Returns:
        Dictionary with list of datasources for the system
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/systems/{system_id}/datasources")


@mcp.tool()
def get_dataflow_systems(schema: str, dataflow_id: str) -> dict:
    """
    Retrieves the sender and receiver Systems for a specific DataFlow.
    
    Args:
        schema: Database schema (dev, prod, or test)
        dataflow_id: Unique identifier for the dataflow
    
    Returns:
        Dictionary with sender and receiver systems
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/dataflows/{dataflow_id}/systems")


@mcp.tool()
def get_dataflow_inventories(schema: str, dataflow_id: str) -> dict:
    """
    Retrieves all technical interfaces (Inventories) that make up a specific DataFlow.
    
    Args:
        schema: Database schema (dev, prod, or test)
        dataflow_id: Unique identifier for the dataflow
    
    Returns:
        Dictionary with list of inventories for the dataflow
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/dataflows/{dataflow_id}/inventories")


# ============================================================================
# MICROSOFT AZURE RELATIONSHIP ENDPOINTS
# ============================================================================

@mcp.tool()
def get_azure_tenant_subscriptions(schema: str, tenant_id: str) -> dict:
    """
    Retrieves all Subscriptions within a specific AzureTenant.
    
    Args:
        schema: Database schema (dev, prod, or test)
        tenant_id: Unique identifier for the Azure tenant
    
    Returns:
        Dictionary with list of subscriptions
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/azure/tenants/{tenant_id}/subscriptions")


@mcp.tool()
def get_azure_subscription_resource_groups(schema: str, subscription_id: str) -> dict:
    """
    Retrieves all ResourceGroups within a specific AzureSubscription.
    
    Args:
        schema: Database schema (dev, prod, or test)
        subscription_id: Unique identifier for the Azure subscription
    
    Returns:
        Dictionary with list of resource groups
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/azure/subscriptions/{subscription_id}/resource_groups")


@mcp.tool()
def get_azure_api_management_service_apis(schema: str, service_id: str) -> dict:
    """
    Retrieves all APIs managed by a specific ApiManagementService.
    
    Args:
        schema: Database schema (dev, prod, or test)
        service_id: Unique identifier for the API Management service
    
    Returns:
        Dictionary with list of APIs
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/azure/api_management_services/{service_id}/apis")


@mcp.tool()
def get_azure_api_management_api_products(schema: str, api_id: str) -> dict:
    """
    Retrieves all Products that a specific API is part of.
    
    Args:
        schema: Database schema (dev, prod, or test)
        api_id: Unique identifier for the API Management API
    
    Returns:
        Dictionary with list of products
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/azure/api_management_apis/{api_id}/products")


@mcp.tool()
def get_azure_standard_app_workflows(schema: str, app_id: str) -> dict:
    """
    Retrieves all Workflows inside a specific StandardApp.
    
    Args:
        schema: Database schema (dev, prod, or test)
        app_id: Unique identifier for the Standard App
    
    Returns:
        Dictionary with list of workflows
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/azure/standard_apps/{app_id}/workflows")


@mcp.tool()
def get_azure_logic_app_workflow_versions(schema: str, workflow_id: str) -> dict:
    """
    Retrieves all historical Versions of a specific LogicAppWorkflow.
    
    Args:
        schema: Database schema (dev, prod, or test)
        workflow_id: Unique identifier for the Logic App workflow
    
    Returns:
        Dictionary with list of workflow versions
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/azure/logic_app_workflows/{workflow_id}/versions")


# ============================================================================
# SAP BTP RELATIONSHIP ENDPOINTS
# ============================================================================

@mcp.tool()
def get_btp_cloud_integration_package_artefacts(schema: str, package_id: str) -> dict:
    """
    Retrieves all integration Artefacts (like iFlows) within a Package.
    
    Args:
        schema: Database schema (dev, prod, or test)
        package_id: Unique identifier for the Cloud Integration package
    
    Returns:
        Dictionary with list of artefacts
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/btp/cloud_integration_packages/{package_id}/artefacts")


@mcp.tool()
def get_btp_cloud_integration_artefact_runtime(schema: str, artefact_id: str) -> dict:
    """
    Shows the runtime status and details for a specific deployed Artefact.
    
    Args:
        schema: Database schema (dev, prod, or test)
        artefact_id: Unique identifier for the Cloud Integration artefact
    
    Returns:
        Dictionary with runtime status and details
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/btp/cloud_integration_artefacts/{artefact_id}/runtime")


@mcp.tool()
def get_btp_api_management_provider_proxies(schema: str, provider_id: str) -> dict:
    """
    Retrieves all API Proxies associated with a specific API Provider.
    
    Args:
        schema: Database schema (dev, prod, or test)
        provider_id: Unique identifier for the API Management provider
    
    Returns:
        Dictionary with list of proxies
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/btp/api_management_providers/{provider_id}/proxies")


@mcp.tool()
def get_btp_api_management_proxy_products(schema: str, proxy_id: str) -> dict:
    """
    Lists which Products a specific API Proxy is included in.
    
    Args:
        schema: Database schema (dev, prod, or test)
        proxy_id: Unique identifier for the API Management proxy
    
    Returns:
        Dictionary with list of products
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/btp/api_management_proxies/{proxy_id}/products")


# ============================================================================
# SAP ABAP RELATIONSHIP ENDPOINTS
# ============================================================================

@mcp.tool()
def get_abap_datasource_partner_profiles(schema: str, datasource_id: str) -> dict:
    """
    Retrieves all PartnerProfiles (e.g., iDoc partners) for a specific DataSource.
    
    Args:
        schema: Database schema (dev, prod, or test)
        datasource_id: Unique identifier for the ABAP datasource
    
    Returns:
        Dictionary with list of partner profiles
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/abap/datasources/{datasource_id}/partner_profiles")


@mcp.tool()
def get_abap_port_rfc_destinations(schema: str, port_id: str) -> dict:
    """
    Shows the RfcDestinations (RFC destinations) associated with a specific AbapPort.
    
    Args:
        schema: Database schema (dev, prod, or test)
        port_id: Unique identifier for the ABAP port
    
    Returns:
        Dictionary with list of RFC destinations
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/abap/ports/{port_id}/rfc_destinations")


@mcp.tool()
def get_abap_soap_service_bindings(schema: str, service_id: str) -> dict:
    """
    Retrieves all Bindings (endpoints) for a specific AbapSoapService.
    
    Args:
        schema: Database schema (dev, prod, or test)
        service_id: Unique identifier for the ABAP SOAP service
    
    Returns:
        Dictionary with list of bindings
    """
    if not client.validate_schema(schema):
        return {
            "success": False,
            "error": f"Invalid schema '{schema}'. Must be one of: dev, prod, test"
        }
    
    return client.get(f"/{schema}/abap/soap_services/{service_id}/bindings")


# ============================================================================
# MCP RESOURCES
# ============================================================================

@mcp.resource("api://config")
def get_api_config() -> str:
    """Get current API configuration (without sensitive data)."""
    import json
    config_info = {
        "base_url": api_config.base_url,
        "auth_method": api_config.auth_method,
        "timeout": api_config.timeout,
        "valid_schemas": api_config.valid_schemas,
        "authenticated": bool(api_config.bearer_token or api_config.api_key or api_config.basic_username)
    }
    return json.dumps(config_info, indent=2)


# Run with streamable HTTP transport
if __name__ == "__main__":
    print("Starting Integration Platform API MCP Server...")
    print(f"API Base URL: {api_config.base_url}")
    print(f"Authentication: {api_config.auth_method}")
    print(f"Valid Schemas: {', '.join(api_config.valid_schemas)}")
    print("Server will run on http://localhost:8020")
    print("\nAvailable Tools: 20")
    print("  - General: 3 tools")
    print("  - Core Relationships: 4 tools")
    print("  - Azure: 6 tools")
    print("  - SAP BTP: 4 tools")
    print("  - SAP ABAP: 3 tools")
    mcp.run(transport="streamable-http")
