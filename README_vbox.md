# VirtualBox Inventory

https://docs.ansible.com/ansible/latest/plugins/inventory/virtualbox.html

## Requirements

VirtualBox must be installed on the localhost where you run the Ansible commands. In the case of Ansible Control Node, simply install it there. If you are configuring this on Ansible Tower you will need to install Virtualbox on each Tower node.

## Collection

As of Ansible 2.10, the inventory plugin is now located and managed within the [Ansible Community General Collection](https://github.com/ansible-collections/community.general). Even if you are using Ansible 2.9 you can use Ansible Collections already.

The specific plugin python file used is [here](https://github.com/ansible-collections/community.general/blob/main/plugins/inventory/virtualbox.py).

## Enabling

export ANSIBLE_INVENTORY_ENABLED=community.general.virtualbox
ansible-inventory -i hosts/virtualbox/vbox.yml --list