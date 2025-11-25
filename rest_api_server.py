"""
REST API Server for Integration Platform
FastAPI application that exposes all integration platform endpoints backed by PostgreSQL.
"""

from fastapi import FastAPI, Depends, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from database import get_db, get_schema_prefix
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Integration Platform API",
    description="REST API for integration platform with Azure, SAP BTP, and SAP ABAP endpoints",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_schema(schema: str):
    """Validate schema parameter."""
    valid_schemas = ["dev", "prod", "test"]
    if schema not in valid_schemas:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid schema '{schema}'. Must be one of: {', '.join(valid_schemas)}"
        )
    return schema


def execute_query(db: Session, query: str, params: Dict = None) -> List[Dict]:
    """Execute a SQL query and return results as list of dicts."""
    try:
        result = db.execute(text(query), params or {})
        if result.returns_rows:
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        return []
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ============================================================================
# GENERAL ENDPOINTS
# ============================================================================

@app.get("/{schema}/properties")
def get_properties(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    db: Session = Depends(get_db)
):
    """Retrieves a list of all Properties from the database."""
    validate_schema(schema)
    
    query = f"""
        SELECT id, name, value, description, created_at, updated_at
        FROM {schema}.properties
        ORDER BY name
    """
    
    return execute_query(db, query)


@app.get("/{schema}/property_types")
def get_property_types(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    db: Session = Depends(get_db)
):
    """Retrieves a list of all available PropertyTypes."""
    validate_schema(schema)
    
    query = f"""
        SELECT id, type_name, description, created_at
        FROM {schema}.property_types
        ORDER BY type_name
    """
    
    return execute_query(db, query)


@app.get("/{schema}/metadata")
def get_metadata(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    db: Session = Depends(get_db)
):
    """Retrieves a list of all Metadata entries from the database."""
    validate_schema(schema)
    
    query = f"""
        SELECT id, key, value, category, created_at, updated_at
        FROM {schema}.metadata
        ORDER BY key
    """
    
    return execute_query(db, query)


# ============================================================================
# CORE & HIGH-LEVEL RELATIONSHIP ENDPOINTS
# ============================================================================

@app.get("/{schema}/relationships/datasources_to_tenants")
def get_datasources_to_tenants(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    db: Session = Depends(get_db)
):
    """Retrieves all DataSources and their associated AzureTenants relationships."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            d.id as datasource_id,
            d.name as datasource_name,
            d.datasource_type,
            t.id as tenant_id,
            t.tenant_name,
            t.tenant_id_guid
        FROM {schema}.datasources d
        LEFT JOIN {schema}.datasource_tenant_mapping dtm ON d.id = dtm.datasource_id
        LEFT JOIN {schema}.azure_tenants t ON dtm.tenant_id = t.id
        ORDER BY d.name
    """
    
    return execute_query(db, query)


@app.get("/{schema}/systems/{system_id}/datasources")
def get_system_datasources(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    system_id: str = Path(..., description="Unique identifier for the system"),
    db: Session = Depends(get_db)
):
    """Retrieves all DataSources that belong to a specific System."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            d.id,
            d.name,
            d.datasource_type,
            d.connection_string,
            d.created_at,
            d.updated_at
        FROM {schema}.datasources d
        WHERE d.system_id = :system_id
        ORDER BY d.name
    """
    
    return execute_query(db, query, {"system_id": system_id})


@app.get("/{schema}/dataflows/{dataflow_id}/systems")
def get_dataflow_systems(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    dataflow_id: str = Path(..., description="Unique identifier for the dataflow"),
    db: Session = Depends(get_db)
):
    """Retrieves the sender and receiver Systems for a specific DataFlow."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            df.id as dataflow_id,
            df.name as dataflow_name,
            sender.id as sender_system_id,
            sender.name as sender_system_name,
            sender.system_type as sender_system_type,
            receiver.id as receiver_system_id,
            receiver.name as receiver_system_name,
            receiver.system_type as receiver_system_type
        FROM {schema}.dataflows df
        LEFT JOIN {schema}.systems sender ON df.sender_system_id = sender.id
        LEFT JOIN {schema}.systems receiver ON df.receiver_system_id = receiver.id
        WHERE df.id = :dataflow_id
    """
    
    result = execute_query(db, query, {"dataflow_id": dataflow_id})
    if not result:
        raise HTTPException(status_code=404, detail=f"DataFlow '{dataflow_id}' not found")
    return result[0]


@app.get("/{schema}/dataflows/{dataflow_id}/inventories")
def get_dataflow_inventories(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    dataflow_id: str = Path(..., description="Unique identifier for the dataflow"),
    db: Session = Depends(get_db)
):
    """Retrieves all technical interfaces (Inventories) that make up a specific DataFlow."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            i.id,
            i.name,
            i.interface_type,
            i.endpoint_url,
            i.created_at,
            i.updated_at
        FROM {schema}.inventories i
        WHERE i.dataflow_id = :dataflow_id
        ORDER BY i.name
    """
    
    return execute_query(db, query, {"dataflow_id": dataflow_id})


