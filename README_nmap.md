# nmap inventory

## Requirements

Install nmap on the machine where you run Ansible.

Installing on RHEL/CentOS:

```shell
sudo yum install nmap
```

Installing on Mac OS:

```shell
brew install nmap
```

## Enabling

To use this inventory you must activate it since it's not one of the default inventory types that are loaded by Ansible.

When using terminal commands, you have two options.

Option 1 - Set the environment variable before you run the ansible commands.

```shell
# Set environment variable to activate inventory type
export ANSIBLE_INVENTORY_ENABLED=nmap
# Run any ansible commands - for example
ansible-inventory -i hosts/nmap/nmap.yml --list
```


```
ANSIBLE_INVENTORY_ENABLED: nmap
```

## Collection

As of Ansible 2.10, the inventory plugin is now located and managed within the [Ansible Community General Collection](https://github.com/ansible-collections/community.general). Even if you are using Ansible 2.9 you can use Ansible Collections already.

The specific plugin python file used is [here](https://github.com/ansible-collections/community.general/blob/main/plugins/inventory/nmap.py).
