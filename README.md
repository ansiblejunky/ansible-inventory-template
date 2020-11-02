# Ansible Inventory

Customers are continually moving to the cloud and yet still using their existing on-premise platform. This brings the interesting challenge of managing the inventories from different sources. Ansible brings a lot of power to not only manage your dynamic inventories but also allows a central place to manage your configuration (variables/facts) on each platform, environment, application stack, etc. In fact it can all be managed nicely within one repo. This can help emphasize your standards as well as expose some of your unicorn environments or applications.

This repo holds example inventory structures for both static and dynamic inventories across multi-platforms and multi-sources.

The `hosts` folder contains a structure that can be used as a model for building your own inventory and configuration management repo.

The `README_xxxx.md` files exist at the root level with detailed explanations on using each inventory plugin that Ansible supports.

There are 2 main goals for this repository:

- Act as config management database (CMDB) where Ansible variables can be defined for various platforms, devices, environments, etc which are then used by the triggered Playbooks and Roles
- Act as inventory configuration

## Inventory Structure

In this repo the `hosts` folder structure has been designed to allow support of a hybrid environment where we have multiple platforms and multiple sources of truth for various devices and device types.  It is important to understood before building your own inventory structure.

### Central Config Management (CMDB)


### Starting Point

Ansible starts loading variables at the defined starting point which is set by telling Ansible the location of your inventory file(s).

### Group Vars - Files or Folders

Ansible always starts with an inventory.

Ansible supports loading group variables from a file named `mygroup.yml` or it can load any files that exist within a folder with the same group name `mygroup`. 

### Symbolic Links

Variable precidence and ascii-betical order.
https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable

```
ln -s hosts/000_shared_vars.yml hosts/aws/group_vars/all/
```

## Plugins vs Scripts

Note that an inventory **script** is different than an inventory **plugin**! As of Ansible 2.8 the concept of an `inventory plugin` was introduced and is recommended over the old style `inventory script`.  Inventory plugins simply require the creation of a YAML file that defines the plugin name and associated parameters to configure it.

Location of inventory plugins on Ansible Tower server:
`/var/lib/awx/venv/awx/lib/python2.7/site-packages/awx/plugins/inventory`

## Inventory Plugins

[Plugin List](https://docs.ansible.com/ansible/latest/plugins/inventory.html#plugin-list)

## Cache Plugins (optional)

[Cache Plugins](https://docs.ansible.com/ansible/latest/plugins/cache.html)

## Collections

https://github.com/ansible/ansible/blob/devel/lib/ansible/config/ansible_builtin_runtime.yml

## Python Virtual Environment

To install special requirements for these inventory plugins it is recommended to create a custom python virtual environment on the Ansible Control Node or Ansible Tower nodes.

## Node Count

To get a count of all returned target nodes, use the following commands. This can help you determine the Ansible Tower license you need to purchase. Be sure to take into account some level of growth.

```shell
ansible-playbook -i <inventory> inventory_count.yml
```

## Proxy

To have Ansible Tower access the public endpoints (such as with Azure), you may need to get past a Proxy layer.

As per [these instructions](https://www.ansible.com/blog/getting-started-adding-proxy-support) we set the following environment vars in Tower -> Settings -> Jobs area.

```yaml
AWX_TASK_ENV['http_proxy']: "http://proxy.example.net:8098/"
AWX_TASK_ENV['https_proxy']: "http://proxy.example.net:8098/"
AWX_TASK_ENV['no_proxy']: "127.0.0.1,localhost"
```

## Author and Licensing

John Wadleigh

[GNU General Public License v3.0](LICENSE)

## References

[Ansible Tower - Inventories](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)

[Github - awx/main/models/inventory.py](https://github.com/ansible/awx/blob/devel/awx/main/models/inventory.py)

[Ansible - Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
[Ansible - Developer Guide - Developing dynamic inventory](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)

[Alan Coding - Examples and counter-examples of Ansible inventory files](https://github.com/AlanCoding/Ansible-inventory-file-examples)
