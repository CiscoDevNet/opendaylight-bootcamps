#!/usr/bin/env python2.7

# Copyright 2015 Hackthon@group10
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

'''  
    Project Name:
        
        prority-based  request with bandwidth reserve link access control network
    
    Project Description:
    
        Our project aims at solving the bandwidth reserve dynamically for the network based on the priority.
        
    Team Member:
        
        Junjie Tong, Xiaodong Pan, Cheng Zhang @ Hackthon-Opendaylight-Group10

'''

from __future__ import print_function as _print_function
#import from the std python lib
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
import json
import re
import string    
    
#import from the odl-learning lib @cisco
from basics.http import json_loads
from basics.odl_http import odl_http_get, odl_http_post
from basics.interface import interface_names
from basics.inventory import inventory_connected
from basics.interface_configuration import interface_configuration
from basics.routes import static_route_create, to_ip_network
from basics.routes import   static_route_list, inventory_static_route


#import from third party lib
import networkx as nx
from networkx.readwrite import  json_graph


#static global url for restconf API
_cdp_enable_interface_url_suffix = 'config/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations/'
url_neighbours = 'operational/opendaylight-inventory:nodes/node/{node-id}/yang-ext:mount/Cisco-IOS-XR-cdp-oper:cdp'
_cdp_enable_interface_request_content = '''
{"Cisco-IOS-XR-ifmgr-cfg:interface-configuration":[
{
"active":"act",
"interface-name":"%s",
"Cisco-IOS-XR-cdp-cfg:cdp" : {"enable" : ""},
"bandwidth":"%s"
}]}
'''
_BUG_CHECK = 'Bug-Check!----%s----'

# global vars 
_MAXMIUM_BANDWIDTH = "1000000"    # define the maximum bandwidth of link
ipmap = {
         '10.0.0.6':'iosxrv-1',  # for easy implement we predefined the host ip and its direct connected router
         '10.0.0.18':'iosxrv-2',
         '10.0.0.26':'iosxrv-2'
         }
host={
      '10.0.0.6':'host1',
      '10.0.0.18':'host2',
      '10.0.0.26':'host3'
      }
initial_flag = True               # flag for initialize the maximum bandwidth of each link
edges = []                        # global var to store the link info, Note: our link is directed         
nodes = []                        # global var to store the node info

# data format of edges and nodes :
#         Edges = [
#                     { 'localnode': local_node_id, 
#                       'localifname': local_interface_name
#                       'localaddr': local_addr,
#                       'localmask': local_netmask,
#                       'remotenode': remote_node_id,
#                       'remoteifname': remote_interface_name
#                       'remoteaddr': remote_node_addr,
#                       'remotemask' : remote_netmask,
#                       'maxbandwidth': xxx ,
#                       'available_bandwidth': xxx,
#                     }, // edge1
#                     {
#                       
#                     } // edge2
#                 ]
#
#         nodes = [
#                    {
#                       'nodename': node_id
#                    }, // node1
#                    {
#                        
#                    } // node2
#                 ]
#                  '    
def devname2devid(devname):
    '''
        Description:
             This function translate the device_name to device_id. Because the default 
             device_name of the router is like xrvr-1, but from the restconf the device_id
             of router is like iosxrv-1. So we need a tranlation between them.
    '''
    if 'ios' not in devname:
        #we got the devname like xrvr-1, we get the number part
        rs = re.match(r'.*-(\d+)$',devname)
        if rs :
            rs2 = 'iosxrv-'+ rs.groups()[0]
            return rs2
    else :
        print(_BUG_CHECK %'you use the wrong tranlation function, try devid2devname!')
        return None
            
def devid2devname(devid):
    '''
        Description: reference the devname2devid(). This is the opposite one.
    '''
    if 'ios' in devid:
        #we got the devid name like iosxrv-1
        rs = re.match(r'.*-(\d+)$',devid)
        if rs:
            rs2 = 'xrvr-'+rs.groups()[0]
            return rs2
    else:
        print(_BUG_CHECK %'you use the wrong tranlation function, try devname2devid!')
        return None



