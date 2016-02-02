__author__ = 'cmcc'

import utils.openflowutils as ofutils
import utils.constants as const
from utils.restconf import ODLRestRequest
from xml.dom.minidom import Document

global auto_flow_id
auto_flow_id = 0
class OFManager(object):

    def __init__(self, ctr_ip=None):
        self.controller_ip = ctr_ip if ctr_ip else const.DEFAULT_ODL_CONTROLLER_IP
        self.odlRequest = ODLRestRequest(self.controller_ip)

    def write_flow(self, flowbody):
        return self.odlRequest.config_openflow(self.controller_ip, flowbody)

    def get_input_elem(self, doc):
        input = doc.createElement('input')
        input.setAttribute("xmlns","urn:opendaylight:flow:service")
        doc.appendChild(input)
        return input

    def get_node_elem(self, node_id, doc):
        node = doc.createElement("node")
        node.setAttribute("xmlns:inv","urn:opendaylight:inventory")
        node_id = doc.createTextNode(node_id)
        node.appendChild(node_id)
        return node

    def get_table_elem(self, table_id, doc):
        table = doc.createElement("table_id")
        table_id = doc.createTextNode(str(table_id))
        table.appendChild(table_id)
        return table

    def get_priority_elem(self, priority, doc):
        priority_node = doc.createElement("priority")
        prio_value = doc.createTextNode(str(priority))
        priority_node.appendChild(prio_value)
        return priority_node

    def convert_dict_to_xml(self, dict_obj, doc):
        node_list = []
        for key, value in dict_obj.iteritems():
            key_node = doc.createElement(key)
            if isinstance(value, dict):
                value_nodes = self.convert_dict_to_xml(value,doc)
                for node in value_nodes:
                    key_node.appendChild(node)
            elif isinstance(value, list):
                value_nodes = self.get_list_node(value, doc)
                for node in value_nodes:
                    key_node.appendChild(node)
            else:
                value = str(value)
                value_node = doc.createTextNode(str(value))
                key_node.appendChild(value_node)
            node_list.append(key_node)
        return node_list

    def get_flow_match(self, match, doc):
        match_nodes = self.convert_dict_to_xml(match, doc)
        return match_nodes

    def get_list_node(self, value_list, doc):
        node_list = []
        for value in value_list:
            if isinstance(value, str) or isinstance(value, int):
                value_node = doc.createTextNode(value)
                node_list.append(value_node)
            elif isinstance(value,dict):
                value_nodes = self.convert_dict_to_xml(value, doc)
                node_list.extend(value_nodes)
        return node_list

    def convert_flow_toxml(self, node_id, table_id, priority, matches, action_list):
        doc = Document()
        input = self.get_input_elem(doc)
        node_id = "/inv:nodes/inv:node[inv:id=\"%s\"]"%node_id
        node = self.get_node_elem(node_id, doc)
        input.appendChild(node)
        table = self.get_table_elem(table_id,doc)
        input.appendChild(table)
        priority = self.get_priority_elem(priority, doc)
        input.appendChild(priority)
        match = self.get_flow_match(matches, doc)
        for node in match:
            input.appendChild(node)
        instructions = doc.createElement("instructions")
        instruction = doc.createElement("instruction")
        appl_action = doc.createElement("apply-actions")
        appl_action_order = doc.createElement("order")
        appl_acion_order_value = doc.createTextNode("0")
        appl_action_order.appendChild(appl_acion_order_value)
        action_list_nodes = self.convert_dict_to_xml({"action":action_list}, doc)
        for action_node in action_list_nodes:
            appl_action.appendChild(action_node)
        instruction.appendChild(appl_action_order)
        instruction.appendChild(appl_action)
        instructions.appendChild(instruction)
        input.appendChild(instructions)
        return input,doc

    def get_flow(self, node_id, table_id, priority=0, flow_id = None,flow_name=None, output_port=None, mod_dmac=None, ret_pkt=False, **kwargs):
        action_list = []
        if output_port:
            action_list.append(ofutils.set_output_action(output_port))
        if mod_dmac:
            action_list.append(ofutils.set_mod_dmac_action(mod_dmac))
        if ret_pkt:
            action_list.append(ofutils.set_return_pkt_action())
        if not flow_id:
            flow_id = 1
        flow = {"input":
            {
                "transaction-uri":"odlTraining8",
                "flow-ref":ofutils.set_flow_ref(node_id,table_id, flow_id),
                "node":ofutils.set_node(node_id),
                "flow-table":ofutils.set_flow_table(node_id, table_id),
                "flow":{
                    "priority":priority,
                    "table_id":table_id,
                    "flow-name":flow_name if flow_name else ofutils.generate_flow_name(node_id,table_id,flow_id),
                    "match":ofutils.set_match_field(**kwargs),
                    "instructions": ofutils.set_actions(action_list)
                }
            }
        }
        return flow

    def construct_flow(self, node_id, table_id, priority=0, flow_name=None, output_port=None, mod_dmac=None, ret_pkt=False, **kwargs):
        flow = self.get_flow(node_id, table_id, priority, flow_name=flow_name, output_port=output_port, mod_dmac=mod_dmac, ret_pkt=ret_pkt, **kwargs)
        matches = {"match": flow["input"]["flow"]["match"]}
        action_list =flow["input"]["flow"]["instructions"]["instruction"][0]["apply-actions"]["action"]
        flow_xml,doc = self.convert_flow_toxml(node_id, table_id, priority, matches, action_list)
        flow_body = doc.toprettyxml()
        print flow_body
        self.write_flow(flow_body)
        return flow_body


    def construct_flow_to_json(self, node_id, table_id, flow_id, priority=0, flow_name=None,output_port=None, mod_dmac=None, ret_pkt=False,**kwargs):
        flow = self.get_flow(node_id, table_id, flow_id, priority, flow_name, output_port, mod_dmac, ret_pkt, **kwargs)
        print(flow)
        self.write_flow(flow)
        return flow
