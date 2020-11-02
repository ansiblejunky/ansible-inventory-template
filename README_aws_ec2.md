# AWS EC2 Inventory

## References

Ansible Collections - AWS EC2 Inventory Plugin:
[ansible-collections/amazon.aws - aws_ec2.py](https://github.com/ansible-collections/amazon.aws/blob/main/plugins/inventory/aws_ec2.py)

For details on configuring the inventory plugin:
[aws_ec2 – AWS EC2 Inventory Plugin](https://docs.ansible.com/ansible/latest/plugins/inventory/aws_ec2.html)

## IAM Profile

<TODO: Add information on using IAM profile instead of access-key and secret-key>

## Overview

The following instructions focus on the AWS EC2 inventory plugin (not inventory script!).

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
