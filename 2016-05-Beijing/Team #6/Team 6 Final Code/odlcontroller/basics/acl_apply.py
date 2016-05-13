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

from __future__ import print_function as _print_function
from basics.odl_http import odl_http_post, odl_http_delete
import json
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

_request_content_acl_packet_filter_template = '''
{"Cisco-IOS-XR-ifmgr-cfg:interface-configuration":[{"active":"act","interface-name":"%s","Cisco-IOS-XR-ip-pfilter-cfg:ipv4-packet-filter":{"%s":{"name":"%s"}}}]}'''

_url_apply_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations'

def acl_apply_packet_filter(
    device_name,
    interface_name,
    bound,
    acl_name
):
    request_content = _request_content_acl_packet_filter_template % (interface_name, bound, acl_name)
#     print url_suffix
#     print json.dumps(json.loads(request_content),indent=2)
    response = odl_http_post(_url_apply_template, {'node-id' : device_name}, 'application/json', request_content)
    if response.status_code != 204:
        raise Exception(response.text)

_url_unapply_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations/interface-configuration/act/{interface-id}/ipv4-packet-filter/{bound}'

def acl_unapply_packet_filter(
    device_name,
    interface_name,
    bound,
    acl_name
):
    url_params = {'node-id' : device_name, 'interface-id' : interface_name, 'bound' : bound}
    odl_http_delete(_url_unapply_template, url_params, expected_status_code=200)
