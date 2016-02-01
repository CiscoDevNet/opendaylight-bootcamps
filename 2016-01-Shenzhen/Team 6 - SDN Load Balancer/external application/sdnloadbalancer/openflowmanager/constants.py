__author__ = 'lijie'


IP_ADDR = "ipaddress"
MAC = "mac"
OFPORT = "ofport"

VIP = "vip"
VPORT = "vport"
PRO = "protocol"

VIR_SERVICE_PRI = "50"
VIR_SERVICE_IN_PRI = "60"
VIR_SERVICE_OUT_PRI = "60"
OUTMAC = 'a4:5e:60:dc:b9:a3'
OUTPORT = '1'

BASE_URL = "http://10.1.0.132:8181"
LOADBALANCE_TABLE = "0"


ADD_FLOW_URL = ("/restconf/config/opendaylight-inventory:nodes/node/{node}/"
                "table/{table_id}/flow/{flow_id}")