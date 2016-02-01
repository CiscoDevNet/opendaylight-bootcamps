import requests
import sys
from basics.odl_http import odl_http_get, odl_http_put
import settings

def get_bytes(device_name, interface_name):
    url = 'operational/network-topology:network-topology/topology/topology-netconf/'
    data=odl_http_get(url_suffix=url, accept= 'application/json')
    topo= data.json()["topology"][0]
    topo_id=topo["topology-id"]
    node=topo["node"]

    
    url2='operational/network-topology:network-topology/topology/topology-netconf/node/' + device_name + '/yang-ext:mount/Cisco-IOS-XR-drivers-media-eth-oper:ethernet-interface/statistics/statistic/' + interface_name
    data2= odl_http_get(url_suffix=url2, accept= 'application/json')
    
    static=data2.json()["statistic"][0]

    total=static["total-good-bytes-transmitted"]

    
    return total


