from __future__ import print_function as _print_function
import pydoc
import settings
import time
from pydoc import plain
from pydoc import render_doc as doc
from basics import topology
from basics.context import EX_OK
from basics.interface import management_interface, interface_configuration_tuple, interface_names, interface_configuration_update
from basics.routes import static_route_list, inventory_static_route, static_route_create, static_route_exists, to_ip_network, static_route_delete
from basics.inventory import inventory_connected
from basics.render import print_table
from os.path import basename,splitext
from runpy import run_module
    
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



    #add static route for flow 1
    destination_network = to_ip_network('100.0.0.0', '24')
    #device_1
    next_hop_address = '10.0.12.2'
    add_static_route(device_1, destination_network, next_hop_address, 0)
    #device_2
    next_hop_address = '198.18.1.34'
    add_static_route(device_2, destination_network, next_hop_address, 0)
    #device_8
    next_hop_address = '10.0.28.2'
    add_static_route(device_8, destination_network, next_hop_address, 0)
    #display
    print('add route for flow 1 (to 100.0.0.0/24): ', device_8, ' -> ', device_2)

    #add static route for flow 2
    destination_network = to_ip_network('200.0.0.0', '24')
    #device_1
    next_hop_address = '10.0.12.2'
    add_static_route(device_1, destination_network, next_hop_address, 0)
    #device_2
    next_hop_address = '198.18.1.34'
    add_static_route(device_2, destination_network, next_hop_address, 0)
    #device_8
    next_hop_address = '10.0.18.1'
    add_static_route(device_8, destination_network, next_hop_address, 0)
    #display
    print('add route for flow 2 (to 200.0.0.0/24): ', device_8, ' -> ', device_1, ' -> ', device_2)
    
    #add static route for flow 3
    destination_network = to_ip_network('50.0.0.0', '24')
    next_hop_address = '198.18.1.32'
    add_static_route(device_8, destination_network, next_hop_address, 0)
    #display
    print('add route for flow 3 (to 50.0.0.0/24): ', device_8, ' -> black_hole')

    
    #display static route
    print('\n')
    routes = static_route_list(device_8)
    print('static route table', device_8)
    print_table(routes)
    
if __name__ == "__main__":
    main()