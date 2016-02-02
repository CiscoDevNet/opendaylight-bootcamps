__author__ = 'cmcc'

from utils.restconf import ODLRestRequest
from service.models import OFNodeBase,OfLink
import utils.constants as const
import time


MAX_RETRY_TIMES = 5

class ODLRscGetter(object):
    def __init__(self, ctr_ip=None):
        self.controller_ip = ctr_ip if ctr_ip else const.DEFAULT_ODL_CONTROLLER_IP
        self.odlRequest = ODLRestRequest(self.controller_ip)

    def generateSwithNode(self, ofNode, node_id):
        node_id = node_id
        node_mac = ofNode["flow-node-inventory:hardware-address"]
        node_name = ofNode["flow-node-inventory:name"].partition("-")[0]
        node_type = const.SWITCH
        node = OFNodeBase()
        node.set_attributes(id=node_id,name=node_name, mac=node_mac, type=node_type)
        return node


    def generateHostNode(self, ofNode):
        node_mac = ofNode["address-tracker:addresses"][0]["mac"]
        node_ip = str(ofNode["address-tracker:addresses"][0]["ip"])
        node_name = "host:"+node_ip
        node_type = const.HOST
        node_profile = "ip:"+node_ip
        node_id = "host:"+node_mac
        node = OFNodeBase()
        node.set_attributes(id=node_id,name=node_name, mac=node_mac, type=node_type, profile=node_profile)
        return node

    def getOFNodes(self):
        ofnode_configs = {}
        node_list = self.odlRequest.list_openflow_nodes()

        for ofnode in node_list:
            group_node = ofnode["node-connector"]
            node_id = ofnode["id"]
            ofnode_configs.update({node_id:{"host":[]}})
            for node in group_node:
                node_type = node["flow-node-inventory:port-number"]
                if node_type == "LOCAL":
                    switch = self.generateSwithNode(node, node_id)
                    ofnode_configs[node_id].update({const.SWITCH:switch})
                elif node.get("address-tracker:addresses", None):
                    host = self.generateHostNode(node)
                    ofnode_configs[node_id][const.HOST].append(host)
                else:
                    continue

        return ofnode_configs

    def _get_ofnode_no(self, node):
        return node.split(":")[1]

    def _get_flow_id(self, lnk_src_node, lnk_dst_node):
        return "openflow:"+self._get_ofnode_no(lnk_src_node) + ":" + self._get_ofnode_no(lnk_dst_node)

    def _generate_links(self, lnk):
        lnk_src_port = lnk["source"]["source-tp"]
        lnk_src_node = lnk["source"]["source-node"]
        lnk_dst_port = lnk["destination"]["dest-tp"]
        lnk_dst_node = lnk["destination"]["dest-node"]

        if lnk_src_node.find("openflow") >= 0 and lnk_dst_node.find("openflow")>=0 :
            lnk_id = self._get_flow_id(lnk_src_node, lnk_dst_node)
            rev_lnk_id = self._get_flow_id(lnk_dst_node, lnk_src_node)
        else:
            lnk_id = lnk["link-id"]
            src, splitor, dst = lnk["link-id"].partition("/")
            rev_lnk_id = "/".join([dst, src])

        of_link = OfLink()
        of_link.set_attributes(link_id=lnk_id,srcnode=lnk_src_node,dstnode=lnk_dst_node,srcport=lnk_src_port, dstport=lnk_dst_port)
        rvs_link = OfLink()
        rvs_link.set_attributes(link_id=rev_lnk_id,srcnode=lnk_dst_node,dstnode=lnk_src_node,srcport=lnk_dst_port, dstport=lnk_src_port)
        return of_link, rvs_link

    def _is_oflink_exist(self, of_links, lnk):
        for link in of_links:
            if link.snode == lnk.snode and link.dnode == lnk.dnode:
                return True
        return False

    def getOFLinks(self, expect_count):
        of_links =[]
        retry = 0
        while(retry < MAX_RETRY_TIMES):
            topology =  self.odlRequest.get_openflow_topology()
            if topology.get("link", []):
                links = topology["link"]
                print("getOFLinks: get link count: " + str(len(links)))
                if len(links) < expect_count:
                    print("OFlinks got less then expect")
                    continue
                for lnk in links:
                    of_link, rev_link = self._generate_links(lnk)
                    if not self._is_oflink_exist(of_links, of_link):
                        of_links.append(of_link)
                    if not self._is_oflink_exist(of_links, rev_link):
                        of_links.append(rev_link)
                return of_links
            time.sleep(0.5)

    def countSw(self):
        node_list = self.odlRequest.list_openflow_nodes()
        return len(node_list)

    def _getAllOFSwitches(self, ofnode_configs):
        switches = []
        for cfg in ofnode_configs.values():
            switch = cfg.get(const.SWITCH, None)
            if switch:
                switches.append(switch)
        return switches

    def _getAllHosts(self, ofnode_configs):
        hosts = []
        for cfg in ofnode_configs.values():
            host_list = cfg.get(const.HOST,[])
            if host_list:
                hosts.extend(host_list)
        return hosts
