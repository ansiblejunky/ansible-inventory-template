# Azure Inventory

## References

[ansible-collections/azure - azure_rm.py](https://github.com/ansible-collections/azure/blob/dev/plugins/inventory/azure_rm.py)

[azure_rm – Azure Resource Manager inventory plugin](https://docs.ansible.com/ansible/latest/plugins/inventory/azure_rm.html)

## Overview

The following instructions focus on Azure inventory plugin (not inventory script!).

For Azure, see [these instructions](https://docs.microsoft.com/en-us/azure/ansible/ansible-manage-azure-dynamic-inventories).

For details on configuring the inventory plugin `azure_rm.yml`, see this [page](https://docs.ansible.com/ansible/latest/plugins/inventory/azure_rm.html). 

Azure requires [the following documented URLs](https://docs.microsoft.com/en-us/azure/azure-portal/azure-portal-safelist-urls?tabs=public-cloud) added to safe-list when behind a proxy.

For local Azure testing you can create a credentials file:

```bash
mkdir ~/.azure
vi ~/.azure/credentials
```

Example `credentials` file for Azure Dev:
```
[default]
subscription_id=subscription123-45b4-a138-5934bcdbf572
client_id=client123-f4aa-4aba-98f3-80c2b01a9fe0
tenant=tenant123-c094-41d7-ab3d-43201da24438
secret=secret123-DsoZpA4YyR?-LQ2qy7n02V]w
```

To test the Azure dynamic inventory plugin, use the following commands.

```bash
cd ~/repos/ansible-playbooks

# set proxy settings if necessary to reach azure endpoints
source ~/proxy.sh
#export https_proxy="https://proxy.example.com:8080"
#export http_proxy="http://proxy.example.com:8080"

# show VMs using graph
ansible-inventory -i hosts/azure/azure_rm.yml --graph
# show VMs using simple list
ansible-inventory -i hosts/azure/azure_rm.yml --list
```

Good examples of configuration for Azure:
https://github.com/ansible/awx/blob/devel/awx/main/tests/data/inventory/plugins/azure_rm/files/azure_rm.yml
https://github.com/ansible/awx/blob/devel/awx/main/tests/data/inventory/plugins/gce/files/gcp_compute.yml
https://github.com/ansible/awx/blob/devel/awx/main/tests/data/inventory/plugins/ec2/files/aws_ec2.yml
