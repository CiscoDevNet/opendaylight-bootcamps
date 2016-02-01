#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, mac="00:00:00:00:00:01",ip='10.0.0.1', defaultRoute='None')
    h2 = net.addHost('h2', cls=Host, mac="00:00:00:00:00:02",ip='10.0.0.2', defaultRoute='None')
    remote_ser = net.addHost('remote_ser', cls=Host, mac="00:00:00:00:00:04",ip='10.0.0.4', defaultRoute='None')
    agent_ser = net.addHost('agent_ser', cls=Host,mac="00:00:00:00:00:03", ip='10.0.0.3', defaultRoute='None')

    info( '*** Add links\n')
    info( '*** Add links\n')
    h2s1 = {'bw':1000,'delay':'1'}
    net.addLink(h2, s1, cls=TCLink , **h2s1)
    s1agent_ser = {'bw':1000,'delay':'1'}
    net.addLink(s1, agent_ser, cls=TCLink , **s1agent_ser)
    s1s2 = {'bw':1,'delay':'100'}
    s2remote_ser = {'bw':1,'delay':'10'}
    net.addLink(s2, remote_ser, cls=TCLink , **s2remote_ser)
    net.addLink(s1,s2)
    h1s1 = {'bw':1000,'delay':'1'}
    net.addLink(h1, s1, cls=TCLink , **h1s1)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c1])
    net.get('s2').start([c1])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

