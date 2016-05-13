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

''' Sample usage of function 'device_dismount'.

    Print the function's documentation then apply the function to every device that is mounted.
'''

from __future__ import print_function
import pydoc
from basics import topology

def dismount_device(device_name):
    """Dismount a single device by removing from the NETCONF topology."""
    print('device_dismount(' + device_name, end=')\n')
    topology.dismount(device_name)

def main():
    print(pydoc.plain(pydoc.render_doc(topology.mount)))
    mounted_list = topology.mounted_nodes()
    if mounted_list:
        for device_name in mounted_list:
            dismount_device(device_name)
    else:
        print('There are no mounted devices to dismount.')

if __name__ == "__main__":
    main()
