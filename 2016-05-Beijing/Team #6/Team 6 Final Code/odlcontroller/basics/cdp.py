from __future__ import print_function as _print_function
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
from basics.http import json_loads, json_dumps
from basics.odl_http import odl_http_get, odl_http_post

_cdp_enable_interface_url_suffix = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations/'

url_neighbours = 'operational/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-cdp-oper:cdp'

_cdp_enable_interface_request_content = '''
{"Cisco-IOS-XR-ifmgr-cfg:interface-configuration":[
{
"active":"act",
"interface-name":"%s",
"Cisco-IOS-XR-cdp-cfg:cdp" : {"enable" : ""}
}]}
'''

def cdp_neighbors_json(device_name):
    response = odl_http_get(url_neighbours,
                            {'node-id': device_name},
                            'application/json',
                            expected_status_code=(200, 404)
                            )
    j = json_loads(response.text)
    container = j["cdp"]["nodes"]["node"][0]
    print(json_dumps(container, indent=2))
    if "neighbors" in container:
        neighbors = container["neighbors"]
        print(len(neighbors))
        print(json_dumps(neighbors, indent=2))

def cdp_enable_interface(device_name, interface_name):
    print('cdp_enable_interface(%s,%s)' % (device_name, interface_name))
    request_content = _cdp_enable_interface_request_content % (interface_name)
    return odl_http_post(_cdp_enable_interface_url_suffix, {'node-id': device_name}, 'application/json', request_content)

from basics.interface import interface_names
def cdp_enable_device(device_name):
    for interface_name in interface_names(device_name):
        cdp_enable_interface(device_name, interface_name)
        
from basics.inventory import inventory_connected
def cdp_enable_network():
    for device_name in inventory_connected():
        cdp_enable_device(device_name)

def demonstrate():
    cdp_enable_network()
    for device_name in inventory_connected():
        cdp_neighbors_json(device_name)

demonstrate()