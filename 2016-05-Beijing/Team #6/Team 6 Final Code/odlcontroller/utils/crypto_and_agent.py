#!/usr/bin/env python

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

# This code uses https://github.com/pexpect/pexpect. The pexpect licence is below:

'''
PEXPECT LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2012, Noah Spurrier <noah@noah.org>
    PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE THIS SOFTWARE FOR ANY
    PURPOSE WITH OR WITHOUT FEE IS HEREBY GRANTED, PROVIDED THAT THE ABOVE
    COPYRIGHT NOTICE AND THIS PERMISSION NOTICE APPEAR IN ALL COPIES.
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

    This script will use other functions in utils to check for the crypto key and netconf-yang
    agents and configure them if necessary.
'''

from __future__ import print_function

from __future__ import absolute_import

import pexpect
import sys

from utils.crypto_key import add_crypto_key
from utils.netconf_agent_configure import configure_netconf_agent

def configure_crypto_and_agent (devices=[], username = 'cisco', password = 'cisco'):
    
    if len(devices) != 0:
        network_devices = devices
    else:
        network_devices = ['198.18.1.50', '198.18.1.51', '198.18.1.52', '198.18.1.53', '198.18.1.54', '198.18.1.55', '198.18.1.56', '198.18.1.57']    
    
    add_crypto_key(network_devices)
    configure_netconf_agent(network_devices)

if __name__ == '__main__':

    configure_crypto_and_agent ()
