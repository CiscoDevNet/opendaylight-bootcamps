from __future__ import print_function
from basics.ipaddress import ip_network, _BaseNetwork
from basics.odl_http import odl_http_get, odl_http_post, odl_http_delete
from basics.inventory import capability_discovery
from basics.acl import _error_message
import json
from basics.render import print_table
from basics.routes import  inventory_static_route, \
    static_route_list,static_route_json


_bgp_url_suffix = 'operational/bgp-rib:bgp-rib/rib/example-bgp-rib/loc-rib/tables/bgp-linkstate:linkstate-address-family/bgp-linkstate:linkstate-subsequent-address-family'

_static_route_url_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/address-family/vrfipv4/vrf-unicast/vrf-prefixes'

_static_route_uni_url_template = _static_route_url_template + '/vrf-prefix/{ip-address}/{prefix-length}'

capability_ns = 'http://cisco.com/ns/yang/'
capability_name = 'Cisco-IOS-XR-ip-static-cfg'


def static_route_create(device_name, destination_network, prefix_len, next_hop_address):
    
    route_list = static_route_json(device_name)
    for route in route_list:
        if route['prefix'] == destination_network:
            print('static_route_delete(%s, %s)' % (device_name, destination_network))
            static_route_delete(device_name, destination_network, prefix_len)
            break
        
    """ Create the specified 'static route' on the specified network device. """
    next_hop = {"next-hop-address" : str(next_hop_address)}
    request_content = {
        "Cisco-IOS-XR-ip-static-cfg:vrf-prefix": [
            {
                "prefix" : destination_network,
                "prefix-length": prefix_len,
                "vrf-route" : {
                    "vrf-next-hops" : {
                        "next-hop-address" : [next_hop]
                    }
                }
            }
        ]
    }
    print('static_route_create(%s, %s, %s)' % (device_name, destination_network, next_hop_address))
    response = odl_http_post(_static_route_url_template, {'node-id' : device_name}, 'application/json', request_content, expected_status_code=[204, 409])
    if response.status_code == 204:
        return True
    else:
        return False
        '''
        try:
            raise ValueError(response.json()['errors']['error'][0]['error-message'])
        except IndexError:
            pass
        except KeyError:
            pass
        raise ValueError('Already exists: static route to destination network %s on device %s' % (destination_network, device_name))
        '''


def demonstrate_all(device_name):
    """
    Apply function 'static_route_delete' to all routes on the specified device.
    """
    print()
    print('static_route_delete(%s)' % device_name)
    static_route_delete(device_name)

    print()
    print('static_route_list(%s)' % device_name)
    print_table(static_route_list(device_name), headers='destination-network')


def test_route_create(router_lists):
    #for router in ["iosxrv-1","iosxrv-2","iosxrv-3","iosxrv-4","iosxrv-5","iosxrv-6","iosxrv-7","iosxrv-8"]:
    #    demonstrate_all(router)
    for router_list in router_lists:
        #print(router_list[0])
        static_route_create(router_list[0], router_list[1], router_list[2], router_list[3])



def static_route_delete(device_name, destination_network=None, prefixlen=0):
    """
    Delete zero, one or more static routes from the specified device.
    
    Parameters:
    - device_name
        Identifies the network device.
    - destination_network
        Either None or an instance of type ipaddress._BaseNetwork
        - Unspecified
            Delete all static routes on the device.
            An exception is raised if there are no routes found on the device.
        - Specified
            Delete the route with the specified destination.
            An exception is raised if the specified route is not found on the device.

    No value is returned.
    An exception is raised if the static route does not exist on the device.
    """
    
    if destination_network:
        route_list = static_route_json(device_name)
        for route in route_list:
            if route['prefix'] == destination_network:
                url_params = {
                'node-id' : device_name, 
                'ip-address' : destination_network, 
                'prefix-length' : prefixlen
                }
                url_template = _static_route_uni_url_template
                response = odl_http_delete(url_template, url_params, 'application/json', expected_status_code=[200, 404, 500])
                if response.status_code != 200:
                    return False
                    #raise Exception(_error_message(response.json()))
                return True
    else:
         url_params_all = {'node-id' : device_name} 
         url_template_all = _static_route_url_template
         response = odl_http_delete(url_template_all, url_params_all, 'application/json', expected_status_code=[200, 404, 500])
         return True

    


def test_route_delete(router_lists_delete):
    for router_list in router_lists_delete:
        route_list_all = static_route_list(router_list[0])
        print(route_list_all)
        return static_route_delete(router_list[0], router_list[1], router_list[2])
    
    

        
    
if __name__ == "__main__":
    router_lists = [['iosxrv-8','1.99.3.190',32,'198.18.1.39'],['iosxrv-8','1.99.3.190',32,'198.18.1.39']]
    router_lists_delete = [['iosxrv-8','1.99.3.190',32]]
  #  test_route_delete(router_lists_delete)   
    test_route_create(router_lists)       
    for router in ["iosxrv-1","iosxrv-2","iosxrv-3","iosxrv-4","iosxrv-5","iosxrv-6","iosxrv-7","iosxrv-8"]:
        demonstrate_all(router)
    