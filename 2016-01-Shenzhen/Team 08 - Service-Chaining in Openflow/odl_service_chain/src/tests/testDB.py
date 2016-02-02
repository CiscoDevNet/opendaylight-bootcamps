__author__ = 'cmcc'

from service.models import OFNodeBase,OfLink,SCTemplate,SCInstance,SCApp
import utils.constants as const
from services.dbServices import DbServices


def test_dbservice():
    print("Try to test dbServices")
    db_svc = DbServices(session)
    swnode = OFNodeBase()
    swnode.set_attributes("openflow:1","s1",const.SWITCH,"aa:bb:cc:dd:ee:ff")
    hostnode = OFNodeBase()
    hostnode.set_attributes("openflow:1:3","10.1.1.3",const.HOST,"bb:bb:cc:dd:ee:ff")
    db_svc.add_ofnode(swnode)
    print( len(db_svc.list_ofnodes()) == 1)
    db_svc.add_ofnode(hostnode)
    print( len(db_svc.list_ofnodes()) == 2)
    fwnode = OFNodeBase()
    fwnode.set_attributes("openflow:2","s2",const.FIREWALL,"aa:cc:cc:dd:ee:ff")
    lbnode = OFNodeBase()
    lbnode.set_attributes("openflow:3","s3",const.LOADBALANCE,"aa:dd:cc:dd:ee:ff")
    db_svc.add_ofnode(fwnode)
    db_svc.add_ofnode(lbnode)
    print( len(db_svc.list_ofnodes()) == 4)
    nv_link1 = OfLink()
    nv_link1.set_attributes(link_id="openflow:1:2",srcnode="openflow:1", dstnode="openflow:2", srcport="openflow:1:1", dstport="openflow:2:1")
    nv_link2 = OfLink()
    nv_link2.set_attributes(link_id="openflow:1:3",srcnode="openflow:1", dstnode="openflow:3", srcport="openflow:1:2", dstport="openflow:3:1")
    db_svc.add_oflink(nv_link1)
    db_svc.add_oflink(nv_link2)
    print( len(db_svc.list_oflink()) == 2)

    sc_template = SCTemplate()
    sc_template.set_attributes("template1", "firewall:loadbalance")
    db_svc.add_sctplt(sc_template)
    print(len(db_svc.list_sctplt()) == 1)

    sc_instance = SCInstance()
    sc_instance.set_attributes("tcp", "80", sc_template.instid,id="sc-template-1")
    db_svc.add_scinstance(sc_instance)
    print(len(db_svc.list_scinstance()) == 1)

    sc_app = SCApp()
    sc_app.set_attributes(hostnode.nodeid, sc_instance.instid)
    db_svc.add_scapp(sc_app)
    print(len(db_svc.list_scapp()) == 1)

    db_svc.mod_ofnode_type(lbnode,const.NAT)
    nat_node = db_svc.get_ofnode_by_type(const.NAT)
    print(nat_node.nodeid == lbnode.nodeid)

if __name__ == '__main__':
    test_dbservice()