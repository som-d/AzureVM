resource "azurerm_linux_virtual_machine" "vm" {
  name = "tf-linux-vm"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  size = "Standard_B1s"
  admin_username = "azureuser"
  network_interface_ids = [ azurerm_network_interface.nic.id ]

  admin_ssh_key {
    username = "azureuser"
    public_key = file("/home/azureuser/.ssh/id_rsa.pub")
  }

  os_disk {
    caching = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer = "UbuntuServer"
    sku = "18.04-LTS"
    version = "latest"
  }

}