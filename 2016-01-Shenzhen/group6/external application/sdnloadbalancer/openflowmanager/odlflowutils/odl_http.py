__author__ = 'lijie'
import requests
from requests.auth import HTTPBasicAuth
from openflowmanager import constants as con
from openflowmanager import utils

from openflowmanager.odlflowutils import flow_template as TEMPLATE

FLOW_ID = 0
AUTH = HTTPBasicAuth('admin', 'admin')
headers = {'Content-Type': 'application/xml'}


def add_flow(suffix_url, template, flow_id):
    request_url = con.BASE_URL + suffix_url.format(
        node='openflow:1',
        table_id=con.LOADBALANCE_TABLE,
        flow_id=flow_id
    )
    template = template.format({'flow_id': FLOW_ID})
    print template
    res = requests.put(request_url, auth=AUTH, headers=headers, data=template)
    print res


def add_virtual_service_flow(vip, vport, protocol):
    global FLOW_ID
    FLOW_ID += 1
    template = TEMPLATE.ADD_VIRTUAL_SERVICE_MATCH.format(
        priority=con.VIR_SERVICE_PRI,
        dst_ipaddress=vip + '/32',
        protocol=protocol,
        dst_port=vport,
        table_id=con.LOADBALANCE_TABLE,
        flow_id=FLOW_ID
    )
    add_flow(con.ADD_FLOW_URL, template, FLOW_ID)


def add_service_in_flow(vip, vport, ip, mac, oport, client_ip):
    global FLOW_ID
    FLOW_ID += 1
    template = TEMPLATE.SERVICE_IN.format(
        priority=con.VIR_SERVICE_IN_PRI,
        src_ip= client_ip + '/32',
        dst_ip=vip+'/32',
        dst_port=vport,
        table_id=con.LOADBALANCE_TABLE,
        bs_ip=ip + '/32',
        bs_mac=mac,
        bs_port=oport,
        flow_id=FLOW_ID
    )
    add_flow(con.ADD_FLOW_URL, template, FLOW_ID)


def add_service_out_flow(vip, bs_ip, cs_ip):
    global FLOW_ID
    FLOW_ID += 1
    template = TEMPLATE.SERVICE_OUT.format(
        priority=con.VIR_SERVICE_OUT_PRI,
        dst_ip=cs_ip+'/32',
        src_ip= bs_ip+'/32',
        flow_id=FLOW_ID,
        table_id=con.LOADBALANCE_TABLE,
        vip=vip+'/32',
        src_mac=con.OUTMAC,
        out_port=con.OUTPORT
    )
    add_flow(con.ADD_FLOW_URL, template, FLOW_ID)

