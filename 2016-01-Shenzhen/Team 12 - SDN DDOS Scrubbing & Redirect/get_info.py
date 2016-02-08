''' 
get config information from controller url
'''

__auth__ = "Team 12"


from __future__ import print_function

import requests
from requests.auth import HTTPBasicAuth
from sys import stderr
import urllib
import urllib2

from basics import odl_http
from basics import render
import settings
import cookielib


def main():
    # It is essential to import module 'settings' because it injects the
    # Controller settings into attribute 'odl_http.coordinates'.     
    # The code below references module 'settings' to prevent it from
    # being auto-removed due to an 'unused import' warning.
    if not settings:
        print('Settings must be configured', file=stderr)
    
    render.print_table(odl_http.coordinates)
    print()
        
    try:
        print('Connecting...')
        url = 'http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:1'

        my_response = requests.get(
                                   url,
                                   auth=HTTPBasicAuth('admin', 'admin')
                                   )
        
        """
        values = {'username':'admin', 'password':'admin'}
        data = urllib.urlencode(values)
        req = urllib2.Request(url,data)
        web_content = urllib2.urlopen(req).read()
        print(web_content)
        """
        print(my_response)
        
        response = odl_http.odl_http_head(
            # Use any URL that is likely to succeed.                                   
            url_suffix='operational/opendaylight-inventory:nodes/node/openflow:1',
            accept='application/json',
            expected_status_code=[200, 404, 503])
        print(response)
        
        outcome = {
            "status code":response.status_code,
            "status":
                'Not found (either the URL is incorrect or the controller is starting).'
                if response.status_code == 404 else
                'Service unavailable (allow 5 or 10 minutes for controller to become ready)'
                if response.status_code == 503 else
                'OK'
                if response.status_code == 200 else
                'Unknown',
            "method":response.request.method,
            "url":response.url}
        render.print_table(outcome)
    except Exception as e:
        print(e, file=stderr)

if __name__ == "__main__":
    main()
