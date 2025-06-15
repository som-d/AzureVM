provider "azurerm" {
    features {

    }
}

resource "azurerm_resource_group" "rg" {
  name = "tf-lab-rg"
  location = "East US"
}