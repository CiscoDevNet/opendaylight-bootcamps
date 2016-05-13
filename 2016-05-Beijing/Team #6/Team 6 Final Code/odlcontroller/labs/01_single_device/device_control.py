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

''' Sample usage of function 'device_control'.

    Print the function's documentation.
    Apply the function to one device.
    Print the output.
    
    This demonstration requires a device that is mounted.
    It is not necessary for the device to be connected.
'''
from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
import os
from basics.inventory import inventory_mounted, device_control, DeviceControl
from basics.render import print_table
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL

def demonstrate(device_name):
    ''' Apply function 'device_control' to the specified device.'''
    print('device_control(' + device_name, end=')\n')
    print_table(device_control(device_name))
    
def main():
    ''' Select a device and demonstrate.'''
    print(plain(doc(device_control)))
    print('DeviceControl fields:', *DeviceControl._fields, sep='\n\t', end='\n\n')
    for device_name in inventory_mounted():
        demonstrate(device_name)
        return EX_OK
    print("There are no suitable network devices. Demonstration cancelled.")
    return EX_TEMPFAIL

if __name__ == "__main__":
    main()
