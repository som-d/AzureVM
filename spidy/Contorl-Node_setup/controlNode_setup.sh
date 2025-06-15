#!/bin/bash
set -e

echo "==============================="
echo " Control Node Setup Script"
echo "==============================="

# Install prerequisites
sudo apt-get update
sudo apt-get install -y wget unzip gnupg software-properties-common curl python3-pip

# Install Terraform if not present
if ! command -v terraform &> /dev/null; then
    echo "Installing Terraform..."
    wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt-get update && sudo apt-get install -y terraform
else
    echo "Terraform already installed: $(terraform version | head -n 1)"
    echo "Upgrading Terraform..."
    sudo apt-get install --only-upgrade terraform
fi

# Install Azure CLI if not present
if ! command -v az &> /dev/null; then
    echo "Installing Azure CLI..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
else
    echo "Azure CLI already installed: $(az version | grep azure-cli)"
    echo "Upgrading Azure CLI..."
    sudo apt-get install --only-upgrade azure-cli
fi

# Ansible installation/upgrade
if command -v ansible &> /dev/null; then
    echo "Ansible already installed: $(ansible --version | head -n 1)"
    echo "Upgrading Ansible..."
    if ! sudo apt-get install --only-upgrade ansible; then
        echo -e "\n[WARNING] Ansible upgrade failed due to package conflict or unmet dependencies."
        read -p "Do you want to uninstall existing Ansible and install the latest from PPA? (y/n): " confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            echo "Removing old Ansible version..."
            sudo apt-get remove --purge -y ansible ansible-core || true
            sudo apt-get autoremove -y
            sudo add-apt-repository --yes --update ppa:ansible/ansible
            sudo apt-get update
            sudo apt-get install -y ansible
        else
            echo "Skipping Ansible upgrade. Existing version remains."
        fi
    fi
else
    echo "Installing Ansible from PPA..."
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install -y ansible
fi

# Install or upgrade Ansible Docker collection
echo "Installing or upgrading community.docker collection for Ansible..."
ansible-galaxy collection install community.docker --upgrade

echo "==============================="
echo " All tools installed and ready!"
echo " Run: 'az login' to authenticate Azure CLI."
echo "==============================="