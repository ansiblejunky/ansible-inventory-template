#!/usr/bin/env python

'''
Custom dynamic inventory script for Ansible and SolarWinds, in Python.
This was tested on:
    Orion Platform 2018.2 HF3
    ansible-2.9.17
    ansible-tower-server-3.8.1-1.el7.x86_64
    python version = 3.8.2 (default, Jul 24 2020, 15:24:42) [Clang 11.0.3 (clang-1103.0.32.62)]

(c) 2019 Vinny Valdez <vvaldez@redhat.com> and David Castellani <dcastell@redhat.com> and John Wadleigh <jwadleig@redhat.com>

Based on original work by Chris Babcock (chris@bluegreenit.com)
https://github.com/cbabs/solarwinds-ansible-inv

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

NOTE:  This software is free to use for any reason or purpose. That said, the
author request that improvements be submitted back to the repo or forked
to something public.

'''
import argparse
import requests
import re
import os
import configparser

# MULTIPLE JUMPHOST SUPPORT
# (optional) pip install --upgrade distribute
# pip install jumpssh
# https://github.com/AmadeusITGroup/JumpSSH
from jumpssh import SSHSession
from jumpssh import RestSshClient

try:
    import json
except ImportError:
    import simplejson as json

from urllib3 import disable_warnings, exceptions as urllib3exc
disable_warnings(category=urllib3exc.InsecureRequestWarning)

config_file = os.environ.get('SW_INI_FILE') or 'solarwinds.ini'

#Get configuration variables
config = configparser.ConfigParser()
config.read(config_file)
#config.readfp(open(config_file))

# Orion Server IP or DNS/hostname
server = os.environ.get('SW_SERVER') or config.get('solarwinds', 'sw_server')

# Orion Server Port (default 17778)
try:
    port = os.environ.get('SW_PORT') or config.get('solarwinds', 'sw_port')
except:
    port = "17778"

# Orion Username
user = os.environ.get('SW_USER') or config.get('solarwinds', 'sw_user')

# Orion Password
password = os.environ.get('SW_PASS') or config.get('solarwinds', 'sw_password')

# Field to use for hostname
hostname_field = os.environ.get('SW_HOSTNAME_FIELD') or 'DNS'

# Field that is used to group by category
# e.g. category_field = 'MachineType'
category_field = os.environ.get('SW_CATEGORY_FIELD') or 'MachineType'

# List of fields to map to host variables 
# These should match columns defined in the payload query. 
# Specified as a comma-separated string, will be converted into a list
# e.g. hostvar_fields = "DNS,IP,Asset_Group"
hostvar_fields = os.environ.get('SW_HOSTVAR_FIELDS') or False
if hostvar_fields:
    hostvar_fields = hostvar_fields.split(',')

# List of fields to to create and add hosts to as groups
# IF empty string or False, no additional groups will be created other than OS groups
# e.g. group_on_fields = "Asset_Group,MachineType"
group_on_fields = os.environ.get('SW_GROUP_ON_FIELDS') or False
if group_on_fields:
    group_on_fields = group_on_fields.split(',')

categories_definition = os.environ.get('SW_CATEGORIES') or "Windows:Windows;Linux:Linux,Red Hat,Debian;Network:Cisco,Catalyst;Other:"
categories = {}
if categories_definition:
    for category in categories_definition.split(';'):
        categories.update({category.split(':')[0]: category.split(':')[-1].split(',')})

# SWSQL query to send to SolarWinds via REST API
query = os.environ.get('SW_QUERY') or "SELECT SysName, DNS, IP, MachineType FROM Orion.Nodes"

url = "https://" + server + ":" + port + "/SolarWinds/InformationService/v3/Json/Query"

