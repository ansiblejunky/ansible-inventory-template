# Ansible Inventory

TODO: Mention that it's recommended to leverage the UUID when pulling hosts into Ansible to ensure unique records.

TODO: Test using `auto` inventory plugin as described here:

Customers are continually moving to the cloud and yet still using their existing on-premise platform. This brings the interesting challenge of managing the inventories from different sources. Ansible brings a lot of power to not only manage your dynamic inventories but also allows a central place to manage your configuration (variables/facts) on each platform, environment, application stack, etc. In fact it can all be managed nicely within one repo. This can help emphasize your standards as well as expose some of your unicorn environments or applications.

This repo holds example inventory structures for both static and dynamic inventories across multi-platforms and multi-sources.

The `hosts` folder contains a structure that can be used as a model for building your own inventory and configuration management repo.

The `README_xxxx.md` files exist at the root level with detailed explanations on using each inventory plugin that Ansible supports.

There are 2 main goals for this repository:

- Act as config management database (CMDB) where Ansible variables can be defined for various platforms, devices, environments, and so on. These can then easily be used by any Playbooks and Roles.
- Act as inventory management and source of truth

## Inventory Structure

In this repo the `hosts` folder structure has been designed to allow support of a hybrid environment where we have multiple platforms and multiple sources of truth for various devices and device types.  There are many ways to structure this information, but this is just one possible way to consider.

## Enabling Inventory Plugins

By default Ansible has a set of inventory plugins that it uses to detect and understand your inventory files. It performs these in the order you specify. You can find the default set of inventory plugins from the documentation [INVENTORY_ENABLED](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#inventory-enabled). Below is an example of the default setting in `ansible.cfg`:

`ansible.cfg`
```yaml
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
```

Essentially Ansible will read the inventory file or folder you provided and use `host_list` plugin first to determine if this plugin understands the file(s) you provided. If it does, great, and Ansible stops there. If it returns failure, then Ansible moves on to the next plugin in the defined list `script` which attempts to just call a python script and get a returned JSON structure. This process continues until hopefully one of the plugins works. If none of them work, it results in a warning and Ansible cannot read the inventory. If it succeeds, then it loads that inventory file or structure.

So when we want to use an inventory plugin that is not yet listed in this setting we can simply add the name to the end of the list - or we can shorten the list and remove plugin names we will never use (making Ansible run a little faster and eliminating any unnecessary warnings as it traverses and attempts to use each plugin listed in the order).

## Plugins vs Scripts

Note that an inventory **script** is different than an inventory **plugin**! As of Ansible 2.8 the concept of an `inventory plugin` was introduced and is recommended over the old style `inventory script`.  Inventory plugins simply require the creation of a YAML file that defines the plugin name and associated parameters to configure it.

Location of inventory plugins on Ansible Tower server:
`/var/lib/awx/venv/awx/lib/python2.7/site-packages/awx/plugins/inventory`

[Plugin List](https://docs.ansible.com/ansible/latest/plugins/inventory.html#plugin-list)

## Group Variables

Ansible starts loading variables at the defined starting point which is set by telling Ansible the location of your inventory file(s). For example, running the command `ansible-playbook -i hosts/aws/ playbook.yml` will result in Ansible looking into the `hosts/aws/` folder for something that looks like an inventory file/script/plugin/etc.

Ansible always starts with an inventory.

Ansible supports loading group variables from a file named `mygroup.yml` or it can load any files that exist within a folder with the same group name `mygroup`.

## Symbolic Links

It's useful to understand variable precidence and the fact that Ansible loads group/host variable files in the ascii-betical order based on filename. For more information read [here](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable).

Using the above information allows us to additionally use symbolic links within our repository to access shared variables. These are variables/facts that apply across multiple platforms or environments but we want to maintain only 1 variable file (not duplicated for each environment).

To create the symbolic link:

```
touch hosts/000_shared_vars.yml
ln -s hosts/000_shared_vars.yml hosts/aws/group_vars/all/
```

For examples use the following article: [How to Manage Multistage Environments with Ansible](https://www.digitalocean.com/community/tutorials/how-to-manage-multistage-environments-with-ansible).

## Collections

This repository uses `collections/requirements.yml` to define the dependent Ansible collections that are needed for the inventory plugins. Ansible Tower comes with some inventory plugins but this is only specific versions at the time of the release of Ansible Tower. If you want to use the latest code, reference and use the specific Ansible Collection that holds the inventory plugin of your choice.

## Dependencies

To install special requirements/dependencies for these inventory plugins it is recommended to create a custom `python virtual environment` on the Ansible Control Node or Ansible Tower nodes. Reference the inventory plugin for specific dependencies.

## Cache Plugins (optional)

Additionally consider using `cache plugins`. The default behavior for Ansible playbooks is to store facts in memory during the run of the playbook. However, you can store/cache facts using various mechanisms. Enable the proper plugin as you wish. 

[Cache Plugins](https://docs.ansible.com/ansible/latest/plugins/cache.html)

## Playbooks

### playbook_tower_virtualenv.yml

Prepare and manage your Ansible Tower python virtual environment using this playbook. Add dependencies to it as needed for your inventory plugins or scripts.

### playbook_inventory_count.yml

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

TODO: The problem with doing it this way is that the proxy settings are globally set. This means it applies for any job templates.

## Debugging

When Ansible Tower synchronizes an Inventory Source, it actually runs a job. The job creates a temporary folder where it calls the `ansible-inventory` command to use the inventory plugin/script, get returned data, and import this data into Ansible Tower. If this fails for some reason and it's difficult to understand the root cause, then it may be easiest to simply run the same command from the terminal in the same folder Ansible Tower uses. However we need to tell Ansible Tower to stop cleaning up these temporary folders.

Disable Ansible Tower to remove temporary folders for manual analysis after the jobs has failed. The temporary directory `/tmp/awx_JOBID_xxxxx` that is created during job run are automatically removed after the job completion. By setting `AWX_CLEANUP_PATHS=False` we can force that temporary runtime directory to persist after the job run for if further analysis/debug is required.

https://access.redhat.com/solutions/5688351

## Writing Inventory Plugins

[Write your own Red Hat Ansible Tower inventory plugin](https://developers.redhat.com/blog/2021/03/10/write-your-own-red-hat-ansible-tower-inventory-plugin#a_sample_inventory_script)

[Developing dynamic inventory](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#developing-an-inventory-plugin)


## Author and Licensing

John Wadleigh

[GNU General Public License v3.0](LICENSE)

## References

[Ansible Tower - Inventories](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)

[Github - awx/main/models/inventory.py](https://github.com/ansible/awx/blob/devel/awx/main/models/inventory.py)

[Ansible - Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
[Ansible - Developer Guide - Developing dynamic inventory](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)

[Alan Coding - Examples and counter-examples of Ansible inventory files](https://github.com/AlanCoding/Ansible-inventory-file-examples)

[Mapping modules to collections](https://github.com/ansible/ansible/blob/devel/lib/ansible/config/ansible_builtin_runtime.yml)

[Digital Ocean - How to Manage Multistage Environments with Ansible](https://www.digitalocean.com/community/tutorials/how-to-manage-multistage-environments-with-ansible)