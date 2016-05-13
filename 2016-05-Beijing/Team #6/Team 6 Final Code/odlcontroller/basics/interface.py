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

from __future__ import unicode_literals
from settings import config
from lxml import etree
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from basics.odl_http import odl_http_get, odl_http_put
from collections import namedtuple
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
from ipaddress import ip_interface, ip_network, ip_address
from basics.inventory import device_control

_network_device_config = config['network_device']

_interface_namespaces = {
    'i':'urn:opendaylight:inventory',
    'ifc':'http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg',
    'ipv4c':'http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg',
    'nni':'urn:opendaylight:netconf-node-inventory'}

_properties_url_template = 'operational/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ifmgr-oper:interface-properties'

_properties_uni_url_template = _properties_url_template + '/data-nodes/data-node/{data-node-id}/system-view/interfaces/interface/{interface-id}'

_configuration_multi_url_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations'

_configuration_uni_url_template = _configuration_multi_url_template + '/interface-configuration/{active}/{interface-id}'

def interface_names(device_name):
    'Return a list of interface names, given the name of a mounted, connected device.'
    response = odl_http_get(_properties_url_template, {'node-id' : device_name}, 'application/xml', expected_status_code=[200, 400])
    if response.status_code == 400:
        return []  # The inventory item does not have interfaces.
    tree = etree.parse(StringIO(response.text))
    namespace = tree.getroot().tag[1:].split("}")[0]
    ns = {'n':namespace}
    return tree.xpath(".//n:system-view//n:interface[n:encapsulation/text()='ether']/n:interface-name/text()", namespaces=ns)

def management_interface(device_name):
    'Return the name of the interface that is used to manage the specified network device.'
    control = device_control(device_name)
    if(not control):
        return None
    response = odl_http_get(_configuration_multi_url_template, {'node-id' : device_name}, 'application/xml', expected_status_code=[200, 400])
    if response.status_code == 400:
        return None  # The specified device does not have interfaces.
    if device_name in _network_device_config.keys():
        device_address = _network_device_config[device_name]['address']
    else:
        device_address = None  # Discovered or configured independently.
    tree = etree.parse(StringIO(response.text))
    for ifc in tree.xpath("/ifc:interface-configurations/ifc:interface-configuration", namespaces=_interface_namespaces):
        for ipv4 in ifc.xpath('ipv4c:ipv4-network/ipv4c:addresses/*', namespaces=_interface_namespaces):
            address = ipv4.findtext('ipv4c:address', namespaces=_interface_namespaces)
            netmask = ipv4.findtext('ipv4c:netmask', namespaces=_interface_namespaces)
            if address == control.address:
                return ifc.findtext('ifc:interface-name', namespaces=_interface_namespaces)
    return None

def same_subnet(address1, address2, netmask):
    'Return True if both addresses are on the same subnet.'
    if address1 == 'localhost':
        return same_subnet('127.0.0.1', address2, netmask)
    if address2 == 'localhost':
        return same_subnet(address1, '127.0.0.1', netmask)
    subnet1 = ip_network(u'%s/%s' % (address1, netmask), strict=False)
    subnet2 = ip_network(u'%s/%s' % (address2, netmask), strict=False)
    return subnet1 == subnet2

def interface_configuration_http(content_type, device_name, interface_name=None):
    '''Return the HTTP request and response, for interface configuration, for the specified, mounted device 
    and (optionally) the specified interface.'''
    if interface_name is None:
        return odl_http_get(_configuration_multi_url_template, {'node-id' : device_name}, content_type)
    else:
        url_params = {'node-id' : device_name, 'active' : 'act', 'interface-id' : interface_name}
        return odl_http_get(_configuration_uni_url_template, url_params, content_type)

def interface_configuration_xml_http(device_name, interface_name=None):
    '''Return the HTTP XML request and response, for interface configuration, for the specified, mounted device
    and (optionally) the specified interface.'''
    return interface_configuration_http('application/xml', device_name, interface_name)

def interface_configuration_json_http(device_name, interface_name=None):
    '''Return the HTTP JSON request and response, for interface configuration, for the specified, mounted device 
    and (optionally) the specified interface.'''
    return interface_configuration_http('application/json', device_name, interface_name)

