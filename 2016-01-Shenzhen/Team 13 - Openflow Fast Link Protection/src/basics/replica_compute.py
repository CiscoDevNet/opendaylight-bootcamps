'''
Created on Jan 22, 2016

@author: Bluesy Wang
@author: Feng Guo
'''
from src.settings import network_configuration
import networkx as nx
import logging as log

class ReplicaComputer():
    def __init__(self,flowinstaller):
        self.Nodes = {}
        self.Links = {}
        self.pathes = []
        self.flowinstaller = flowinstaller
    
    def setNodes(self,nodes):
        self.Nodes = nodes
        print self.Nodes
        
    def setLinks(self,links):
        self.Links = links
        print self.Links
    
    def computePath(self):
        Topo = nx.Graph()
        Topo_Nodes = []
        for Node in self.Nodes:
            Topo_Nodes.append(self.get_physical_node_id(Node))
            Topo.add_nodes_from(Topo_Nodes)
        for Link in self.Links:
            top_node_port_pair = Link.split('-')
            top_node = top_node_port_pair[0]
            tail_node_port_pair = self.Links[Link].split('-')
            tail_node = tail_node_port_pair[0]
            Topo.add_edge(int(top_node), int(tail_node), weight=1)
        host1 = network_configuration.host1_node.split(':')
        host2 = network_configuration.host2_node.split(':')
        path_iter = nx.all_simple_paths(Topo, int(host1[1]), int(host2[1]))
        
        for p in path_iter:
            self.pathes.append(p)
        print self.pathes
          
        for p in self.pathes: 
            print self.get_path_length(Topo, p), '\t', p
        
        least_length = 100;
        for p in self.pathes:
            path_length = self.get_path_length(Topo, p)
            if least_length > path_length:
                least_length = path_length
                self.normal_path = p
        print self.normal_path
        
        iterate_num = 0
        for this_node in self.normal_path:
            if iterate_num == 0:
                next_node = self.get_next_node(self.normal_path, this_node)
                if self.Links.has_key(str(this_node)+'-'+str(next_node)):
                    port_pair = self.Links[str(this_node)+'-'+str(next_node)]
                    out_port = port_pair.split('-')[1]
                else:
                    port_pair = self.Links[str(next_node)+'-'+str(this_node)]
                    out_port = port_pair.split('-')[1]

                flow1 = {"node-id":'openflow:'+this_node,"table-id":"0","flow-id":"odl"+iterate_num+'init',"in-port":network_configuration.host1_port,
        "dl-src":network_configuration.host1_mac,"dl-dst":network_configuration.host2_mac,"out-port":out_port}
                self.flowinstaller.installflow(flow1)
                log.info('install flow entry!')
            iterate_num+=1
            
            
    def get_physical_node_id(self, logical_node_id):
        physical_node_id = self.Nodes[str(logical_node_id)]
        physical_node_id_tmp =  physical_node_id.split(':')
        return int(physical_node_id_tmp[1])
    
    def get_path_length(self, graph, p):
        length = 0.0
        for i in range(len(p) - 1):
            length += graph[p[i]][p[i + 1]]['weight']
        return length
    
    def get_next_node(self,path, node):
        node_index = 0
        for node_iter in path:
            if node_index == len(path)-1:
                return path[0]
            if node == node_iter:
                return path[node_index+1]
            node_index+=1
        return

    def get_front_node(self,path, node):
        node_index = len(path)-1;
        for node_iter in path:
            if node_index == 0:
                return path[len(path)-1]
            if node == node_iter:
                return path[node_index-1]
            node_index-=1
        return

Nodes = {'1':'openflow:1', '2':'openflow:2', '3':'openflow:3', '4':'openflow:4', '5':'openflow:5', '6':'openflow:6', '7':'openflow:7'}
Links = {'2-2':'5-1', '4-1':'3-3', '4-2':'5-2', '5-4':'6-3', '5-3':'7-1', '7-2':'6-4', '3-2':'2-1', '3-1':'1-3'}
   
Topo = nx.Graph()
Topo_Nodes = []
for Node in Nodes:
    Topo_Nodes.append(int(Node))
Topo.add_nodes_from(Topo_Nodes)
for Link in Links:
    top_node_port_pair = Link.split('-')
    top_node = top_node_port_pair[0]
    tail_node_port_pair = Links[Link].split('-')
    tail_node = tail_node_port_pair[0]
    Topo.add_edge(int(top_node), int(tail_node), weight=1)
'''    
TODO 1 6
'''
  
def get_path_length(graph, p):
    length = 0.0
    for i in range(len(p) - 1):
        length += graph[p[i]][p[i + 1]]['weight']
    return length
  
def get_next_node(path, node):
    node_index = 0
    for node_iter in path:
        if node_index == len(path)-1:
            return path[0]
        if node == node_iter:
            return path[node_index+1]
        node_index+=1
    return
  
def get_front_node(path, node):
    node_index = len(path)-1;
    for node_iter in path:
        if node_index == 0:
            return path[len(path)-1]
        if node == node_iter:
            return path[node_index-1]
        node_index-=1
    return
  
pathes = []
path_iter = nx.all_simple_paths(Topo, 1, 6)
for p in path_iter:
    pathes.append(p)
print pathes
  
for p in pathes: 
    print get_path_length(Topo, p), '\t', p
      
least_length = 100;
for p in pathes:
    path_length = get_path_length(Topo, p)
    if least_length > path_length:
        least_length = path_length
        normal_path = p
  
print normal_path
print least_length
  
iterate_num = 0
node_signal = []
for node in normal_path:
    '''
    the first node, mark it as drop node
    '''
    if iterate_num==1:
        '''
        [node-id, backup, node-type]
        '''
        node_signal.append([node,0,0])
        pass
    '''
    the last node, mark it as no-consider node
    '''
    if iterate_num==least_length:
        pass
    for p in pathes:
        if p == normal_path:
                pass
        '''
        consider no-normal path
        '''
        for node_in_otherpath in p:
            '''
            look up the same node in other pathes, find out its next node, if it has another next node,
            we can find this node be a node with a backup path  
            '''
            if node_in_otherpath == node:
                if get_next_node(p, node_in_otherpath) != get_next_node(normal_path, node):
                    backup_node = get_next_node(p, node_in_otherpath)
                    '''
                    continue to look up its front node, if it has another front node, we can find this node 
                    be a aggregation node
                    '''
                    for node_in_otherpath in p:
                        if node_in_otherpath == node:
                            if get_front_node(p, node_in_otherpath) != get_front_node(normal_path, node):
                                node_signal.append([node,backup_node,3])
                                break;
                    break;
            '''
            if all the same nodes in other pathes have same next node and front node, we can find this node
            be a relay node 
            '''
                          
      
    iterate_num+=1
   


