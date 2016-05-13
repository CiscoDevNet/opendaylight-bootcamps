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

''' Sample usage of function 'basics.topology.dismount'.

    Print the function's documentation then apply the function to any one device that is mounted.
'''

from __future__ import print_function
import pydoc
import settings
from basics import topology

def dismount_device(device_name):
    """Dismount a single device by removing from the NETCONF topology."""
    print('device_dismount(' + device_name, end=')\n')
    topology.dismount(device_name)

def main():
    print(pydoc.plain(pydoc.render_doc(topology.dismount)))
    try:
        # Select a mounted device that is in our settings.config
        device_name = next(name for name in topology.mounted_nodes() if name in settings.config['network_device'])
        dismount_device(device_name)
    except(TypeError, StopIteration):
        print('There are no mounted devices to dismount. Demonstration cancelled.')

if __name__ == "__main__":
    main()