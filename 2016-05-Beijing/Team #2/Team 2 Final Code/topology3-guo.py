"""
    parseNodes Updated 20150726 by Niklas for OSPF support and ISIS/OSPF broadcast network/pseudo node support
    changed prints to logging, Niklas 20151005
    """
from basics.odl_http import odl_http_request
import settings
import json
from basics.topology import nodes
from pygments.lexer import this


url="operational/network-topology:network-topology/topology/example-linkstate-topology"


def main():    
    response=odl_http_request('get', url, None, None, None, 'application/json', 200)
    #print(response)
    service = topologyservice()
    nodes = service.parseNodes(response.json())
    print ('this is node information')
    print (nodes)
    links1 = service.parseLinks(response.json())

    links = service.dupLink(links1)
    print ('this is link information')
    print (links)
    #result = {}
    #result["nodes"] = nodes
    #result['links'] = links

class topologyservice(object):
    def __init__(self):
        pass
        
    def parseNodes(self, my_topology):
        node_list = []
        try:
            for nodes in my_topology['topology'][0]['node']:                           
                node = {}                
                prefix_array = []                
                if 'prefix' in nodes['l3-unicast-igp-topology:igp-node-attributes'].keys():
                    for prefix in nodes['l3-unicast-igp-topology:igp-node-attributes']['prefix']:
                        prefix_array.append(prefix['prefix'])
                #node_ports = []
                if 'router-id' in nodes['l3-unicast-igp-topology:igp-node-attributes'].keys():
                    if 'name' in nodes['l3-unicast-igp-topology:igp-node-attributes'].keys():
                        node['name'] = nodes['l3-unicast-igp-topology:igp-node-attributes']['name']
                        #node['name'] = nodes['l3-unicast-igp-topology:igp-node-attributes']['node-name']
                    else:
                        pass
                    node['loopback'] = nodes['l3-unicast-igp-topology:igp-node-attributes']['router-id'][0]
                else:
                    node['name'] = 'zzzzz'
                    node['loopback'] = "0.0.0.0"
                node['prefix'] = prefix_array                
                node['id'] = nodes['node-id']
                node_list.append(node)
        except Exception:
            print('error')
        return node_list
    
    def parseLinks(self, my_topology):
            link_list = []
            try:
                for link in my_topology['topology'][0]['link']:
                    temp = {}
                    temp['source'] = link['source']['source-node']
                    temp['target'] = link['destination']['dest-node']
                    temp['metric'] = link['l3-unicast-igp-topology:igp-link-attributes']['metric']
                    link_list.append(temp)
                    
            except Exception:
                print('error')
            return link_list   
    
    #
    def dupLink(self, links):   
        link_list=[]
        for i in range(len(links)-1):                    
            temp={}
            for j in range(i+1,len(links)):
                if links[i]['source'] == links[j]['target'] and links[i]['target'] == links[j]['source']:
                    temp["source"] = links[i]['source']
                    temp["target"] = links[i]['target']
                    link_list.append(temp)
                    
        return link_list

              

if __name__ == "__main__":
    main()