# Azure Monitoring Stack — Ansible & Docker Compose

## Overview

This project automates the deployment of a full-featured open-source monitoring stack (Prometheus, Grafana, Alertmanager, Node Exporter, Uptime Kuma) on Azure VMs using Ansible and Docker Compose.

---

## Features

- Infrastructure as Code: Use Terraform (not included here) to provision VMs and outputs their IPs.
- Ansible playbook installs Docker & Docker Compose and configures everything.
- Docker Compose manages all services on the collector VM.
- Easy-to-extend: Add more Node Exporter agents (just add to `group_vars/all.yml`).
- Preloaded Grafana dashboards, datasources, and Prometheus alerts.

---

## Project Structure

```plaintext
ansible/
├── inventory.ini
├── playbook.yml
├── group_vars/
│   └── all.yml
├── files/
│   ├── docker-compose.yml
│   ├── prometheus.yml
│   ├── alert.rules.yml
│   └── grafana/
│       ├── datasources/
│       │   └── datasource.yml
│       └── dashboards/
│           └── node_exporter_dashboard.json
```

---

## Usage — Step by Step

1. **Provision Azure VMs**
   - Use your existing Terraform to create VMs and NSG rules.
   - Note the public/private IPs for collector and agent.

2. **Update Ansible Variables**
   - Edit `group_vars/all.yml` to reflect your VM IPs and alert email.

3. **Update Inventory**
   - Edit `inventory.ini` with the public IPs of your VMs.

4. **Run the Playbook**
   ```sh
   cd ansible
   ansible-playbook -i inventory.ini playbook.yml
   ```

5. **Access Services**
   - Grafana: `http://<collector_public_ip>:3000`
   - Prometheus: `http://<collector_public_ip>:9090`
   - Alertmanager: `http://<collector_public_ip>:9093`
   - Uptime Kuma: `http://<collector_public_ip>:3001`

---

## How to Customize

- **Add more agents:**  
  - Deploy Node Exporter on additional VMs.
  - Add their private IP and port to `prometheus_targets` in `group_vars/all.yml`.

- **Change alert rules:**  
  - Edit `files/alert.rules.yml`.

- **Add/replace dashboards:**  
  - Place JSON files in `files/grafana/dashboards/`.

- **Change alert email:**  
  - Edit `alert_email` in `group_vars/all.yml`.

---

## For Clients & Freelancers

- Fork/clone this repo for every project.
- Update `group_vars/all.yml` for each client.
- Use the same structure for new monitoring gigs (Fiverr, Upwork, etc).
- All config is managed from variables for easy maintenance.

---

## Security Notes

- Ensure SSH keys are used for Ansible access.
- Open only necessary ports in Azure NSG (22, 3000, 9090, 9093, 3001, 9100).