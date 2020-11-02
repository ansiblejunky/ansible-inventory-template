# VMware Inventory

This document covers the configuration of the VMware dynamic inventory within Ansible Tower.

## References

[VMWare VM Inventory Plugin Host Filters #65571](https://github.com/ansible/ansible/issues/65571)

[VMWare script or plugin does not allow filtering inventory by tags. #64365](https://github.com/ansible/ansible/issues/64365)

[Quick Filters Available for vSphere Objects](https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.vcenterhost.doc/GUID-2B6A1637-384D-4597-B453-B575F0ECD8A7.html)

## Known Issues

Ansible Tower is only able to detect IP from one of the two interfaces in Vmware. It always fetches the first Interface IP address and hence the desired IP is not getting fetched.
[While Using Vmware Dynamic Inventory in Ansible Tower, How do I Select The Desired Interface IP for VMware Host Having Multiple Interfaces?](https://access.redhat.com/solutions/3701361)

## Overview

For VMware, see [these instructions](https://docs.ansible.com/ansible/latest/scenario_guides/vmware_scenarios/vmware_inventory.html).

Below are the 3 possible directions for configuring dynamic inventory for VMware. The recommendation is to use the Inventory Plugin (`vmware_vm_inventory.py`) within the Ansible VMware Collection since this is the latest version that supports filtering, tags, and filtering by tags, etc.

Quick Filters Available for vSphere Objects
https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.vsphere.vcenterhost.doc/GUID-2B6A1637-384D-4597-B453-B575F0ECD8A7.html

vmware_vm_inventory plugin docs/code for version included with Ansible Tower 3.6.x
https://docs.ansible.com/ansible/latest/plugins/inventory/vmware_vm_inventory.html
https://github.com/ansible/ansible/blob/v2.9.7/lib/ansible/plugins/inventory/vmware_vm_inventory.py

vmware_vm_inventory plugin latest from collections
https://github.com/ansible-collections/vmware/blob/master/plugins/inventory/vmware_vm_inventory.py

vmware_inventory script included with Ansible Tower 3.6.x
https://github.com/ansible/ansible/blob/v2.9.7/contrib/inventory/vmware_inventory.py
https://github.com/ansible/ansible/blob/v2.9.7/contrib/inventory/vmware_inventory.ini

Using Virtual machine attributes in VMware dynamic inventory plugin
https://github.com/ansible/ansible/blob/devel/docs/docsite/rst/scenario_guides/vmware_scenarios/vmware_inventory_vm_attributes.rst

VMware Managed Object Types
https://pubs.vmware.com/vi-sdk/visdk250/ReferenceGuide/index-mo_types.html

PyVmomi Community Samples
https://github.com/vmware/pyvmomi-community-samples/tree/master/samples

Red Hat internal vCenter information
https://mojo.redhat.com/docs/DOC-115645

## Misc

Repo for testing the VMware dynamic inventory plugin for Ansible Core and Ansible Tower

To test the plugin run the command:

```shell
ansible-inventory -i vmware.yml --graph
```

The plugin was ripped from the Ansible Collections for VMware and then the defined plugin `name` inside the code was changed so that it can live and work inside a non-collection repo.

## VMware vCenter (Ansible Tower)

Selecting the `VMware vCenter` option for the `Source` field on an Inventory Source object in Ansible Tower is actually going to call a version of the `Inventory Script` that comes with Ansible Tower. 

This inventory script can be found here:
`/var/lib/awx/venv/awx/lib/python3.6/site-packages/awx/plugins/inventory/vmware_inventory.py`
The file can also be found within the AWX source code repo here:
https://github.com/ansible/awx/blob/devel/awx/plugins/inventory/vmware_inventory.py

The script loads an INI file that contains the configuration settings such as `host_filters`. You can see all of the options here in the source code:
https://github.com/ansible/awx/blob/72de660ea1039039ffd7e7c72d72e5a44ffcbdf7/awx/plugins/inventory/vmware_inventory.py#L208-L235

Using Ansible Tower the INI file will be automatically generated for you. You can provide the options in the Inventory Source field `Source Variables` or using the `Instance Filters` and `Only Group By` fields. For all options, review the following INI example file: 
https://github.com/ansible-collections/vmware/blob/master/scripts/inventory/vmware_inventory.ini

To use the `VMware vCenter` source, you need to first create a Credential of type `VMware vCenter`.

### VMware Inventory Script

The second choice for configuring dynamic inventory for VMware is to pull the latest inventory script from the Ansible repo. This will be a newer version of the dynamic script file that was used by Ansible Tower.

Note that the inventory script is **only** available up to Ansible 2.9.x. Afterwards Ansible Tower is moving to inventory plugins.

To configure Ansible Tower with this inventory script:

- Custom credential type
- Credential (uses custom credential type)

Custom credential type:

name: "vmware-inventory-credential-type"
description: "Custom credential to inject environment vars for VMware dynamic inventory"

Inputs:

```yaml
fields:
  - id: username
    type: string
    label: Username
  - id: password
    type: string
    label: Password
    secret: true
  - id: hostname
    type: string
    label: Hostname
  - id: port
    type: string
    label: Port
required:
  - username
  - password
  - hostname
  - port
```

Injectors:

```yaml
env:
  VMWARE_PASSWORD: '{{ password }}'
  VMWARE_SERVER: '{{ hostname }}'
  VMWARE_USERNAME: '{{ username }}'
  VMWARE_PORT: '{{ port }}'
```

Credential:

```yaml
name: "vcenter-credential"
description: "VMware vCenter dynamic inventory credential"
credential_type: "vmware-inventory-credential-type"
inputs:
  username: 'username'
  password: 'passw0rd'
  hostname: 'vcenter.example.com'
```

Code Requirements:
- Python inventory script from [here](https://github.com/ansible/ansible/blob/v2.9.7/contrib/inventory/vmware_inventory.py)
- INI configuration file from [here](https://github.com/ansible/ansible/blob/v2.9.7/contrib/inventory/vmware_inventory.ini)

Place both of these files inside your `hosts/...` structure in your playbooks repo. They need to be side-by-side as the python script looks for the INI file in the same folder by default.

Example INI file settings:

```ini
# Ansible VMware external inventory script settings

[vmware]

# The resolvable hostname or ip address of the vsphere
server=vcenter.example.com

# The port for the vsphere API
#port=443

# The username with access to the vsphere API. This setting
# may also be defined via the VMWARE_USERNAME environment variable.
username=username

# The password for the vsphere API. This setting
# may also be defined via the VMWARE_PASSWORD environment variable.
password=passw0rd

# Verify the server's SSL certificate
validate_certs = False

# Specify the number of seconds to use the inventory cache before it is
# considered stale.  If not defined, defaults to 0 seconds.
#cache_max_age = 3600
cache_max_age = 0

# Specify the directory used for storing the inventory cache.  If not defined,
# caching will be disabled.
#cache_path = ~/.cache/ansible


# Max object level refers to the level of recursion the script will delve into
# the objects returned from pyvomi to find serializable facts. The default
# level of 0 is sufficient for most tasks and will be the most performant.
# Beware that the recursion can exceed python's limit (causing traceback),
# cause sluggish script performance and return huge blobs of facts.
# If you do not know what you are doing, leave this set to 1.
#max_object_level=1


# Lower the keynames for facts to make addressing them easier.
lower_var_keys=True


# Don't retrieve and process some VMware attribute keys
# Default values permit to sanitize inventory meta and to improve a little bit
# performance by removing non-common group attributes.
#skip_keys = declaredalarmstate,disabledmethod,dynamicproperty,dynamictype,environmentbrowser,managedby,parent,childtype,resourceconfig


# Host alias for objects in the inventory. VMware allows duplicate VM names
# so they can not be considered unique. Use this setting to alter the alias
# returned for the hosts. Any atributes for the guest can be used to build
# this alias. The default combines the config name and the config uuid and
# expects that the ansible_host will be set by the host_pattern.
#alias_pattern={{ config.name + '_' + config.uuid }}
alias_patter={{ guest.hostname }}

# Host pattern is the value set for ansible_host and ansible_ssh_host, which
# needs to be a hostname or ipaddress the ansible controlhost can reach.
#host_pattern={{ guest.ipaddress }}
host_pattern={{ guest.hostname }}

# Host filters are a comma separated list of jinja patterns to remove
# non-matching hosts from the final result.
# EXAMPLES:
#   host_filters={{ config.guestid == 'rhel7_64Guest' }}
#   host_filters={{ config.cpuhotremoveenabled != False }},{{ runtime.maxmemoryusage >= 512 }}
#   host_filters={{ config.cpuhotremoveenabled != False }},{{ runtime.maxmemoryusage >= 512 }}
#   host_filters={{ runtime.powerstate == "poweredOn" }}
#   host_filters={{ guest.gueststate == "notRunning" }}
# The default value is powerstate of virtual machine equal to "poweredOn". (Changed in version 2.5)
# Runtime state does not require to have vmware tools installed as compared to "guest.gueststate"
#host_filters={{ runtime.powerstate == "poweredOn" }}
host_filters={{ guest.hostname.startswith('pwaus') }},{{ runtime.powerstate == "poweredOn" }}


# Groupby patterns enable the user to create groups via any possible jinja
# expression. The resulting value will the groupname and the host will be added
# to that group. Be careful to not make expressions that simply return True/False
# because those values will become the literal group name. The patterns can be
# comma delimited to create as many groups as necessary
#groupby_patterns={{ guest.guestid }},{{ 'templates' if config.template else 'guests'}}
groupby_patterns={{ 'os_linux' if guest.guestfamily == 'linuxGuest' else 'os_windows' }}

# Group by custom fields will use VMware custom fields to generate hostgroups
# based on {{ custom_field_group_prefix }} + field_name + _ + field_value
# Set groupby_custom_field to True will enable this feature
# If custom field value is comma separated, multiple groups are created.
# Warning: This required max_object_level to be set to 2 or greater.
#groupby_custom_field = False

# You can customize prefix used by custom field hostgroups generation here.
# vmware_tag_ prefix is the default and consistent with ec2_tag_
#custom_field_group_prefix = vmware_tag_

# You can blacklist custom fields so that they are not included in the
# groupby_custom_field option. This is useful when you have custom fields that
# have values that are unique to individual hosts. Timestamps for example.
# The groupby_custom_field_excludes option should be a comma separated list of custom
# field keys to be blacklisted.
#groupby_custom_field_excludes=<custom_field_1>,<custom_field_2>,<custom_field_3>

# The script attempts to recurse into virtualmachine objects and serialize
# all available data. The serialization is comprehensive but slow. If the
# vcenter environment is large and the desired properties are known, create
# a 'properties' section in this config and make an arbitrary list of
# key=value settings where the value is a path to a specific property. If
# If this feature is enabled, be sure to fetch every property that is used
# in the jinja expressions defined above. For performance tuning, reduce
# the number of properties to the smallest amount possible and limit the
# use of properties that are not direct attributes of vim.VirtualMachine
#[properties]
#prop01=name
#prop02=config.cpuHotAddEnabled
#prop03=config.cpuHotRemoveEnabled
#prop04=config.instanceUuid
#prop05=config.hardware.numCPU
#prop06=config.template
#prop07=config.name
#prop08=guest.hostName
#prop09=guest.ipAddress
#prop10=guest.guestId
#prop11=guest.guestState
#prop12=runtime.maxMemoryUsage
# In order to populate `customValue` (virtual machine's custom attributes) inside hostvars,
# uncomment following property. Please see - https://github.com/ansible/ansible/issues/41395
#prop13=customValue
```

### VMware Inventory Plugin

https://docs.ansible.com/ansible/latest/scenario_guides/vmware_scenarios/vmware_inventory.html

Information about the available settings are listed [here](https://docs.ansible.com/ansible/latest/plugins/inventory/vmware_vm_inventory.html).

Starting with Ansible v2.10, the VMware modules are moved to the following collection:
- https://galaxy.ansible.com/community/vmware
- https://github.com/ansible-collections/vmware

Before Ansible v2.10, the inventory plugin was included with Ansible Engine:
- https://github.com/ansible/ansible/blob/v2.9.7/lib/ansible/plugins/inventory/vmware_vm_inventory.py

Note that the "VMware vCenter" credential in Ansible Tower only injects the username/password/hostname into an INI file for the inventory script. It does NOT inject these as environment variables. The inventory plugin needs environment variables to be properly set. Hence, we need to create a custom credential type inside Ansible Tower that accepts username/password/hostname and injects them as environment variables. Once you have this created, then set the inventory source to use this credential.

For questions or issues on the VMware inventory plugin, please reference [this Wiki](https://github.com/ansible/community/wiki/VMware). The plugin is created and supported by the community.

VMware requirements:

- Opening a firewall to the vCenter endpoint for port 80 and 443
- For basic functionality, you need `pyvmomi` python library: `pip install pyvmomi`
- To include tag-related information for the virtual machines in your dynamic inventory:
  - install the [vSphere Automation SDK](https://code.vmware.com/web/sdk/65/vsphere-automation-python), which supports REST API features like tagging and content libraries, on your control node. You can install the vSphere Automation SDK following [these instructions](https://github.com/vmware/vsphere-automation-sdk-python#installing-required-python-packages)
  - request proxy changes for the following URLs

Testing the plugin from command-line:

```shell
cd ~/repos/ansible-playbooks
ansible-inventory -i vmware.yml --graph > output_tags.json
ansible-inventory -i vmware.yml --list > output_tags.json
```

Contents of `vmware.yml`:

```yaml
---
plugin: vmware_vm_inventory
strict: False
hostname: 'vcenter.example.com'
username: 'username'
password: 'passw0rd'
validate_certs: False
with_tags: True
```

Environment Variable required for using plugin in Ansible Tower with 'Sourced from Project':

```yaml
ANSIBLE_INVENTORY_ENABLED: vmware_vm_inventory, ini, auto
```

- Customize the yml file by overriding the defaults (from example):
https://github.com/ansible/ansible/blob/devel/contrib/inventory/vmware_inventory.ini
- Install VMware SDK Python tools (required to do tagging, but check first without tagging)
pyVmomi is SOAP based API binding for Python whereas vSphere Automation SDK is REST based API interface. Latest features like tagging, content library etc. are supported via vSphere Automation SDK only. pyVmomi does not support these features so in order to support tagging feature in vmware_vm_inventory Ansible requires vSphere Automation SDK.
https://github.com/ansible/ansible/issues/57224#issuecomment-497953871


### VMware - Demo using Ansible Tower with VMware Inventory Script to vcsim

This was successful. It pulled data from vcsim into Tower.

Prepare Tower:

- Create Credential, with type "VMware vCenter"
  - Username = user
  - Password = pass
  - Host = logger.example.com
- Create Inventory
- Create Inventory Source
  - Source = "VMware vCenter"
  - Credential = <created above>
  - Environment Variables

    ```yaml
    ---
    VMWARE_SERVER: 192.168.33.30
    VMWARE_USERNAME: user
    VMWARE_PASSWORD: pass
    ```

Prepare ansible python virtual environment to test VMware plugin:

```shell
# Prepare python virtual environment using PyEnv
pyenv install --skip-existing 3.8.2
pyenv local 3.8.2
pyenv virtualenv ansible-vcenter
pyenv activate ansible-vcenter

pip install --upgrade pip
pip install ansible
pip install pyvmomi
pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git
```

### VMware vcsim - A vCenter and ESXi API based simulator

https://github.com/vmware/govmomi/tree/master/vcsim

Prepare vcsim:

- Start vagrant box
- Inside the box do the following

  ```shell
  sudo su -
  yum install git
  wget https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz
  tar -C /usr/local -xzf ~/go1.14.2.linux-amd64.tar.gz
  mkdir -p $HOME/go
  echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc
  echo 'export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin' >> $HOME/.bashrc
  source ~/.bashrc
  go env GOPATH
  go get github.com/vmware/govmomi/vcsim
  # Need to use root/sudo to use port 443
  vcsim -l 192.168.33.30:443
  ```

Instructions on setting up simulator:
https://opensourceforu.com/2017/10/vcenter-server-simulation-govcsim/

Containerized simulator:
https://github.com/ansible/vcenter-test-container

Quay container image for simulator with Flask:
https://quay.io/repository/ansible/vcenter-test-container

### Support

For any issues related to the VMware Ansible modules, please create a Github issue against the correct repo. This might be the [ansible repo](https://github.com/ansible/ansible) or the newer [VMware collection repo](https://github.com/ansible-collections/vmware).

From Red Hat, we have the following people who contribute and fix issues for the VMware modules:

- [Abhijeet Kasurde](http://akasurde.github.io/)
- [Gonéri Le Bouder](https://github.com/goneri)

These are the [contributors](https://github.com/ansible-collections/vmware/graphs/contributors) for the VMware collection repo.

### VMware pyvmomi community samples - filtering

The following repo has samples:
https://github.com/vmware/pyvmomi-community-samples

Prepare the sample python code to filter.

```shell
wget https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/filter_vms.py
wget https://raw.githubusercontent.com/vmware/pyvmomi-community-samples/master/samples/tools/cli.py
<edit filter_vms.py and change the import of `cli` to `import cli` so it loads local version>
# run the filter script
python filter_vms.py -s vmware.example.com -o 443 -u admin@vsphere.local -p password -n config.name -v romesh
```