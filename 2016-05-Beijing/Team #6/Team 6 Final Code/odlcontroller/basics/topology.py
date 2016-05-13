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
from collections import namedtuple
from basics.odl_http import odl_http_get, odl_http_post, odl_http_delete
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

_url_topology = '{config}/network-topology:network-topology/topology/{topology-id}'
_url_topology_node = _url_topology + '/node/{node-id}'
_url_mount = _url_topology + '/node/controller-config/yang-ext:mount/config:modules'
_url_connector = _url_mount + '/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/{node-id}'

def mountRequestJSON(name, address, port, username, password):
    return json.dumps({
                       "module": [
                                  {
                                   "type": "odl-sal-netconf-connector-cfg:sal-netconf-connector",
                                   "name": name,
                                   "odl-sal-netconf-connector-cfg:address": address,
                                   "odl-sal-netconf-connector-cfg:port": port,
                                   "odl-sal-netconf-connector-cfg:username": username,
                                   "odl-sal-netconf-connector-cfg:password": password,
                                   "odl-sal-netconf-connector-cfg:dom-registry": {
                                                                                  "name": "dom-broker",
                                                                                  "type": "opendaylight-md-sal-dom:dom-broker-osgi-registry"
                                                                                  },
                                   "odl-sal-netconf-connector-cfg:processing-executor": {
                                                                                         "name": "global-netconf-processing-executor",
                                                                                         "type": "threadpool:threadpool"
                                                                                         },
                                   "odl-sal-netconf-connector-cfg:binding-registry": {
                                                                                      "name": "binding-osgi-broker",
                                                                                      "type": "opendaylight-md-sal-binding:binding-broker-osgi-registry"
                                                                                      },
                                   "odl-sal-netconf-connector-cfg:client-dispatcher": {
                                                                                       "name": "global-netconf-dispatcher",
                                                                                       "type": "odl-netconf-cfg:netconf-client-dispatcher"
                                                                                       },
                                   "odl-sal-netconf-connector-cfg:between-attempts-timeout-millis": 2000,
                                   "odl-sal-netconf-connector-cfg:sleep-factor": 1.5,
                                   "odl-sal-netconf-connector-cfg:reconnect-on-changed-schema": True,
                                   "odl-sal-netconf-connector-cfg:connection-timeout-millis": 20000,
                                   "odl-sal-netconf-connector-cfg:tcp-only": False,
                                   "odl-sal-netconf-connector-cfg:event-executor": {
                                                                                    "name": "global-event-executor",
                                                                                    "type": "netty:netty-event-executor"
                                                                                    },
                                   "odl-sal-netconf-connector-cfg:max-connection-attempts": 0,
                                   }
                                  ]
                       })
    
def topology(config):
    """Return the NETCONF topology JSON format.

    The topology should be the only topology in the list.
    The topology includes all mounted devices.
    The topology excludes all unmounted devices.
    The topology can contain devices that are neither mounted nor unmounted.
    The topology includes all connected devices.
    The topology can contain unconnected devices.
    """
    response = odl_http_get(_url_topology, {'config': config, 
                                                    'topology-id': 'topology-netconf',
                                                    }, 
                            'application/json')
    return response.json()['topology'][0]

def nodes(config):
    '''Retrieve the list of nodes in the NETCONF topology.'''
    nodeList = topology(config)['node']
    nodeList.sort(key=lambda node: node['node-id'])
    return [ node for node in nodeList if node['node-id'] != 'controller-config' ]
    
def node(config, node_id):
    """Retrieve JSON for a single node based on node-id.
    
    Should be the only node in the list.
    """
    response = odl_http_get(_url_topology_node.format(**{'config': config, 
                                                         'topology-id': 'topology-netconf',
                                                         'node-id': quote_plus(node_id),
                                                         }), 
                            'application/json',
                            expected_status_code=(200, 404)
                            )
    if response.status_code == 404:
        return None
    return response.json()['node'][0]
    
def mounted(node_id):
    """Determine whether a single device is mounted on the Controller.
    
    Return True if mounted, False otherwise.
    """
    request_url = _url_connector.format(**{'config': 'config', 
                                          'topology-id': 'topology-netconf',
                                          'node-id': quote_plus(node_id),
                                          })
    response = odl_http_get(request_url, 'application/json', expected_status_code=[200, 404])
    return response.status_code == 200
    
def mounted_nodes():
    """"Names of network devices known to the Controller."""
    return [ node['node-id'].encode('utf-8') for node in nodes('config') ] 
    
def unmounted_nodes():
    """Names of network devices not mounted on the Controller."""
    return [ node for node in settings.config['network_device'].keys() if node not in mounted_nodes() ]

def mount(node_id, device_address, device_port, device_username, device_password):
    """Add the specified network device to the topology of the Controller."""
    request_url = _url_mount.format(**{'config': 'config', 
                                       'topology-id': 'topology-netconf',
                                       })
    request_content = mountRequestJSON(node_id, device_address, device_port, device_username, device_password)
    return odl_http_post(request_url, {}, 'application/json', request_content)

def dismount(node_id):
    """Remove node_id from the topology of the Controller.
    
    It is not necessary for the device to be connected. 
    The outcome is undefined if the device is not already mounted.
    """
    request_url = _url_connector.format(**{'config': 'config', 
                                          'topology-id': 'topology-netconf',
                                          'node-id': quote_plus(node_id),
                                          })
    odl_http_delete(request_url, {}, 'application/json', expected_status_code=200)
    
def connected(node_id):
    """Determine whether a single device is connected to the Controller.
    
    Return True if connected, False otherwise.
    """
    nodeJSON = node('operational', node_id)
    if nodeJSON:
        return nodeJSON['netconf-node-topology:connection-status'] == 'connected'
    else:
        return False
    
def connected_nodes():
    """Names of network devices connected to the Controller.
    
    Output a list of names.
    Connected devices are a subset of the topology.
    """
    return [ node['node-id'].encode('utf-8') for node in nodes('operational') if node['netconf-node-topology:connection-status'] == 'connected' ]

def disconnected_nodes():
    """Names of network devices mounted on the Controller but not connected to the Controller."""
    return [ node['node-id'].encode('utf-8') for node in nodes('operational') if node['netconf-node-topology:connection-status'] != 'connected' ]
    
class DeviceControl(namedtuple('DeviceControl', 
                               ['address', 'port', 'username', 'password'])):
    """Properties of a connection to a management interface to control a device."""
    pass

def device_control(node_id):
    """A DeviceControl if the specified device is mounted, otherwise None"""
    request_url = _url_connector.format(**{'config': 'config', 
                                          'topology-id': 'topology-netconf',
                                          'node-id': quote_plus(node_id),
                                          })
    response = odl_http_get(request_url, 'application/json', expected_status_code=[200, 404])
    if response.status_code == 404:
        return None
    module = response.json()['module'][0]
    assert module['name'] == node_id
    return DeviceControl(
        address  = module['odl-sal-netconf-connector-cfg:address'],
        port     = module['odl-sal-netconf-connector-cfg:port'],
        username = module['odl-sal-netconf-connector-cfg:username'],
        password = module['odl-sal-netconf-connector-cfg:password']
    )

def capability(node_id):
    """Return a list of capability names for the specified device."""
    nodeJSON = node('operational', node_id)
    if nodeJSON:
        return nodeJSON['netconf-node-topology:available-capabilities']['available-capability']
    else:
        return None
