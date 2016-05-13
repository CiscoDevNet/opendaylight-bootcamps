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

odl_server_hostname = 'localhost'
odl_server_url_prefix = "http://%s:8181/restconf/" % odl_server_hostname

config = {'odl_server' : {
                          'url_prefix' : odl_server_url_prefix,
                          'username' : 'admin',
                          'password' : 'admin'
                          },
          'network_device': {
                             'iosxrv-1': {
                                     'address': '198.18.1.30',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             'iosxrv-2': {
                                     'address': '198.18.1.31',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             'iosxrv-3': {
                                     'address': '198.18.1.32',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             'iosxrv-4': {
                                     'address': '198.18.1.33',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             'iosxrv-5': {
                                     'address': '198.18.1.34',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             'iosxrv-6': {
                                     'address': '198.18.1.35',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             'iosxrv-7': {
                                     'address': '198.18.1.36',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             'iosxrv-8': {
                                     'address': '198.18.1.37',
                                     'port': 830,
                                     'password': 'cisco',
                                     'username': 'cisco'
                                     },
                             }
          }
