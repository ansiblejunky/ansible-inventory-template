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

Notice that on the Ansible documentation it states to enable the inventory plugin you need to use `nmap` string for the plugin name. However we want to use the plugin from the Collection. This plugin is named differently `community.general.nmap` and so we need to use that instead.

When using terminal commands, you have two options to enable the inventory.

Option 1 - Set the environment variable before you run the ansible commands.

```shell
# Set environment variable to activate inventory type
export ANSIBLE_INVENTORY_ENABLED=community.general.nmap
# Run any ansible commands - for example
ansible-inventory -i hosts/nmap/nmap.yml --list
```

Option 2 - Set the option in the `ansible.cfg` to explicitly enable the inventory plugin. You can remove the others if you do not need them, otherwise Ansible will attempt to read the inventory files in the order from left-to-right of the list of enabled plugins.

```ini
[inventory]
# enable inventory plugins, default: 'host_list', 'script', 'auto', 'yaml', 'ini', 'toml'
enable_plugins = 'host_list', 'script', 'auto', 'yaml', 'ini', 'toml', community.general.nmap
```

```
ANSIBLE_INVENTORY_ENABLED: community.general.nmap
```

## Collection

As of Ansible 2.10, the inventory plugin is now located and managed within the [Ansible Community General Collection](https://github.com/ansible-collections/community.general). Even if you are using Ansible 2.9 you can use Ansible Collections already.

The specific plugin python file used is [here](https://github.com/ansible-collections/community.general/blob/main/plugins/inventory/nmap.py).
