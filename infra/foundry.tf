resource "azapi_resource" "foundry" {
  type      = "Microsoft.CognitiveServices/accounts@2025-06-01"
  name      = format("aif-%s", local.resource_suffix_kebabcase)
  parent_id = local.resource_group_id
  location  = local.resource_group_location
  tags      = local.tags_azapi

  body = {
    kind = "AIServices"
    identity = {
      type = "SystemAssigned"
    }

    properties = {
      allowProjectManagement = true
      publicNetworkAccess    = "Enabled"
      disableLocalAuth       = true
      customSubDomainName    = format("aif-%s", local.resource_suffix_kebabcase)
    }
    sku = {
      name = "S0"
    }
  }
  response_export_values = ["*"]
}

resource "azapi_resource" "foundry_app_insights_connection" {
  type      = "Microsoft.CognitiveServices/accounts/connections@2025-06-01"
  name      = "appi-connection-foundry"
  parent_id = azapi_resource.foundry.id
  body = {
    properties = {
      authType = "ApiKey"
      category = "AppInsights"
      credentials = {
        key = azapi_resource.application_insights.output.properties.ConnectionString
      }
      error         = null
      expiryTime    = null
      isSharedToAll = false
      metadata = {
        ApiType    = "Azure"
        ResourceId = azapi_resource.application_insights.id
      }
      peRequirement               = "NotRequired"
      peStatus                    = "NotApplicable"
      sharedUserList              = []
      target                      = azapi_resource.application_insights.id
      useWorkspaceManagedIdentity = false
    }
  }
  ignore_casing             = false
  ignore_missing_property   = true
  ignore_null_property      = false
  schema_validation_enabled = true
}