def interface_configurations_xml_http(device_name):
    'deprecated'
    return interface_configuration_xml_http(device_name)

def interface_configuration_xml(device_name, interface_name=None):
    '''Return a XML document containing interface configuration for the specified, mounted device 
    and (optionally) the specified interface.'''
    response = interface_configuration_xml_http(device_name, interface_name)
    #print(response.text)
    return etree.parse(StringIO(response.text))

def interface_configurations_xml(device_name):
    'deprecated'
    return interface_configuration_xml(device_name)

def interface_configurations_json_http(device_name):
    'deprecated'
    return interface_configuration_json_http(device_name)

def interface_configuration_json(device_name, interface_name=None):
    '''Return a JSON document containing interface configuration for the specified, mounted device 
    and (optionally) the specified interface.'''
    return interface_configuration_json_http(device_name, interface_name).json();

def interface_configurations_json(device_name):
    'Return a JSON document containing interface configuration for the specified, mounted device.'
    return interface_configuration_json_http(device_name).json();

# Implementation note: define the named tuple separately so that it is fully
# formed when used as a super-class. This helps Eclipse IDE to understand it.
# Otherwise Eclipse IDE shows an error related to class attribute _fields.
InterfaceConfiguration = namedtuple('InterfaceConfiguration', 
[
    'name', 
    'description', 
    'shutdown', 
    'address', 
    'netmask', 
    'packet_filter_outbound', 
    'packet_filter_inbound', 
    'active'
])
                       
class InterfaceConfiguration(InterfaceConfiguration):
    """
    Immutable class/tuple encapsulating the configuration of one network interface.
    """
    @property
    def ip_network(self): 
        """
        Convenience property returning the ip_network as per module ipaddress.
        """
        return None if self.address is None or self.netmask is None \
        else ip_network(u'%s/%s' % (self.address, self.netmask), strict=False)

    @property
    def ip_address(self): 
        """
        Convenience property returning the ip_address as per module ipaddress.
        """
        return None if self.address is None or self.netmask is None \
        else ip_address(u'%s/%s' % self.address)

    @property
    def ip_interface(self): 
        """
        Convenience property returning the ip_interface as per module ipaddress.
        """
        return None if self.address is None or self.netmask is None \
        else ip_interface(u'%s/%s' % (self.address, self.netmask))

def interface_configuration_tuple_from_xml(tree):
    'Return a named tuple containing the configuration information in the specified XML.'
    result = InterfaceConfiguration(
        name=tree.findtext('{*}interface-name'),
        description=tree.findtext('{*}description'),
        packet_filter_outbound=tree.findtext('{*}ipv4-packet-filter/{*}outbound/{*}name'),
        packet_filter_inbound=tree.findtext('{*}ipv4-packet-filter/{*}inbound/{*}name'),
        active=tree.findtext('{*}active'),
        shutdown=tree.find('{*}shutdown') is not None,
        address=tree.findtext('.//{*}primary/{*}address'),
        netmask=tree.findtext('.//{*}primary/{*}netmask'))
    return result

def interface_configuration_tuple(
    device_name,
    interface_name=None
):
    'Return a named tuple containing the configuration information for the specified interface of the specified, mounted device.'
    xml = interface_configuration_xml(device_name, interface_name)
    if interface_name is None:
        return [interface_configuration_tuple_from_xml(config) for config in xml.iterfind('{*}interface-configuration')]
    else:
        return interface_configuration_tuple_from_xml(xml)

