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

''' Connect to each Network Device.

    Establish a connection to the each network device and display relevant information.
'''

from __future__ import print_function
import settings
import socket
from settings import network_configuration

def main():
    for (device_name, device_config) in settings.config['network_device'].items():
        s = socket.socket()
        try:
            print( 'testing connectivity to ', device_config['address'], ' on port ', device_config['port'] )
            s.connect((device_config['address'], device_config['port']))
            print( '    ', device_name, s.getsockname(), '-->', s.getpeername())
        except Exception as e:
            print( '    ', device_name, '-->', device_config['address'], device_config['port'], e)
        finally:
            s.close()
            del s

if __name__ == "__main__":
    main()