# Copyright 2014 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
from lxml import etree
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

from basics.odl_http import odl_http_post, odl_http_delete, odl_http_get
from basics.inventory import capability_discovery
import json

_request_content_acl_port_grant_template = '''
{"Cisco-IOS-XR-ipv4-acl-cfg:accesses" : [{"access":[{"access-list-name":"%s","access-list-entries":{"access-list-entry":[{"sequence-number":20,"grant":"permit"},{"sequence-number":10,"destination-port":{"first-destination-port":"%s","destination-operator":"equal"},"grant":"%s","protocol":"%s"}]}}]}]}
'''

_request_create_template = '''
{
  "Cisco-IOS-XR-ipv4-acl-cfg:accesses": [
    {
      "access": [
        {
          "access-list-name": "foo", 
          "access-list-entries": {
            "access-list-entry": [
              {
                "sequence-number": 20, 
                "grant": "permit"
              }, 
              {
                "destination-port": {
                  "first-destination-port": "www", 
                  "destination-operator": "equal"
                }, 
                "protocol": "tcp", 
                "sequence-number": 10, 
                "grant": "deny"
              }
            ]
          }
        }
      ]
    }
  ]
}
'''

_url_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ipv4-acl-cfg:ipv4-acl-and-prefix-list'

_url_named_acl = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ipv4-acl-cfg:ipv4-acl-and-prefix-list/accesses/access/{access-id}/'

def _error_message(error_json):
    """A string representation of the error message given a JSON representation of the error."""
    try:
        return error_json['errors']['error'][0]['error-message']
    except:
        return json.dumps(error_json);

def acl_create_port_grant(
    device_name,
    acl_name,
    port,
    grant,
    protocol
):
    request_content = _request_content_acl_port_grant_template % (quote_plus(acl_name), port, grant, protocol)
    response = odl_http_post(_url_template, {'node-id' : device_name}, 'application/json', request_content, expected_status_code=[204, 409])
    if response.status_code != 204:
        raise Exception(_error_message(response.json()))

def acl_delete(
    device_name,
    acl_name
):
    """ Delete the specified ACL from the specified device.
    
        No value is returned.
        An exception is raised if the ACL does not exist on the device.
        If the ACL is currently 'applied' then it is not deleted.
    """
    response = odl_http_delete(_url_named_acl, {'node-id' : device_name, 'access-id' : acl_name}, expected_status_code=[200, 500])
    if response.status_code != 200:
        raise Exception(_error_message(response.json()))

_url_acl_all_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ipv4-acl-cfg:ipv4-acl-and-prefix-list/accesses'

def acl_list(device_name):
    """ List the names of all ACLs on one network device."""
    return [acl['access-list-name'] for acl in acl_json_all(device_name)]

def acl_xml_all(device_name):
    'Return xml tree of all ACLs for the specified network device.'
    response = odl_http_get(_url_acl_all_template, {'node-id' : device_name}, 'application/xml')
    tree = etree.parse(BytesIO(response.content))
    return tree

def acl_json(
    device_name,
    acl_name
):
    ''' JSON representation of one ACL.
    
        Return JSON data structure if exists; otherwise None.
    '''
    url_params = {'node-id' : device_name, 'access-id' : acl_name}
    response = odl_http_get(_url_named_acl, url_params, 'application/json', expected_status_code=[200, 404])
    if response.status_code != 200:
        return None
    else:
        acl_list = response.json()
        return acl_list['access'][0]

def acl_json_all(device_name):
    """ List of ACLs on one network device.

        Return a list where each element is a JSON representation of an ACL.
    """
    response = odl_http_get(_url_acl_all_template, {'node-id' : device_name}, 'application/json', [200, 404])
    if response.status_code == 404:
        return []
    else:
        return response.json()['accesses']['access']

capability_ns = 'http://cisco.com/ns/yang/'
capability_name = 'Cisco-IOS-XR-ipv4-acl-cfg'

def inventory_acl(capability_revision=None, device_name=None):
    """ Determine which devices have ACL capability.
    
        A specific revision of the capability is optional.
        The discovery process can be scoped to a single device.
        Returns a list of device names. 
    """
    discoveries = capability_discovery(
        capability_name=capability_name,
        capability_ns=capability_ns,
        capability_revision=capability_revision,
        device_name=device_name)
    return [discovered.device_name for discovered in discoveries]

def acl_exists(
    device_name,
    acl_name
):
    """ Determine whether the specified ACL exists on the specified device. """
    response = odl_http_get(_url_named_acl, {'node-id' : device_name, 'access-id' : acl_name}, 'application/json', expected_status_code=[200, 404])
    return response.status_code == 200