_configurations_xsl = u'''\
<?xml version="1.0" ?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:ifc="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"
xmlns:ipv4="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg"
exclude-result-prefixes="ifc ipv4">

<xsl:output method="html" encoding="UTF-8" omit-xml-declaration="yes"/>

<xsl:template match="/">
<table border="1">
    <thead>
        <tr style="background-color:lightgray;">
          <th style="text-align:left;" rowspan="2">Name</th>
          <th style="text-align:left;" rowspan="2">Description</th>
          <th style="text-align:center;" rowspan="2">Shutdown</th>
          <th style="text-align:left;" rowspan="2">Address</th>
          <th style="text-align:left;" rowspan="2">Netmask</th>
          <th style="text-align:center;" colspan="2">Packet Filter</th>
        </tr>
        <tr style="background-color:lightgray;">
          <th style="text-align:center;">In</th>
          <th style="text-align:center;">Out</th>
        </tr>
    </thead>
    <tbody>
        <style>tr:nth-of-type(even) {background-color:#eee;}</style>
<xsl:for-each select=".//ifc:interface-configuration">
<xsl:sort select="ifc:interface-name"/>
        <tr>
            <td style="text-align:left;"><xsl:value-of select="ifc:interface-name"/></td>
            <td style="text-align:left;"><xsl:value-of select="ifc:description"/></td>
            <td style="text-align:center;"><xsl:value-of select="boolean(ifc:shutdown)"/></td>
            <td style="text-align:left;"><xsl:value-of select=".//ipv4:primary/ipv4:address"/></td>
            <td style="text-align:left;"><xsl:value-of select=".//ipv4:primary/ipv4:netmask"/></td>
            <td style="text-align:center;"><xsl:value-of select=".//ipv4-packet-filter/ipv4:inbound/ipv4:name"/></td>
            <td style="text-align:center;"><xsl:value-of select=".//ipv4-packet-filter/ipv4:outbound/ipv4:name"/></td>
        </tr>
</xsl:for-each>
    </tbody>
  </table>
</xsl:template>
</xsl:stylesheet>
'''

# XSL parsed and compiled.
_configurations_xslt = etree.XSLT(etree.fromstring(_configurations_xsl))

def interface_configuration_to_html(xml):
    'Return a HTML table containing interface configuration, given a XML representation of the configuration.'
    return _configurations_xslt(xml)

def interface_configuration_update(
    device_name,
    interface_name,
    description=None,
    address=None,
    netmask=None,
    active='act',
    shutdown=False
):
    '''Update the configuration of the specified interface of the specified device.
    
    The outcome is undefined if the specified device is not connected. 
    '''
    fields = {"interface-name": interface_name}
    if shutdown:
        fields["shutdown"] = ""
    if active:
        fields["active"] = active
    if description:
        fields["description"] = description
    if address or netmask:
        primary = {}
        if address:
            primary["address"] = address
        if netmask:
            primary["netmask"] = netmask
        #TODO test if address is IPv4 or IPv6
        fields["Cisco-IOS-XR-ipv4-io-cfg:ipv4-network"] = {
            "addresses": {
                "primary": primary
            }
        } 
    request_content = {"interface-configuration": [fields]}
    url_params = {'node-id' : device_name, 'active' : active, 'interface-id' : interface_name}
    odl_http_put(_configuration_uni_url_template, url_params, 'application/json', request_content, expected_status_code=200)

def interface_properties_http(content_type, device_name, interface_name=None):
    '''Return the HTTP request and response, for interface properties, for the specified, mounted device 
    and (optionally) the specified interface.'''
    if interface_name is None:
        return odl_http_get(_properties_url_template, {'node-id' : device_name}, content_type)
    else:
        url_params = {'node-id' : device_name, 'interface-id' : interface_name}
        return odl_http_get(_properties_uni_url_template, url_params, content_type)

def interface_properties_xml_http(device_name, interface_name=None):
    '''Return the HTTP XML request and response, for interface properties, for the specified, mounted device 
    and (optionally) the specified interface.'''
    return interface_properties_http('application/xml', device_name, interface_name)

def interface_properties_json_http(device_name, interface_name=None):
    '''Return the HTTP JSON request and response, for interface properties, for the specified, mounted device 
    and (optionally) the specified interface.'''
    return interface_properties_http('application/json', device_name, interface_name)

def interface_properties_xml(device_name, interface_name=None):
    '''Return a XML document containing interface properties for the specified, mounted device
    and (optionally) the specified interface.'''
    response = interface_properties_xml_http(device_name, interface_name)
#     print response.text
    return etree.parse(StringIO(response.text))

def interface_properties_json(device_name, interface_name=None):
    '''Return a JSON document containing interface properties for the specified, mounted device 
    and (optionally) the specified interface.'''
    return interface_properties_json_http(device_name, interface_name).json()

InterfaceProperties = namedtuple('InterfaceProperties', [
    'name',
    'type',
    'bandwidth',
    'encapsulation',
    'encapsulation_type',
    'state',  # physical state
    'line_state',  # layer 2 state
    'actual_state',
    'actual_line_state',
    'l2_transport',
    'mtu',
    'sub_interface_mtu_overhead'])

