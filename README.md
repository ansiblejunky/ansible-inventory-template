# Ansible Inventory Template

The challenge of managing multiple inventory sources spread across on-premise and cloud platfoms is becoming costly and challenging. Ansible brings a lot of power to manage these inventories by offering a single source of truth to manage your entire configuration (variables/facts) on each platform, environment, application stack, etc. In fact we can manage it all nicely within one git repository. Having this structure in place can help emphasize your standards as well as expose some of your unicorn environments or applications.

There are 2 main goals for this repository:

- Act as a config management database (CMDB)
- Establish a single source of truth for infrastructure, pulling from multiple sources across multiple onprem and cloud platforms

This repository has the following structure:

- [hosts](./hosts/) folder contains an example structure that can be used as a model for building your own inventory and configuration management repo.
- [playbooks](./playbooks/) to perform various checks on the inventory
- `README_xxxx.md` files provide details of using specific inventory plugins

TODO: Mention that it's recommended to leverage the UUID when pulling hosts into Ansible to ensure unique records.
TODO: Test using `auto` inventory plugin as described here:
TODO: Rewrite this article into this repo using animated GIFs etc!
- [Digital Ocean - How to Manage Multistage Environments with Ansible](https://www.digitalocean.com/community/tutorials/how-to-manage-multistage-environments-with-ansible)
TODO: Add information to setup on AAP using Project, Credential(s), Credential Type(s), Inventory, Inventory Source(s)
TODO: Use execution environment and ansible-navigator instead and possibly remove the `galaxy` folder? except maybe for an ansible role?

## Inventory

In this repo the `hosts` folder structure has been designed to allow support of a hybrid environment where we have multiple platforms and multiple sources of truth for various devices and device types.  There are many ways to structure this information, but this is just one possible way to consider.

> Group Variables

Ansible starts loading variables at the defined starting point which is set by telling Ansible the location of your inventory file(s). For example, running the command `ansible-playbook -i hosts/aws/ playbook.yml` will result in Ansible looking into the `hosts/aws/` folder for something that looks like an inventory file/script/plugin/etc.

Ansible always starts with an inventory.

Ansible supports loading group variables from a file named `mygroup.yml` or it can load any files that exist within a folder with the same group name `mygroup`.

> Symbolic Links

It's useful to understand variable precidence and the fact that Ansible loads group/host variable files in the ascii-betical order based on filename. For more information read [here](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable).

Using the above information allows us to additionally use symbolic links within our repository to access shared variables. These are variables/facts that apply across multiple platforms or environments but we want to maintain only 1 variable file (not duplicated for each environment).

To create the symbolic link:

```
touch hosts/000_shared_vars.yml
ln -s hosts/000_shared_vars.yml hosts/aws/group_vars/all/
```

For examples use the following article: [How to Manage Multistage Environments with Ansible](https://www.digitalocean.com/community/tutorials/how-to-manage-multistage-environments-with-ansible).

> Plugins

By default Ansible has a set of `inventory plugins` that it uses to detect and understand your inventory files. It performs these in the order you specify. You can find the default set of inventory plugins from the documentation [INVENTORY_ENABLED](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#inventory-enabled). Below is an example of the default setting in `ansible.cfg`:

`ansible.cfg`
```yaml
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
```

Essentially Ansible will read the inventory file or folder you provided and use `host_list` plugin first to determine if this plugin understands the file(s) you provided. If it does, great, and Ansible stops there. If it returns failure, then Ansible moves on to the next plugin in the defined list `script` which attempts to just call a python script and get a returned JSON structure. This process continues until hopefully one of the plugins works. If none of them work, it results in a warning and Ansible cannot read the inventory. If it succeeds, then it loads that inventory file or structure.

So when we want to use an inventory plugin that is not yet listed in this setting we can simply add the name to the end of the list - or we can shorten the list and remove plugin names we will never use (making Ansible run a little faster and eliminating any unnecessary warnings as it traverses and attempts to use each plugin listed in the order).

Note that an inventory **script** is different than an inventory **plugin**! As of Ansible 2.8 the concept of an `inventory plugin` was introduced and is recommended over the old style `inventory script`.  Inventory plugins simply require the creation of a YAML file that defines the plugin name and associated parameters to configure it. Below are some additional references to develop your own inventory plugin.

- [Write your own Red Hat Ansible Tower inventory plugin](https://developers.redhat.com/blog/2021/03/10/write-your-own-red-hat-ansible-tower-inventory-plugin#a_sample_inventory_script)
- [Developing dynamic inventory](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#developing-an-inventory-plugin)

## Collections

Many inventory plugins are managed now within an Ansible Collection. For example, the AWS EC2 Inventory Plugin, or VMware Inventory Plugin. As a result, we need to declare these dependencies and download the necessary collections.

To do this, there are two methods available:

- Using a [requirements.yml](./galaxy/requirements.yml) to define the required Ansible Collections and running the `ansible-galaxy` command to download them. The only gotcha here is that each Ansible Collection has additional Python library requirements which you'll also have to consider and add to your local Python virtual environment.
- Building an Ansible Execution Environment (container image) with all the dependencies we need.

Note that, even though Ansible comes with some inventory plugins but this is only specific versions at the time of the release of Ansible Tower. If you want to use the latest code, reference and use the specific Ansible Collection that holds the inventory plugin of your choice.

## Cache Plugins (optional)

Additionally consider using [Cache Plugins](https://docs.ansible.com/ansible/latest/plugins/cache.html). The default behavior for Ansible playbooks is to store facts in memory during the run of the playbook. However, you can store/cache facts using various mechanisms. Enable the proper plugin as you wish.

## Proxy (optional)

To have Ansible access the public endpoints (such as with Azure), you may need to get past a Proxy layer. To do so, leverage the `environment` keyword at the Play, Block or Task level as described [here](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_environment.html).

## Author

John Wadleigh

## License

[GNU General Public License v3.0](LICENSE)

## References

- [Ansible Tower - Inventories](https://docs.ansible.com/ansible-tower/latest/html/userguide/inventories.html)
- [Github - awx/main/models/inventory.py](https://github.com/ansible/awx/blob/devel/awx/main/models/inventory.py)
- [Ansible - Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible - Developer Guide - Developing dynamic inventory](https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html)
- [Examples and counter-examples of Ansible inventory files - by Alan Coding](https://github.com/AlanCoding/Ansible-inventory-file-examples)
- [Mapping modules to collections](https://github.com/ansible/ansible/blob/devel/lib/ansible/config/ansible_builtin_runtime.yml)
