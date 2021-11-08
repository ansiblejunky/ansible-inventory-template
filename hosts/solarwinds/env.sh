#!/bin/bash

export JH1_SSH_IP=jh1.example.com
export JH1_SSH_PORT=22
export JH1_SSH_USER=vagrant
export JH1_SSH_PRIVATE_KEY=./key-jh3
export JH2_SSH_IP=jh2.example.com
export JH2_SSH_PORT=22
export JH2_SSH_USER=vagrant
export JH2_SSH_PRIVATE_KEY=./key-jh3
export JH3_SSH_IP=jh3.example.com
export JH3_SSH_PORT=22
export JH3_SSH_USER=vagrant
export JH3_SSH_PRIVATE_KEY=./key-jh3

# SWSQL query to send to SolarWinds via REST API
export SW_QUERY="SELECT CP.Asset_Group, SysName, DNS, IP, NodeID, MachineType, CP.AppOwner, CP.Responsible_Teams, CP.Environment, CP.APP_Group, CP.APP_Group1, CP.APP_Group2, CP.APP_Group3, CP.Asset_Category, CP.Loc1_SiteCode, CP.Loc2_Region, CP.Loc3_Country FROM Orion.Nodes as N JOIN Orion.NodesCustomProperties as CP on N.NodeID = CP.NodeID WHERE CP.Asset_Group != '' AND N.SysName != '' AND N.DNS != '' AND N.MachineType != '' AND CP.AppOwner != '' AND CP.Responsible_Teams != '' AND CP.APP_Group != ''"
# Field in query results to use for hostname
# e.g. "DNS"
export SW_HOSTNAME_FIELD="DNS"
# Field in query results that will be used to match against categories
# e.g. "MachineType"
export SW_CATEGORY_FIELD="MachineType"
# comma-separated list of fields from query results to create and add hosts to as groups - these should NOT be NULL, ensure via payload query
# e.g. SW_GROUP_ON_FIELDS="Asset_Group,MachineType"
export SW_GROUP_ON_FIELDS="MachineType"
# comma-separated list of fields from query results to map to host variables - these should match columns defined in the payload query 
# e.g. SW_HOSTVAR_FIELDS="Asset_Group,SysName,DNS,IP,NodeID,MachineType,AppOwner,Responsible_Teams,Environment,APP_Group,APP_Group3,APP_Group2,APP_Group3,Asset_Category,Loc1_SiteCode,Loc2_Region,Loc3_Country"
export SW_HOSTVAR_FIELDS="SysName,DNS,MachineType"
# List of categories and strings used to match against 'category_field'. Any fields not matched will be placed in a category defined with no matching strings
# In order to facilitate converting this environment variable into a Python data structure, it should be entered as follows:
#
# Category1:Comma,Separated,Strings; Category2:Unique,Matches; Category3:More; Other:
#
# In this case there will be 4 total Categories as follows:
# Category1 - Any hosts with category_field matching one of the strings 'Comma', 'Separated', or 'Strings' will be placed here
# Category2 - Any hosts with category_field matching one of the strings 'Unique', or 'Matches' will be placed here
# Category3 - Any hosts with category_field matching 'More' will be placed here
# Other - Any hosts not matching one of the previously defined 3 categories will default into this category - this should NOT contain any strings to match
#
# e.g. SW_CATEGORIES="Windows:Windows;Linux:Linux,Red Hat,Debian;Network:Cisco,Catalyst;Other:"
export SW_CATEGORIES="Windows:Windows;Linux:Linux,Red Hat,Debian;Network:Cisco,Catalyst;Other:"