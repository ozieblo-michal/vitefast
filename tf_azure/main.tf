resource "azurerm_resource_group" "aci_rg" {
  name     = "aciResourceGroup"
  location = "West Europe"
}

resource "azurerm_container_group" "aci" {
  name                = "aci-container-group"
  location            = azurerm_resource_group.aci_rg.location
  resource_group_name = azurerm_resource_group.aci_rg.name
  os_type             = "Linux"

  container {
    name   = "fastapi-container"
    image  = "ozieblomichal/fastapi-template:dev"
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }
  }

  ip_address {
    type = "Public"
    ports {
      port     = 80
      protocol = "TCP"
    }
  }
}
