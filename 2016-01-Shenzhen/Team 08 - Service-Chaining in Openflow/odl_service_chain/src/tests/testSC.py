__author__ = 'cmcc'
from services.scService import SvcChain
import utils.constants as const

def create_match():
    match={
        "src_mac":"ee:9d:32:7f:f6:1e",
        "protocol":"tcp",
        "dst_port":"80"
    }
    return match

def create_svc_path():
    fw_node_id = "openflow:2"
    nat_node_id = "openflow:3"
    lb_node_id = "openflow:4"
    sc_path =[fw_node_id, nat_node_id, lb_node_id]

def init_connection(sc_func):
    sc_func.sync_ofnodes()
    sc_func.initial_oflinks()

def test_scFuction(controller_ip):
    sc_func = SvcChain(controller_ip)
    init_connection(sc_func)
    sc_func.set_vnf_type("s2",const.FIREWALL)
    sc_func.set_vnf_type("s3",const.NAT)
    sc_func.set_vnf_type("s4",const.LOADBALANCE)
    tplt = sc_func.define_sc_tplt(":".join([const.FIREWALL,const.NAT,const.LOADBALANCE]),"template_1")
    tpId = tplt.id
    print(tpId)
    inst = sc_func.define_sc_inst(tpId, "tcp", 80)
    print(inst.id)
    sc_func.define_sc_app("host:10.0.0.1", inst.id)

if __name__ == "__main__":
    controller_ip = "120.52.145.138"
    test_scFuction(controller_ip)