def showstaticroute():
    device_names = inventory_static_route()
    if not device_names:
        print("There are no 'static route' capable devices to examine. Demonstration cancelled.")
    else:
        for device_name in device_names:
            print('static_route_list(' + device_name, end=')\n')
            routes = static_route_list(device_name)
            print('\t', [str(route) for route in routes])


def findneighbor(device_name):
    '''
        Description : 
            This function retrieve the cdp information for the specific device through 
            restconf API. It then parse the data and store the information in global
            var like nodes and edges.
                
    '''
    #get the result from cdp url for device_name
    response = odl_http_get(url_neighbours.format(**{'node-id': quote_plus(device_name), }),
                            'application/json',
                            expected_status_code=(200, 404)
                            )
    if response.status_code == 400:
        print(_BUG_CHECK %'This interface is not provided!')
        return None
    j = json_loads(response.text)
    #add the node into the nodes, we store the device_id
    nodes.append(dict(nodename=devname2devid(device_name)))
    container = j["cdp"]["nodes"]["node"][0]
    #print(json_dumps(container, indent=2))
    if "neighbors" in container:
        neighbors = container["neighbors"]
        if 'summaries' in neighbors:
            summaries = neighbors['summaries']['summary']
            #now we get the list of summarirs, each summary is a {} dict type
            for summary in summaries:
                #here we skip the mgt interface
                if 'MgmtEth' in summary['interface-name']:
                    continue
                #add the data of an edge
                dict_item = {'localnode':devname2devid(device_name),\
                             'remotenode':summary['device-id'],\
                             'localifname':summary['interface-name'],\
                             'remoteifname':summary['cdp-neighbor'][0]['port-id']
                             }
                #At first we have to set the interface's bandwidth to maxmium,
                #in our design, we use available_bandwidth to implement the 
                #route calculate and bandwidth reserve.
                if initial_flag == True :              
                    dict_item['maxbandwidth'] = _MAXMIUM_BANDWIDTH
                    dict_item['available_bandwidth'] = _MAXMIUM_BANDWIDTH                   
                # now we have to set the  local network address and networkmask
                netresult = interface_configuration(devid2devname(dict_item['localnode']), dict_item['localifname'])
                # !!-.-!! here i can only accees the element by index even if the debugger tell me the data in it is address=10.0xxx, but
                # it is not a dict. so can anyone help?
                if netresult is not None :
                    dict_item['localaddr'] = netresult[3]
                    dict_item['localmask'] = netresult[4]
                    netresult = None
                else :
                    print(_BUG_CHECK %'The interface of the local node is wrong, maybe the device is not mounted')
                # now it is the remote address and networkmask
                netresult = interface_configuration(devid2devname(dict_item['remotenode']), dict_item['remoteifname']) 
                if netresult is not None :
                    dict_item['remoteaddr'] = netresult[3]
                    dict_item['remotemask'] = netresult[4]
                else :
                    print(_BUG_CHECK %'The interface of the remote node is wrong, maybe the device is not mounted')
                          
                edges.append(dict_item)              

    else :
        print(_BUG_CHECK %'The node has no neighbors or maybe the device is not mounted')
        return None


def cdp_enable_interface(device_name, interface_name):
    '''
        Description:
            This function will enable the cdp for every interface on device.
            
    '''
    url_suffix = _cdp_enable_interface_url_suffix.format(**{'node-id': quote_plus(device_name), })
    request_content = _cdp_enable_interface_request_content % (interface_name,_MAXMIUM_BANDWIDTH)
    return odl_http_post(url_suffix, 'application/json', request_content)

def cdp_enable_device(device_name):
    '''
        Description:
            This function will iterate all the devices to enable the cdp.
            
    '''
    for interface_name in interface_names(device_name):
        cdp_enable_interface(device_name, interface_name)        

def cdp_enable_network():
    '''
        Description:
            This function will check every connected device and enable them one by one.
    '''
    for device_name in inventory_connected():
        if device_name:
            cdp_enable_device(device_name)
        
def topodetect():
    '''
        Description:
            This function first will enable cdp of all the connected devices, and then
            iterate them to set up the topology. 
    '''
    cdp_enable_network()
    for device_name in inventory_connected():
        findneighbor(device_name) 

