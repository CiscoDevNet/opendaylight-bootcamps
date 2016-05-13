#!/usr/bin/env python2.7

#team
#boat
#end

from __future__ import print_function
from basics.context import sys_exit
from basics.odl_http import odl_http_post
import json
import settings

_bgp_url_suffix = 'operational/bgp-rib:bgp-rib/rib/example-bgp-rib/loc-rib/tables/bgp-linkstate:linkstate-address-family/bgp-linkstate:linkstate-subsequent-address-family'
_static_route_url_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/address-family/vrfipv4/vrf-unicast/vrf-prefixes'
_static_route_uni_url_template = _static_route_url_template + '/vrf-prefix/{ip-address}/{prefix-length}'

def static_route_create2(device, destination_address,prefixlen, next_address, description=None):
    """ Create the specified 'static route' on the specified network device. """
    next_hop = {"next-hop-address" : str(next_address)}
    if description:
        next_hop["description"] = description

    request_content = {
        "Cisco-IOS-XR-ip-static-cfg:vrf-prefix": [
            {
                "prefix" : str(destination_address),
                "prefix-length": prefixlen,
                "vrf-route" : {
                    "vrf-next-hops" : {
                        "next-hop-address" : [next_hop]
                    }
                }
            }
        ]
    }
    response = odl_http_post(_static_route_url_template, {'node-id' : device}, 'application/json', request_content, expected_status_code=[204, 409,400])
    if response.status_code == 409:
        try:
            raise ValueError(response.json()['errors']['error'][0]['error-message'])
        except IndexError:
            pass
        except KeyError:
            pass
        raise ValueError('Already exists: static route to destination network %s on device %s' % (destination_address, device))

def main():
    static_route_create2('iosxrv-5', '192.18.1.33/32', 32,'192.18.1.30')
    static_route_create2('iosxrv-1', '192.18.1.33/32', 32,'192.18.1.32')
    static_route_create2('iosxrv-3', '192.18.1.33/32', 32,'192.18.1.35')
    static_route_create2('iosxrv-6', '192.18.1.33/32', 32,'192.18.1.33')
    static_route_create2('iosxrv-4', '192.18.1.34/32', 32,'192.18.1.36')
    static_route_create2('iosxrv-7', '192.18.1.34/32', 32,'192.18.1.37')
    static_route_create2('iosxrv-8', '192.18.1.34/32', 32,'192.18.1.31')
    static_route_create2('iosxrv-2', '192.18.1.34/32', 32,'192.18.1.34')
    print('yes, we are completed!')
if __name__ == "__main__":
    sys_exit(main())
