# vmware-inventory

Repo for testing the VMware dynamic inventory plugin for Ansible Core and Ansible Tower

To test the plugin run the command:

```shell
ansible-inventory -i vmware.yml --graph
```

The plugin was ripped from the Ansible Collections for VMware and then the defined plugin `name` inside the code was changed so that it can live and work inside a non-collection repo.


