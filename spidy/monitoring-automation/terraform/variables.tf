variable "location" {
  description = "Azure region"
  default     = "East US"
}

variable "resource_group_name" {
  description = "Resource group name"
  default     = "monitoring-demo-rg"
}

variable "vnet_name" {
  default = "monitoring-vnet"
}

variable "address_space" {
  default = ["10.0.0.0/16"]
}

variable "subnet_name" {
  default = "monitoring-subnet"
}

variable "subnet_prefix" {
  default = "10.0.1.0/24"
}

variable "admin_username" {
  description = "Admin username"
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key"
  default     = "~/.ssh/id_rsa.pub"
}