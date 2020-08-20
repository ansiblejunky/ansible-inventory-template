# nmap inventory

## Requirements

```
sudo yum install nmap
```

## Enabling

```
ANSIBLE_INVENTORY_ENABLED: nmap
```

## Collection

As of Ansible 2.10, the inventory plugin is now located and managed within the [Ansible Community General Collection](https://github.com/ansible-collections/community.general). Even if you are using Ansible 2.9 you can use Ansible Collections already.

The specific plugin python file used is [here](https://github.com/ansible-collections/community.general/blob/main/plugins/inventory/nmap.py).
