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

from lxml import etree
from collections import namedtuple
from basics.odl_http import odl_http_get, odl_http_post, odl_http_delete
from settings import config
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
    
def inventory_json_http():
    'Return a HTTP request/response pair for the inventory items in JSON representation.'
    return odl_http_get(_url_inventory, accept='application/json')

def inventory_json():
    'Return a list of inventory items in JSON representation.'
    response = inventory_json_http()
    return response.json()['nodes']['node']

def inventory_xml_http():
    'Return a HTTP request/response pair for the inventory items in XML representation.'
    return odl_http_get(_url_inventory, accept='application/xml')

def inventory_xml():
    'Return a XML tree representation of the inventory items.'
    response = inventory_xml_http()
    return etree.parse(BytesIO(response.content) if isinstance(response.content, (bytes, bytearray)) else StringIO(response.content))

def inventory():
    '''Names of network devices known to the Controller.
    
    The inventory includes all mounted devices.
    The inventory excludes all unmounted devices.
    The inventory includes all connected devices.
    The inventory can contain unconnected devices.

    The inventory can contain devices that are introduced independently of the
    Controller's mounting process. 
    Examples of these devices are Open Flow switches.
    Such devices have the following characteristics:
    - not considered to be 'mounted' (see function 'inventory_mounted')
    - no 'control' information available (see function 'inventory_control')
    - not considered to be 'unmounted' because there are no settings configured
      (see function 'inventory_unmounted')
    - cannot be mounted (because not unmounted)
    - cannot be dismounted (because not mounted)

    Returns type is list, which may be empty.
    '''
    tree = inventory_xml()
    names = tree.xpath("i:node/i:id/text()", namespaces=_inventory_namespaces)
    names = [node for node in names if node != 'controller-config']
    return names

def inventory_connected():
    '''Names of network devices connected to the Controller.
    
    Output a list of names.
    Connected devices are a subset of the inventory.
    '''
    tree = inventory_xml()
    names = tree.xpath("i:node[nni:connected/text()='true']/i:id/text()", namespaces=_inventory_namespaces)
    names = [node for node in names if node != 'controller-config']
    return names

def inventory_not_connected():
    '''Names of network devices mounted on the Controller but not connected to the Controller.'''
    tree = inventory_xml()
    return tree.xpath("i:node[not(nni:connected/text()='true')]/i:id/text()", namespaces=_inventory_namespaces)

def connected(device_name):
    '''Determine whether a single device is connected to the Controller.
    
    Return True if connected.
    '''
    response = odl_http_get(_url_inventory_node, {'node-id' : device_name}, 'application/xml', expected_status_code=(200, 404))
    if response.status_code == 404:
        return False
    tree = etree.parse(StringIO(response.text))
    names = tree.xpath("/i:node[nni:connected/text()='true']/i:id/text()", namespaces=_inventory_namespaces)
    return len(names) > 0

# Implementation note: define the named tuple separately so that it is fully
# formed when used as a super-class. This helps Eclipse IDE to understand it.
# Otherwise Eclipse IDE shows an error related to class attribute _fields.
DeviceControl = namedtuple('DeviceControl',
[
    'device_name',
    'address',
    'port',
    'username',
    'password'
])

class DeviceControl(DeviceControl):
    """Properties of a connection to a management interface to control a device."""
    pass
        
def device_control(device_name):
    """A DeviceControl if the specified device is mounted, otherwise None."""
    response = odl_http_get(_url_connector, {'node-id':device_name}, 'application/xml', expected_status_code=[200, 404])
    if response.status_code == 404:
        return None
    tree = etree.parse(BytesIO(response.content))
    # print(etree.tostring(tree, pretty_print=True, xml_declaration=True))
    module_name = tree.findtext('/m:name', namespaces=_inventory_namespaces)
    assert module_name == device_name
    address = tree.findtext('/c:address', namespaces=_inventory_namespaces)
    port = tree.findtext('/c:port', namespaces=_inventory_namespaces)
    username = tree.findtext('/c:username', namespaces=_inventory_namespaces)
    password = tree.findtext('/c:password', namespaces=_inventory_namespaces)
    return DeviceControl(device_name, address=address, port=int(port), username=username, password=password)

def inventory_control():
    """ List the DeviceControl for every mounted device.
    
        Return type is 'list of DeviceControl'.
        If no devices are mounted the list returned is empty.
    """
    return [device_control(device_name) for device_name in inventory_mounted()]

