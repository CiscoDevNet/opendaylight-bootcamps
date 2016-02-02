from dbServices import DbServices
from resroucemanage import ODLRscGetter
import utils.constants as const
from service.models import SCApp,SCInstance,SCTemplate
from flowmanage import OFManager

SC_TPLT_NAME_PREFIX = "sc_template_"

class SvcChain(object):
    def __init__(self, controller):
        self.controller = controller
        self.dbSvc = DbServices()
        self.flowSvc = OFManager(controller)
        self.base_flow_id = 1000
        self.rscSvc = ODLRscGetter(controller)

    def _generate_name(self, prefix, model):
        modle_list = self.dbSvc._list_rsc(self.session, model)
        count = "0"
        if modle_list:
            count = str(len(modle_list))
        return prefix+count

    def define_sc_tplt(self, pipeline, tpltName=None, tpltID=None):
        if not tpltName:
            tplt_name = self._generate_name(SC_TPLT_NAME_PREFIX, SCTemplate)
        else:
            tplt_name = tpltName
        sc_tplt = SCTemplate()
        sc_tplt.set_attributes(tpltName= tplt_name,tpltPipe= pipeline, tpltId=tpltID)
        self.dbSvc.add_sctplt(sc_tplt)
        return sc_tplt

    def define_sc_inst(self, tpltId, proto, dst_port, instId):
        sc_inst = SCInstance()
        sc_inst.set_attributes(protocol=proto, port=dst_port, template=tpltId,id=instId)
        self.dbSvc.add_scinstance(sc_inst)
        return sc_inst

    def define_sc_app(self,node_name, inst_id):
        of_node = self.dbSvc.get_ofnode_by_name(node_name)
        node_id = of_node.nodeid
        return self.define_sc_app_by_id(node_id, inst_id)
    
    def define_sc_app_by_id(self, node_id, inst_id):
        sc_app = SCApp()
        app_id = "/".join([node_id,inst_id])
        sc_app.set_attributes(node_id, inst_id, app_id)
        self.dbSvc.add_scapp(sc_app)
        self.write_flow(node_id, inst_id)
        return sc_app

    def _generate_flow_id(self):
        self.base_flow_id +=1
        return self.base_flow_id

    def calculate_outpute_port(self, srcNode, dstNode):
        of_link = self.dbSvc.get_oflink_by_srcdst(srcNode.nodeid, dstNode.nodeid)
        src_port = of_link.srcPort
        of_port_no = int(src_port.split(":")[-1])
        return of_port_no

    def is_nfv_node(self, nodetype):
        return nodetype in const.available_nfv_types

    def calculate_inport(self, from_node, to_node):
        of_link = self.dbSvc.get_oflink_by_srcdst(from_node.nodeid, to_node.nodeid)
        dst_port = of_link.dstPort
        of_port_no = int(dst_port.split(":")[-1])
        return of_port_no

    def get_app_match_fields(self, host_node,sc_instance):
        sc_proto = sc_instance.proto
        sc_port = sc_instance.port
        src_mac = host_node.mac
        return {
            "src_mac":src_mac,
            "protocol":sc_proto,
            "dst_port":sc_port
        }

    def construct_sw_flow(self, sw_node, priority, from_node, to_node , **match_fields):
        in_port = self.calculate_inport(from_node, sw_node)
        outputPort = self.calculate_outpute_port(sw_node, to_node)
        match_fields.update({"in_port":in_port})
        flow_node_id = sw_node.nodeid
        table_id = 0
        flow_id = self._generate_flow_id()

        self.flowSvc.construct_flow(flow_node_id, table_id, flow_id, priority, output_port=outputPort, return_pts = False, **match_fields)

    def construct_vnf_flow(self, vnf, sw_node, priority, **match_fields):
        flow_node_id = vnf.nodeid
        flow_id = self._generate_flow_id()
        table_id = const.TABLE_ID_VNF
        self.flowSvc.construct_flow(flow_node_id, table_id, flow_id, priority, ret_pkt=True, **match_fields)

    def write_flow(self, host_node_id, inst_id):
        host_node = self.dbSvc.get_ofnode(host_node_id)
        sc_instance = self.dbSvc.get_scinstance(inst_id)
        sc_template = self.dbSvc.get_sctplt(sc_instance.tpltID)
        sw_node = self.dbSvc.get_ofnode_by_type(const.SWITCH)
        match_fields = self.get_app_match_fields(host_node,sc_instance)
        from_node = host_node
        sw_priority = const.PRIORITY_SW_FLOW
        vnf_priority = const.PRIORITY_VNF_FLOW
        for node_type in sc_template.getPipleLine():
            if not self.is_nfv_node(node_type):
                continue
            vnf = self.dbSvc.get_ofnode_by_type(node_type)
            self.construct_sw_flow(sw_node, sw_priority, from_node, vnf, **match_fields)
            self.construct_vnf_flow(vnf, sw_node, vnf_priority, **match_fields)
            from_node = vnf

    def is_node_exists(self, ofnode):
        node = self.dbSvc.get_ofnode_by_mac(ofnode.mac)
        if node:
            return True
        return False
    
    def is_link_exist(self, link):
        link = self.dbSvc.get_oflink(link.linkid)
        if link:
            return True
        return False

    def sync_ofnodes(self):
        ofnode_configs = self.rscSvc.getOFNodes()
        for key in ofnode_configs.keys():
            switch_node = ofnode_configs[key][const.SWITCH]
            if not self.is_node_exists(switch_node):
                self.dbSvc.add_ofnode(switch_node)
            host_nodes = ofnode_configs[key][const.HOST]
            for host in host_nodes:
                if not self.is_node_exists(host):
                    self.dbSvc.add_ofnode(host)
        self.sync_oflinks()
        return ofnode_configs

    def sync_oflinks(self):
        expect_count = self.rscSvc.countSw() - 1
        expect_count = expect_count if expect_count> 0 else 0
        of_links = self.rscSvc.getOFLinks(expect_count)
        for lnk in of_links:
            if not self.is_link_exist(lnk):
                self.dbSvc.add_oflink(lnk)
        return of_links

    def set_vnf_type_by_name(self, sw_name, type):
        ofnode = self.dbSvc.get_ofnode_by_name(sw_name)
        self.dbSvc.mod_ofnode_type(ofnode.nodeid, type)

    def get_all_ofnods(self):
        self.sync_ofnodes()
        nodes_list = self.dbSvc.list_ofnodes()
        return nodes_list

    def get_tpltid_by_name(self, name):
        tplt = self.dbSvc.get_tplt_by_name(name)
        if tplt:
            return tplt.tpltid
        
    def get_all_templates(self):
        return self.dbSvc.list_sctplt()
    
    def get_all_instances(self):
        return self.dbSvc.list_scinstance()
    
    def get_all_apps(self):
        return self.dbSvc.list_scapp()
    
    def update_node_type(self, node_id, type):
        self.dbSvc.mod_ofnode_type(node_id, type)