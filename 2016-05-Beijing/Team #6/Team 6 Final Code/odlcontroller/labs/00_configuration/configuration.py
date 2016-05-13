#!/usr/bin/env python2.7


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

''' Display configuration settings.

    Print the documentation of the 'settings' module.
    Print the location of the module the configuration is loaded from.
    Print the configuration data, including the co-ordinates of the Controller and network devices.
'''

from __future__ import print_function
from os import environ as _environ
import settings
import pydoc

if __name__ == "__main__":
    
    # Documentation of settings module.
    print(pydoc.plain(pydoc.render_doc(settings)))
    
    # Environment variable that determines configuration.
    print("os.environ['NETWORK_PROFILE']:")
    print('    ', _environ["NETWORK_PROFILE"] if "NETWORK_PROFILE" in _environ else "<empty>")
    print()

    # Configuration module that was dynamically loaded.
    print('settings.config.network_settings_module:')
    print('    ', settings.network_settings_module)
    print()
    
    # Controller co-ordinates.     
    print('settings.config:')
    print('    odl_server:')
    [print('        ',k,'=',v) for (k,v) in settings.config['odl_server'].items()]
    
    # Network device co-ordinates.     
    print('    network_device:')
    for (device_name, device_config) in settings.config['network_device'].items():
        print('        ' + device_name)
#        [print('            ',k,'=',v) for (k,v) in device_config.items()]
        for( key, value ) in device_config.items():
            print( '            chuck: ', key, '=', value )