def mounted_xml_http():
    'Return a HTTP request/response pair for the mounted items, in XML representation.'
    return odl_http_get(_url_mounted, accept='application/xml')

def mounted_xml():
    'Return a XML tree representation of the mounted items.'
    response = mounted_xml_http()
    return etree.parse(StringIO(response.text))

def inventory_mounted():
    '''Names of network devices mounted on the Controller.

    Output a list of names.
    Mounted devices are a subset of the inventory.
    Mounted devices can be connected or not.
    '''
    tree = mounted_xml()
    names = tree.xpath("i:node/i:id/text()", namespaces=_inventory_namespaces)
    names = [node for node in names if node != 'controller-config']
    return names

def mounted(device_name):
    '''Determine whether a single device is mounted on the Controller.
    
    Return True if mounted.
    '''
    response = odl_http_get(_url_connector, {'node-id' : device_name}, 'application/xml', expected_status_code=[200, 404])
    return response.status_code == 200

def inventory_unmounted():
    '''    
        Names of network devices not mounted on the Controller.
    
        Returns a list.
    '''
    configured = config['network_device'].keys()
    mounted_list = inventory_mounted()
    unmounted_list = list(set(configured) - set(mounted_list)) if mounted_list else list(configured)
    return unmounted_list

InventorySummary = namedtuple('InventorySummary',
[
    'name',
    'connected',
    'capabilities'
])

def inventory_summary_from_xml(xml):
#     xml_bytes = etree.tostring(xml, pretty_print=True, xml_declaration=True)
#     xml_str = xml_bytes.decode("utf-8")
#     print(xml_str)
    return [ 
        InventorySummary(
            name=item.findtext('i:id', namespaces=_inventory_namespaces),
            connected=item.findtext('nni:connected', namespaces=_inventory_namespaces) == 'true',
            capabilities=int(
                item.xpath('count(nni:initial-capability)', namespaces=_inventory_namespaces) + 
                item.xpath('count(fi:switch-features/fi:capabilities)', namespaces=_inventory_namespaces)
            )
        ) for item in xml.iterfind('i:node', namespaces=_inventory_namespaces)
    ]

def inventory_summary():
    ''''Return a list containing one instance of InventorySummary per inventory item.
    '''
    return inventory_summary_from_xml(inventory_xml())

def capability(device_name):
    """Return a list of capability names for the specified device.
    
    This function is superseded by capability_discovery.
    It has not been removed because it discovers OpenFlow capabilities,
    which fn capability_discovery does not yet do.
    """
    response = odl_http_get(_url_inventory_node, {'node-id' : device_name}, 'application/xml')
    tree = etree.parse(StringIO(response.text))
    initial_capability_list = tree.xpath(".//nni:initial-capability/text()", namespaces=_inventory_namespaces)
    if initial_capability_list:
        return initial_capability_list
    else:
        return tree.xpath(".//fi:switch-features/fi:capabilities/text()", namespaces=_inventory_namespaces)

# One capability of one device.
DeviceCapability = namedtuple('DeviceCapability', [
    'device_name',
    'capability'])

# One capability
Capability = namedtuple('Capability', [
    'name',
    'namespace',
    'revision'])

import re

_capability_pattern = re.compile(r'\((.*)\?revision\=(.*)\)(.*)')

