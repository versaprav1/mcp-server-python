# API MCP Server Tools

This document lists the available tools in the Integration Platform API MCP Server (`api_server`). These tools allow you to interact with the integration platform's data via the REST API.

## General Tools

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_properties` | Retrieves a list of all Properties from the database. | `schema` (str): dev, prod, or test |
| `get_property_types` | Retrieves a list of all available PropertyTypes. | `schema` (str): dev, prod, or test |
| `get_metadata` | Retrieves a list of all Metadata entries from the database. | `schema` (str): dev, prod, or test |

## Core & High-Level Relationship Tools

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_datasources_to_tenants` | Retrieves all DataSources and their associated AzureTenants relationships. | `schema` (str) |
| `get_system_datasources` | Retrieves all DataSources that belong to a specific System. | `schema` (str), `system_id` (str) |
| `get_dataflow_systems` | Retrieves the sender and receiver Systems for a specific DataFlow. | `schema` (str), `dataflow_id` (str) |
| `get_dataflow_inventories` | Retrieves all technical interfaces (Inventories) that make up a specific DataFlow. | `schema` (str), `dataflow_id` (str) |

## Microsoft Azure Tools

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_azure_tenant_subscriptions` | Retrieves all Subscriptions within a specific AzureTenant. | `schema` (str), `tenant_id` (str) |
| `get_azure_subscription_resource_groups` | Retrieves all ResourceGroups within a specific AzureSubscription. | `schema` (str), `subscription_id` (str) |
| `get_azure_api_management_service_apis` | Retrieves all APIs managed by a specific ApiManagementService. | `schema` (str), `service_id` (str) |
| `get_azure_api_management_api_products` | Retrieves all Products that a specific API is part of. | `schema` (str), `api_id` (str) |
| `get_azure_standard_app_workflows` | Retrieves all Workflows inside a specific StandardApp. | `schema` (str), `app_id` (str) |
| `get_azure_logic_app_workflow_versions` | Retrieves all historical Versions of a specific LogicAppWorkflow. | `schema` (str), `workflow_id` (str) |

## SAP BTP Tools

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_btp_cloud_integration_package_artefacts` | Retrieves all integration Artefacts (like iFlows) within a Package. | `schema` (str), `package_id` (str) |
| `get_btp_cloud_integration_artefact_runtime` | Shows the runtime status and details for a specific deployed Artefact. | `schema` (str), `artefact_id` (str) |
| `get_btp_api_management_provider_proxies` | Retrieves all API Proxies associated with a specific API Provider. | `schema` (str), `provider_id` (str) |
| `get_btp_api_management_proxy_products` | Lists which Products a specific API Proxy is included in. | `schema` (str), `proxy_id` (str) |

## SAP ABAP Tools

| Tool Name | Description | Arguments |
| :--- | :--- | :--- |
| `get_abap_datasource_partner_profiles` | Retrieves all PartnerProfiles (e.g., iDoc partners) for a specific DataSource. | `schema` (str), `datasource_id` (str) |
| `get_abap_port_rfc_destinations` | Shows the RfcDestinations (RFC destinations) associated with a specific AbapPort. | `schema` (str), `port_id` (str) |
| `get_abap_soap_service_bindings` | Retrieves all Bindings (endpoints) for a specific AbapSoapService. | `schema` (str), `service_id` (str) |
