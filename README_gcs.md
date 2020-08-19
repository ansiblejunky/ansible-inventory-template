# Google Cloud Platform Inventory

Get inventory hosts from Google Cloud Platform GCE (Google Cloud Compute Engine)

Uses a YAML configuration file that ends with gcp_compute.(yml|yaml) or gcp.(yml|yaml)

## Requirements

The below requirements are needed on the local master node that executes this inventory.

requests >= 2.18.4
google-auth >= 1.3.0

## Example Plugin Configuration

An example of the plugin yaml configuration file can be found in this repo:
[example](hosts/google/gcp.yml)

Another example is shown below.

```yaml
plugin: gcp_compute
zones: # populate inventory with instances in these regions
  - us-east1-a
projects:
  - gcp-prod-gke-100
  - gcp-cicd-101
filters:
  - machineType = n1-standard-1
  - scheduling.automaticRestart = true AND machineType = n1-standard-1
service_account_file: /tmp/service_account.json
auth_kind: serviceaccount
scopes:
 - 'https://www.googleapis.com/auth/cloud-platform'
 - 'https://www.googleapis.com/auth/compute.readonly'
keyed_groups:
  # Create groups from GCE labels
  - prefix: gcp
    key: labels
hostnames:
  # List host by name instead of the default public ip
  - name
compose:
  # Set an inventory parameter to use the Public IP address to connect to the host
  # For Private ip use "networkInterfaces[0].networkIP"
  ansible_host: networkInterfaces[0].accessConfigs[0].natIP
```

## Resources

[Ansible Collection - Inventory Plugin Source Code](https://github.com/ansible-collections/google.cloud/blob/master/plugins/inventory/gcp_compute.py)

[gcp_compute inventory plugin parameters](https://docs.ansible.com/ansible/latest/plugins/inventory/gcp_compute.html)