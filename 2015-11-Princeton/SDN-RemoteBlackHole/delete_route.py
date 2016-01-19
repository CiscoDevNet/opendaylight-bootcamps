# Author: Kevin Boutarel
# Date: 11/05/2015
# Purpose: Delete an IPv4 unicast route to the ODL Controller
# Usage: python delete_route.py ODL_IP_address destination_prefix

import sys

from basics.interface import interface_names
from v4_uni_app_route import app_route

def main():
    if(sys.argv < 1):
        print("Usage: python insert_route.py ODL_IP_address router_IP_address destination_prefix")
        exit(1)
        
    # Store command line arguments
    #odl_ip = sys.argv[1]
    #destination_prefix = sys.argv[2]

    odl_ip = "localhost"
    destination_prefix = '10.210.210.1/32'
    
    # Create an app route
    route = app_route(odl_ip)
    
    # Delete the app route from the controller
    print("Deleting route going to %s from the controller %s" % (destination_prefix, odl_ip))
    route.del_app_route(destination_prefix)
    
    print("Route deleted => Connection open to %s\n" % (destination_prefix))
    
if __name__ == "__main__":
    main()