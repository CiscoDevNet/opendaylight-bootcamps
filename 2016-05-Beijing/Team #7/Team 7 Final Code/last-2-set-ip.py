from __future__ import print_function as _print_function
import pydoc
import settings
import time
from pydoc import plain
from pydoc import render_doc as doc
from basics import topology
from basics.context import EX_OK
from basics.interface import management_interface, interface_configuration_tuple, interface_names, interface_configuration_update
from basics.inventory import inventory_connected
from basics.render import print_table
from os.path import basename,splitext
from runpy import run_module

def main():   
    device_list=settings.config['network_device']
    connected_list = topology.connected_nodes()
    
    if len(connected_list) != len(device_list):
        print('not all devices are connected!')
        return
    
    device_1 = 'iosxrv-1'
    device_2 = 'iosxrv-2'
    device_3 = 'iosxrv-3'
    device_4 = 'iosxrv-4'
    device_5 = 'iosxrv-5'
    device_6 = 'iosxrv-6'
    device_7 = 'iosxrv-7'
    device_8 = 'iosxrv-8'
    interface_0 = 'GigabitEthernet0/0/0/0'
    interface_1 = 'GigabitEthernet0/0/0/1'
    interface_2 = 'GigabitEthernet0/0/0/2'
    interface_3 = 'GigabitEthernet0/0/0/3'
    interface_4 = 'GigabitEthernet0/0/0/4'
    interface_5 = 'GigabitEthernet0/0/0/5'
    interface_6 = 'GigabitEthernet0/0/0/6'
    
    #link device_1 to device_2
    initial = interface_configuration_tuple(device_1, interface_0)
    #print_table(initial)
    ip_address = '10.0.12.1'
    ip_netmask = '255.255.255.0'
    description = 'connect to device_2'
    interface_configuration_update(device_1, initial.name, description=description, address=ip_address, netmask=ip_netmask, shutdown=False)
    print_table(interface_configuration_tuple(device_1, interface_0))
    #link device_2 to device_1
    initial = interface_configuration_tuple(device_2, interface_0)
    #print_table(initial)
    ip_address = '10.0.12.2'
    ip_netmask = '255.255.255.0'
    description = 'connect to device_1'
    interface_configuration_update(device_2, initial.name, description=description, address=ip_address, netmask=ip_netmask, shutdown=False)
    print_table(interface_configuration_tuple(device_2, interface_0))
    #display
    print('set link device_1 <-> device_2')
    
    #link device_1 to device_8
    initial = interface_configuration_tuple(device_1, interface_5)
    #print_table(initial)
    ip_address = '10.0.18.1'
    ip_netmask = '255.255.255.0'
    description = 'connect to device_8'
    interface_configuration_update(device_1, initial.name, description=description, address=ip_address, netmask=ip_netmask, shutdown=False)
    print_table(interface_configuration_tuple(device_1, interface_5))
    #link device_8 to device_1
    initial = interface_configuration_tuple(device_8, interface_1)
    #print_table(initial)
    ip_address = '10.0.18.8'
    ip_netmask = '255.255.255.0'
    description = 'connect to device_1'
    interface_configuration_update(device_8, initial.name, description=description, address=ip_address, netmask=ip_netmask, shutdown=False)
    print_table(interface_configuration_tuple(device_8, interface_1))
    #display
    print('set link device_1 <-> device_8')
    
    #link device_2 to device_8
    initial = interface_configuration_tuple(device_2, interface_2)
    #print_table(initial)
    ip_address = '10.0.28.2'
    ip_netmask = '255.255.255.0'
    description = 'connect to device_8'
    interface_configuration_update(device_2, initial.name, description=description, address=ip_address, netmask=ip_netmask, shutdown=False)
    print_table(interface_configuration_tuple(device_2, interface_2))
    #link device_8 to device_2
    initial = interface_configuration_tuple(device_8, interface_2)
    #print_table(initial)
    ip_address = '10.0.28.8'
    ip_netmask = '255.255.255.0'
    description = 'connect to device_2'
    interface_configuration_update(device_8, initial.name, description=description, address=ip_address, netmask=ip_netmask, shutdown=False)
    print_table(interface_configuration_tuple(device_8, interface_2))
    #display
    print('set link device_2 <-> device_8')
    
if __name__ == "__main__":
    main()