class SwInventory(object):

    def read_cli(self):
        """ Parse CLI arguments and call proper method"""
        parser = argparse.ArgumentParser()
        parser.add_argument('--host')
        parser.add_argument('--list', action='store_true')
        self.options = parser.parse_args()

    def __init__(self):
        """Run query against SolarWinds and build an Ansible-compatible JSON inventory"""

        # Initialize  inventory
        self.inventory = {'_meta': {'hostvars': {}}}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.query_results = self.get_hosts(query)
            self.inventory = self.add_hosts_to_inventory(self.inventory, self.query_results)
            if group_on_fields:
                if category_field in group_on_fields:
                    self.inventory = self.add_to_category_groups(self.inventory, self.query_results, 'children')
                    for group in group_on_fields:
                        self.inventory = self.add_hosts_to_group(self.inventory, self.query_results, group)
                else:
                    self.inventory = self.add_to_category_groups(self.inventory, self.query_results, 'hosts')
            else:
                self.inventory = self.add_to_category_groups(self.inventory, self.query_results, 'hosts')
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If args return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        # Print inventory for Ansible to consume
        print(json.dumps(self.inventory, indent=2))
        
    def get_hosts(self, query):
        """Execute SWSQL query against SolarWinds REST API and return results"""
        
        # MULTIPLE JUMPHOST SUPPORT - START
        jumphost1_ip = os.environ['JH1_SSH_IP']
        jumphost1_user = os.environ['JH1_SSH_USER']
        jumphost1_port = os.environ['JH1_SSH_PORT']
        jumphost1_privatekey = os.environ['JH1_SSH_PRIVATE_KEY']

        jumphost2_ip = os.environ['JH2_SSH_IP']
        jumphost2_user = os.environ['JH2_SSH_USER']
        jumphost2_port = os.environ['JH2_SSH_PORT']
        jumphost2_privatekey = os.environ['JH2_SSH_PRIVATE_KEY']

        jumphost3_ip = os.environ['JH3_SSH_IP']
        jumphost3_user = os.environ['JH3_SSH_USER']
        jumphost3_port = os.environ['JH3_SSH_PORT']
        jumphost3_privatekey = os.environ['JH3_SSH_PRIVATE_KEY']

        final_session = None
        if jumphost1_ip:
            jump1 = SSHSession(host=jumphost1_ip, port=jumphost1_port, username=jumphost1_user,
                private_key_file=jumphost1_privatekey).open()
            final_session = jump1
        if jumphost2_ip:
            jump2 = jump1.get_remote_session(host=jumphost2_ip, port=jumphost2_port, username=jumphost2_user, 
                private_key_file=jumphost2_privatekey)
            final_session = jump2
        if jumphost3_ip:
            jump3 = jump2.get_remote_session(host=jumphost3_ip, port=jumphost3_port, username=jumphost3_user, 
                private_key_file=jumphost3_privatekey)
            final_session = jump3
        if final_session:
            requests = RestSshClient(final_session, verify=False)
        # MULTIPLE JUMPHOST SUPPORT - END

        # requests library requires params passed as dictionary
        params = {"query": query}
        req = requests.get(url, params=params, verify=False, auth=(user, password))
        query_results = req.json()

        return query_results

    def add_hosts_to_inventory(self, inventory, query_results):
        """Iterate through results of query and create Ansible-compatible JSON dictionary with hosts 

        The defined 'hostname_field' is used to assign the variable 'ansible_host' to the host inventory
        If 'hostvar_fields' is defined, those fields will be mapped to host variables for each host
        """

        for host in query_results['results']:
            inventory['_meta']['hostvars'].update({host[hostname_field]: {"ansible_host": host[hostname_field] }})
            if hostvar_fields:
                for field in hostvar_fields:
                    inventory['_meta']['hostvars'][host[hostname_field]][field] = max(host[field],'')
        return inventory

    def add_hosts_to_group(self, inventory, query_results, group):
        """Iterate through results of query and create groups for hosts that contain a matching field for the sent variable 'group'

        e.g. all hosts with a field of 'MachineType' matching 'Red Hat' will be added to a group 'Red Hat'
        """

        for host in query_results['results']:
            if host[group] in inventory:
                if host[hostname_field] not in inventory[host[group]]['hosts']:
                    inventory[host[group]]['hosts'].append(host[hostname_field])
            else:
                inventory[host[group]] = {'hosts': [host[hostname_field]]}
                inventory[host[group]].update({'children': []})
                inventory[host[group]].update({'vars': {}})
        return inventory

    def add_to_category_groups(self, inventory, query_results, group_type):
        """Add either hosts or groups to category groups matching their 'category_field'"""

        def add_category_entry_to_inventory(category):
            """Add host to matching category by 'group_type'. Create category group if needed"""

            if category in inventory:
                if host[append_with] not in inventory[category][group_type]:
                    inventory[category][group_type].append(host[append_with])
            else:
                inventory[category] = {group_type: [host[append_with]]}
                inventory[category].update({initialize_key: []})
                inventory[category].update({'vars': {}})
            return

        def match_host_to_category(host):
            """Match host to category based on 'category_field'. Return on first match."""

            for category, matches in categories.items(): 
                if matches != ['']:
                    for match in matches:
                        if match in host[category_field]:
                            add_category_entry_to_inventory(category)
                            return
            else:
                add_category_entry_to_inventory(category_unmatched)

        if group_type == 'hosts':
            append_with = hostname_field
            initialize_key = 'children'
        elif group_type == 'children':
            append_with = category_field
            initialize_key = 'hosts'

        for category, matches in categories.items(): 
            if matches == ['']:
                category_unmatched = category
                break
        else:
            category_unmatched = 'Other'

        for host in query_results['results']:
            match_host_to_category(host)

        return inventory

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()

# Get the inventory.
SwInventory()