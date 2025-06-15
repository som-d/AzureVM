# Terraform Infrastructure for Monitoring Stack

This folder contains [Terraform](https://www.terraform.io/) code to provision the infrastructure required for the monitoring stack (e.g. servers for Prometheus, Grafana, exporters, etc).

---

## Prerequisites

- [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed
- Cloud provider credentials (AWS, Azure, GCP, etc.) configured locally or via environment variables
- (Optional) SSH key pair for remote access to created VMs

---

## Usage

1. **Initialize Terraform (downloads providers and modules):**
    ```sh
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

6. **(Optional) Destroy infrastructure:**
    ```sh
    terraform destroy
    ```

---

## Variables

- Define your own values in a `terraform.tfvars` file or pass them with `-var` flags.
- Sensitive variables (like secrets or keys) should **not** be committed to version control.

---

## Outputs

- After `terraform apply`, note the output values (such as public IPs) – these are often used by Ansible inventory for subsequent configuration.

---

## Example: Using Outputs in Ansible

You can generate an inventory file dynamically using Terraform output:
```sh
terraform output -json > tf_outputs.json
# Use a script or tool to convert tf_outputs.json to Ansible inventory if needed
```

---

## Best Practices

- Use remote state (e.g., S3, Azure Blob) for team collaboration.
- Keep provider credentials secure.
- Use modules for reusable infrastructure.
- Commit only non-sensitive files (`*.tf`, not `terraform.tfvars` or `.terraform/`).

---

## Cleaning Up

To remove all resources created by Terraform:
```sh
terraform destroy
```

---

## References

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Providers](https://registry.terraform.io/browse/providers)
- [HashiCorp Configuration Language](https://www.terraform.io/language)

---

## License

MIT