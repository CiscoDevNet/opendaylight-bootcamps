'''
Created on Jan 22, 2016

@author: Hu Qiwei
'''
#-*- coding:utf-8 -*-
import requests
import threading
import logging as log
import time



class TopoMonitor(threading.Thread):
    
    def __init__(self, replicacompute):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ip = '10.1.0.221'
        self.port = 8181
        'structure data topology {node1:{port1:{(nodex,nodex_portx,current_port_status)},'
        'port2:{(nodex,nodex_portx,up_True or down_False)},......},node2:{},......}'
        self.topoid = ''
        self.topoid_normal = ''
        self.topo_status= 'normal'
        'down_port'
        self.down_port = []
        self.replicacompute = replicacompute
    
    '''
    to get nodes,pls use method get_topo() first
    return {'1':'node',......}
    '''
    def get_nodes(self):
        node_to_int = {}
        node_index = 1
        for node in self.topoid_normal:
            node_to_int['%d'%node_index] = node
            node_index += 1
        node_to_del = []
        for node in node_to_int:
            if ('host' in node_to_int[node]) or ('host' in node):
                node_to_del.append(node)
        for node in node_to_del:
            del node_to_int[node]
        return node_to_int
    
    '''
    to get links,pls use method get_topo() first
    return {'1':'2',......} i.e. switch1<--->switch2
    '''
    def get_links(self):
        links_dict = {}
#         node_2_int_s = ''
#         node_2_int_d = ''
#         port_2_int_s = ''
#         port_2_int_d = ''
        node_to_del = []
        'remove the hosts'
        for node in self.topoid_normal: 
            for port in self.topoid_normal[node]:          
                if ('host' in node) or ('host' in  self.topoid_normal[node][port][0]):
                    if node in node_to_del:
                        pass
                    else:
                        node_to_del.append(node)
#         print node_to_del
        for node in node_to_del:
                del self.topoid_normal[node]                              
#         print self.topoid_normal
        
        for node in self.topoid_normal:           
            for port in self.topoid_normal[node]:           
                if (self.topoid_normal[node][port][0] != '') and (self.topoid_normal[node][port][1] != ''):
                    src = '%s-%s'%(port.split(':')[1],port.split(':')[2])                   
                    dst = '%s-%s'%(self.topoid_normal[node][port][1].split(':')[1],self.topoid_normal[node][port][1].split(':')[2])
                    links_dict[src] = dst
#         print links_dict
#         links_dict_del = []

# to remove multi same links
        src_list = []
        dst_list = []
#             if src == links_dict[links_dict[src]]:
#                 links_dict_del.append(src)
#                 print links_dict_del
        for src in links_dict:
            dst_list.append(links_dict[src]) 
        for src in links_dict:
            src_list.append(src) 
        for src in src_list:
            if src in dst_list:
                dst_list.remove(links_dict[src])                
                del links_dict[src]                           
        #print links_dict
        'to remove the redundancy links'
#         del_list_tmp = []
#         for element in links_dict:
#             if element == links_dict[links_dict[element]]:
#                 del_list_tmp.append(element)
#         for element in del_list_tmp:
#             del links_dict[element]
#     
#     for element in links_dict:
#         
        return links_dict
                
    '''
    to get the topo from the controller
    '''
    def request_topo_json(self):
    #     url = 'http://:8181/restconf/config/network-topology:network-topology/topology/topology-openflow''
        self.url = 'http://%s:%d/restconf/operational/network-topology:network-topology/'%(self.ip,self.port)
        headers = {'content-type': 'application/json', }
        response = requests.get(self.url,auth = ('admin','admin'),headers=headers)
        result_json = response.json()
