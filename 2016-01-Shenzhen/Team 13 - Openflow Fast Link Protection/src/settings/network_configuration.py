'''
Created on Jan 22, 2016

@author: Bluesy Wang
'''

odl_server_hostname = '10.1.0.221'
odl_server_port = '8181'
odl_server_url_prefix = "http://%s:%s/restconf/" % (odl_server_hostname, odl_server_port)
odl_server_user = 'admin'
odl_server_password = 'admin'
odl_base_flowid = '1'
odl_base_flowpriority = '10'

host1_mac = '00:00:00:00:00:01'
host1_node = 'openflow:1'
host1_port = '1'
host2_mac = '00:00:00:00:00:03'
host2_node = 'openflow:6'
host2_port = '1'