def interface_properties_from_json(json):
    'Return a named tuple containing the information available in the specified JSON.'
    return InterfaceProperties(
        name=json['interface-name'],
        type=json['type'],
        bandwidth=json['bandwidth'],
        encapsulation=json['encapsulation'],
        encapsulation_type=json['encapsulation-type-string'],
        state=json['state'],
        line_state=json['line-state'],
        actual_state=json['actual-state'],
        actual_line_state=json['actual-line-state'],
        l2_transport=json['l2-transport'],
        mtu=json['mtu'],
        sub_interface_mtu_overhead=json['sub-interface-mtu-overhead'])

def interface_properties_tuple(
    device_name,
    interface_name=None
):
    '''Return a tuple of the interface properties for the specified, mounted device.
    A single tuple is returned if the interface name is specified, otherwise a list
    of one tuple per interface is returned.'''
    # Implementation Note: Use JSON not XML because it determines the type of each field value.
    json = interface_properties_json(device_name, interface_name)
    if interface_name is None:
        return [interface_properties_from_json(props) for props in json[u'interface-properties'][u'data-nodes'][u'data-node'][0][u'system-view'][u'interfaces'][u'interface']]
    else:
        return interface_properties_from_json(json['interface'][0])

_properties_xsl = '''\
<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:ifo="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-oper"
exclude-result-prefixes="ifo">

<xsl:output method="html" encoding="UTF-8" omit-xml-declaration="yes"/>

<xsl:template match="ifo:interface" mode="first_batch">
        <tr>
            <td style="text-align:left;"><xsl:value-of select="ifo:interface-name"/></td>
            <td style="text-align:left;"><xsl:value-of select="ifo:type"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:bandwidth"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:encapsulation"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:encapsulation-type-string"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:l2-transport"/></td>
        </tr>
</xsl:template>

<xsl:template match="ifo:interface" mode="second_batch">
        <tr>
            <td style="text-align:left;"><xsl:value-of select="ifo:interface-name"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:state"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:line-state"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:actual-state"/></td>
            <td style="text-align:center;"><xsl:value-of select="ifo:actual-line-state"/></td>
            <td style="text-align:right;"><xsl:value-of select="ifo:mtu"/></td>
        </tr>
</xsl:template>

<xsl:template match="/">
<table border="1">
    <thead>
        <tr style="background-color:lightgray;">
          <th style="text-align:left;">Name</th>
          <th style="text-align:center;">Type</th>
          <th style="text-align:right;">Bandwidth</th>
          <th style="text-align:center;" colspan="2">Encapsulation</th>
          <th style="text-align:center;">L2 Transport</th>
        </tr>
    </thead>
    <tbody>
        <style>tr:nth-of-type(even) {background-color:#eee;}</style>
<xsl:apply-templates select=".//ifo:system-view/ifo:interfaces/ifo:interface" mode="first_batch">
    <xsl:sort select="ifo:interface-name"/>
</xsl:apply-templates>
<xsl:apply-templates select="./ifo:interface" mode="first_batch" />
    </tbody>
  </table>
  <p/>
  <table border="1">
    <thead>
        <tr style="background-color:lightgray;">
          <th style="text-align:left;">Name</th>
          <th style="text-align:center;">State</th>
          <th style="text-align:center;">Line State</th>
          <th style="text-align:center;">Actual State</th>
          <th style="text-align:center;">Actual Line State</th>
          <th style="text-align:right;">MTU</th>
        </tr>
    </thead>
    <tbody>
        <style>tr:nth-of-type(even) {background-color:#eee;}</style>
<xsl:apply-templates select=".//ifo:system-view/ifo:interfaces/ifo:interface" mode="second_batch">
    <xsl:sort select="ifo:interface-name"/>
</xsl:apply-templates>
<xsl:apply-templates select="./ifo:interface" mode="second_batch" />
    </tbody>
  </table>
</xsl:template>
</xsl:stylesheet>
'''

# XSL parsed and compiled.
_properties_xslt = etree.XSLT(etree.fromstring(_properties_xsl))

def interface_properties_to_html(xml):
    'Return a HTML table containing interface properties, given a XML representation of the properties.'
    return _properties_xslt(xml)
