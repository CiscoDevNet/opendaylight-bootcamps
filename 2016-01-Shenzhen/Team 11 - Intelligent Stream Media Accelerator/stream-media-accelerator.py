from basics.odl_http import odl_http_put
import settings


def FlowMod_Change_DST(src_ipv4, dst_ipv4, change_macdst, change_ipv4dst, dst_port=None, outPort="1",change_portdst=None, prioritys="1", flowId="1"):
    return '''
{
    "flow": [
        {
            "id": "%s",
            "flow-name": "ODL-CAMP-11",
            "priority": "%s",
            "table_id": "0",
            "out_port": "%s",
            "match": {
                "ethernet-match": {
                    "ethernet-type": {
                        "type": "2048"
                    }
                },
                "ipv4-source": "%s",
                "ipv4-destination": "%s"
            },
            "instructions": {
                "instruction": [
                    {
                        "order": "1",
                        "apply-actions": {
                            "action": [
                                {
                                    "set-dl-dst-action": {
                                        "address": "%s"
                                    },
                                    "order": "1"
                                },
                                {
                                    "set-nw-dst-action": {
                                        "ipv4-address": "%s"
                                    },
                                    "order": "2"
                                },
                                {
                                    "output-action": {
                                        "output-node-connector":"%s",
                                    "max-length":"65535"
                                    },
                                    "order" : "3"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ]
}
''' % (flowId,prioritys, outPort, src_ipv4 , dst_ipv4,  change_macdst, change_ipv4dst, outPort)

def FlowMod_Change_SRC(src_ipv4, dst_ipv4, change_macsrc, change_ipv4src, src_port=None,  outPort="1",change_portsrc=None, prioritys="1", flowId="2"):
    return '''
{
    "flow": [
        {
            "id": "%s",
            "flow-name": "ODL-CAMP-11",
            "priority": "%s",
            "table_id": "0",
            "out_port": "%s",
            "match": {
                "ethernet-match": {
                    "ethernet-type": {
                        "type": "2048"
                    }
                },
                "ipv4-source": "%s",
                "ipv4-destination": "%s"
            },
            "instructions": {
                "instruction": [
                    {
                        "order": "1",
                        "apply-actions": {
                            "action": [
                                {
                                    "set-dl-src-action": {
                                        "address": "%s"
                                    },
                                    "order": "1"
                                },
                                {
                                    "set-nw-src-action": {
                                        "ipv4-address": "%s"
                                    },
                                    "order": "2"
                                },
                                {
                                    "output-action": {
                                        "output-node-connector":"%s",
                                    "max-length":"65535"
                                    },
                                    "order" : "3"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ]
}
''' % (flowId, prioritys, outPort, src_ipv4 , dst_ipv4,  change_macsrc, change_ipv4src, outPort)


def Add_flow(VIP_Hosts):
    for (k,host) in VIP_Hosts.items():
        priority = str(2001)  
        go_flow_id = str(1)
        come_flow_id= str(2)
        
        host_access_switch = host["host_access_switch"]
        host_access_port = host["host_access_port"]
        
        host_ipv4 = host["ip"]
        print host_ipv4
        remote_ipv4 = Remote["YouTube"]
        cache_mac=Cache[1]["mac"]
        cache_ipv4 = Cache[1]["ip"]
        cache_access_port = Cache[1]["cache_access_port"]
        
        # redirect to cache    
        response = odl_http_put(
                                url_suffix = "config/opendaylight-inventory:nodes/node/{openflow_1}/table/0/flow/{flow_id}",
                                url_params = {"openflow_1" : host_access_switch, "flow_id" : go_flow_id},
                                contentType = "application/json",
                                content = FlowMod_Change_DST(host_ipv4,
                                                             remote_ipv4,
                                                             cache_mac,
                                                             cache_ipv4,
                                                             prioritys=priority, 
                                                             flowId=go_flow_id, 
                                                             outPort=cache_access_port),
                                expected_status_code = 200
                                )
        print "go:",response
        # redirect to host
        response = odl_http_put(
                                url_suffix = "config/opendaylight-inventory:nodes/node/{openflow_1}/table/0/flow/{flowId}",
                                url_params = {"openflow_1" : host_access_switch, "flowId" : come_flow_id},
                                contentType = "application/json",
                                content = FlowMod_Change_SRC(cache_ipv4,
                                                             host_ipv4,
                                                             GW_MAC,
                                                             remote_ipv4,
                                                             prioritys=priority, 
                                                             flowId=come_flow_id, 
                                                             outPort=host_access_port),
                                expected_status_code = 200
                                )
        print "come:",response
        
Cache={1:{"mac":"00:00:00:00:00:03","ip":"10.0.0.3/32","cache_access_port":"2"}}
Remote = {"YouTube":"10.0.0.4/32"}
GW_MAC= "00:00:00:00:00:04"
Host_List ={"A":{"ip":"10.0.0.1/32", "host_access_switch":"openflow:1","host_access_port":"4"},
            "B":{"ip":"10.0.0.2/32", "host_access_switch":"openflow:1","host_access_port":"1"}}

VIP_Host={}
while True:
    Host= raw_input("Do you want continue to Select a host as a VIP? (N/Y)\n>>")
    if Host != "n" and Host != "N": 
        Host= raw_input("Select a host as a VIP. such as A,B,C..\n>>")
        VIP_Host[Host]=Host_List[Host]
    else:
        break
    
if VIP_Host:
    for key in VIP_Host.keys():
        print "Now VIP hosts are %s"%key
        
    Add_flow(VIP_Host)
else:
    print "No VIP host"


