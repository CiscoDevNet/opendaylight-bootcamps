#the gui of our app
from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
from basics.interface import management_interface,interface_configuration_tuple
from basics.interface_configuration import interface_configuration
from basics.interface_names import interface_names
from basics.routes import to_ip_network,static_route_json_all
from basics.inventory import inventory_connected
from basics.render import print_rich
from basics.routes import static_route_create, static_route_delete

from Tkinter import *

import networkx as nx
import matplotlib.pyplot as plt


def demonstrate(device_name, interface_name):
    ''' Apply function 'interface_configuration' to the specified device/interface.'''
    print_rich('  ', interface_configuration(device_name, interface_name))

def match(device_name, interface_network):
    """ Discover matching interface on a different device."""
    for other_device in inventory_connected():
        if other_device == device_name:
            continue
        for interface_name in interface_names(other_device):
            interface_config = interface_configuration_tuple(other_device, interface_name)
            if interface_config.address is None:
                # Skip network interface with unassigned IP address.             
                continue
            other_network = to_ip_network(interface_config.address, interface_config.netmask)
            if other_network == interface_network:
                print('Match %s/%s/%s to %s/%s' % (device_name, interface_config.address, interface_config.netmask, \
                                                   other_device, interface_network))
#                return (other_device,interface_config.name)
                return other_device
    return None


def draw_backup():
    ''' Select a device/interface and demonstrate.'''
    print(plain(doc(interface_configuration)))
    foundInterface = False
    
    G=nx.Graph()

    for device_name in sorted(inventory_connected()):
        G.add_node(device_name)
        print("%s:" % device_name)
        mgmt_name = management_interface(device_name)
        for interface_name in sorted(interface_names(device_name)):
            # Choose interface on 'data plane' not 'control plane'.
            if interface_name == mgmt_name:
                continue
            else:
                foundInterface = True
                demonstrate(device_name, interface_name)
                interface= interface_configuration(device_name, interface_name)
                address=interface.address
                netmask=interface.netmask
                to_node=match(device_name,to_ip_network(address,netmask))
                print("to_node:%s" % to_node)
                if  to_node:
                    G.add_edge(device_name, to_node)
        if not foundInterface:
            print("There are no suitable network interfaces for this device.")

    print(G.nodes())
    print(G.edges())
    #nx.draw(G)
    nx.draw_networkx(G, with_labels=True)
    plt.show()


def draw():
    ''' Select a device/interface and demonstrate.'''
    print(plain(doc(interface_configuration)))
    foundInterface = False
    
    G=nx.Graph()

    for device_name in sorted(inventory_connected()):
        G.add_node(device_name)
        print("%s:" % device_name)
        mgmt_name = management_interface(device_name)
        for interface_name in sorted(interface_names(device_name)):
            # Choose interface on 'data plane' not 'control plane'.
            if interface_name == mgmt_name:
                continue
            else:
                match(device_name,interface_name)
                foundInterface = True
                demonstrate(device_name, interface_name)
                to_interface= interface_configuration(device_name, interface_name)[1].split(' ')[1]
                print("interface:%s"  % to_interface)
                G.add_edge(device_name, to_interface)
        if not foundInterface:
            print("There are no suitable network interfaces for this device.")

    print(G.nodes())
    print(G.edges())
    #nx.draw(G)
    nx.draw_networkx(G, with_labels=True)
    plt.show()



class GUI:
    def __init__(self,master):
        self.root=master
        
        self.hi_there = Button(master, text="Draw Topology", command=self.draw_topology)
        self.hi_there.grid(row=1,column=1,sticky='W')
        
        self.button = Button(master,text="QUIT",fg ="red", command=master.quit)
        self.button.grid(row=1,column=2,sticky='W')
        
        self.label1 =Label(master,text="Device_Name:")
        self.label1.grid(row=2,column=1,sticky='W')
        self.input1=Entry(master)
        self.input1.grid(row=2,column=2,sticky='W')
        
        self.label2=Label(master,text=" IP:")
        self.label2.grid(row=2,column=3,sticky='W')
        self.input2=Entry(master)
        self.input2.grid(row=2,column=4,sticky='W')
        
        self.label4=Label(master,text=" Netmask:")
        self.label4.grid(row=2,column=5,sticky='W')
        self.input4=Entry(master)
        self.input4.grid(row=2,column=6,sticky='W')
        
        self.label3=Label(master,text=" Next Hop:")
        self.label3.grid(row=2,column=7,sticky='W')
        self.input3=Entry(master)
        self.input3.grid(row=2,column=8,sticky='W')
           
        self.button = Button(master,text="Add",fg ="blue", command=self.add)
        self.button.grid(row=2,column=9,sticky='W')
        self.button = Button(master,text="Delete",fg ="blue", command=self.delete)
        self.button.grid(row=2,column=10,sticky='W')

        
        self.devicename = StringVar()
        self.input1.config(textvariable=self.devicename)
        
        self.ipset= StringVar()
        self.input2.config(textvariable=self.ipset)
        
        self.nexthop= StringVar()
        self.input3.config(textvariable=self.nexthop)
        
        self.netmask= StringVar()
        self.input4.config(textvariable=self.netmask)
        
        
        self.label5 =Label(master,text="Find_Name:")
        self.label5.grid(row=3,column=1,sticky='W')
        self.input5=Entry(master)
        self.input5.grid(row=3,column=2,sticky='W')
        self.finddev= StringVar()
        self.input5.config(textvariable=self.finddev)
       
        self.button_find = Button(master,text="Show",fg ="blue", command=self.find)
        self.button_find.grid(row=3,column=3,sticky='W')
        
        self.showtext=Text(master)
        self.showtext.grid(row=4,columnspan=500,sticky='W')
        
    
    def find(self):   
        
        device_name=self.finddev.get()
        routes=static_route_json_all(device_name)
        self.showtext.delete(0.0,END)
        
        for route in routes:
            print("keys:%s" % route.keys())
            print("network:%s,netmask:%s,nethop:%s" % (route['prefix'], route['prefix-length'], route['vrf-route']))
            print("nethop:%s" % route['vrf-route']['vrf-next-hops']["next-hop-address"][0]['next-hop-address'])
       
            strr='Destination:{0}/{1} Nexthop:{2}'.format(route['prefix'], route['prefix-length'],route['vrf-route']['vrf-next-hops']["next-hop-address"][0]['next-hop-address'])
            self.showtext.insert(INSERT,strr)
            self.showtext.insert(INSERT,'\n')
            
    def add(self):
        device_name=self.devicename.get()
        destination_network=self.ipset.get()
        netmask=self.netmask.get()
        dest=to_ip_network(destination_network,netmask)
        next_hop_address=self.nexthop.get()
        static_route_create(device_name, dest, next_hop_address)
        
    def delete(self):
        device_name=self.devicename.get()
        destination_network=self.ipset.get()
        netmask=self.netmask.get()
        dest=to_ip_network(destination_network,netmask)
        static_route_delete(device_name, dest)
        
    def draw_topology(self):
        draw()
        
if __name__ == "__main__":     
    root= Tk()
    root.geometry("1000x300+200+100")#size
    app = GUI(root)
    root.mainloop()