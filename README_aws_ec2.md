# AWS EC2 Inventory

## References

[ansible-collections/amazon.aws - aws_ec2.py](https://github.com/ansible-collections/amazon.aws/blob/main/plugins/inventory/aws_ec2.py)

[aws_ec2 – AWS EC2 Inventory Plugin](https://docs.ansible.com/ansible/latest/plugins/inventory/aws_ec2.html)

## Overview

The following instructions focus on the AWS EC2 inventory plugin (not inventory script!).

For AWS, see [these instructions](https://docs.microsoft.com/en-us/azure/ansible/ansible-manage-azure-dynamic-inventories).

For details on configuring the inventory plugin `azure_rm.yml`, see this [page](https://docs.ansible.com/ansible/latest/plugins/inventory/azure_rm.html). 

AWS requires [the following documented URLs](https://docs.microsoft.com/en-us/azure/azure-portal/azure-portal-safelist-urls?tabs=public-cloud) added to safe-list when behind a proxy.

For local AWS testing you can create a credentials file:

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

To test the dynamic inventory plugin from command line:

```bash
# Install dependencies for AWS into virtual environment
pip install boto3 botocore

# set proxy settings if necessary to reach azure endpoints
#source ~/proxy.sh
#export https_proxy="https://proxy.example.com:8080"
#export http_proxy="http://proxy.example.com:8080"

# Set environment variables (if you do not have this information in the config file)
export AWS_ACCESS_KEY=123
export AWS_SECRET_KEY=xyz

# show VMs using graph
ansible-inventory -i hosts/aws/aws_ec2.yml --graph
# show VMs using simple list
ansible-inventory -i hosts/aws/aws_ec2.yml --list
```
