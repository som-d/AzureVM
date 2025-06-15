# Control Node Setup Guide

This guide will walk you through using the `controlNode_setup.sh` script to prepare your control node for automation with Terraform, Azure CLI, and Ansible.

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

## Step-by-Step Instructions

### 1. **Copy the Script to Control Node**

From your **laptop**:

- If your control node is a remote VM, copy the script using `scp`:
  ```sh
  scp ./controlNode_setup.sh <your-username>@<control-node-ip>:~
  ```
- If you are already on the control node, just make sure the script file is in your home or working directory.

### 2. **Connect to the Control Node**

From your **laptop**:

- SSH into your control node:
  ```sh
  ssh <your-username>@<control-node-ip>
  ```

### 3. **Make the Script Executable**

On the **control node** terminal:
```sh
chmod +x ./controlNode_setup.sh
```

### 4. **Run the Setup Script**

On the **control node** terminal:
```sh
./controlNode_setup.sh
```
- The script will check for and install or upgrade:
  - Terraform
  - Azure CLI
  - Ansible (with user prompts if conflicts)
  - Ansible Docker collection

**Follow any prompts** (especially for upgrading or reinstalling Ansible).

### 5. **Login to Azure**

After the script completes, run:
```sh
az login
```
- This will open a browser window or give you a code to enter at https://microsoft.com/devicelogin
- Login with your Azure credentials.

### 6. **Verify Installation (Optional)**

Check that each tool is ready by running:
```sh
terraform version
az --version
ansible --version
ansible-galaxy collection list | grep community.docker
```

---

## Using VS Code to Connect via SSH (from your laptop)

You can use [Visual Studio Code](https://code.visualstudio.com/) with the **Remote - SSH** extension for a rich, graphical development experience directly on your control node.

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

VS Code will connect and open a new window where you are now working **directly on the control node**. You can open folders, edit files, run terminals, and use all VS Code features as if you were local.

---

## Troubleshooting

- If you see errors about unmet dependencies or package conflicts, follow the script prompts.
- For any login or permission issues, ensure your user has `sudo` privileges.
- For SSH connection issues, ensure port 22 is open and accessible, and your user is correctly configured on the control node.

---

## Next Steps

You’re now ready to use Terraform, Azure CLI, and Ansible for automation tasks!

---

**Questions?**  
Open an issue in this repo or contact [soham](mailto:sohamdeshmukh611@gmail.com) (project maintainer).