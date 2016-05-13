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

from __future__ import print_function
from basics import topology, topology_interface

def main():
    for device_name in topology.connected_nodes():
        print('%s:' % device_name)
        for interface_name in topology_interface.interface_names(device_name):
            #print('Interface Properties for %s:' % interface_name)
            interface_configuration = topology_interface.interface_configuration(device_name, interface_name)
            print('\t', interface_name, '-->',  interface_configuration)

if __name__ == "__main__":
    main()