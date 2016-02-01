#!/usr/bin/python

import inspect
import os
import atexit
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.topo import SingleSwitchTopo
from mininet.node import RemoteController


net = None

class NWTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        hconfig = {'inNamespace':True}
        low_link_config = {'bw': 10}
        high_link_config = {'bw': 100}
        host_link_config = {}

        # Create switch nodes
        for i in range(8):
            sconfig = {'dpid': "%016x" % (i+1)}
            self.addSwitch('s%d' % (i+1), **sconfig)

        # Create host nodes
        for i in range(4):
            self.addHost('h%d' % (i+1), **hconfig)

        # Add switch links
        # Specified to the port numbers to avoid any port number consistency issue
        
        self.addLink('s2', 's1', port1=1, port2=1, **low_link_config)
        self.addLink('s3', 's1', port1=1, port2=2, **high_link_config)
        self.addLink('h1', 's1', port1=1, port2=3, **host_link_config)
        self.addLink('h2', 's1', port1=1, port2=4, **host_link_config)
       
	self.addLink('s2', 's4', port1=2, port2=1, **low_link_config)

	self.addLink('s3', 's4', port1=2, port2=2, **high_link_config) 

	self.addLink('s4', 's5', port1=3, port2=1, **low_link_config)
	self.addLink('s4', 's7', port1=4, port2=1, **high_link_config)

	self.addLink('s5', 's6', port1=2, port2=1, **low_link_config)	

	self.addLink('s6', 's7', port1=2, port2=2, **low_link_config)
	self.addLink('s6', 's8', port1=3, port2=1, **low_link_config)

	self.addLink('s7', 's8', port1=3, port2=2, **high_link_config)

        self.addLink('h3', 's8', port1=1, port2=3, **host_link_config)
        self.addLink('h4', 's8', port1=1, port2=4, **host_link_config)
        

        


def startNetwork():
    info('** Creating Overlay network topology\n')
    topo = NWTopo()
    global net
    net = Mininet(topo=topo, link = TCLink,
                  controller=lambda name: RemoteController(name, ip='10.1.0.242'),
                  listenPort=6633, autoSetMacs=True, autoStaticArp=True)

    info('** Starting the network\n')
    net.start()


    info('** Running CLI\n')
    CLI(net)


def stopNetwork():
    if net is not None:
        info('** Tearing down Overlay network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()

