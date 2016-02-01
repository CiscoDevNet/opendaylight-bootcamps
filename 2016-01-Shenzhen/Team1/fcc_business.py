import json
from group1.constant import *
import route_algorithm
import static_route_create_dong
import get_rtl
import pcep_put_dong

def load(text):
    with open(text) as json_file:
        data = json.load(json_file)
        return data

class Node():
    def __init__(self, node_id):
        self.long_id = node_id
        self.id = self.long_id[-14:]
        self.name = ID2NAME[self.id]
        self.mng_ip = ID2MNGIP[self.id]

class Link():

    CAPACITY = 10

    def __init__(self, link_id, capacity=None):
        self.long_id = link_id
        self.id = self._id_trans()
        self.snode_id = self._get_snode_id()
        self.dnode_id = self._get_dnode_id()
        self.sinterface_ip = self._get_sinterface_ip()
        self.dinterface_ip = self._get_dinterface_ip()
        if capacity:
            self.capacity = capacity
        else:
            self.capacity = self.CAPACITY

    def _id_trans(self):
        return self.long_id[-23:-21] + '.' + self.long_id[-2:]

    def _get_snode_id(self):
        return self.long_id[-125:-111]

    def _get_dnode_id(self):
        return self.long_id[-56:-42]

    def _get_sinterface_ip(self):
        return self.long_id[-30:-21]

    def _get_dinterface_ip(self):
        return self.long_id[-9:]

class Topo():
    def __init__(self, nodes, links):
        self.nodes = nodes
        self.man_nodes = self._get_man_nodes()
        self.links = links
        self.man_links = self._get_man_links()
        self.adj_graph = self._get_adj_graph()
        self.man_adj_graph = self._get_man_adj_graph()

    def _get_adj_graph(self):
        adj_graph = []
        for i in range(len(self.nodes)):
            adj_graph.append(len(self.nodes) * M1)
        for link in self.links:
            i = ID2SEQ[link.snode_id]
            j = ID2SEQ[link.dnode_id]
            adj_graph[i][j] = 1
        
        return adj_graph
    
    def _get_man_adj_graph(self):                 
        man_adj_graph = []
        for i in range(len(self.man_nodes)):
            man_adj_graph.append(len(self.man_nodes) * M1)
        for link in self.man_links:
            i = ID2SEQ[link.snode_id]
            j = ID2SEQ[link.dnode_id]
            man_adj_graph[i][j] = 1
        
        return man_adj_graph
        
    def _get_man_nodes(self):    
        man_nodes = []
        for node in self.nodes:
            if ROUTER_DESCRIPTION[node.id] == MAN_ROUTER or ROUTER_DESCRIPTION[node.id] == FCC_ROUTER:
                man_nodes.append(node)
        
        return man_nodes
    
    def _get_man_links(self):
        man_links = []
        for link in self.links:
            if ROUTER_DESCRIPTION[link.snode_id] and ROUTER_DESCRIPTION[link.dnode_id]:
                man_links.append(link)
        
        return man_links

    def get_man_rtl_graph(self):
        return self._get_man_rtl_graph()
        
    def _get_man_rtl_graph(self):
        man_rtl_graph = []
        for i in range(len(self.man_nodes)):
            man_rtl_graph.append(len(self.man_nodes) * M2)
        for link in self.man_links:            
            snode_id = link.snode_id
            dnode_id = link.dnode_id            
            i = ID2SEQ[link.snode_id]
            j = ID2SEQ[link.dnode_id]
            
            sdevice_name = ID2DEV[snode_id]
            sinterface_name = IP2INTNAME[link.sinterface_ip]
            
            sinterface_rtl = get_rtl.get_real_time_load(sdevice_name, sinterface_name)
            man_rtl_graph[i][j] = sinterface_rtl        
    
    def getlink(self, current_hop_id, next_hop_id):
        for link in self.links:
            if link.snode_id == current_hop_id and link.dnode_id == next_hop_id:
                return link

def print_node(node):
    print(node.name)
    print(node.long_id)
    print(node.id)

def print_link(link):
    print(link.long_id)
    print(link.id)
    print(link.snode)
    print(link.dnode)

def print_topo(topo):
    pass

def main():
    # PATH = bgp_ls_sync()
    def traffic_washing(topo, protect_target): 
        man_nodes = topo.man_nodes
        man_routers_id = []
        fcc_routers_id = []
        
        for node in man_nodes:
            if ROUTER_DESCRIPTION[node.id] == MAN_ROUTER:
                man_routers_id.append(node.id)
            elif ROUTER_DESCRIPTION[node.id] == FCC_ROUTER:
                fcc_routers_id.append(node.id)
        
        fcc_router_id = get_fcc_for_target(protect_target)
        #assert fcc_router_id in fcc_routers_id
             
        traffic_steer_to_fcc(topo, man_routers_id, fcc_router_id, protect_target)
        traffic_inject_from_fcc(topo, fcc_router_id, protect_target)
        
    def traffic_steer_to_fcc(topo, man_routers_id, fcc_router_id, protect_target):
        for man_router_id in man_routers_id:
            seq1 = ID2SEQ[man_router_id]
            seq2 = ID2SEQ[fcc_router_id]
            
            man_adj_graph = topo.man_adj_graph
            #man_rtl_graph = topo.get_man_rtl_graph()
            
            #rtl_route= route_algorithm.rtl_route(man_adj_graph, man_rtl_graph, seq1, seq2)
            #if rtl_route:
              #  sroute_for_fcc = rtl_route
            #else:
            sroute_for_fcc = route_algorithm.spf_route(man_adj_graph, seq1, seq2)
            #print(sroute_for_fcc)
            print('sroute_for_fcc')
            print(sroute_for_fcc)
            
            router_sroute_sent = []
            for i in range(len(sroute_for_fcc) - 1):
                
                current_hop_id = SEQ2ID[sroute_for_fcc[i]]
                next_hop_id = SEQ2ID[sroute_for_fcc[i+1]]
                
                dev = ID2DEV[current_hop_id]
                nexthop_ipaddr = topo.getlink(current_hop_id, next_hop_id).dinterface_ip
                
                print(dev)
                print(nexthop_ipaddr)
        
                if current_hop_id not in router_sroute_sent:
                    static_route_create_dong.demonstrate(dev, nexthop_ipaddr)
                    router_sroute_sent.append(current_hop_id)
    
    def traffic_inject_from_fcc(topo, fcc_router_id, protect_target):
        pcep_put_dong.pcep_update_lsp()
        
    def get_fcc_for_target(protect_target):
        return FCCSERV[protect_target]

    data = load(PATH)
    rnodes = data["topology"]["node"]
    rlinks = data["topology"]["link"]

    nodes = []
    for rnode in rnodes:
        rnode_id = rnode["node-id"]
        node = Node(rnode_id)
        nodes.append(node)

    links = []
    for rlink in rlinks:
        rlink_id = rlink["link-id"]
        # capacity =
        link = Link(rlink_id)
        links.append(link)

    topo = Topo(nodes, links)    

    traffic_washing(topo, "1.2.3.4")

if __name__ == '__main__':
    main()
