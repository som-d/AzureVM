output "collector_public_ip" {
  value = azurerm_public_ip.collector.ip_address
  description = "Public IP of the collector VM"
}

output "agent_public_ip" {
  value = azurerm_public_ip.agent.ip_address
  description = "Public IP of the monitoring agent VM"
}

output "collector_private_ip" {
  value = azurerm_network_interface.collector.private_ip_address
  description = "Private IP of the collector VM"
}

output "agent_private_ip" {
  value = azurerm_network_interface.agent.private_ip_address
  description = "Private IP of the monitoring agent VM"
}

output "collector_vm_name" {
  value = azurerm_linux_virtual_machine.collector.name
  description = "Name of the collector VM"
}

output "agent_vm_name" {
  value = azurerm_linux_virtual_machine.agent.name
  description = "Name of the monitoring agent VM"
}