#         print result_json
        return result_json
    
    '''
    to parse the response of json 
    '''
    def parse_topo_json(self,result_json):   
        'Note:It is just a OpenFlow topology in our project.'
        'Each topology is a dictionary that is contained in topo_flow list and/or topo_temp'
        topo_flow = []
        topo_temp = []
        'to get all topologies'
        for tp in result_json['network-topology']["topology"]:
            topo_temp.append(tp)
        'to get topo based OpenFlow'
        for tp in topo_temp:
            if 'flow' in tp["topology-id"]:
                    topo_flow.append(tp)
        'print three properties of one topology'
        print 'The 1th topo based OpenFlow is %s'%topo_flow[0]['topology-id']
    #     print topo_flow[0]['link']
    #     print topo_flow[0]['node']
        topo = self.analyses_nodes(topo_flow[0]['node'])
        'The topo will be used to add links between ports'
        'i.e. we will get the links between SDN switch now'
        topo = self.analyses_links(topo_flow[0]['link'],topo)
    #     link_l = analyses_links(topo_flow[0]['link'])
        
        return topo
    
    '''
    to parse the response of xml 
    unused
    '''
    def parse_topo_xml(self,result_xml):    
        return self.topoid
    
    # def compute_backup_path():
    #     pass
    # 
    # def install_flow():
    #     pass
    '''
    to get topo
    '''
    def get_topo(self):    
        topo_id = self.parse_topo_json(self.request_topo_json())
        return topo_id
    
    '''
    to get links between SDN switches
    '''
    def analyses_links(self,links,topo):
        '''
        topo:topo_id
        node:node_id
        port:tp_id
        link:link_id
        '''
        for nodeid in topo:
            for tpid in topo[nodeid]:
                for link in links:
    #                 print link
    #                 print nodeid
    #                 print tpid
                    if (link['source']['source-node'] == nodeid) or (link['destination']['dest-node'] == nodeid):
                        if link['source']['source-tp'] == tpid: 
                            topo[nodeid][tpid][0] = link['destination']['dest-node']
                            topo[nodeid][tpid][1] = link['destination']['dest-tp']
                        elif link['destination']['dest-tp'] == tpid:
                            topo[nodeid][tpid][0] = link['source']['source-node']
                            topo[nodeid][tpid][1] = link['source']['source-tp']
                            
                         
        return topo
    
    '''
    to get all nodes
    this method will invoke method "analyses_ports" to get ports of each SDN switch
    '''
    def analyses_nodes(self, nodes):
        node_dict = {}
        for n in nodes:
            'to create 1th level dictionary'
            node_dict[n['node-id']] = self.analyses_ports(n['termination-point'])           
        'test'
    #     print node_dict
        return node_dict
    
    '''
    to get ports of each SDN switch
    '''
    def analyses_ports(self, ports):
        port_dict = {}
        for p in ports:
            'to create 2th level dictionary'
            'True,port is up '
            'False or not'
            port_dict[p['tp-id']] = ['','']
        'test'
    #     print port_list
        return port_dict
    
    '''
    to detect the link-down,it's just to judge SDN switch port status
    When the link is down,the link between SDN switches will be rewoved by the SDN switches.
    So if the amount of link is changed,the topo will be requested to refresh.
    Then the new paths including normal path and backup path will be computed out
    '''
    def dtect_network_change(self):
    #   topo_before = topoid
    #   time.sleep(18)
        self.topoid = self.get_topo()
    #   topo_now = topoid
        self.dtect_link_change(self.topoid_normal,self.topoid)
    
    '''
    to dect link change,the lost link will be return
    return lost links in dict
    '''
    def dtect_link_change(self,topoid_normal,topoid):
        'node dtection first'
    #     print 'enter......'
        
    #     node_lost = dtect_node_change(topo_before,topo_now)
    #     if len(node_lost) != 0:
    #             '---------------------------------------------------'
    #             'to invoke module of computing path'
    #             '---------------------------------------------------'
    #             pass
        'link dtection second'
        link_b = {}
        link_n = {}
        link_lost = []
        link_lost_dict = {}
        for node in self.topoid_normal:
            for port in self.topoid_normal[node]:
        #print topoid_normal[node][port]
                link_b[port] = self.topoid_normal[node][port]
        for node in self.topoid:
            for port in self.topoid[node]:
                link_n[port] = self.topoid[node][port]
        for element in link_b:
#             print link_b[element]
            if link_b[element] == link_n[element]:
                if self.topo_status == 'inormal':
                    self.topo_status = 'normal'
#                     print 'Warning:The link is normal!!!'
                
            elif link_b[element] != link_n[element]:
                if self.topo_status == 'normal':
                    self.topo_status = 'inormal'
#                     print 'Warning:The link which is releated to port %s is lost!!!'%link_b[element]
                    link_lost.append(element)
                    src_p = '%s-%s'%(element.split(':')[1],element.split(':')[2])
                    if link_b[element][1] == '':
                        dst_p = ['','']
                    else:
                        dst_p = '%s-%s'%(link_b[element][1].split(':')[1],link_b[element][1].split(':')[2])
                    link_lost_dict[src_p] = dst_p 
                    '---------------------------------------------------'
                    'to invoke module of computing path'
                    '---------------------------------------------------'  
        print link_lost_dict            
                 
        return link_lost_dict
    
    '''
    to dtect node change,the lost node will be return
    '''
    def dtect_node_change(self, topo_before,topo_now):
        node_lost=[]
        node_list_b = []
        node_list_n = []
        for node_b in topo_before:
            node_list_b.append(node_b)
        for node_n in topo_now:
            node_list_n.append(node_n)
        for element in node_list_b:
            if element in  node_list_n:
                pass
            else:
                print 'Warning:The node %s is lost!!!'%element
                node_lost.append(element)
                print 'node_lost%s'%node_lost
        return node_lost
    
    
    def run(self):
        """
        Main function run by thread
        """
        log.info("Topo Awaring starting")
        self.topoid_normal = self.get_topo()
        self.replicacompute.setNodes(self.get_nodes())
        self.replicacompute.setLinks(self.get_links())
        self.replicacompute.computePath()
        while(True):
            self.dtect_network_change()
            time.sleep(1)

'''
if __name__ == '__main__':
    print get_topo()
    dtect_network_change(topoid)
'''