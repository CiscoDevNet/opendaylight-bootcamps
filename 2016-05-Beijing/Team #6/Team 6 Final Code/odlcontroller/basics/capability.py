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

from lxml import etree
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from basics.odl_http import odl_http_get
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
import re

_url_template = 'operational/opendaylight-inventory:nodes/node/{node-id}'

_short_name = re.compile(r'\(.*\)(.*)')

ns = {'i':'urn:opendaylight:inventory',
      'nni':'urn:opendaylight:netconf-node-inventory'}

def capability(device_name):
    'Return a list of capability names, given the name of a mounted, connected device.'
    response = odl_http_get(_url_template, {'node-id' : device_name}, 'application/xml')
    tree = etree.parse(StringIO(response.text))
    return [
        _short_name.match(long_name).group(1) 
        for long_name 
        in tree.xpath(".//nni:initial-capability/text()", namespaces=ns)]
    