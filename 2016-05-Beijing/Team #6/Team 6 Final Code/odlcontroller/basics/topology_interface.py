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
from basics.odl_http import odl_http_get, odl_http_put
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

_url_topology = '{config}/network-topology:network-topology/topology/{topology-id}'
_url_topology_node = _url_topology + '/node/{node-id}'
_url_interface                = _url_topology_node + '/yang-ext:mount/Cisco-IOS-XR-ifmgr-oper:interface-properties'
_url_interfaces               = _url_interface + '/data-nodes/data-node/0%2F0%2FCPU0/system-view/interfaces'
_url_interface_properties     = _url_interfaces + '/interface/{interface-name}'
_url_interface_configurations = _url_topology_node + '/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations'
_url_interface_configuration  = _url_interface_configurations +  '/interface-configuration/{active}/{interface-name}'
    
def interfaceRequestJSON(active, netmask, address, interface_name, description, shutdown):
    request_content = {
                       "interface-configuration": [
                                                   {
                                                    "active": active,
                                                    "Cisco-IOS-XR-ipv4-io-cfg:ipv4-network": {
                                                                                              "addresses": {
                                                                                                            "primary": {
                                                                                                                        "netmask": netmask, 
                                                                                                                        "address": address
                                                                                                                        }
                                                                                                            }
                                                                                              },
                                                    "interface-name": interface_name, 
                                                    "description": description
                                                    }
                                                   ]
                       }
    if shutdown:
        request_content['interface-configuration'][0]['shutdown'] = ""
    return json.dumps(request_content)
    
def interface_names(node_id):
    """Retrieve the interface names for a particular XRV node."""
    url_params = {'config': 'operational', 
                  'topology-id': 'topology-netconf',
                  'node-id': node_id,
                 }
    response = odl_http_get(_url_interfaces, url_params, 'application/json', expected_status_code=[200, 400])
    all_names = [ interface['interface-name'].encode('utf-8') for interface in response.json()['interfaces']['interface'] if interface['type'].lower().find('ethernet') >= 0 ] 
    management_name= management_interface_name(node_id)
    return sorted( [ name for name in all_names if name != management_name ] )
    
def interface_properties(node_id, interface_name):
    """Retrieve the interface properties for a particular XRV node."""
    url_params = {'config': 'operational', 
                  'topology-id': 'topology-netconf',
                  'node-id': node_id,
                  'interface-name': interface_name,
                  }
    response = odl_http_get(_url_interface_properties, url_params, 'application/json', expected_status_code=[200, 400])
    return response.json()

def interface_configuration(node_id, interface_name):
    """Retrieve the interface configuration for a particular XRV node."""
    url_params = {'config': 'operational', 
                  'topology-id': 'topology-netconf',
                  'node-id': node_id,
                  'active': 'act',
                  'interface-name': interface_name,
                  }
    response = odl_http_get(_url_interface_configuration, url_params, 'application/json', expected_status_code=[200, 400])
    return response.json()

def management_interface_name(node_id):
    """Retrieve the management interface name for a particular XRV node."""
    url_params = {'config': 'config', 
                  'topology-id': 'topology-netconf',
                  'node-id': node_id,
                 }
    response = odl_http_get(_url_interface_configurations, url_params, 'application/json', expected_status_code=[200, 400])
    interfaces = response.json()['interface-configurations']['interface-configuration']
    return next(interface['interface-name'] for interface in interfaces if interface['Cisco-IOS-XR-ipv4-io-cfg:ipv4-network']['addresses']['primary']['address'] == settings.config['network_device'][node_id]['address'])    

def interface_configuration_update(
                                   node_id,
                                   interface_name,
                                   description,
                                   address,
                                   netmask,
                                   active='act',
                                   shutdown=False
                                   ):
    """Update the configuration of the specified interface of the specified device."""
    url_params = {'config': 'config', 
                  'topology-id': 'topology-netconf',
                  'node-id': node_id,
                  'active': active,
                  'interface-name': interface_name,
                  }
    request_content = interfaceRequestJSON(active, netmask, address, interface_name, description, shutdown)
    odl_http_put(_url_interface_configuration, url_params, 'application/json', request_content, expected_status_code=200)

def interface_toggle(node_id, interface_name, shutdown):
    """Toggle the state of the specified interface of the specified device."""
    url_params = {'config': 'config', 
                  'topology-id': 'topology-netconf',
                  'node-id': node_id,
                  'active': 'act',
                  'interface-name': interface_name,
                  }
    ifcfg = interface_configuration(node_id, interface_name)
    if shutdown:
        ifcfg['interface-configuration'][0]['shutdown'] = ""
    else: # bring back up
        if 'shutdown' in ifcfg['interface-configuration'][0]:
            ifcfg['interface-configuration'][0].pop('shutdown')
    request_content = json.dumps(ifcfg)
    odl_http_put(_url_interface_configuration, url_params, 'application/json', request_content, expected_status_code=200)

def interface_shutdown(node_id, interface_name):
    interface_toggle(node_id, interface_name, shutdown=True)
    
def interface_startup(node_id, interface_name):
    interface_toggle(node_id, interface_name, shutdown=False)