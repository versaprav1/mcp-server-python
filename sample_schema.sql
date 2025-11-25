-- Sample Database Schema for Integration Platform
-- This creates tables for dev, prod, and test schemas

-- Create schemas
CREATE SCHEMA IF NOT EXISTS dev;
CREATE SCHEMA IF NOT EXISTS prod;
CREATE SCHEMA IF NOT EXISTS test;

-- ============================================================================
-- GENERAL TABLES
-- ============================================================================

-- Properties table
CREATE TABLE IF NOT EXISTS dev.properties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Property Types table
CREATE TABLE IF NOT EXISTS dev.property_types (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Metadata table
CREATE TABLE IF NOT EXISTS dev.metadata (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) NOT NULL,
    value TEXT,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- CORE ENTITIES
-- ============================================================================

-- Systems table
CREATE TABLE IF NOT EXISTS dev.systems (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    system_type VARCHAR(50),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DataSources table
CREATE TABLE IF NOT EXISTS dev.datasources (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    system_id VARCHAR(100) REFERENCES dev.systems(id),
    datasource_type VARCHAR(100),
    connection_string TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DataFlows table
CREATE TABLE IF NOT EXISTS dev.dataflows (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sender_system_id VARCHAR(100) REFERENCES dev.systems(id),
    receiver_system_id VARCHAR(100) REFERENCES dev.systems(id),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventories table (technical interfaces)
CREATE TABLE IF NOT EXISTS dev.inventories (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dataflow_id VARCHAR(100) REFERENCES dev.dataflows(id),
    interface_type VARCHAR(100),
    endpoint_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- MICROSOFT AZURE TABLES
-- ============================================================================

-- Azure Tenants table
CREATE TABLE IF NOT EXISTS dev.azure_tenants (
    id VARCHAR(100) PRIMARY KEY,
    tenant_name VARCHAR(255) NOT NULL,
    tenant_id_guid UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure Subscriptions table
CREATE TABLE IF NOT EXISTS dev.azure_subscriptions (
    id VARCHAR(100) PRIMARY KEY,
    subscription_name VARCHAR(255) NOT NULL,
    tenant_id VARCHAR(100) REFERENCES dev.azure_tenants(id),
    subscription_id_guid UUID,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure Resource Groups table
CREATE TABLE IF NOT EXISTS dev.azure_resource_groups (
    id VARCHAR(100) PRIMARY KEY,
    resource_group_name VARCHAR(255) NOT NULL,
    subscription_id VARCHAR(100) REFERENCES dev.azure_subscriptions(id),
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure API Management Services table
CREATE TABLE IF NOT EXISTS dev.azure_api_management_services (
    id VARCHAR(100) PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    resource_group_id VARCHAR(100) REFERENCES dev.azure_resource_groups(id),
    publisher_email VARCHAR(255),
    publisher_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure API Management APIs table
CREATE TABLE IF NOT EXISTS dev.azure_api_management_apis (
    id VARCHAR(100) PRIMARY KEY,
    api_name VARCHAR(255) NOT NULL,
    service_id VARCHAR(100) REFERENCES dev.azure_api_management_services(id),
    api_path VARCHAR(255),
    api_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure API Management Products table
CREATE TABLE IF NOT EXISTS dev.azure_api_management_products (
    id VARCHAR(100) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    requires_subscription BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure API to Product mapping
CREATE TABLE IF NOT EXISTS dev.azure_api_product_mapping (
    api_id VARCHAR(100) REFERENCES dev.azure_api_management_apis(id),
    product_id VARCHAR(100) REFERENCES dev.azure_api_management_products(id),
    PRIMARY KEY (api_id, product_id)
);

-- Azure Standard Apps table
CREATE TABLE IF NOT EXISTS dev.azure_standard_apps (
    id VARCHAR(100) PRIMARY KEY,
    app_name VARCHAR(255) NOT NULL,
    resource_group_id VARCHAR(100) REFERENCES dev.azure_resource_groups(id),
    app_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure Logic App Workflows table
CREATE TABLE IF NOT EXISTS dev.azure_logic_app_workflows (
    id VARCHAR(100) PRIMARY KEY,
    workflow_name VARCHAR(255) NOT NULL,
    standard_app_id VARCHAR(100) REFERENCES dev.azure_standard_apps(id),
    state VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Azure Logic App Workflow Versions table
CREATE TABLE IF NOT EXISTS dev.azure_logic_app_workflow_versions (
    id VARCHAR(100) PRIMARY KEY,
    workflow_id VARCHAR(100) REFERENCES dev.azure_logic_app_workflows(id),
    version_number VARCHAR(50) NOT NULL,
    definition JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- SAP BTP TABLES
-- ============================================================================

-- BTP Cloud Integration Packages table
CREATE TABLE IF NOT EXISTS dev.btp_cloud_integration_packages (
    id VARCHAR(100) PRIMARY KEY,
    package_name VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BTP Cloud Integration Artefacts table
CREATE TABLE IF NOT EXISTS dev.btp_cloud_integration_artefacts (
    id VARCHAR(100) PRIMARY KEY,
    artefact_name VARCHAR(255) NOT NULL,
    package_id VARCHAR(100) REFERENCES dev.btp_cloud_integration_packages(id),
    artefact_type VARCHAR(50), -- iFlow, Value Mapping, etc.
    version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BTP Cloud Integration Artefact Runtime table
CREATE TABLE IF NOT EXISTS dev.btp_cloud_integration_artefact_runtime (
    id VARCHAR(100) PRIMARY KEY,
    artefact_id VARCHAR(100) REFERENCES dev.btp_cloud_integration_artefacts(id),
    status VARCHAR(50), -- Started, Stopped, Error
    deployment_status VARCHAR(50),
    last_deployed_at TIMESTAMP,
    error_message TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BTP API Management Providers table
CREATE TABLE IF NOT EXISTS dev.btp_api_management_providers (
    id VARCHAR(100) PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL,
    description TEXT,
    base_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BTP API Management Proxies table
CREATE TABLE IF NOT EXISTS dev.btp_api_management_proxies (
    id VARCHAR(100) PRIMARY KEY,
    proxy_name VARCHAR(255) NOT NULL,
    provider_id VARCHAR(100) REFERENCES dev.btp_api_management_providers(id),
    proxy_endpoint TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BTP API Management Products table
CREATE TABLE IF NOT EXISTS dev.btp_api_management_products (
    id VARCHAR(100) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BTP Proxy to Product mapping
CREATE TABLE IF NOT EXISTS dev.btp_proxy_product_mapping (
    proxy_id VARCHAR(100) REFERENCES dev.btp_api_management_proxies(id),
    product_id VARCHAR(100) REFERENCES dev.btp_api_management_products(id),
    PRIMARY KEY (proxy_id, product_id)
);

-- ============================================================================
-- SAP ABAP TABLES
-- ============================================================================

-- ABAP DataSources table (extends main datasources)
CREATE TABLE IF NOT EXISTS dev.abap_datasources (
    id VARCHAR(100) PRIMARY KEY,
    datasource_id VARCHAR(100) REFERENCES dev.datasources(id),
    system_id VARCHAR(50),
    client VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ABAP Partner Profiles table
CREATE TABLE IF NOT EXISTS dev.abap_partner_profiles (
    id VARCHAR(100) PRIMARY KEY,
    abap_datasource_id VARCHAR(100) REFERENCES dev.abap_datasources(id),
    partner_number VARCHAR(50) NOT NULL,
    partner_type VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ABAP Ports table
CREATE TABLE IF NOT EXISTS dev.abap_ports (
    id VARCHAR(100) PRIMARY KEY,
    port_name VARCHAR(255) NOT NULL,
    port_type VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ABAP RFC Destinations table
CREATE TABLE IF NOT EXISTS dev.abap_rfc_destinations (
    id VARCHAR(100) PRIMARY KEY,
    port_id VARCHAR(100) REFERENCES dev.abap_ports(id),
    destination_name VARCHAR(255) NOT NULL,
    connection_type VARCHAR(50),
    target_host VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ABAP SOAP Services table
CREATE TABLE IF NOT EXISTS dev.abap_soap_services (
    id VARCHAR(100) PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    service_definition TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ABAP SOAP Service Bindings table
CREATE TABLE IF NOT EXISTS dev.abap_soap_service_bindings (
    id VARCHAR(100) PRIMARY KEY,
    service_id VARCHAR(100) REFERENCES dev.abap_soap_services(id),
    binding_name VARCHAR(255) NOT NULL,
    endpoint_url TEXT,
    binding_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- RELATIONSHIP TABLES
-- ============================================================================

-- DataSources to Azure Tenants mapping
CREATE TABLE IF NOT EXISTS dev.datasource_tenant_mapping (
    datasource_id VARCHAR(100) REFERENCES dev.datasources(id),
    tenant_id VARCHAR(100) REFERENCES dev.azure_tenants(id),
    PRIMARY KEY (datasource_id, tenant_id)
);

-- ============================================================================
-- REPLICATE FOR PROD AND TEST SCHEMAS
-- ============================================================================

-- Note: In a real scenario, you would run the same CREATE TABLE statements
-- for 'prod' and 'test' schemas. For brevity, this sample shows 'dev' only.
-- You can copy all the above statements and replace 'dev.' with 'prod.' and 'test.'

-- ============================================================================
-- SAMPLE DATA (DEV SCHEMA ONLY)
-- ============================================================================

-- Insert sample properties
INSERT INTO dev.properties (name, value, description) VALUES
    ('max_connections', '100', 'Maximum number of concurrent connections'),
    ('timeout_seconds', '30', 'Request timeout in seconds'),
    ('retry_count', '3', 'Number of retry attempts')
ON CONFLICT DO NOTHING;

-- Insert sample property types
INSERT INTO dev.property_types (type_name, description) VALUES
    ('String', 'Text property'),
    ('Integer', 'Numeric property'),
    ('Boolean', 'True/False property')
ON CONFLICT DO NOTHING;

-- Insert sample metadata
INSERT INTO dev.metadata (key, value, category) VALUES
    ('version', '1.0.0', 'system'),
    ('environment', 'development', 'system'),
    ('last_sync', '2025-11-25', 'sync')
ON CONFLICT DO NOTHING;

-- Insert sample systems
INSERT INTO dev.systems (id, name, description, system_type, status) VALUES
    ('sys-001', 'SAP ERP', 'SAP ERP Production System', 'SAP', 'active'),
    ('sys-002', 'Azure Integration', 'Azure Integration Services', 'Azure', 'active'),
    ('sys-003', 'BTP Platform', 'SAP Business Technology Platform', 'SAP_BTP', 'active')
ON CONFLICT DO NOTHING;

-- Insert sample datasources
INSERT INTO dev.datasources (id, name, system_id, datasource_type) VALUES
    ('ds-001', 'ERP Database', 'sys-001', 'Database'),
    ('ds-002', 'Azure SQL', 'sys-002', 'Database'),
    ('ds-003', 'BTP Integration', 'sys-003', 'API')
ON CONFLICT DO NOTHING;

-- Insert sample dataflows
INSERT INTO dev.dataflows (id, name, description, sender_system_id, receiver_system_id, status) VALUES
    ('df-001', 'ERP to Azure Sync', 'Synchronize ERP data to Azure', 'sys-001', 'sys-002', 'active'),
    ('df-002', 'Azure to BTP Integration', 'Integrate Azure with BTP', 'sys-002', 'sys-003', 'active')
ON CONFLICT DO NOTHING;

-- Insert sample Azure tenants
INSERT INTO dev.azure_tenants (id, tenant_name, tenant_id_guid) VALUES
    ('tenant-001', 'Main Tenant', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890')
ON CONFLICT DO NOTHING;

-- Insert sample Azure subscriptions
INSERT INTO dev.azure_subscriptions (id, subscription_name, tenant_id, subscription_id_guid, status) VALUES
    ('sub-001', 'Production Subscription', 'tenant-001', 'b2c3d4e5-f6a7-8901-bcde-f12345678901', 'active')
ON CONFLICT DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_datasources_system_id ON dev.datasources(system_id);
CREATE INDEX IF NOT EXISTS idx_dataflows_sender ON dev.dataflows(sender_system_id);
CREATE INDEX IF NOT EXISTS idx_dataflows_receiver ON dev.dataflows(receiver_system_id);
CREATE INDEX IF NOT EXISTS idx_inventories_dataflow ON dev.inventories(dataflow_id);
CREATE INDEX IF NOT EXISTS idx_azure_subs_tenant ON dev.azure_subscriptions(tenant_id);
CREATE INDEX IF NOT EXISTS idx_azure_rg_subscription ON dev.azure_resource_groups(subscription_id);
