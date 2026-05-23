# Azure Monitoring Stack — Ansible & Docker Compose

## Overview

This project automates the deployment of a full-featured open-source monitoring stack (Prometheus, Grafana, Alertmanager, Node Exporter, Uptime Kuma) on Azure VMs using Ansible and Docker Compose.

---

## Project Structure

```plaintext
ansible/
├── inventory.ini
├── main.yml
├── README.md
├── group_vars/
│   └── all_vars.yml
├── files/
│   ├── docker-compose.yml
│   ├── prometheus.yml.j2
│   ├── alert.rules.yml
│   └── grafana/
│       ├── dashboards/
│       │   └── node_exporter_dashboard.json
│       ├── provisioning/
│       │   └── dashboards
│       │       └── dashboards.yml
│       │   └── datasource
│       │       └── datasource.yml
│       
```

---

## How to Customize

- **Add more agents:**  
  - Deploy Node Exporter on additional VMs.
  - Add their private IP and port to `prometheus_targets` in `group_vars/all_vars.yml`.

- **Change alert rules:**  
  - Edit `files/alert.rules.yml`.

- **Add/replace dashboards:**  
  - Place JSON files in `files/grafana/dashboards/`.

- **Change alert email:**  
  - Edit `alert_email` in `group_vars/all_vars.yml`.

---

## Security Notes

- Ensure SSH keys are used for Ansible access.
- Open only necessary ports in Azure NSG (22, 3000, 9090, 9093, 3001, 9100).

---

## Usage — Step by Step

1. **Update Ansible Variables**
   - Edit `group_vars/all_vars.yml` to reflect your VM IPs and alert email.

2. **Update Inventory**
   - Edit `inventory.ini` with the public IPs of your VMs.

3. **Run the Playbook**
   ```sh
   cd ansible
   ansible-playbook -i inventory.ini main.yml
   ```
   Type **yes** press **Enter** again type **yes** press **Enter**

4. **Access Services**
   - Grafana: `http://<collector_public_ip>:3000`   userid: admin  passwd: admin (default) then navigate to Home > Dashboards > Node Exporter Full (dashboardName)
   - Prometheus: `http://<collector_public_ip>:9090`
   - Alertmanager: `http://<collector_public_ip>:9093`
   - Uptime Kuma: `http://<collector_public_ip>:3001`
