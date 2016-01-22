# Author: Kevin Boutarel
# Date: 11/05/2015
# Purpose: Monitors the bytes received from a device on a specific interface using ODL
#          Inserts a route after MAX_OCCURENCES have hit the threshold and deletes the route
#          after MAX_NORMAL runs and if the route is set
# Usage: python monitor.py ODL_IP_address router_IP_address interface_name threshold

from time import sleep, time
from urllib import quote_plus as encode

import os
import json
import base64
import requests
import subprocess

import settings


def write_data(difference, start_time, id):
    ''' 
    Writes the difference in packets to the test.json file
    The file will help populate the graph.
    
    Keyword Arguments:
    difference -- int. Difference in packets.
    start_time -- in. Starting time of script
    id -- int. Id of input
    '''
    current_time = int(time())
    input1 = {"index": {"_index":"test", "_type":"traffic", "_id": id}}
    input2 = {"line_id":1, "bytecountdifference":difference, "time":current_time-start_time + 2010}
    with open("test.json", "a") as test:
        test.write(json.dumps(input1))
        test.write("\n")
        test.write(json.dumps(input2))
        test.write("\n")        


def send_data():
    '''
    Sends the file test.json to the computer with the front-end code
    '''
    ip_address = "10.16.9.6"
    port = "9200"
    filename = "test.json"
    
    subprocess.Popen("curl -XPUT %s:%s/_bulk --data-binary @%s" %(ip_address, port, os.getcwd() + os.path.sep + filename),
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)


def main():
    # first: odl_ip --- second: device name
    base_url = "http://%s:8181/restconf/operational/" +\
               "network-topology:network-topology/topology/" +\
               "topology-netconf/node/%s/yang-ext:mount/Cisco-IOS-XR-pfi-im-cmd-oper:interfaces/"

    # Constants
    odl_ip = "localhost"
    input_router_ip = "198.18.1.30"
    interface_name = "GigabitEthernet0/0/0/4"
    threshold = 9000
    MAX_OCCURENCES = 2
    MAX_NORMAL = 8

    # Get device name from the source IP address
    found = False
    for (device_name, device_config) in settings.config['network_device'].items():
        address = device_config['address']
        if(address == input_router_ip):
            source_name = device_name
            found = True
            break
    
    if(not found):
        print("Input source IP %s could not be found among the list of devices" % (input_source_ip))
        exit(1)

    # Need to go deeper into the yang model to get the statistics
    statistics_url = "interface-xr/interface/%s/interface-statistics/full-interface-stats/"
    request_url = base_url % (odl_ip, device_name) + statistics_url % (encode(interface_name))
    
    # Start time of experiment
    start_time = int(time())
    
    first = True                  # If getting stats for the first time
    occurences = MAX_OCCURENCES   # Number of times threshold can be hit before route is set
    id = 0                        # id of input to send to elasticsearch
    previous_bytes = 0            # bytes from previous GET request
    current_bytes = 0             # bytes from current GET request
    route_set = False             # Whether the route is set on the controller
    normal_runs = 0               # Number of normal runs after the route is set
    while(True):
        # Perform a get request to retrieve all of the interface statistics
        print("[GET] Full interface stats")
        response = requests.get(request_url, auth=(base64.b64decode("YWRtaW4="), base64.b64decode("YWRtaW4=")))
        if(response.status_code == 200):
            # Parse JSON text into Python object
            stats = json.loads(response.text)
            current_bytes = stats["full-interface-stats"]["bytes-sent"]
            if(first):
                print("Bytes sent = %d" % (current_bytes))
                previous_bytes = current_bytes
                first = False
            else:
                difference = current_bytes - previous_bytes
                print("Bytes sent = %d --- Difference = %d" % (current_bytes, difference))
                if(difference > threshold and occurences != 0):
                    print("THRESHOLD HIT -- %d more chances" % (occurences))
                    occurences -= 1
                elif(difference > threshold and occurences == 0):
                    print("\nStopping connection on interface %s\n" % (interface_name))
                    subprocess.Popen("python insert_route.py", shell=True)
                    route_set = True  # route is set
                    normal_runs = 0   # start checking for normal runs
                    occurences = MAX_OCCURENCES    # reset the occurences
                elif(route_set and normal_runs < MAX_NORMAL):
                    normal_runs += 1  # found one normal run
                elif(route_set and normal_runs == MAX_NORMAL):
                    # Delete the route
                    print("\nResetting connection on interface %s\n" % (interface_name))
                    subprocess.Popen("python delete_route.py", shell=True)
                    route_set = False  # route is not set
                # write data to json file        
                write_data(difference, start_time, id)
                # send data
                send_data()
                id += 1  # increase the id for the data
                previous_bytes = current_bytes
        else:
            print("Expected status code 200 but received %d." % response.status_code)
        
        sleep(2)
    
if __name__ == "__main__":
    main()