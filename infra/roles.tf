resource "azurerm_role_assignment" "user_cognitive_services_open_ai_contributor" {
  scope                = azapi_resource.foundry.id
  role_definition_name = "Cognitive Services OpenAI Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "user_azure_ai_user" {
  scope                = azapi_resource.foundry.id
  role_definition_name = "Azure AI User"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "user_azure_ai_project_manager" {
  scope                = azapi_resource.foundry.id
  role_definition_name = "Azure AI Project Manager"
  principal_id         = data.azurerm_client_config.current.object_id
}