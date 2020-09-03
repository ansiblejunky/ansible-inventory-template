# Hosts Examples

The following `tree` output explains the overall hosts folder structure.

```
├── 000_shared_vars.yml
├── 001_powerbroker_vars.yml
├── 001_windows_vars.yml
├── azure
│   ├── 100_azure_vars.yml
│   ├── dev
│   │   ├── azure_rm.yml
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   │   ├── 000_shared_vars.yml -> ../../../../000_shared_vars.yml
│   │   │   │   ├── 100_azure_vars.yml -> ../../../100_azure_vars.yml
│   │   │   │   └── dev.yml
│   │   │   ├── gemfire.yml
│   │   │   ├── ldap_jump_server.yml
│   │   │   ├── os_linux.yml
│   │   │   ├── os_windows.yml
│   │   └── inventory
│   ├── lab
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   │   ├── 000_shared_vars.yml -> ../../../../000_shared_vars.yml
│   │   │   │   ├── 100_azure_vars.yml -> ../../../100_azure_vars.yml
│   │   │   │   └── lab.yml
│   │   │   ├── os_linux.yml
│   │   │   └── os_windows.yml
│   │   └── inventory
│   ├── prod
│   │   ├── azure_rm.yml
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   │   ├── 000_shared_vars.yml -> ../../../../000_shared_vars.yml
│   │   │   │   ├── 100_azure_vars.yml -> ../../../100_azure_vars.yml
│   │   │   │   └── prod.yml
│   │   │   ├── gemfire.yml
│   │   │   ├── ldap_jump_server.yml
│   │   │   ├── os_linux.yml
│   │   │   └── os_windows.yml
│   │   └── inventory
│   └── test
│       ├── azure_rm.yml
│       ├── group_vars
│       │   ├── all
│       │   │   ├── 000_shared_vars.yml -> ../../../../000_shared_vars.yml
│       │   │   ├── 100_azure_vars.yml -> ../../../100_azure_vars.yml
│       │   │   └── test.yml
│       │   ├── gemfire.yml
│       │   ├── ldap_jump_server.yml
│       │   ├── os_linux.yml
│       │   └── os_windows.yml
│       └── inventory
├── vmware
│   ├── 100_vmware_vars.yml
│   ├── dev
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   │   ├── 000_shared_vars.yml -> ../../../../000_shared_vars.yml
│   │   │   │   ├── 100_vmware_vars.yml -> ../../../100_vmware_vars.yml
│   │   │   │   └── dev.yml
│   │   │   ├── mq_cluster.yml
│   │   │   ├── mq_standalone.yml
│   │   │   ├── powerbroker.yml -> ../../../001_powerbroker_vars.yml
│   │   │   └── os_windows
│   │   │       └── 001_windows_vars.yml -> ../../../../001_windows_vars.yml
│   │   └── inventory
│   ├── prod
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   │   ├── 000_shared_vars.yml -> ../../../../000_shared_vars.yml
│   │   │   │   ├── 100_vmware_vars.yml -> ../../../100_vmware_vars.yml
│   │   │   │   └── prod.yml
│   │   │   ├── ece_logstash.yml
│   │   │   ├── hpov_jump_server.yml
│   │   │   ├── linux.yml
│   │   │   ├── mq_cluster.yml
│   │   │   ├── mq_standalone.yml
│   │   │   ├── os_windows
│   │   │   │   └── 001_windows_vars.yml -> ../../../../001_windows_vars.yml
│   │   │   └── zena_servers.yml
│   │   └── inventory
│   └── test
│       ├── group_vars
│       │   ├── all
│       │   │   ├── 000_shared_vars.yml -> ../../../../000_shared_vars.yml
│       │   │   ├── 100_vmware_vars.yml -> ../../../100_vmware_vars.yml
│       │   │   └── test.yml
│       │   ├── ece_logstash.yml
│       │   ├── hpov_jump_server.yml
│       │   ├── mq_cluster.yml
│       │   ├── mq_standalone.yml
│       │   ├── os_windows
│       │   │   └── 001_windows_vars.yml -> ../../../../001_windows_vars.yml
│       │   └── zena_servers.yml
│       └── inventory
└── vagrant
    ├── group_vars
    │   ├── all
    │   │   ├── 000_shared_vars.yml -> ../../../000_shared_vars.yml
    │   │   └── all.yml
    │   ├── os_linux.yml
    │   └── os_windows.yml
    └── inventory
```
