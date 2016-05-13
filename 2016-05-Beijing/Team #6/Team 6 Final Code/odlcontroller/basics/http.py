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

from requests import Response
import json
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
from lxml import etree
from xml.sax.saxutils import escape

_http_header_table_template = '''\
<table>
%s
</table>
'''

_http_header_table_row_template = '''\
    <tr>
        <td>
            %s
        </td>
        <td>
            %s
        </td>
    </tr>
'''

def http_headers_transform(headers):
#     return '; '.join([k + '=' + v for (k, v) in headers.items()])
    return _http_header_table_template % ''.join([_http_header_table_row_template % (k, v) for (k, v) in headers.items()])

def http_content_transform(headers, content):
    if content is None or not content:
        return ''
    elif 'Content-Type' in headers:
        contentType = headers['Content-Type']
        if contentType.endswith("/json"):
            content_json = json.loads(content if isinstance(content, str) else content.decode('utf-8'))
            return '<pre>' + json.dumps(content_json, sort_keys=False, indent=2, separators=(',', ': ')) + '</pre>'
        elif contentType.endswith('/xml'):
            try:
                parser = etree.XMLParser(remove_blank_text=True)
                tree = etree.parse(BytesIO(content) if isinstance(content, (bytes, bytearray)) else StringIO(content),
                                   parser=parser)
                xml_bytes = etree.tostring(tree, pretty_print=True, xml_declaration=True)
                xml_str = xml_bytes.decode("utf-8")
                html_str = escape(xml_str)
                return '<pre>' + html_str + '</pre>'
            except Exception as e:
                # Swallow the exception thrown by the XMLParser and abandon XML.                 
                return '<xmp>' + str(e) + '</xmp>'
    return '<xmp>' + str(content) + '</xmp>'

# deprecated in favour of simpler alternative (sans 90 degree headings).
_http_table_template_90_degrees = '''\
<table border="1" >
  <style>tr:nth-of-type(even) {background-color:#eee;}</style>
  <style>tr:nth-of-type(odd) {background-color:#fff;}</style>
  <tr>
    <th style="text-align:left;transform:rotate(-90deg);" rowspan="4">Request</th>
    <th style="text-align:left;background-color:lightgray;">Method</th>
    <td>%s</td>
  </tr>
  <tr>
    <th style="text-align:left;background-color:lightgray;">URL</th>
    <td>%s</td>
  </tr>
  <tr>
    <th style="text-align:left;background-color:lightgray;">Headers</th>
    <td>%s</td>
  </tr>
  <tr>
    <th style="text-align:left;background-color:lightgray;">Content</th>
    <td>%s</td>
  </tr>
  <tr>
    <th style="text-align:left;transform:rotate(-90deg);" rowspan="3">Response</th>
    <th style="text-align:left;background-color:lightgray;">Status Code</th>
    <td>%s</td>
  </tr>
  <tr>
    <th style="text-align:left;background-color:lightgray;">Headers</th>
    <td>%s</td>
  </tr>
  <tr>
    <th style="text-align:left;background-color:lightgray;">Content</th>
    <td>%s</td>
  </tr>
</table>
'''

_http_table_template = '''\
<table>
  <style>table {border: 1px solid black;}</style>
  <style>tr:nth-of-type(even) {background-color:#eee;}</style>
  <style>tr:nth-of-type(odd) {background-color:#fff;}</style>
  <style>th {background-color:lightgray;}</style>
  <thead>
    <tr>
      <th style="text-align:center" colspan="2">Request</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Method</th>
      <td>%s</td>
    </tr>
    <tr>
      <th>URL</th>
      <td>%s</td>
    </tr>
    <tr>
      <th>Headers</th>
      <td>%s</td>
    </tr>
    <tr>
      <th>Content</th>
      <td>%s</td>
    </tr>
  </tbody>
  <thead>
      <tr>
        <th style="text-align:center;background-color:white" colspan="2"/>
      </tr>
      <tr>
        <th style="text-align:center" colspan="2">Response</th>
      </tr>
  </thead>
  <tbody>
    <tr>
      <th>Status Code</th>
      <td>%s</td>
    </tr>
    <tr>
      <th>Headers</th>
      <td>%s</td>
    </tr>
    <tr>
      <th>Content</th>
      <td>%s</td>
    </tr>
  </tbody>
</table>
'''

# deprecated. renamed http_to_html
def http_html(http):
    return http_to_html(http)

def http_to_html(http):
    'Return the HTML representation/view of a HTTP request and response.'
    if isinstance(http, Response):
        return _http_table_template % (
            http.request.method,
            http.url,
            http_headers_transform(http.request.headers),
            http_content_transform(http.request.headers, http.request.body),
            http.status_code,
            http_headers_transform(http.headers),
            http_content_transform(http.headers, http.content)
        )
    else:
        return str(http)
    

def http_to_html_with_index(http, i, n):
    '''Prefix HTML of HTTP with an index.
    
    Parameter i: 1-based index of current item
    Parameter n: total number of items
    '''
    html = 'HTTP request/response: '
    for j in range(1, i):
        html += '<A href="#http' + str(j) + '">' + str(j) + '</A>&nbsp;'
    html += str(i) + '&nbsp;'
    for j in range(i + 1, n + 1):
        html += '<A href="#http' + str(j) + '">' + str(j) + '</A>&nbsp;'
    return html + '<BR id="http' + str(i) + '"/>' + http_to_html(http)

def http_history_to_html(http_history):
    '''Return the HTML representation/view of multiple HTTP requests and responses.
    
    Parameter 'http_history' is a list.
    '''
    N = len(http_history)
    if N == 0:
        return 'No HTTP requests occurred.'
    elif N == 1:
        return http_to_html(http_history[0])
    else:
        html = "<DIV>"
        i = 1
        for http in http_history:
            html += http_to_html_with_index(http, i, N)
            i += 1
        html += "</DIV>"
        return html

def json_loads(s, encoding=None):
    """Replace newline characters with the escape sequence then loads normally."""
    return json.loads(s.replace('\n', '\\n'),encoding)

#def json_dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
#        allow_nan=True, cls=None, indent=None, separators=None,
#        default=None, sort_keys=False, **kw):
#    """Exactly the same as json.dumps."""
#    # Beware that json.dumps signature is different for Python 2 and 3.
#    return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default, sort_keys=sort_keys)

    
