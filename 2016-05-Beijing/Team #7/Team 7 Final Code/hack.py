from __future__ import print_function as _print_function
import pydoc
import settings
import time
from pydoc import plain
from pydoc import render_doc as doc
from basics import topology
from basics.context import EX_OK
from basics.interface import management_interface, interface_configuration_tuple, interface_names, interface_configuration_update
from basics.routes import static_route_list, inventory_static_route, static_route_create, static_route_exists, to_ip_network, static_route_delete
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
run_script('last-1-mount-all')
run_script('last-2-set-ip')
run_script('last-3-set-route')
run_script('last-4-change-path')