# ============================================================================
# MICROSOFT AZURE RELATIONSHIP ENDPOINTS
# ============================================================================

@app.get("/{schema}/azure/tenants/{tenant_id}/subscriptions")
def get_azure_tenant_subscriptions(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    tenant_id: str = Path(..., description="Unique identifier for the Azure tenant"),
    db: Session = Depends(get_db)
):
    """Retrieves all Subscriptions within a specific AzureTenant."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            s.id,
            s.subscription_name,
            s.subscription_id_guid,
            s.status,
            s.created_at,
            s.updated_at
        FROM {schema}.azure_subscriptions s
        WHERE s.tenant_id = :tenant_id
        ORDER BY s.subscription_name
    """
    
    return execute_query(db, query, {"tenant_id": tenant_id})


@app.get("/{schema}/azure/subscriptions/{subscription_id}/resource_groups")
def get_azure_subscription_resource_groups(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    subscription_id: str = Path(..., description="Unique identifier for the Azure subscription"),
    db: Session = Depends(get_db)
):
    """Retrieves all ResourceGroups within a specific AzureSubscription."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            rg.id,
            rg.resource_group_name,
            rg.location,
            rg.created_at,
            rg.updated_at
        FROM {schema}.azure_resource_groups rg
        WHERE rg.subscription_id = :subscription_id
        ORDER BY rg.resource_group_name
    """
    
    return execute_query(db, query, {"subscription_id": subscription_id})


@app.get("/{schema}/azure/api_management_services/{service_id}/apis")
def get_azure_api_management_service_apis(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    service_id: str = Path(..., description="Unique identifier for the API Management service"),
    db: Session = Depends(get_db)
):
    """Retrieves all APIs managed by a specific ApiManagementService."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            a.id,
            a.api_name,
            a.api_path,
            a.api_version,
            a.created_at,
            a.updated_at
        FROM {schema}.azure_api_management_apis a
        WHERE a.service_id = :service_id
        ORDER BY a.api_name
    """
    
    return execute_query(db, query, {"service_id": service_id})


@app.get("/{schema}/azure/api_management_apis/{api_id}/products")
def get_azure_api_management_api_products(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    api_id: str = Path(..., description="Unique identifier for the API Management API"),
    db: Session = Depends(get_db)
):
    """Retrieves all Products that a specific API is part of."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            p.id,
            p.product_name,
            p.description,
            p.requires_subscription,
            p.created_at,
            p.updated_at
        FROM {schema}.azure_api_management_products p
        INNER JOIN {schema}.azure_api_product_mapping apm ON p.id = apm.product_id
        WHERE apm.api_id = :api_id
        ORDER BY p.product_name
    """
    
    return execute_query(db, query, {"api_id": api_id})


@app.get("/{schema}/azure/standard_apps/{app_id}/workflows")
def get_azure_standard_app_workflows(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    app_id: str = Path(..., description="Unique identifier for the Standard App"),
    db: Session = Depends(get_db)
):
    """Retrieves all Workflows inside a specific StandardApp."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            w.id,
            w.workflow_name,
            w.state,
            w.created_at,
            w.updated_at
        FROM {schema}.azure_logic_app_workflows w
        WHERE w.standard_app_id = :app_id
        ORDER BY w.workflow_name
    """
    
    return execute_query(db, query, {"app_id": app_id})


@app.get("/{schema}/azure/logic_app_workflows/{workflow_id}/versions")
def get_azure_logic_app_workflow_versions(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    workflow_id: str = Path(..., description="Unique identifier for the Logic App workflow"),
    db: Session = Depends(get_db)
):
    """Retrieves all historical Versions of a specific LogicAppWorkflow."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            v.id,
            v.version_number,
            v.definition,
            v.created_at
        FROM {schema}.azure_logic_app_workflow_versions v
        WHERE v.workflow_id = :workflow_id
        ORDER BY v.created_at DESC
    """
    
    return execute_query(db, query, {"workflow_id": workflow_id})


# ============================================================================
# SAP BTP RELATIONSHIP ENDPOINTS
# ============================================================================

@app.get("/{schema}/btp/cloud_integration_packages/{package_id}/artefacts")
def get_btp_cloud_integration_package_artefacts(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    package_id: str = Path(..., description="Unique identifier for the Cloud Integration package"),
    db: Session = Depends(get_db)
):
    """Retrieves all integration Artefacts (like iFlows) within a Package."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            a.id,
            a.artefact_name,
            a.artefact_type,
            a.version,
            a.created_at,
            a.updated_at
        FROM {schema}.btp_cloud_integration_artefacts a
        WHERE a.package_id = :package_id
        ORDER BY a.artefact_name
    """
    
    return execute_query(db, query, {"package_id": package_id})


