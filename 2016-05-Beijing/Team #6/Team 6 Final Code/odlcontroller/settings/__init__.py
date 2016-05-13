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

''' Obtain settings by dynamically loading a configuration module located in package 'settings'.

    The configuration module is a normal Python module.
    The configuration module is located in package 'settings' (this package).
    The configuration module must have a variable named 'config', 
    The name of the configuration module is determined by environment variable NETWORK_PROFILE.
    The default configuration module is 'learning_lab.py'.
    The variable named 'config' in the configuration modules is assigned to the
    variable named 'config' in package 'settings' (this package).
    That is:
        settings.config = settings.<configuration_module>.config
    This redirection provides independence.
    Configuration data is accessed in a consistent manner (from 'settings.config').
    Sample Usage:
        import settings
        print(settings.config['_odl_server']['address'])
        
    Update 08-July-2015, the configuration file does not need to be on the 
    Python path. It can be located anywhere and therefore can be external to an
    egg file, which allows cosc-learning-labs to be deployed as an egg.
'''

from __future__ import print_function as _print_function
from importlib import import_module
from os import getenv
from os.path import dirname
from basics import odl_http
from basics.odl_http import ControllerCoordinates
from basics.odl_http import default_coordinates as _odl_default_coordinates
from basics.context import load_module

_network_profile = getenv('NETWORK_PROFILE', 'learning_lab')

try:
    network_settings_module = load_module('network_profile', _network_profile, dirname(__file__))
    config = network_settings_module.config 
    
    # Inject configuration into module odl_http.
    if 'odl_server' in config:
        _odl_server = config['odl_server']
        odl_http.coordinates = ControllerCoordinates(
            url_prefix = _odl_server.get('url_prefix', _odl_default_coordinates.url_prefix),
            username = _odl_server.get('username', _odl_default_coordinates.username),
            password = _odl_server.get('password', _odl_default_coordinates.password))
except Exception as e:
    raise ImportError('Unable to import settings.' + _network_profile, e)

# TODO fill in missing fields with default values, such as Netconf port 830.
