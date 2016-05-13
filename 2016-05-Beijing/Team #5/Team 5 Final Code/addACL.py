'''
Created on May 12, 2016

@author: hailiu
'''
from __future__ import print_function as _print_function
from importlib import import_module
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.acl import acl_create_port_grant, inventory_acl
acl_fixture = import_module('learning_lab.05_acl_fixture')

device_name = "iosxrv-1"
acl_name = "acd"
acl_port = "30.30.30.30"
acl_grant = "permit"
acl_protocol = ""

def demonstrate(device_name, acl_name, port, grant, protocol):
    ''' Apply function 'acl_create_port_grant' to the specified device and ACL.'''
    print('\nacl_create_port_grant(' + device_name, acl_name, port, grant, protocol, sep=', ', end=')\n')
    acl_create_port_grant(device_name, acl_name, port, grant, protocol)

def main():
    ''' Select a device and demonstrate with each ACL.'''
    print(plain(doc(acl_create_port_grant)))
    inventory = inventory_acl()
    if not inventory:
        print('There are no ACL capable devices to examine. Demonstration cancelled.')
    else:
        try:
            demonstrate(device_name, acl_name, acl_port, acl_grant, acl_protocol)
            return EX_OK
        except Exception as e:
            print(e)
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
    