def pathCompute(src_ip,dst_ip,upband=2000,downband=2000):
    '''
    Description:
        This function will calculate the path between src host and dst host based on the 
        requirement of upside bandwidth, downside bandwidth and available_bandwidth. For 
        now we use the a bi-directed graph to modelize the network and use weighed Dijkstra
        algorithm to find the route. The weight parameter = (require_bandwidth/available_bandwidth) 
    Argument:
        src_ip : The src addr of the host
        dst_ip : The dst addr of the host
        upband : The up bandwidth requirement of the src host
        downban: The down bandwidth requirement of the dst host
        
    '''
    #use networkx to compute the path
    G=nx.DiGraph()
    #translate the ip_src and ip_dst to node
    src_node = ipmap[src_ip]
    des_node = ipmap[dst_ip]
    edge_band={}
    for node in nodes:
        G.add_node(node['nodename'])
    for edge in edges:
        tmp_node1_name=edge['localnode']
        tmp_node2_name=edge['remotenode']
        tmp_edge_band=edge['available_bandwidth']
        #we use used_bandwidth as the weight of the link
        tmp_used_band = int(edge['maxbandwidth'])-int(tmp_edge_band)
        edge_band[(tmp_node1_name,tmp_node2_name)]=int(tmp_edge_band)
        G.add_edge(tmp_node1_name,tmp_node2_name,weight = tmp_used_band)  
        #because we compute the shortest later, so we have converse the bandwidth here. eg.1/2M to assure enough bandwidth for using
    up_paths=nx.dijkstra_path(G,src_node,des_node)
    up_path_edge=[]
    if len(up_paths)==0:
        return 'No Available Resource for Up Path!'
    else:
        i=0
        while i<len(up_paths)-1:
            if edge_band[(up_paths[i],up_paths[i+1])]<upband:
                return 'No Available Resource for Up Path'
            else:
                for edge in edges:
                    if edge['localnode']==up_paths[i] and edge['remotenode']==up_paths[i+1]:
                        up_path_edge.append(edge)
                i=i+1
    down_paths=nx.dijkstra_path(G,des_node, src_node)
    down_path_edge=[]
    if len(down_paths)==0:
        return 'No Available Resource for Down Path!'
    else:
        i=0
        while i<len(down_paths)-1:
            if edge_band[(down_paths[i],down_paths[i+1])]<downband:
                return 'No Available Resource for Down Path'
            else:
                for edge in edges:
                    if edge['localnode']==down_paths[i] and edge['remotenode']==down_paths[i+1]:
                        down_path_edge.append(edge)
                i=i+1
    print('%s ---> %s Up Path Edge is calculated successfully:' %(src_ip,dst_ip))
    #print(up_path_edge)
    print('%s <--- %s Down Path Edge is calculated successfully:' %(src_ip,dst_ip))
    #print(down_path_edge)
    return (up_path_edge,down_path_edge)


def static_route_send_sub(edge,ip):
    '''
        Descripthon :
            This is the subroutine of the static_route_send function
    '''
    remote_ip = edge['remoteaddr']
    nodesrc = edge['localnode']
    destination_network=to_ip_network(ip,'255.255.255.255')
    #detination_network should be destination node's network
    rs = static_route_create(devid2devname(nodesrc), destination_network, remote_ip)
    if rs.status_code == 204 or rs.status_code == 409 :
        return rs
    else:
        print(_BUG_CHECK %'push static route is failed!')
        return None
            
            
def static_route_send(up_path_edges,down_path_edges,dst_ip,src_ip,upband =2000,downband=2000):
    '''
        Description:
            This will push the static route to each node on the path.
    '''
    for edge in up_path_edges:
        if static_route_send_sub(edge,dst_ip) :
            edge['available_bandwidth']=str(int(edge['available_bandwidth'])-upband)
            print('%s--->%s : push static route to node %s is successful!' %(src_ip,dst_ip,edge['localnode']))
        else :
            return None
    for edge in down_path_edges:
        if static_route_send_sub(edge,src_ip) :
            edge['available_bandwidth']=str(int(edge['available_bandwidth'])-downband)
            print('%s--->%s : push static route to node %s is successful!' %(dst_ip,src_ip,edge['localnode']))
        else :
            return None
          
    print("push route finish! Listing the static route on nodes.... ")
    showstaticroute()
    print(' ')
    print(' ')
    
