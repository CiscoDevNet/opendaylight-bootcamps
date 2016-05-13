# encoding=utf8
from mininet.topo import Topo


class TestFullTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        t1_sw = self.addSwitch('s1')
        t2_sw = self.addSwitch('s2')
        access_switch = self.addSwitch('s3')
        self.addLink(access_switch, t1_sw, 1, 1)
        self.addLink(access_switch, t2_sw, 2, 1)

        t1_srv_list = self.create_vdc(1, t1_sw, 2)
        t2_srv_list = self.create_vdc(2, t2_sw, 2)

        # create access layer
        computer_num = 3
        computer_list = []
        for i in xrange(computer_num):
            computer_list.append(
                self.addHost('c%d' % i, mac='00:00:00:00:00:0%d' % (i + 1), ip='10.0.0.%d/8' % (i + 1)))

        for computer in computer_list:
            self.addLink(computer, access_switch)

    def create_vdc(self, vdc_id, vdc_switch, server_num):
        server_list = []
        for i in xrange(server_num):
            server = self.addHost('t%s_h%d' % (vdc_id, i), mac='00:00:00:00:00:%d%d' % (vdc_id, i+1),
                                  ip='10.0.%d.%d/8' % (vdc_id, i + 1))
            server_list.append(server)
            self.addLink(server, vdc_switch, 2)

        return server_list


topos = {'test-topo': (lambda: TestFullTopo())}

if __name__ == '__main__':
    import os

    os.system(
        'sudo mn --custom mytopo.py --topo test-topo --controller=remote,ip=172.16.62.1')
