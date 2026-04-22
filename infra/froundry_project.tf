resource "azapi_resource" "project" {
  type      = "Microsoft.CognitiveServices/accounts/projects@2025-06-01"
  name      = format("proj-%s", local.resource_suffix_kebabcase)
  location  = local.resource_group_location
  parent_id = azapi_resource.foundry.id
  tags      = local.tags_azapi

  identity {
    type = "SystemAssigned"
  }

  body = {
    properties = {
      description = "Agent Project"
      displayName = "Agent Project"
    }
  }
}

resource "azapi_resource" "foundry_project_app_insights_connection" {
  type      = "Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01"
  name      = "appi-connection-foundry-project"
  parent_id = azapi_resource.project.id
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
