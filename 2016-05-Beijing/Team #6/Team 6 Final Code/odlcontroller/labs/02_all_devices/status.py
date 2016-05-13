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

"""Display the status of all devices."""

from __future__ import print_function
import settings
from basics import topology

def main():
    print('config.network_devices:  ', settings.config['network_device'].keys())
    print('mounted:  ', topology.mounted_nodes())
    print('unmounted:  ', topology.unmounted_nodes())
    print('connected:  ', topology.connected_nodes())
    print('disconnected:  ', topology.disconnected_nodes())
    
if __name__ == "__main__":
    main()