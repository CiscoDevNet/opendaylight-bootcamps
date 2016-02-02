"""
OpenFlow Config Demo:
{
"input": {
    "transaction-uri" : "foo",
    "flow-ref" : "/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:node-id=\"openflow:1\"]/opendaylight-inventory:table/0/opendaylight-inventory:flow/0",
    "node" : "/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:node-id=\"openflow:1\"]",
    "flow-table" : "/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:node-id=\"openflow:1\"]/opendaylight-inventory:table/0",
    "flow": {
        "match": {
            "in-port": "openflow:1:1",
            "ethernet-match" : {
                "ethernet-type" : {
                    "type" : 2048
                }
            },
            "ip-match": {
                "ip-protocol" : 17
            }
        },
        "instructions": {
            "instruction": [
                {
                    "order": 0,
                    "apply-actions": {
                        "action": [
                            {
                                "order": 0,
                                "output-action": {
                                    "output-node-connector": "2",
                                    "max-length": 65535
                                }
                            },
                            {
                                "order": 1,
                                "output-action": {
                                    "output-node-connector": "3",
                                    "max-length": 65535
                                }
                            }
                        ]
                    }
                }
            ]
        },
        "priority": 2,
        "idle-timeout": 0,
        "hard-timeout": 0,
        "cookie": 3098476543630901223,
        "table_id": 0,
        "flow-name" : "fork"
    }
}
}
"""

def set_flow_table(node_id, table_id):
    flow_table="/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:" \
               "node-id=\"%(node)s\"]/opendaylight-inventory:table/%(table)s" % \
               ({"node":node_id, "table":str(table_id)})

    return flow_table

def set_flow_ref(node_id, table_id, flow_id):
    flow_ref = "/opendaylight-inventory:nodes/opendaylight-inventory:" \
               "node[opendaylight-inventory:node-id=\"%(node_id)s\"]/opendaylight-inventory:" \
               "table/%(table_id)s/opendaylight-inventory:flow/%(flow_id)s"%\
               ({"node_id":node_id, "table_id":table_id, "flow_id":flow_id})
    return flow_ref

def set_node(node_id):
    node =  "/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:" \
            "node-id=\"%(node_id)s\"]"%({"node_id":node_id})
    return node

def set_match_field(**kwargs):
    match = {}
    match.update({"ethernet-match":
        {
            "ethernet-type": {
                "type": 2048}
        }
    })
    if kwargs.get("in_port", None):
        match.update({"in-port":kwargs["in_port"]})
    if kwargs.get("src_mac",None) or kwargs.get("dst_mac", None):
        if kwargs.get("src_mac",None):
            src_mac = kwargs["src_mac"]
            match["ethernet-match"].update({'ethernet-source': {'address': src_mac}})
        if kwargs.get("dst_mac", None):
            dst_mac = kwargs["dst_mac"]
            match["ethernet-match"].update({'ethernet-destination': {'address': dst_mac}})

    src_ip = kwargs.get("src_ip", None)
    dst_ip = kwargs.get("dst_ip", None)
    protocol = kwargs.get("protocol", None)
    src_port = kwargs.get("src_port", None)
    dst_port = kwargs.get("dst_port", None)

    if src_ip:
        match.update({"ipv4-source": str(src_ip)})
    if dst_ip:
        match.update({"ipv4-destination": str(dst_ip)})

    if protocol:
        match.update({"ip-match":{}})
        if protocol.lower()=="tcp":
            match["ip-match"]["ip-protocol"] = 6
            if src_port:
                match.update({"tcp-source-port": int(src_port)})
            if dst_port:
                match.update({"tcp-destination-port": int(dst_port)})
        elif protocol.lower() == "udp":
            match["ip-match"]["ip-protocol"] = 17
            l4_match={"udp-match":{}}
            if src_port:
                match.update({"udp-source-port": int(src_port)})
            if dst_port:
                match.update({"udp-destination-port": int(dst_port)})
        elif protocol.lower() == "icmp":
            match["ip-match"]["ip-protocol"] = 1
    return match

def set_mod_dmac_action(dst_mac, order=0):
    set_dmc_action = {"order": order,
                      "set-dl-dst-action": dst_mac}
    return set_dmc_action

def set_output_action(output_port, order=2):
    output_action = {"order": order,
                     "output-action": {
                         "output-node-connector": str(output_port)
                     }}
    return output_action

def set_return_pkt_action(order=1):
    output_action = {
        "order": order,
        "output-action": {
             "output-node-connector": "INPORT"
         }}
    return output_action

def set_actions(action_list=[]):
    actions= {
            "instruction": [
                {
                    "order": 0,
                    "apply-actions": {
                        "action":[]
                    }
                }
            ]
        }
    if action_list:
        actions["instruction"][0]["apply-actions"]["action"].extend(action_list)
    return actions

def generate_flow_name(node_id,table_id,flow_id):
    return node_id + "/" + table_id + "/" + flow_id