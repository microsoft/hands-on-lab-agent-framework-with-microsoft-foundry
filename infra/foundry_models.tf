resource "azapi_resource" "chat_model_deployment" {
  type      = "Microsoft.CognitiveServices/accounts/deployments@2025-04-01-preview"
  name      = "chatmodel"
  parent_id = azapi_resource.foundry.id
  tags      = local.tags_azapi
  body = {
    properties = {
      currentCapacity = 50
      model = {
        format  = "OpenAI"
        name    = "gpt-4.1"
        version = "2025-04-14"
      }
      raiPolicyName = "Microsoft.DefaultV2"
    }
    sku = {
      capacity = 100
      name     = "GlobalStandard"
    }
  }
}
