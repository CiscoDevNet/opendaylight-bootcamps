from __future__ import print_function as _print_function
import pydoc
import settings
import time
from pydoc import plain
from pydoc import render_doc as doc
from basics import topology
from basics.context import EX_OK
from basics.interface import management_interface
from basics.interface import interface_configuration_tuple
from basics.interface import interface_names
from basics.interface import interface_configuration_update
from basics.inventory import inventory_connected
from basics.render import print_table
from basics.routes import static_route_list, inventory_static_route, static_route_create, static_route_exists, to_ip_network, static_route_delete
from basics.acl import acl_list, inventory_acl, acl_create_port_grant, acl_exists
from os.path import basename,splitext



def delete_static_route(device_name, destination_network, print_tag):
    #if static route exist, delete it first
    if static_route_exists(device_name, destination_network):
        static_route_delete(device_name, destination_network)
        if print_tag == 1:
            print('remove route to %s' % destination_network, 'in %s' % device_name)



def add_static_route(device_name, destination_network, next_hop_address, print_tag):
    #if static route exist, delete it first
    if static_route_exists(device_name, destination_network):
        static_route_delete(device_name, destination_network)
        if print_tag == 1:
            print('remove route to %s' % destination_network, 'in %s' % device_name)
    #add the static route
    static_route_create(device_name, destination_network, next_hop_address)
    if print_tag == 1:
        print('add route to %s' % destination_network, ' next_hop: %s' % next_hop_address, 'in %s' % device_name)


def main():
    #device_list=settings.config['network_device']
    device_list = settings.config['network_device']
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
    
    
    #change path for flow 1
    destination_network = to_ip_network('100.0.0.0', '24')
    prior_next_hop = '10.0.28.2'
    second_next_hop = '10.0.18.1'
    if (interface_configuration_tuple(device_2, interface_2).shutdown == False) & (interface_configuration_tuple(device_8, interface_2).shutdown == False):
        link_status = 'up'
    else:
        link_status = 'down'
    #loop
    #for i in range(100):
    while True:
        #check the link
        if (interface_configuration_tuple(device_2, interface_2).shutdown == False) & (interface_configuration_tuple(device_8, interface_2).shutdown == False):
            new_status = 'up'
            #print('link: device_2 <-> device_8 is OK')
        else:
            new_status = 'down'
            #print('link: device_2 <-> device_8 is fail')
            
        #link status unchange
        if link_status == new_status:
            print('device_2 <-> device_8 link status unchange')
            time.sleep(1)
            continue
        #link status up -> down
        elif (link_status == 'up') & (new_status == 'down'): 
            delete_static_route(device_8, destination_network, 1)
            add_static_route(device_8, destination_network, second_next_hop, 1)
            print('device_2 <-> device_8 link status from up to down: delete prior_route, add second_route, at last for 10s')
            link_status = new_status
            time.sleep(10)
        #link status down -> up
        elif (link_status == 'down') & (new_status == 'up'): 
            delete_static_route(device_8, destination_network, 1)
            add_static_route(device_8, destination_network, prior_next_hop, 1)
            print('device_2 <-> device_8 link status from down to up: delete second_route, add prior_route')
            link_status = new_status
            time.sleep(3)
    
if __name__ == "__main__":
    main()