#from __future__ import print_function as _print_function

#from basics.http import json_loads
#from basics.interface import management_interface
#from basics.odl_http import odl_http_get, odl_http_post
from __future__ import print_function as _print_function
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
#from basics.http import json_loads, json_dumps

import pydoc
from basics import topology
from basics.inventory import inventory_connected
import connect_all_devices
from basics.interface import management_interface
from basics.http import json
from basics.interface import management_interface
import urllib
import json
from basics.odl_http import odl_http_get, odl_http_post
from basics.inventory import inventory_connected
from connect_all_devices import connected_all_devices
#make sure all devices connected
connected_all_devices()

_cdp_enable_interface_url_suffix = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations/'

url_neighbors = 'operational/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-cdp-oper:cdp'

_cdp_enable_interface_request_content = {"Cisco-IOS-XR-ifmgr-cfg:interface-configuration":[{"active":"act","interface-name":"%s","Cisco-IOS-XR-cdp-cfg:cdp" : {"enable" : ""}}]}


Neighbor_link_set = {}


def cdp_neighbors_json(device_name):    
    response = odl_http_get(url_neighbors,
                            {'node-id': device_name},
                            'application/json',
                            expected_status_code=(200, 404)
                            )
    j = json.loads(response.text)
    container = j["cdp"]["nodes"]["node"][0]
    mgmt_name = management_interface(device_name)
    neighbor_set = set()
    if "neighbors" in container:
        neighbors = container["neighbors"]
#       print(json.dumps(neighbors, indent=2))
        if "summaries" in neighbors:
            summary = neighbors["summaries"]["summary"]
            for device_info in summary:
                neighbor_id = device_info["device-id"]
                neighbor_interface = device_info["cdp-neighbor"][0]["port-id"]
                device_interface = device_info["interface-name"]
                if device_interface in mgmt_name:
                    continue
                neighbor_info = (device_name, device_interface.encode('utf8'), neighbor_id.encode('utf8'), neighbor_interface.encode('utf8'))
                neighbor_set.add(neighbor_info)
            return neighbor_set

#result:{0: ('iosxrv-8', 'iosxrv-3'), 1: ('iosxrv-8', 'iosxrv-1'), 2: ('iosxrv-8', 'iosxrv-2'), 3: ('iosxrv-8', 'iosxrv-6'), 4: ('iosxrv-8', 'iosxrv-7'), 5: ('iosxrv-7', 'iosxrv-4'), 6: ('iosxrv-6', 'iosxrv-3'), 7: ('iosxrv-6', 'iosxrv-4'), 8: ('iosxrv-5', 'iosxrv-1'), 9: ('iosxrv-5', 'iosxrv-2'), 10: ('iosxrv-3', 'iosxrv-1')}
def link_info():  
#def main():  
    ii = 0
    link_info_dic = {}
    for device_name in inventory_connected():
      
        response = odl_http_get(url_neighbors,
                                {'node-id': device_name},
                                'application/json',
                                expected_status_code=(200, 404)
                                )
        l = json.loads(response.text)
        container_l = l["cdp"]["nodes"]["node"][0]
        mgmt_name = management_interface(device_name)
        
        if "neighbors" in container_l:
            neighbors = container_l["neighbors"]
#           print(json.dumps(neighbors, indent=2))
            if "summaries" in neighbors:
                summary = neighbors["summaries"]["summary"]
                for device_info in summary:
                    neighbor_id = device_info["device-id"]
                    if neighbor_id == "kcy":
                        neighbor_id = 'iosxrv-1'
                    elif neighbor_id == "lax":
                        neighbor_id = 'iosxrv-2'
                    elif neighbor_id == "min":
                        neighbor_id = 'iosxrv-3'
                    elif neighbor_id == "por":
                        neighbor_id = 'iosxrv-4'
                    elif neighbor_id == "san":
                        neighbor_id = 'iosxrv-5'
                    elif neighbor_id == "sea":
                        neighbor_id = 'iosxrv-6'
                    elif neighbor_id == "sfc":
                        neighbor_id = 'iosxrv-7'      
                    else :
                        neighbor_id = 'iosxrv-8'                
                    device_interface = device_info["interface-name"]
                    if device_interface in mgmt_name:
                        continue
                    link_info = (device_name,neighbor_id.encode('utf8'))
                    link_info_re = (neighbor_id.encode('utf8'),device_name)
                    jj=0
                    flag=1
                    while ii > jj:
                        if link_info_dic[jj]==link_info or link_info_dic[jj]==link_info_re:
                            flag = 0       
                            jj=jj+1                      
                        else:
                            jj=jj+1
                    if flag==1:
                        link_info_dic[ii] = link_info 
                        ii=ii+1
                    else:
                        jj=0
                        
