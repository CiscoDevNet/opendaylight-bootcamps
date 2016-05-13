# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import settings
import json
from basics.odl_http import odl_http_get, odl_http_post, odl_http_delete
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

_url_node_loopback_address='config/network-topology:network-topology/topology/topology-netconf/node/%s/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations/interface-configuration/act/Loopback0/Cisco-IOS-XR-ipv4-io-cfg:ipv4-network/addresses/primary'




def get_loopback(device_name):
    _url_node_loopback_2 = _url_node_loopback_address % device_name
    device_address_response=odl_http_get(_url_node_loopback_2,
                        {},
                        'application/json',
                        )                    
    ttt1 = json.loads(device_address_response.text)
    container = ttt1["Cisco-IOS-XR-ipv4-io-cfg:primary"]["address"]
    return container
#    print(device_loopback_set)

from basics.inventory import inventory_connected    
loopback_container = {}

def get_all_devices_loopback():
#def main():
    for device_name in inventory_connected():
        loopback_container[device_name] = get_loopback(device_name)        
    print(loopback_container)   
'''    
if __name__ == "__main__":
    main()    
'''    

    
