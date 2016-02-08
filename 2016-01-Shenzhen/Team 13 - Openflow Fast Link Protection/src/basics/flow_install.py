'''
Created on Jan 22, 2016

@author: Bluesy Wang
@author: Hu Qiwei
'''

import requests
import json


class FlowInstaller():
    def __init__(self, odluser, odlpassword, base_url, base_flowid, base_flowpriority):
        self.odluser = odluser
        self.odlpassword = odlpassword
        self.base_url = base_url
        self.base_flowid = base_flowid
        self.base_flowpriority = base_flowpriority
    
    def installflow(self, flow):
        """
        {"node-id":"openflow:1","table-id":"0","flow-id":"odl-1","in-port":"1",
        "dl-src":"aa:aa:aa:aa:aa:aa","dl-dst":"bb:bb:bb:bb:bb:bb","out-port":"2"}
        """
        node_id = flow['node-id']
        table_id = flow['table-id']
        flow_id = flow['flow-id']
        in_port = flow['in-port']
        dl_src = flow['dl-src']
        dl_dst = flow['dl-dst']
        out_port = flow['out-port']
        
        self.jsonrequest(node_id, table_id, flow_id, in_port, dl_src, dl_dst, out_port)
        
    def jsonrequest(self, node_id, table_id, flow_id, in_port, dl_src, dl_dst, out_port):
        jsondata = json.dumps(self.create_flow_dict(node_id, table_id, flow_id, in_port, dl_src, 
                                               dl_dst, out_port, self.base_flowpriority))
        
        print jsondata
        headers = {'content-type': 'application/json'}
        response = requests.put(self.base_url+'config/opendaylight-inventory:nodes/node/'+node_id
                                +'/flow-node-inventory:table/'+table_id+'/flow/'+flow_id, 
                                auth = (self.odluser, self.odlpassword), data=jsondata, headers=headers)
        print response
        
    '''
    cuntom flow format
    '''
    def create_flow_dict(self, node_id, table_id, flow_id, in_port, dl_src, dl_dst, out_port, priority):
        return       {
                    "flow": [
                        {
                            "id": flow_id,
                            "match": {                     
                                "in-port": in_port,               
                                "ethernet-match": {
                                    "ethernet-source": {
                                        "address": dl_src
                                    },
                                    "ethernet-destination": {
                                        "address": dl_dst
                                    }
                                }
                                  },
                            "instructions": {
                                "instruction": [
                                    {
                                        "order": "1",
                                        "apply-actions": {
                                            "action": [
                                                {
                                                    "output-action": {
                                                        "output-node-connector": out_port
                                                    },
                                                    "order": "1"
                                                }
                                            ]
                                        }
                                    }
                                ]
                            },
                            "priority": priority,
                            "table_id": table_id
                        }
                    ]
                }
    
    def convert_flow_dict_2_jobject(self, flow_dict):
        return json.dumps(flow_dict)

    