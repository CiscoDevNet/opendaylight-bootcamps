import requests
import sys
from basics.odl_http import odl_http_get, odl_http_put
import settings
from get_dong import get_bytes
import time


def get_real_time_load(device_name, interface_name):
    #device_name = 'iosxrv-2'
    #interface_name = 'GigabitEthernet0%2F0%2F0%2F1'
    
    total_bytes1 = get_bytes(device_name, interface_name)
    time1 = time.time()
    time.sleep(0.001)
    total_bytes2 = get_bytes(device_name, interface_name)
    time2 = time.time()
    
    total_bytes = int(total_bytes1) + int(total_bytes2)
    #time0 = time2 - time1
    
    bandwidth = int(total_bytes1 - total_bytes2) / (time2 - time1)
    #bandwith = total_bytes / int(time0)
    #print(bandwith)
    
    return bandwidth



