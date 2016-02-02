__author__ = 'cmcc'

SWITCH = "switch"
FIREWALL = "firewall"
NAT = "nat"
LOADBALANCE = "loadbalance"
HOST = "host"
available_nfv_types=(SWITCH,FIREWALL,NAT,LOADBALANCE)

PRIORITY_MOD_DMAC = 999
PRIORITY_SW_FLOW = 200
PRIORITY_VNF_FLOW = 1000
DEFAULT_ODL_CONTROLLER_IP = "120.52.145.138"

TABLE_ID_VNF = 0
