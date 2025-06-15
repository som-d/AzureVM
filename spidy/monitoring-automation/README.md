# Azure VM Infrastructure Monitoring Automation - SOP

---

## Purpose

This Standard Operating Procedure (SOP) outlines the automated setup of a scalable, secure, and maintainable Azure VM monitoring infrastructure using industry best practices.  
**Target Audience:**  
- **Clients** evaluating professional automation solutions for Azure infrastructure.  
- **Myself** (or new engineers) as a future-proof, easy-to-follow reference for setup, maintenance, and expansion.

---

## Why This SOP?

- **For Clients:**  
  This SOP is designed to showcase not only my technical expertise but also my commitment to clear communication, repeatability, and world-class delivery. You’ll see that I deliver solutions you can trust, scale, and hand off to your team with confidence.

- **For Myself/Team:**  
  This document ensures that anyone—returning after years or onboarding for the first time—can quickly and accurately deploy, update, or extend this automation without guesswork. It minimizes operational risk and maximizes business continuity.

---

## What Sets This Solution Apart?

- **Enterprise-Ready Standards:**  
- **Clear Documentation:**  
- **Future-Proof:**  
- **Professional Delivery:**  

---

## Table of Contents

1. [Project Overview & Structure](#project-overview--structure)
2. [Control Node Setup](#control-node-setup)
3. [Terraform: Azure VM Provisioning](#terraform-azure-vm-provisioning)
4. [Ansible Automation](#ansible-automation)
5. [Best Practices & Troubleshooting](#best-practices--troubleshooting)
6. [Appendix: Screenshots & References](#appendix-screenshots--references)

---

## Project Overview & Structure

- **Main Directory:** `spidy/monitoring-automation`
- **Subfolders:**
  - `control-node/`: Control Node configuration and setup scripts
  - `terraform/`: Infrastructure as Code for Azure VMs
  - `ansible/`: Playbooks, inventory, and variables for automation
![alt text](images/image.png)
---


## VM Configuration Recommendation

Before you begin, make sure your control node VM meets the following minimum configuration.  
**You can use this as a reference to create your VM in Azure, AWS, or other cloud providers:**

| Setting             | Recommended Value               |
|---------------------|---------------------------------|
| **OS**              | Ubuntu 22.04 LTS (preferred)    |
| **vCPUs**           | 2 or more                       |
| **RAM**             | 4 GB or more                    |
| **Disk**            | 40 GB SSD or more               |
| **Network**         | Public IP, SSH (port 22) open   |
| **User**            | Non-root user with sudo         |
| **Region**          | Close to your location          |

- **Tip:** You can use a Standard B2s (Azure) / t3.small (AWS) or better.
- **Ensure:** You can SSH into the VM and have internet access.

---

## Prerequisites

- You have access to the control node (a Linux VM, e.g., Ubuntu).
- You can connect via SSH or already have a terminal open on the node.
- You have the `controlNode_setup.sh` file (provided in this repo).

---

## setup VS Code (on your laptop) to control project on VM (optional)

VS Code will connect and open a new window where you are now working **directly on the control node**. You can open folders, edit files, run terminals, and use all VS Code features as if you were local.

### **Step 1: Install Prerequisites**

- Install [VS Code](https://code.visualstudio.com/Download) on your laptop (Windows/macOS/Linux).
- Install the **Remote - SSH** extension from the VS Code Extensions marketplace.

### **Step 2: Set Up Your SSH Keys (if not already done)**

If you don’t already have an SSH key pair on your laptop, generate one:
```sh
ssh-keygen -t ed25519 -C "your_email@example.com"
```
Copy your public key to the control node:
```sh
ssh-copy-id <your-username>@<control-node-ip>
```

### **Step 3: Connect to the Control Node with VS Code**

1. Open VS Code.
2. Press `F1` (or `Ctrl+Shift+P`), and type `Remote-SSH: Connect to Host...`.
3. Enter:  
   ```
   <your-username>@<control-node-ip>
   ```
4. Select your saved SSH configuration or enter details when prompted.


---

## Troubleshooting

- If you see errors about unmet dependencies or package conflicts, follow the script prompts.
- For any login or permission issues, ensure your user has `sudo` privileges.
- For SSH connection issues, ensure port 22 is open and accessible, and your user is correctly configured on the control node.

![alt text](images/image-1.png)

---
## Step-by-Step Control Node Setup Instructions


This guide describes how to set up the Control Node for the Azure VM Infrastructure Monitoring Automation project.

---

## Steps

1. **Clone the Repository on control node**
   ```sh
   git clone <your-repo-url>
   ```

2. **Navigate to the Project Directory**
   ```sh
   cd monitoring-automation
   ```

3. **Run the Control Node Setup Script**
   For Linux:
   ```sh
   ./Control-Node_setup/controlNode_setup_linux.sh
   ```

   > _Ensure the script has execution permissions. If not, run:_
   > ```sh
   > chmod +x ./Control-Node_setup/controlNode_setup_linux.sh
   > ```

- The script will check for and install or upgrade:
  - Terraform
  - Azure CLI
  - Ansible (with user prompts if conflicts)
  - Ansible Docker collection

**Follow any prompts** (especially for upgrading or reinstalling Ansible).
![alt text](images/image-2.png)

### 5. **Login to Azure**

After the script completes, run:
```sh
az login
```
**Come back to prompt press Enter for no change**

- This will open a browser window or give you a code to enter at https://microsoft.com/devicelogin
- Login with your Azure credentials.

![alt text](images/image-3.png)
![alt text](images/image-4.png)

**Come back to prompt press Enter for no change**

![alt text](images/image-5.png)

### 6. **Verify Installation (Optional)**

Check that each tool is ready by running:
```sh
terraform version
az --version
ansible --version
ansible-galaxy collection list | grep community.docker
```

![alt text](images/image-6.png)

---

## Terraform: Azure VM Provisioning

**Reference:** `terraform/README.md`

1. **Configure Variables:**  
   Set up `variables.tf` with Azure credentials, VM sizes, etc.  
   _Screenshot: Sample `variables.tf` file._
2. **Run Terraform:**  
   ```
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```
Type "yes" and Press **Enter**.

3. **VM Details:**  (**VIMP**)
   Save IPs and credentials for use with Ansible.

   Past the IP in ansible/group_vars/all_vars.yml
   
   Replace "=" with ":"


![alt text](images/tf.png)
![alt text](images/tf-1.png)

Type "yes" and Press **Enter**.

![alt text](images/tf-2.png)

**Copy IP to use in ansible inventory**

![alt text](images/tf-3.png)

---

**Past the IP in ansible/group_vars/all_vars.yml**

![alt text](images/tf-4.png)

**Replace "=" with ":"**

![alt text](images/tf-5.png)

---



**Questions?**  
Open an issue in this repo or contact [soham](mailto:sohamdeshmukh611@gmail.com) (project owner).