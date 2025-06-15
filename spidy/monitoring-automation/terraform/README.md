# Terraform Infrastructure for Monitoring Stack

This folder contains [Terraform](https://www.terraform.io/) code to provision the infrastructure required for the monitoring stack (e.g. servers for Prometheus, Grafana, exporters, etc).

---

## Variables

- Set up `variables.tf` with Azure credentials, location etc.  
- Update `vms.tf` file for adding more vms and configuring vms settings

---

## IMP

- After `terraform apply`, note the output values (such as IPs) – these are used by Ansible inventory for subsequent configuration.

---

## Usage

1. **Initialize Terraform (downloads providers and modules):**
    ```sh
    cd terraform
    terraform init
    ```

2. **Check and review the planned infrastructure changes:**
    ```sh
    terraform plan
    ```

3. **Apply to provision infrastructure:**
    ```sh
    terraform apply
    ```
    - Respond `yes` when prompted to confirm.

4. **(Optional) List all resources managed by Terraforme:**
    ```sh
    terraform state list
    ```

5. **(Optional) Show full details of all resources:**
    ```sh
    terraform show   
    ```
    Type "yes" and Press **Enter**.

6. **VM Details:**  (**VIMP**)
   Save IPs and credentials for use with Ansible.

   Past the IP in ansible/group_vars/all_vars.yml
   
   Replace "=" with ":"
---

## Cleaning Up

To remove all resources created by Terraform:
```sh
terraform destroy
```

---

## Best Practices

- Use remote state (e.g., S3, Azure Blob) for team collaboration.
- Keep provider credentials secure.
- Use modules for reusable infrastructure.
- Commit only non-sensitive files (`*.tf`, not `terraform.tfvars` or `.terraform/`).
