#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import lg, setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

# CORES = {
#   '100': {'dpid': '0000000000001000'},
#   '200': {'dpid': '0000000000002000'}
#   }

# AGGREGATES = {
#   '110': {'dpid': '0000000000001100'},
#   '120': {'dpid': '0000000000001200'},
#   '210': {'dpid': '0000000000002100'},
#   '220': {'dpid': '0000000000002200'}
#   }

# ACCESSES = {
#   '111': {'dpid': '0000000000001110'},
#   '121': {'dpid': '0000000000001210'},
#   '211': {'dpid': '0000000000002110'},
#   '221': {'dpid': '0000000000002210'}
#   }

# VEBS = {
#   '112': {'dpid': '000000000000112%s'},
#   '113': {'dpid': '000000000000113%s'},
#   '122': {'dpid': '000000000000122%s'},
#   '123': {'dpid': '000000000000123%s'},
#   '212': {'dpid': '000000000000212%s'},
#   '213': {'dpid': '000000000000213%s'},
#   '222': {'dpid': '000000000000222%s'},
#   '223': {'dpid': '000000000000223%s'}
# }

# FANOUT = 4
    
# class FTTopo(Topo):
class TestTopo(Topo):

  def __init__(self, enable_all = True):
    "Create test topology."

    # Add default members to class.
    super(TestTopo, self).__init__()

    # Add core switches
    # self.cores = {}
    # for switch in CORES:
    #   self.cores[switch] = self.addSwitch('s'+switch, dpid=(CORES[switch]['dpid']))

    # # Add aggregate switches
    # self.aggregates = {}
    # for switch in AGGREGATES:
    #   self.aggregates[switch] = self.addSwitch('s'+switch, dpid=(AGGREGATES[switch]['dpid']))

    # # Add access switches
    # self.accesses = {}
    # for switch in ACCESSES:
    #   self.accesses[switch] = self.addSwitch('s'+switch, dpid=(ACCESSES[switch]['dpid']))

    # # Add veb switches
    # self.vebs = {}
    # for switch in VEBS:
    #   self.vebs[switch] = self.addSwitch('s'+switch, dpid=(VEBS[switch]['dpid'] % '0'))

    # # Add hosts and connect them to their veb switch
    # sum = 1
    # for switch in VEBS:
    #   for count in xrange(1, FANOUT + 1):
    #     # Add hosts
    #     host = 'h%s%s' % (switch, count)
    #     ip = '10.0.0.%s' % ((int(switch[0])-1)*16+(int(switch[1])-1)*8+(int(switch[2])-2)*4+count)
    #     sum = sum + 1
    #     mac = VEBS[switch]['dpid'][4:] % count
    #     h = self.addHost(host, ip=ip, mac=mac)
    #     # Connect hosts to veb switches
    #     self.addLink(h, self.vebs[switch])

    host_a1 = 'h_a1'
    host_a2 = 'h_a2'
	host_f1 = 'h_f1'
	host_f2 = 'h_f2'
    ip_a1 = '10.0.0.1'
    ip_a2 = '10.0.0.2'
	ip_f1 = '10.0.0.3'
	ip_f2 = '10.0.0.4'
    h_a1 = self.addHost(host_a1, ip=ip_a1)
	h_a2 = self.addHost(host_a2, ip=ip_a2)
	h_f1 = self.addHost(host_f1, ip=ip_f1)
	h_f2 = self.addHost(host_f2, ip=ip_f2)
	s_a = self.addSwitch('s_a', dpid='0000000000000001')
	s_b = self.addSwitch('s_b', dpid='0000000000000002')
	s_c = self.addSwitch('s_c', dpid='0000000000000003')
	s_d = self.addSwitch('s_d', dpid='0000000000000004')
	s_e = self.addSwitch('s_e', dpid='0000000000000005')
	s_f = self.addSwitch('s_f', dpid='0000000000000006')
	s_g = self.addSwitch('s_g', dpid='0000000000000007')	
	self.addLink(host_a1,s_a)
	self.addLink(host_a2,s_a)
	self.addLink(host_f1,s_f)
	self.addLink(host_f2,s_f)
	self.addLink(s_a,s_c)
	self.addLink(s_c,s_b)
	self.addLink(s_c,s_d)
	self.addLink(s_b,s_e)
	self.addLink(s_d,s_e)
	self.addLink(s_e,s_g)
	self.addLink(s_e,s_f)
	self.addLink(s_g,s_f)
    # # Connect switches
    # self.addLink(self.cores['100'], self.aggregates['110'])
    # self.addLink(self.cores['100'], self.aggregates['120'])
    # self.addLink(self.cores['100'], self.aggregates['210'])
    # self.addLink(self.cores['100'], self.aggregates['220'])
    # self.addLink(self.cores['200'], self.aggregates['110'])
    # self.addLink(self.cores['200'], self.aggregates['120'])
    # self.addLink(self.cores['200'], self.aggregates['210'])
    # self.addLink(self.cores['200'], self.aggregates['220'])




    # self.addLink(self.aggregates['110'], self.accesses['111'])
    # self.addLink(self.aggregates['110'], self.accesses['121'])
    # self.addLink(self.aggregates['120'], self.accesses['111'])
    # self.addLink(self.aggregates['120'], self.accesses['121'])
    # self.addLink(self.aggregates['210'], self.accesses['211'])
    # self.addLink(self.aggregates['210'], self.accesses['221'])
    # self.addLink(self.aggregates['220'], self.accesses['211'])
    # self.addLink(self.aggregates['220'], self.accesses['221'])

    # self.addLink(self.accesses['111'], self.vebs['112'])
    # self.addLink(self.accesses['111'], self.vebs['113'])
    # self.addLink(self.accesses['121'], self.vebs['122'])
    # self.addLink(self.accesses['121'], self.vebs['123'])
    # self.addLink(self.accesses['211'], self.vebs['212'])
    # self.addLink(self.accesses['211'], self.vebs['213'])
    # self.addLink(self.accesses['221'], self.vebs['222'])
    # self.addLink(self.accesses['221'], self.vebs['223'])

if __name__ == '__main__':
   topo = FTTopo()
   ip = '10.1.0.143'
   port = 6633
   c = RemoteController('c', ip=ip, port=port)
   net = Mininet(topo=topo, autoSetMacs=True, xterms=False, controller=None)
   net.addController(c)
   net.start()
   print "Hosts configured with IPs, switches pointing to Controller at %s:%s" % (ip, port)
   CLI(net)
   net.stop()