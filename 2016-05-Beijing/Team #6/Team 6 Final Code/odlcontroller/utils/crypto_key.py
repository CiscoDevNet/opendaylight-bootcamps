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

    This script will use telnet to login to a Cisco XRv device and set the cryptographic keys 
    to support SSH connectivity. This version of the script uses the arguments encoded in the
    script itself.
    
    To test for whether the crypto key is set, and whether the netconf agent is running, we can
    use this command:
    
    ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 830 cisco@172.16.1.11 -s netconf
    
    Guidance from: See http://linuxcommando.blogspot.com/2008/10/how-to-disable-ssh-host-key-checking.html
    
    By configuring the null device file as the host key database, SSH is fooled into thinking that the 
    SSH client has never connected to any SSH server before, and so will never run into a mismatched host key.
    
    The parameter StrictHostKeyChecking specifies if SSH will automatically add new host keys to the 
    host key database file. By setting it to no, the host key is automatically added, without user 
    confirmation, for all first-time connection. Because of the null key database file, all 
    connection is viewed as the first-time for any SSH server host. Therefore, the host key is 
    automatically added to the host key database with no user confirmation. Writing the key to 
    the /dev/null file discards the key and reports success.
'''

from __future__ import print_function

from __future__ import absolute_import

import pexpect
import sys

def add_crypto_key (devices=[], username = 'cisco', password = 'cisco'):
    
    if len(devices) != 0:
        network_devices = devices
    else:
        network_devices = ['172.16.1.11']    
    
    for network_device in network_devices:
        try:
            telnet_command = "telnet %s" % network_device
            child = pexpect.spawn (telnet_command) 
            child.logfile = sys.stdout
            child.expect ('Username:')
            child.sendline (username)
            child.expect ('Password:')
            child.sendline (password)
            child.expect ('#')
            child.sendline ('crypto key generate dsa')
            index = child.expect (['[yes/no]','1024]'])
            if index == 0:
                child.sendline ('yes')
                child.expect ('1024]')
                child.sendline ('')
                child.sendline ('')
            elif index == 1:
                child.sendline ('')
                child.sendline ('')
        except:
            print ("Could not connect to %s" % network_device)
            continue
if __name__ == '__main__':

    add_crypto_key ()
