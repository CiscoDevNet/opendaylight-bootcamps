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


"""Sample usage of function 'topology_interface.interface_shutdown' to shutdown an interface.

    Apply the function to one interface on one device.
    The device must be connected.
    The interface must be on the 'data plane', not the 'control plane'.
    The interface should be 'up'.
"""
from __future__ import print_function
from basics import topology, topology_interface

def main():
    connected_nodes = topology.connected_nodes()
    if connected_nodes:
        node_id = connected_nodes[0]
        interface_names = topology_interface.interface_names(node_id)
        if interface_names:
            interface_name = interface_names[0]
            print('Shutting down interface %s on %s' % (interface_name, node_id))
            topology_interface.interface_shutdown(node_id, interface_name)
        else:
            print('No interfaces on %s' % node_id)        
    else:
        print('No connected devices')

if __name__ == "__main__":
    main()