class CapabilityDiscovery(object):
    def __init__(self, capability_name=None, capability_ns=None, capability_revision=None, device_name=None):
        
        # Field values that must match to accept a discovered capability for each device.
        # Each field value can be None to allow any value to pass (wildcard).
        self.capability_name = capability_name
        self.capability_ns = capability_ns
        self.capability_revision = capability_revision
        self.device_name = device_name

        # Field values discovered.
        self.node_id = None
        
        # Flags indicating nested path.
        self.in_nodes = bool(device_name)
        self.in_node = False
        self.in_id = False
        self.in_capability = False
        
        # List of (device_name, capability) discovered and accepted.
        self.discovered = []
        
    def start(self, tag, attrib):
        if tag.endswith('nodes'):
            self.in_nodes = True
        elif self.in_nodes and tag.endswith('node'):
            self.in_node = True
        elif self.in_node:
            if tag.endswith('id'):
                self.in_id = True
            elif tag.endswith('capability'):
                self.in_capability = (self.device_name is None or self.node_id == self.device_name)
    
    def end(self, tag):
        if tag.endswith('nodes'):
            self.in_nodes = False
        elif self.in_nodes and tag.endswith('node'):
            self.in_node = False
        elif self.in_node:
            if tag.endswith('id'):
                self.in_id = False
            elif tag.endswith('capability'):
                self.in_capability = False
    
    def data(self, data):
        if self.in_id:
            self.node_id = data
        elif self.in_capability:
            capability_text = data
            parts = self.parts(capability_text)
            accept = parts is not None
            if accept and self.capability_name:
                accept = parts[0] == self.capability_name
            if accept and self.capability_ns:
                accept = parts[1] == self.capability_ns
            if accept and self.capability_revision:
                accept = parts[2] == self.capability_revision
            if accept:
                self.discovered.append(DeviceCapability(self.node_id, parts))
    
    def close(self):
        return self.discovered
    
    def parts(self, entire_capability):
        match = _capability_pattern.match(entire_capability)
        if not match:
            return None
        full_name = match.group(1)
        revision = match.group(2)
        short_name = match.group(3)
        # truncate redundant information from tail of full_name
        ns = full_name[:-len(short_name)] if full_name.endswith(short_name) else full_name
        return Capability(short_name, ns, revision)

def capability_discovery(capability_name=None, capability_ns=None, capability_revision=None, device_name=None):
    '''
    Discover network capability.
    
    Parameters:
    - device_name
        If specified then other network devices are excluded.
    - capability_name
        For example, 'Cisco-IOS-XR-cdp-oper'.
        If specified then non-matching capabilities are excluded.
    - capability_ns
        The name-space, such as 'http://cisco.com/ns/yang/'.
        If specified then non-matching capabilities are excluded.
    - capability_revision
        Type string but usually represents a day, such as '2015-01-07'.
        If specified then non-matching capabilities are excluded.
        There is no ability to search for a range of revisions,
        such as 'on or after 2015-01-07'. To achieve this, leave this
        parameter unspecified then apply a filter to the output.

    Returns a list of nested, named tuples, structured as follows:
        (device-name, (capability-name, capability-ns, capability-revision)). 
    '''
    parser = etree.XMLParser(target=CapabilityDiscovery(capability_name, capability_ns, capability_revision, device_name))
    if device_name:
        response = odl_http_get(_url_inventory_node, {'node-id' : device_name}, 'application/xml', expected_status_code=(200, 404))
        if response.status_code == 404:
            return []
    else:
        response = inventory_xml_http()

    # When iterated over, 'results' will contain the output from 
    # target parser's close() method
    discoveries = etree.parse(BytesIO(response.content), parser=parser)

    # Filter out the internal components of the ODL Controller.
    discoveries = [discovered for discovered in discoveries if discovered[0] != 'controller-config']
    return discoveries

def device_mount_http(
    device_name,
    device_address,
    device_port,
    device_username,
    device_password
):
    request_content = _request_content_mount_template % (device_name, device_address, device_port, device_username, device_password)
    return odl_http_post(_url_mount, {}, 'application/xml', request_content)

def device_mount(
    device_name,
    device_address,
    device_port,
    device_username,
    device_password
): 
    'Add the specified network device to the inventory of the Controller.'
    device_mount_http(
        device_name,
        device_address,
        device_port,
        device_username,
        device_password
    )

def device_dismount(
    device_name
):
    """    Remove one network device from the inventory of the Controller.
    
    It is not necessary for the device to be connected. 
    The outcome is undefined if the device is not already mounted.
    """
    odl_http_delete(_url_connector, {'node-id' : device_name}, 'application/xml', expected_status_code=200)

_inventory_namespaces = {
    'fi':'urn:opendaylight:flow:inventory',
    'i':'urn:opendaylight:inventory',
    'm':'urn:opendaylight:params:xml:ns:yang:controller:config',
    'c':'urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf',
    'nni':'urn:opendaylight:netconf-node-inventory'}

_url_inventory = 'operational/opendaylight-inventory:nodes'

_url_inventory_node = _url_inventory + '/node/{node-id}'

_url_mounted = 'config/opendaylight-inventory:nodes'

_url_mount = _url_mounted + '/node/controller-config/yang-ext:mount/config:modules'

_url_connector = _url_mount + '/module/odl-sal-netconf-connector-cfg:sal-netconf-connector/{node-id}'

_request_content_mount_template = '''<?xml version="1.0"?>
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