@app.get("/{schema}/btp/cloud_integration_artefacts/{artefact_id}/runtime")
def get_btp_cloud_integration_artefact_runtime(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    artefact_id: str = Path(..., description="Unique identifier for the Cloud Integration artefact"),
    db: Session = Depends(get_db)
):
    """Shows the runtime status and details for a specific deployed Artefact."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            r.id,
            r.artefact_id,
            a.artefact_name,
            r.status,
            r.deployment_status,
            r.last_deployed_at,
            r.error_message,
            r.updated_at
        FROM {schema}.btp_cloud_integration_artefact_runtime r
        INNER JOIN {schema}.btp_cloud_integration_artefacts a ON r.artefact_id = a.id
        WHERE r.artefact_id = :artefact_id
    """
    
    result = execute_query(db, query, {"artefact_id": artefact_id})
    if not result:
        raise HTTPException(status_code=404, detail=f"Runtime info for artefact '{artefact_id}' not found")
    return result[0]


@app.get("/{schema}/btp/api_management_providers/{provider_id}/proxies")
def get_btp_api_management_provider_proxies(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    provider_id: str = Path(..., description="Unique identifier for the API Management provider"),
    db: Session = Depends(get_db)
):
    """Retrieves all API Proxies associated with a specific API Provider."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            p.id,
            p.proxy_name,
            p.proxy_endpoint,
            p.created_at,
            p.updated_at
        FROM {schema}.btp_api_management_proxies p
        WHERE p.provider_id = :provider_id
        ORDER BY p.proxy_name
    """
    
    return execute_query(db, query, {"provider_id": provider_id})


@app.get("/{schema}/btp/api_management_proxies/{proxy_id}/products")
def get_btp_api_management_proxy_products(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    proxy_id: str = Path(..., description="Unique identifier for the API Management proxy"),
    db: Session = Depends(get_db)
):
    """Lists which Products a specific API Proxy is included in."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            p.id,
            p.product_name,
            p.description,
            p.created_at,
            p.updated_at
        FROM {schema}.btp_api_management_products p
        INNER JOIN {schema}.btp_proxy_product_mapping ppm ON p.id = ppm.product_id
        WHERE ppm.proxy_id = :proxy_id
        ORDER BY p.product_name
    """
    
    return execute_query(db, query, {"proxy_id": proxy_id})


# ============================================================================
# SAP ABAP RELATIONSHIP ENDPOINTS
# ============================================================================

@app.get("/{schema}/abap/datasources/{datasource_id}/partner_profiles")
def get_abap_datasource_partner_profiles(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    datasource_id: str = Path(..., description="Unique identifier for the ABAP datasource"),
    db: Session = Depends(get_db)
):
    """Retrieves all PartnerProfiles (e.g., iDoc partners) for a specific DataSource."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            pp.id,
            pp.partner_number,
            pp.partner_type,
            pp.description,
            pp.created_at,
            pp.updated_at
        FROM {schema}.abap_partner_profiles pp
        WHERE pp.abap_datasource_id = :datasource_id
        ORDER BY pp.partner_number
    """
    
    return execute_query(db, query, {"datasource_id": datasource_id})


@app.get("/{schema}/abap/ports/{port_id}/rfc_destinations")
def get_abap_port_rfc_destinations(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    port_id: str = Path(..., description="Unique identifier for the ABAP port"),
    db: Session = Depends(get_db)
):
    """Shows the RfcDestinations (RFC destinations) associated with a specific AbapPort."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            rd.id,
            rd.destination_name,
            rd.connection_type,
            rd.target_host,
            rd.created_at,
            rd.updated_at
        FROM {schema}.abap_rfc_destinations rd
        WHERE rd.port_id = :port_id
        ORDER BY rd.destination_name
    """
    
    return execute_query(db, query, {"port_id": port_id})


@app.get("/{schema}/abap/soap_services/{service_id}/bindings")
def get_abap_soap_service_bindings(
    schema: str = Path(..., description="Schema name: dev, prod, or test"),
    service_id: str = Path(..., description="Unique identifier for the ABAP SOAP service"),
    db: Session = Depends(get_db)
):
    """Retrieves all Bindings (endpoints) for a specific AbapSoapService."""
    validate_schema(schema)
    
    query = f"""
        SELECT 
            b.id,
            b.binding_name,
            b.endpoint_url,
            b.binding_type,
            b.created_at,
            b.updated_at
        FROM {schema}.abap_soap_service_bindings b
        WHERE b.service_id = :service_id
        ORDER BY b.binding_name
    """
    
    return execute_query(db, query, {"service_id": service_id})


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Integration Platform API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": 20,
        "documentation": "/docs"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    print("Starting Integration Platform REST API Server...")
    print("Server will run on http://localhost:3000")
    print("API Documentation: http://localhost:3000/docs")
    print("Available endpoints: 20")
    uvicorn.run(app, host="0.0.0.0", port=3000)
