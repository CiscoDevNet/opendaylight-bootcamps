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

from requests import post

_request_content_template = '''<?xml version="1.0" encoding="UTF-8"?>
<module xmlns="urn:opendaylight:params:xml:ns:yang:controller:config">
    <type
        xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">prefix:sal-netconf-connector</type>
    <name>%s</name>
    <address
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</address>
    <port
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</port>
    <username
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</username>
    <password
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">%s</password>
    <tcp-only
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">false</tcp-only>
    <event-executor
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:netty">prefix:netty-event-executor</type>
        <name>global-event-executor</name>
    </event-executor>
    <binding-registry
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:binding">prefix:binding-broker-osgi-registry</type>
        <name>binding-osgi-broker</name>
    </binding-registry>
    <dom-registry
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:md:sal:dom">prefix:dom-broker-osgi-registry</type>
        <name>dom-broker</name>
    </dom-registry>
    <client-dispatcher
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:config:netconf">prefix:netconf-client-dispatcher</type>
        <name>global-netconf-dispatcher</name>
    </client-dispatcher>
    <processing-executor
        xmlns="urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf">
        <type xmlns:prefix="urn:opendaylight:params:xml:ns:yang:controller:threadpool">
            prefix:threadpool</type>
        <name>global-netconf-processing-executor</name>
    </processing-executor>
</module>
'''

_url_template = 'http://%s:%d/restconf/config/opendaylight-inventory:nodes/node/controller-config/yang-ext:mount/config:modules'

_headers_template = {
    'Content-Type' : 'application/xml',
#    'Content-Length' : "%d"
}

def register_node(
    node_name,
    node_username,
    node_password,
    node_address,
    node_port,
    odl_username,
    odl_password,
    odl_address,
    odl_port
):
    request_data = _request_content_template % (node_name, node_address, node_port, node_username, node_password)
    url = _url_template % (odl_address, odl_port)
    response = post(url, headers=_headers_template, data=request_data)
    if response.status_code != 204:
        raise Exception('Expected HTTP status code 204, got %d' % response.status_code)
