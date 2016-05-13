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

''' HTTP API of ODL
    
    @author: Ken Jarrad (kjarrad@cisco.com)
'''

from __future__ import print_function
from past.builtins import basestring
from threading import Lock
from requests import request, ConnectionError
from requests.auth import HTTPBasicAuth
#from basics.http import json_loads, json_dumps
import json

try:
    import Queue as queue
except ImportError:
    import queue


_url_template = 'http://%s:%d/restconf/%s'

_http_history = queue.Queue(20)
_http_history_lock = Lock()

from collections import namedtuple
ControllerCoordinates = namedtuple('ControllerCoordinates', ['url_prefix', 'username', 'password'])
default_coordinates = ControllerCoordinates(
    url_prefix='http://localhost:8181/restconf/',
    username='admin',
    password='admin')
coordinates = None

def http_history_append(http):
    '''Append one HTTP request to the historical record.
    
    If the historical record reaches capacity the oldest HTTP request is removed and discarded.
    '''
    _http_history_lock.acquire()
    try:
        if _http_history.full():
            # discard oldest.             
            _http_history.get_nowait()
        _http_history.put_nowait(http)
        # print(_http_history.qsize())
    finally:
        _http_history_lock.release()

    
def http_history():
    '''Remove all HTTP requests from the historical record and return them.
    
    Result is a list of zero or more HTTP requests.
    Order of list is chronological. Oldest in element zero.
    '''
    popped = []
    _http_history_lock.acquire()
    try:
        while not _http_history.empty():
            popped.append(_http_history.get_nowait())
    finally:
        _http_history_lock.release()
    return popped

def http_history_clear():
    '''Remove all HTTP requests from the historical record and discard them.'''
    _http_history_lock.acquire()
    try:
        while not _http_history.empty():
            _http_history.get_nowait()
    finally:
        _http_history_lock.release()

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
url_encode = quote_plus

def odl_http_request(
    method,
    url_suffix,
    url_params,
    contentType,
    content,
    accept,
    expected_status_code
):
    'Request a response from the ODL server.'
    assert coordinates, "Import module 'settings' to configure Controller's coordinates."
    url = coordinates.url_prefix + url_suffix
    if url_params:
        assert isinstance(url_params, dict), 'Expect url_params to be %s, got %s' % (dict, type(url_params))
        # Note: in the line below I am using 'items()' because it works for Python 2 and 3.
        #       In Python 2 it creates a duplicate of the dict which is inefficient.                   
        url_params = {k:url_encode(str(v)) for k, v in url_params.items()}
        url = url.format(**url_params)
    headers = {}
    if accept is not None:
        headers['Accept'] = accept
    if contentType is not None:
        headers['Content-Type'] = contentType
    if content is not None:
        if not isinstance(content, basestring):
            if contentType.endswith('json'):
                content = json_dumps(content) 
        headers['Content-Length'] = len(content)
    try:
        response = request(
            method,
            url,
            headers=headers,
            data=content,
            auth=HTTPBasicAuth(coordinates.username, coordinates.password),
            verify=False)
        http_history_append(response)
        status_code_ok = response.status_code in expected_status_code \
            if isinstance(expected_status_code, (list, tuple)) \
            else  response.status_code == expected_status_code
        if not status_code_ok:
            msg = 'Expected HTTP status code %s, got %d' % (expected_status_code, response.status_code)
            if response.text:
                msg += ', "%s"' % response.text
            raise Exception(msg)
        else:
            return response
    except ConnectionError as e:
        raise Exception("%s, %s" % (e, coordinates)) #from e

def odl_http_head(
    url_suffix,
    url_params={},
    accept='text/plain',
    expected_status_code=200,
    contentType=None,
    content=None
):
    'Get a response from the ODL server.'
    return odl_http_request('head', url_suffix, url_params, contentType, content, accept, expected_status_code)

def odl_http_get(
    url_suffix,
    url_params={},
    accept='text/plain',
    expected_status_code=200,
    contentType=None,
    content=None
):
    'Get a response from the ODL server.'
    return odl_http_request('get', url_suffix, url_params, contentType, content, accept, expected_status_code)

def odl_http_post(
    url_suffix,
    url_params,
    contentType,
    content,
    accept=None,
    expected_status_code=204
):
    'Request a post to the ODL server.'
    return odl_http_request('post', url_suffix, url_params, contentType, content, accept, expected_status_code)

def odl_http_put(
    url_suffix,
    url_params,
    contentType,
    content,
    accept=None,
    expected_status_code=204
):
    'Request a put into the ODL server.'
    return odl_http_request('put', url_suffix, url_params, contentType, content, accept, expected_status_code)

def odl_http_delete(
    url_suffix,
    url_params={},
    accept=None,
    expected_status_code=204,
    contentType=None,
    content=None
):
    'Request a delete on the ODL server.'
    return odl_http_request('delete', url_suffix, url_params, contentType, content, accept, expected_status_code)

def json_dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):
    """Exactly the same as json.dumps."""
    # Beware that json.dumps signature is different for Python 2 and 3.
    return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default, sort_keys=sort_keys)

