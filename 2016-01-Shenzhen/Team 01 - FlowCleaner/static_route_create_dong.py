#!/usr/bin/env python2.7

# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
Demonstrate how to configure the next-hop of a 'static route'.

Introduce function 'static_route_create'.
Print the function's documentation.

Use any one network device that is capable.
Use any one network interface on the data plane.
Use any one destination, such as 2.2.2.2, 3.3.3.3, etc.
Exclude destinations for which a static route exists.
Create a static route on the network device to the destination
network via the next-hop of the device's exit interface.
"""

from __future__ import print_function
from future.builtins import next
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from inspect import cleandoc
from basics.inventory import inventory_mounted, device_control
from basics.interface import interface_names, interface_configuration_tuple
from basics.render import print_table
from basics.routes import static_route_create, static_route_exists, inventory_static_route, to_ip_network
from importlib import import_module
from ipaddress import ip_network

# Share the same destination networks across across all sample scripts.
destination_network_generator = import_module('learning_lab.04_static_route_exists').destination_network_generator

def match(device_name, interface_network):
    """ Discover matching interface on a different device."""
    for other_device in inventory_mounted():
        if other_device == device_name:
            continue
        for interface_name in interface_names(other_device):
            interface_config = interface_configuration_tuple(other_device, interface_name)
            if interface_config.address is None:
                # Skip network interface with unassigned IP address.             
                continue
            other_network = to_ip_network(interface_config.address, interface_config.netmask)
            if other_network == interface_network:
                print('Match %s/%s/%s to %s/%s' % (device_name, interface_config.address, interface_config.netmask, \
                                                   other_device, interface_network))
                return interface_config.address
    return None

def demonstrate(device_name, nexthop_ipaddr):
    """
    Apply function 'static_route_create' to the specified device.
    
    Choose a destination that does not already exist. 
    Choose a next-hop on the same sub-network as an existing interface.
    If the next-hop is unknown then use any valid ip-address.
    """
    
    print('Select a destination network for which a static route does not exist.')
    destination_network_iterator = destination_network_generator()
    while True: 
        destination_network = next(destination_network_iterator)
        print('static_route_exists(%s, %s)' % (device_name, destination_network))
        exists = static_route_exists(device_name, destination_network)
        print(exists)
        print()
        if not exists:
            break
    
    print('Determine which interface is on the management plane (to avoid it).')     
    print('device_control(%s)' % device_name)
    device_mgmt = device_control(device_name)
    #dong
    #print_table(device_mgmt)
    print()

    print('Determine ip-address and network-mask of every interface.')     
    print('interface_configuration_tuple(%s)' % device_name)
    interface_config_list = interface_configuration_tuple(device_name)
    print_table(interface_config_list)
    print()
    
    for interface_config in interface_config_list:
        if interface_config.address is None:
            # Skip network interface with unassigned IP address.             
            continue
        if interface_config.address == device_mgmt.address:
            # Do not configure static routes on the 'management plane'.             
            continue
        if 'Loopback' in interface_config.name:
            # Do not configure static routes on the 'control plane'.             
            continue
        
        print('Determine next-hop for a network interface.')
        interface_network = interface_config.ip_network
        next_hop_address = match(device_name, interface_network)
        if next_hop_address is None:
            print('Next-hop for %s/%s %s/%s is outside the known topology.' % (device_name, interface_config.name, interface_config.address, interface_config.netmask))
            next_hop_address = interface_network.network_address
            if next_hop_address == interface_config.ip_interface:
                next_hop_address += 1
            print('Assume that next-hop for %s/%s %s/%s is %s.' % (device_name, interface_config.name, interface_config.address, interface_config.netmask, next_hop_address))
        else:
            print('Next-hop for %s/%s %s/%s is %s.' % (device_name, interface_config.name, interface_config.address, interface_config.netmask, next_hop_address))
        print()

        print('static_route_create(%s, %s, %s)' % (device_name, destination_network, next_hop_address))
        #dictDong = {'network_address': '5.5.5.5', 'prefixlen': 32}
        destination_network = ip_network(u"%s.%s.%s.%s/255.255.255.255" % (1, 2, 3, 4), strict=False) 
        #next_hop_address = '50.0.0.1'
        static_route_create(device_name, destination_network, nexthop_ipaddr)
        #static_route_create(device_name, dictDong, next_hop_address)
        #dong
        #static_route_create(device_name, '9.9.9.9', next_hop_address)
        return True
    return False

demonstrate('iosxrv-3', '50.0.0.1')