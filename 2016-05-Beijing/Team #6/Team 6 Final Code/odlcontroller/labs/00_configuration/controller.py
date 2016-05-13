#!/usr/bin/env python3.4

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

''' Connect to the Controller.

    Establish a connection to the Controller and display relevant information.
'''

from __future__ import print_function
import settings
from sys import stderr
from basics import render
from basics import odl_http


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
        response = odl_http.odl_http_head(
            # Use any URL that is likely to succeed.                                   
            url_suffix='operational/opendaylight-inventory:nodes',
            accept='application/json',
            expected_status_code=[200, 404, 503])
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
