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

## Boto3 SSL Certificate Verify Failed

If you receive a certificate validation error when attempting to access the AWS inventory plugin, then the currently known workaround is to set the following environment variable. `boto3` looks for the `AWS_CA_BUNDLE` environment variable to tell it where to find the certificates. If it's not set, then it may cause this error:

```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

You will need to set the following environment variable before calling the dynamic inventory:

```shell
export AWS_CA_BUNDLE=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
```

So from Ansible CLI, use the following commands:

```shell
# Ensure Amazon certificate exist
grep "Amazon" /etc/pki/ca-trust/extracted/pem/*

# Set environment variable to point to certificate file containing Amazon certs
export AWS_CA_BUNDLE=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem

# Enable dynamic inventory plugin
export ANSIBLE_INVENTORY_ENABLED=amazon.aws.aws_ec2

# Test Ansible dynamic inventory plugin
ansible-inventory -i hosts/aws/aws_ec2.yml --list
```

Once this works, checkin the code and test from Ansible Tower.

To enable the environment variable in Ansible Tower go to `Settings -> Jobs` and add the environemnt variable in the text box in JSON format. This will enable it for all jobs executed in the Tower application.

```json
{
  "AWS_CA_BUNDLE": "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem"
}
```