#                   return link_info_set
    return link_info_dic
'''    
reslut:{'iosxrv-2': set([('iosxrv-2', 'GigabitEthernet0/0/0/1', 'san', 'GigabitEthernet0/0/0/3'), ('iosxrv-2', 'GigabitEthernet0/0/0/2', 'sjc', 'GigabitEthernet0/0/0/2')]), 
'iosxrv-3': set([('iosxrv-3', 'GigabitEthernet0/0/0/3', 'sea', 'GigabitEthernet0/0/0/1'), ('iosxrv-3', 'GigabitEthernet0/0/0/0', 'sjc', 'GigabitEthernet0/0/0/0'), ('iosxrv-3', 'GigabitEthernet0/0/0/2', 'kcy', 'GigabitEthernet0/0/0/3')]), 
'iosxrv-1': set([('iosxrv-1', 'GigabitEthernet0/0/0/3', 'min', 'GigabitEthernet0/0/0/2'), ('iosxrv-1', 'GigabitEthernet0/0/0/4', 'san', 'GigabitEthernet0/0/0/2'), ('iosxrv-1', 'GigabitEthernet0/0/0/5', 'sjc', 'GigabitEthernet0/0/0/1')]), 'iosxrv-6': set([('iosxrv-6', 'GigabitEthernet0/0/0/3', 'sjc', 'GigabitEthernet0/0/0/3'), ('iosxrv-6', 'GigabitEthernet0/0/0/2', 'por', 'GigabitEthernet0/0/0/1'), ('iosxrv-6', 'GigabitEthernet0/0/0/1', 'min', 'GigabitEthernet0/0/0/3')]), 'iosxrv-7': set([('iosxrv-7', 'GigabitEthernet0/0/0/2', 'sjc', 'GigabitEthernet0/0/0/4'), ('iosxrv-7', 'GigabitEthernet0/0/0/1', 'por', 'GigabitEthernet0/0/0/2')]), 'iosxrv-4': set([('iosxrv-4', 'GigabitEthernet0/0/0/1', 'sea', 'GigabitEthernet0/0/0/2'), ('iosxrv-4', 'GigabitEthernet0/0/0/2', 'sfc', 'GigabitEthernet0/0/0/1')]), 'iosxrv-5': set([('iosxrv-5', 'GigabitEthernet0/0/0/3', 'lax', 'GigabitEthernet0/0/0/1'), ('iosxrv-5', 'GigabitEthernet0/0/0/2', 'kcy', 'GigabitEthernet0/0/0/4')]), 'iosxrv-8': set([('iosxrv-8', 'GigabitEthernet0/0/0/0', 'min', 'GigabitEthernet0/0/0/0'), ('iosxrv-8', 'GigabitEthernet0/0/0/3', 'sea', 'GigabitEthernet0/0/0/3'), ('iosxrv-8', 'GigabitEthernet0/0/0/1', 'kcy', 'GigabitEthernet0/0/0/5'), ('iosxrv-8', 'GigabitEthernet0/0/0/4', 'sfc', 'GigabitEthernet0/0/0/2'), ('iosxrv-8', 'GigabitEthernet0/0/0/2', 'lax', 'GigabitEthernet0/0/0/2')])}
'''
def cdp_get_nei():
    for device_name in inventory_connected():
        neighbor = cdp_neighbors_json(device_name)
        Neighbor_link_set[device_name] = neighbor
#       print(Neighbor_link_set[device_name])
    return Neighbor_link_set

'''
#def nexr_hop():
def main():
    next_hop_set = {}
    for device_name in inventory_connected():
        neighbor = cdp_neighbors_json(device_name)
        response = odl_http_get(url_neighbors,
                            {'node-id': device_name},
                            'application/json',
                            expected_status_code=(200, 404)
                            )
        nn = json.loads(response.text)
        container_n = nn["cdp"]["nodes"]["node"][0]
        mgmt_name = management_interface(device_name)
        next_hop_set = set()
        if "neighbors" in container_n:
            neighbors = container_n["neighbors"]
#           print(json.dumps(neighbors, indent=2))
            if "details" in neighbors:
                detail= neighbors["details"]["detail"]
           
                for n_info in summary:
                    neighbor_id = device_info["device-id"]
                    neighbor_interface = device_info["cdp-neighbor"][0]["port-id"]
                    device_interface = device_info["interface-name"]
                    if device_interface in mgmt_name:
                        continue
                    next_hop_info = (device_name, device_interface.encode('utf8'), neighbor_id.encode('utf8'), neighbor_interface.encode('utf8'))
                    next_hop_set.add(next_hop_info)
#                    return next_hop_set

if __name__ == "__main__":
    main()
'''