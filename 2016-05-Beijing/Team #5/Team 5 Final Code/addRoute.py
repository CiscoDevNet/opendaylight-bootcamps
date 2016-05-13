'''
Created on May 12, 2016

@author: chuck
'''
from __future__ import print_function as _print_function
from importlib import import_module
from pydoc import plain
from pydoc import render_doc as doc
from basics.context import sys_exit, EX_OK, EX_TEMPFAIL
from basics.acl import acl_create_port_grant, inventory_acl, add_route_grant
acl_fixture = import_module('learning_lab.05_acl_fixture')

from tkinter import *
import tkinter.messagebox as messagebox

device_name = "iosxrv-3"
prefix_address = ""

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='please type', command=self.hello)
        self.alertButton.pack()

    def hello(self):
        self.add_name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Ip received, %s' % self.add_name)


def demonstrate(device_name, prefix_address):
    ''' Apply function 'acl_create_port_grant' to the specified device and ACL.'''
    add_route_grant(device_name, prefix_address)

'''here we try to add acl to route, but it not admission permit'''

'''def demonstrate(device_name, acl_name, port, grant, protocol):
    print('\nacl_create_port_grant(' + device_name, acl_name, port, grant, protocol, sep=', ', end=')\n')
    acl_create_port_grant(device_name, acl_name, port, grant, protocol)'''


def main():
    ''' Select a device and demonstrate with each ACL.'''
    print(plain(doc(acl_create_port_grant)))
    inventory = inventory_acl()
    if not inventory:
        print('There are no ACL capable devices to examine. Demonstration cancelled.')
    else:
        try:
            app = Application()
            app.master.title('chinaunicom')
            app.mainloop()
            prefix_address = app.add_name
            demonstrate(device_name, prefix_address)
            return EX_OK
        except Exception as e:
            print(e)
    return EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())