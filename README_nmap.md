# nmap inventory

## Requirements

Install nmap on the machine where you run Ansible. This might be from Ansible Tower, in which case you need to install it on all nodes.

Installing on RHEL/CentOS:

```shell
sudo yum install nmap
```

Installing on Mac OS:

```shell
brew install nmap
```

## Collection

As of Ansible 2.10, the inventory plugin is now located and managed within the [Ansible Community General Collection](https://github.com/ansible-collections/community.general). Even if you are using Ansible 2.9 you can use Ansible Collections already.

The specific plugin python file used is [here](https://github.com/ansible-collections/community.general/blob/main/plugins/inventory/nmap.py).

The supported parameters are documented [here](https://docs.ansible.com/ansible/latest/collections/community/general/nmap_inventory.html).

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

When using Ansible Tower and creating the Inventory with an Inventory Source, you should additionally set the following environment variable. This is not necessary if you already enabled the plugin within the `ansible.cfg` but it helps to produce a clean job output (less pink WARNING messages) for the Inventory Source sync as it will narrow the plugins attempted. Typically you will not need all of the plugins for a specific Inventory Source. So limit it using the environment variable as shown below.

```yaml
ANSIBLE_INVENTORY_ENABLED: community.general.nmap
```

## Parameters

The following parameters and example values are available for the `nmap` plugin. [Here](https://docs.ansible.com/ansible/latest/collections/community/general/nmap_inventory.html) is the comprehensive list of those parameters.

```yaml
# Inventory plugin type
plugin: community.general.nmap
# Invalid entries do not cause a fatal error and will be skipped
strict: False
# Network IP or range of IPs to scan, you can use a simple range 10.2.2.15-25 or CIDR notation.
address: 192.168.1.0/24
# List of addresses to exclude
exclude:
    - '192.168.1.0'
# Enable/disable scanning for open ports; poor performance when scanning all ports
ports: False

# At least one of ipv4 or ipv6 is required to be True, both can be True, but they cannot both be False.
# Use IPv4 type addresses
ipv4: True
# Use IPv6 type addresses
ipv6: False

# Create vars from jinja2 expressions. (dictionary)
compose:
    open_ports_exist: "{{ ports | count }}"
# Add hosts to group based on Jinja2 conditionals (dictionary)
groups:
    'ports_open': "{{ ports is defined }}"
# Add hosts to group based on the values of a variable. (list)
keyed_groups:
- key: ports | default("none")
  parent_group: ports
  prefix: port
```