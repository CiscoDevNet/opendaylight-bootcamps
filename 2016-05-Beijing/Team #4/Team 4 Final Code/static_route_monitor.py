'''
Created on May 10, 2016

@author: jushao
'''

from __future__ import print_function
from basics import topology, topology_interface
from basics.odl_http import odl_http_get, odl_http_post, odl_http_delete
import json
import time

_static_route_url_template = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/address-family/vrfipv4/vrf-unicast/vrf-prefixes'

if __name__ == '__main__':
    '''
    response = odl_http_get('config/sjtest:sjtest',accept='application/json', expected_status_code=200)
    print("the response is :"+response.text)
    
    request_content = "{'sjtest' : {'count' : 1} }"
    res = odl_http_post('config/sjtest:sjtest', {}, 'application/json', {'sjtest' : {'count' : 1} })
    print("the res is :"+res.text)
    '''
    
    #create static route :  iosxrv-1   iosxrv-5
    device_name1 = 'iosxrv-1'
    request_content1 = {'Cisco-IOS-XR-ip-static-cfg:vrf-prefix': [{'prefix': '27.27.27.27', 'vrf-route': {'vrf-next-hops': {'next-hop-address': [{'next-hop-address': '45.0.0.27'}]}}, 'prefix-length': 32}]}
    response1 = odl_http_post(_static_route_url_template, {'node-id' : device_name1}, 'application/json', request_content1, expected_status_code=[204, 409])
    
    device_name5 = 'iosxrv-5'
    request_content5 = {'Cisco-IOS-XR-ip-static-cfg:vrf-prefix': [{'prefix': '21.21.21.21', 'vrf-route': {'vrf-next-hops': {'next-hop-address': [{'next-hop-address': '45.0.0.21'}]}}, 'prefix-length': 32}]}
    response5 = odl_http_post(_static_route_url_template, {'node-id' : device_name5}, 'application/json', request_content5, expected_status_code=[204, 409])
    
    #read interface state for every 5 second
    count = 0
    for i in range(0,9):
        flag = True
        for device_name in topology.connected_nodes():
            #print('%s:' % device_name)
            
            if device_name == "iosxrv-1":
                for interface_name in topology_interface.interface_names(device_name):
                    #print('Interface Properties for %s:' % interface_name)
                    if interface_name == "GigabitEthernet0/0/0/4":
                        interface_properties = topology_interface.interface_properties(device_name, interface_name)
                        print('\t', interface_name, '-->',  interface_properties['interface'][0]['state'].encode('utf-8'))
                        interface_status = interface_properties['interface'][0]['state'].encode('utf-8')
                        
                        #if interface status is shutdown, count++
                        if interface_status == "im-state-up":
                            pass
                        else:
                            flag = False
                            break
                        
            elif device_name == "iosxrv-5":
                    for interface_name in topology_interface.interface_names(device_name):
                        #print('Interface Properties for %s:' % interface_name)
                        if interface_name == "GigabitEthernet0/0/0/2":
                            interface_properties = topology_interface.interface_properties(device_name, interface_name)
                            print('\t', interface_name, '-->',  interface_properties['interface'][0]['state'].encode('utf-8'))
                            interface_status = interface_properties['interface'][0]['state'].encode('utf-8')
                            
                            #if interface status is shutdown, count++
                            if interface_status == "im-state-up":
                                pass
                            else:
                                flag = False
                                break
        
        if not flag:
            count = count + 1

        time.sleep(5)
    
    #read MD-SAL sjtest yang,get threshold value
    response = odl_http_get('config/sjtest:sjtest',accept='application/json', expected_status_code=200)
    print("the response is :"+response.text)
    threshold  = response.text.sjtest.threshold
    
    #if count > threshold, shutdown iosxrv-1 and iosxrv-5 ,start up another line 
    if count > threshold:
        url_params1 = {'prefix-length': 32, 'node-id': 'iosxrv-1', 'ip-address': '27.27.27.27'}
        url_template1 = "config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/address-family/vrfipv4/vrf-unicast/vrf-prefixes/vrf-prefix/{ip-address}/{prefix-length}"
        response = odl_http_delete(url_template1, url_params1, 'application/json', expected_status_code=[200, 404, 500])
        
        url_params5 = {'prefix-length': 32, 'node-id': 'iosxrv-5', 'ip-address': '21.21.21.21'}
        url_template5 = "config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ip-static-cfg:router-static/default-vrf/address-family/vrfipv4/vrf-unicast/vrf-prefixes/vrf-prefix/{ip-address}/{prefix-length}"
        response = odl_http_delete(url_template5, url_params5, 'application/json', expected_status_code=[200, 404, 500])
        
        ##shutdown
        device_name_new1 = 'iosxrv-1'
        request_content_new1 = {'Cisco-IOS-XR-ip-static-cfg:vrf-prefix': [{'prefix': '27.27.27.27', 'vrf-route': {'vrf-next-hops': {'next-hop-address': [{'next-hop-address': '58.0.0.22'}]}}, 'prefix-length': 32}]}
        response1 = odl_http_post(_static_route_url_template, {'node-id' : device_name_new1}, 'application/json', request_content_new1, expected_status_code=[204, 409])
        
        device_name_new2 = 'iosxrv-2'
        request_content_new2 = {'Cisco-IOS-XR-ip-static-cfg:vrf-prefix': [{'prefix': '27.27.27.27', 'vrf-route': {'vrf-next-hops': {'next-hop-address': [{'next-hop-address': '48.0.0.27'}]}}, 'prefix-length': 32}]}
        response1 = odl_http_post(_static_route_url_template, {'node-id' : device_name_new2}, 'application/json', request_content_new2, expected_status_code=[204, 409])
        
        device_name_new2_1 = 'iosxrv-2'
        request_content_new2_1 = {'Cisco-IOS-XR-ip-static-cfg:vrf-prefix': [{'prefix': '21.21.21.21', 'vrf-route': {'vrf-next-hops': {'next-hop-address': [{'next-hop-address': '58.0.0.21'}]}}, 'prefix-length': 32}]}
        response1 = odl_http_post(_static_route_url_template, {'node-id' : device_name_new2_1}, 'application/json', request_content_new2_1, expected_status_code=[204, 409])
        
        device_name_new5 = 'iosxrv-5'
        request_content_new5 = {'Cisco-IOS-XR-ip-static-cfg:vrf-prefix': [{'prefix': '27.27.27.27', 'vrf-route': {'vrf-next-hops': {'next-hop-address': [{'next-hop-address': '48.0.0.22'}]}}, 'prefix-length': 32}]}
        response1 = odl_http_post(_static_route_url_template, {'node-id' : device_name_new5}, 'application/json', request_content_new5, expected_status_code=[204, 409])
     
    print(count)
     
     
        