def store_network_as_jason(up_path_edges,down_path_edges,upband=2000,downband=2000):
    '''
        Description:
            This function export the node and link information to the frontend lib, to visiualize the 
            topo and the calculated path between hosts.
    '''
    graph1=nx.DiGraph()
    graph2=nx.DiGraph()
    for edge in edges:
        if edge['localnode'] not in graph1.nodes():
            group=1
            if edge['localaddr'] in ipmap.keys():
                group=0
            graph1.add_node(edge['localnode'],{'localinterface':edge['localifname'],'IPAdd':edge['localaddr'],'group':group})
        if edge['remotenode'] not in graph1.nodes():
            group=1
            if edge['remoteaddr'] in ipmap.keys():
                group=0
            graph1.add_node(edge['remotenode'],{'remoteinterface':edge['remoteifname'],'IPAdd':edge['remoteaddr'],'group':group})
        graph1.add_edge(edge['localnode'],edge['remotenode'],{'AvailableBandwidth':edge['available_bandwidth'],'value':edge['available_bandwidth']})
    for edge in up_path_edges:
        if edge['localnode'] not in graph2.nodes():
            group=1
            if edge['localaddr'] in ipmap.keys():
                group=0
            graph2.add_node(edge['localnode'],{'localinterface':edge['localifname'],'IPAdd':edge['localaddr'],'group':group})
        if edge['remotenode'] not in graph2.nodes():
            group=1
            if edge['remoteaddr'] in ipmap.keys():
                group=0
            graph2.add_node(edge['remotenode'],{'remoteinterface':edge['remoteifname'],'IPAdd':edge['remoteaddr'],'group':group})
        graph2.add_edge(edge['localnode'],edge['remotenode'],{'UpBandwidth':upband,'value':upband})
    for edge in down_path_edges:
        if edge['localnode'] not in graph2.nodes():
            group=1
            if edge['localaddr'] in ipmap.keys():
                group=0
            graph2.add_node(edge['localnode'],{'localinterface':edge['localifname'],'IPAdd':edge['localaddr'],'group':group})
        if edge['remotenode'] not in graph2.nodes():
            group=1
            if edge['remoteaddr'] in ipmap.keys():
                group=0
            graph2.add_node(edge['remotenode'],{'remoteinterface':edge['remoteifname'],'IPAdd':edge['remoteaddr'],'group':group})
        graph2.add_edge(edge['localnode'],edge['remotenode'],{'DownBandwidth':downband,'value':downband})
    for node in host.keys():
        graph1.add_node(host[node],{'IPAdd':node,'group':0})
        graph2.add_node(host[node],{'IPAdd':node,'group':0})
        graph1.add_edge(host[node],ipmap[node])
        graph2.add_edge(host[node],ipmap[node])
    d1=json_graph.node_link_data(graph1)
    d2=json_graph.node_link_data(graph2)
    json.dump(d1,open('/Users/eric/Desktop/topo/1.json','w'))
    json.dump(d2,open('/Users/eric/Desktop/topo/2.json','w'))

    


def main():
    
    print('Initializing the topology')
    topodetect()
    while( True ):
    
        ip_src = input("Please input the src host ip address :")
        ip_dst = input('please input the dst host ip address :')
        upband_requirement = input('please input the required bandwidth of uplink :')
        dwband_requirement = input('please input the required bandwidth of dwonlink :')
        
        if ip_src == 'quit' or ip_dst == 'quit' or upband_requirement =='quit' or dwband_requirement == 'quit':
            break      
        #ip_src = '10.0.0.18'
        #ip_dst = '10.0.0.22'
        (up_path_edges,down_path_edges)=pathCompute(ip_src,ip_dst,upband_requirement,dwband_requirement)
        static_route_send(up_path_edges,down_path_edges,ip_dst,ip_src,upband_requirement,dwband_requirement)
        store_network_as_jason(up_path_edges,down_path_edges,upband_requirement,dwband_requirement)
        
    print('ok')
    
if __name__ == "__main__":
    main()