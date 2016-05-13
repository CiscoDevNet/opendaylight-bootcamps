from __future__ import print_function as _print_function
import pydoc
import settings
import time
from pydoc import plain
from pydoc import render_doc as doc
from basics import topology
from basics.inventory import inventory_connected
from basics.render import print_table
from os.path import basename,splitext
from runpy import run_module

def run_script(script):
    try:
        run_module(script, run_name='__main__')
    except SystemExit as e:
        # Return the exit code of the script.
        # It indicates whether the script able to proceed.         
        # Don't actually exit, though.              
        return e.code

# Run settings scripts.
run_script('00_settings')
run_script('00_devices')
run_script('00_controller')

#mount all device
def mount_device(device_name):
    device_config = settings.config['network_device'][device_name]
    #print('device_mount(' + device_name, *device_config.values(), sep=', ', end=')\n')
    topology.mount(
        device_name,
        device_config['address'],
        device_config['port'],
        device_config['username'],
        device_config['password'])


def main():   
    device_list=settings.config['network_device']
    
    #dismount each nodes
    mounted_list = topology.mounted_nodes()
    if mounted_list:
        for device_name in mounted_list:
            topology.dismount(device_name)
    print('all devices dismount.')
        
    #mount each nodes
    unmounted_list = topology.unmounted_nodes()
    if unmounted_list:
        for device_name in unmounted_list:
            mount_device(device_name)
            print('mount %s' % device_name)
            time.sleep(1)
    print('mount each nodes.')
    
    time.sleep(5)
    
    connected_list = topology.connected_nodes()
    print('connected:  ', connected_list)
    
    #mount each disconnected nodes
    mounted_list = topology.mounted_nodes()
    while len(device_list)!=len(connected_list):
        print('%s devices connected' % len(connected_list))
        for device_name in device_list:
            if device_name in connected_list:
                continue
            else:
                if device_name in mounted_list:
                    topology.dismount(device_name)
                    print('dismount %s' % device_name)
                    time.sleep(1)
                
                mount_device(device_name)
                print('mount %s' % device_name)
                time.sleep(3)
                if device_name in topology.connected_nodes():
                    print('connected %s success' % device_name)
                else:
                    print('connected %s failed' % device_name)
                connected_list = topology.connected_nodes()
                    
    print('all devices are connected!', connected_list)

if __name__ == "__main__":
    main()