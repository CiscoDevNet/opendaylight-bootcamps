from services.resroucemanage import ODLRscGetter
import utils.constants as const
from services.flowmanage import OFManager

def test_rscgetter(controller_ip):
    rsc_getter = ODLRscGetter(controller_ip)
    ofnode_configs = rsc_getter.getOFNodes()
    for key in ofnode_configs.keys():
        print("OF Node key: "+key)
        switch = ofnode_configs[key].get(const.SWITCH, None)
        if switch:
            print("  Switch: " + str(switch.make_dict()))

        host_list =ofnode_configs[key].get(const.HOST, [])
        if host_list:
            for host in host_list:
                print("  Host: "+str(host.make_dict()))
    switches = rsc_getter._getAllOFSwitches(ofnode_configs)
    print("Total Switch count: %d"%(len(switches)))
    hosts = rsc_getter._getAllHosts(ofnode_configs)
    print("Total Host count: %d"%(len(hosts)))

    of_links = rsc_getter.getOFLinks(7)
    for lnk in of_links:
        print("Link: " + str(lnk.make_dict()))
    print("OFLink Count: "+ str(len(of_links)))

def test_flowMgr(controller_ip):
    flowMgr = OFManager(controller_ip)

    flow = flowMgr.construct_flow("openflow:1",0,"1",111, "test_flow",3,ret_pkt=False,protocol="tcp",dst_port=1111,
                                  src_mac="72:60:16:ea:9e:8a")
    print(flow)

if __name__ == '__main__':
    controller_ip = "120.52.145.138"
    # test_rscgetter(controller_ip)
    test_flowMgr(controller_ip)