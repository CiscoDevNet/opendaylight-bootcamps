# Author: Kevin Boutarel
# Date: 11/05/2015
# Purpose: Insert IPv4 unicast route to the ODL Controller
# Usage: python insert_route.py ODL_IP_address router_IP_address destination_prefix

import sys
import settings

from basics.interface import interface_names
from route_attributes import attributes
from v4_uni_app_route import app_route

def main():
    if(sys.argv < 1):
        print("Usage: python insert_route.py ODL_IP_address router_IP_address destination_prefix")
        exit(1)
        
    # Store command line arguments
    #odl_ip = sys.argv[1]
    #input_source_ip = sys.argv[2]
    #destination_prefix = sys.argv[3]

    odl_ip = "localhost"
    #input_router_ip = "198.18.1.30"
    destination_prefix = '10.210.210.1/32'

    print("Starting insert_route")

    # Get device name from the source IP address
    #print("Getting device name from IP address %s" % (input_router_ip))
    #found = False
    #for (device_name, device_config) in settings.config['network_device'].items():
    #    address = device_config['address']
    #    if(address == input_router_ip):
    #        source_name = device_name
    #        found = True
    #        break
    
    #if(not found):
    #    print("Input source IP %s could not be found among the list of devices" % (input_source_ip))
    #    exit(1)

    # Set the next hop in the attributes for the prefix
    print("Setting attributes")
    prefix_attributes = attributes()
    prefix_attributes.set_next_hop('1.2.3.4')
    
    # Create an app route
    print("Creating ipv4 unicast route for %s" % (destination_prefix))
    route = app_route(odl_ip)
    
    print("Setting route to %s" % (destination_prefix))
    
    # Put the app route into the controller
    route.put_app_route(destination_prefix, prefix_attributes.get())
        
    print("Route Set => Connection closed to %s\n" % (destination_prefix))
    
if __name__ == "__main__":
    main()