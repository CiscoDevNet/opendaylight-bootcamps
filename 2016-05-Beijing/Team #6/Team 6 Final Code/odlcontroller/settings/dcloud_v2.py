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

from __future__ import print_function
from basics.cosc_http import cosc_authentication_token

import requests.packages
requests.packages.urllib3.disable_warnings()

odl_server_hostname = '198.18.1.25'

odl_server_url_prefix = "https://%s/controller/restconf/" % odl_server_hostname

config = {
    'odl_server' : {
        'url_prefix' : odl_server_url_prefix,
        'username' : 'token',
        'password' : cosc_authentication_token(odl_server_hostname, 8181, 'admin', 'cisco123')},
 'network_device': {'kcy':{
                     'address': '198.18.1.50',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'},
                    'lax':{
                     'address': '198.18.1.51',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'},
                    'min':{
                     'address': '198.18.1.52',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'},
                    'por':{
                     'address': '198.18.1.53',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'},
                    'san':{
                     'address': '198.18.1.54',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'},
                    'sea':{
                     'address': '198.18.1.55',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'},
                    'sfc':{
                     'address': '198.18.1.56',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'},
                    'sjc':{
                     'address': '198.18.1.57',
                     'port': 830,
                     'password': 'cisco',
                     'username': 'cisco'}}}
