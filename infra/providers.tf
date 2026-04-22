terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.54.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.7.2"
    }

    azapi = {
      source  = "Azure/azapi"
      version = "2.7.0"
    }
  }

  backend "local" {}
  # backend "azurerm" {}
}

provider "azurerm" {
  features {}
}

provider "azapi" {
  # Configuration options
}