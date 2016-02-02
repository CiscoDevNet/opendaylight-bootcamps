#!/usr/bin/env python
import optparse
import time
import sys
import httplib2
# import xml.dom.minidom

controller='10.1.0.242'
def getBodyByXML(filename,id,ip,port,outputport):
    '''
    Get body of xml by name and set params of id,ip,port,output
    '''
#     xmlbodylist = []
#     with open(filename, 'r') as infile:
#         xmlbodylist=infile.readlines()
#     xmlbody= ''.join(xmlbodylist)
    xmlbody=''
    if filename=='toflow.xml':
        xmlbody="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\">    <flow-name>add-policy</flow-name>    <table_id>0</table_id>    <id>#ID#</id>    <installHw>false</installHw>    <strict>false</strict>\t<priority>100</priority>\t    <instructions>        <instruction>            <order>0</order>            <apply-actions>                <action>                    <order>0</order>                    <output-action>                        <output-node-connector>#OUTPUTPORT#</output-node-connector>                    </output-action>                </action>            </apply-actions>        </instruction>    </instructions>    <match>        <ethernet-match>            <ethernet-type>                <type>2048</type>            </ethernet-type>        </ethernet-match>        <ipv4-destination>#IP#/32</ipv4-destination>        <ip-match>            <ip-protocol>6</ip-protocol>        </ip-match>        <tcp-destination-port>#PORT#</tcp-destination-port>    </match></flow>"
    elif filename=='fromflow.xml':
        xmlbody="<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\">    <flow-name>add-policy</flow-name>    <table_id>0</table_id>    <id>#ID#</id>    <installHw>false</installHw>    <strict>false</strict>\t<priority>100</priority>\t    <instructions>        <instruction>            <order>0</order>            <apply-actions>                <action>                    <order>0</order>                    <output-action>                        <output-node-connector>#OUTPUTPORT#</output-node-connector>                    </output-action>                </action>            </apply-actions>        </instruction>    </instructions>    <match>        <ethernet-match>            <ethernet-type>                <type>2048</type>            </ethernet-type>        </ethernet-match>        <ipv4-source>#IP#/32</ipv4-source>        <ip-match>            <ip-protocol>6</ip-protocol>        </ip-match>        <tcp-source-port>#PORT#</tcp-source-port>    </match></flow>"
    xmlbody=xmlbody.replace('#ID#', id)
    xmlbody=xmlbody.replace('#IP#', ip)
    xmlbody=xmlbody.replace('#PORT#', port)
    xmlbody=xmlbody.replace('#OUTPUTPORT#',str(outputport))
    return xmlbody
    
def post_dict(url, d):
    h = httplib2.Http(".cache")
    h.add_credentials('admin', 'admin')
    resp, content = h.request(
      uri = url,
      method = 'POST',
      headers={'Content-Type' : 'application/xml'},
      body=d,
      )
    return resp, content

def clearflow():
    for i in range(8):
        h = httplib2.Http(".cache")
        h.add_credentials('admin', 'admin')
        resp, content = h.request(
          uri = 'http://10.1.0.242:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(i+1)+'/table/0/',
          method = 'DELETE',
          headers={'Content-Type' : 'application/xml'}
          )
    return resp, content
    
def process_flows(dstip,dstport,priority):
    global controller
    switch_list=[]
    # if priority is high
    if priority=='1':
        #install high this flow entity across the switch of high bandwidth path
        #getHDeviceList(list);
        switch_list=[1,3,4,7,8]
        for sw in switch_list:
            url='http://'+controller+':8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(sw)+'/table/0/'
            id='10'
            outputport='no'
            if sw==1 or sw==3:
                outputport=2
            elif sw==4:
                outputport=4
            elif sw==7 or sw==8:
                outputport=3
            if dstip=='10.0.0.3' and sw==8:
                outputport=3
            elif dstip=='10.0.0.4' and sw==8:
                outputport=4
            xmlbody= getBodyByXML('toflow.xml',id,dstip,dstport,outputport)
#             xmlbody=xml.dom.minidom.parseString(txmlbody).toxml('UTF-8')
            resp, content = post_dict(url,xmlbody)
            print 'H [toflow],flow installed in switch',sw,',status',resp
        
        switch_list=[8,7,4,3,1]
        for sw in switch_list:
            url='http://'+controller+':8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(sw)+'/table/0/'
            id='20'
            outputport='no'
            if sw==8  or sw==4:
                outputport=2
            elif sw==7 or sw==3:
                outputport=1
            elif sw==1 :
                outputport=4
            
            xmlbody= getBodyByXML('fromflow.xml',id,dstip,dstport,outputport)
            resp, content = post_dict(url,xmlbody)
            print 'H [fromflow],flow installed in switch',sw,',status',resp
        
            
        
    # if priority is low
    if priority=='0':
        #install high this flow entity across the switch of low bandwidth path
        #getLDeviceList(list);
        switch_list=[1,2,4,5,6,8]
        for sw in switch_list:
            url='http://'+controller+':8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(sw)+'/table/0/'
            id='30'
            outputport='no'
            if sw==1 :
                outputport=1
            elif sw==2 or sw==5:
                outputport=2
            elif sw==4 or sw==6:
                outputport=3
            elif sw==8 :
                outputport=3   
            if dstip=='10.0.0.3' and sw==8:
                outputport=3
            elif dstip=='10.0.0.4' and sw==8:
                outputport=4
            xmlbody= getBodyByXML('toflow.xml',id,dstip,dstport,outputport)
            resp, content = post_dict(url,xmlbody)
            print 'L [fromflow],flow installed in switch',sw,',status',resp['status']
        
        switch_list=[8,6,5,4,2,1]
        for sw in switch_list:
            url='http://'+controller+':8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(sw)+'/table/0/'
            id='40'
            outputport='no'
            if sw==8 or sw==6 or sw==5 or sw==4 or sw==2:
                outputport=1
            elif sw==1 :
                outputport=3
            xmlbody= getBodyByXML('fromflow.xml',id,dstip,dstport,outputport)
            resp, content = post_dict(url,xmlbody)
            print 'L [fromflow],flow installed in switch',sw,',status',resp['status']
    
    
    
    
def main():
    """
   Slicing the underlay network and assigning priority to different flowspace. 
   For example we can divide flowspace (dstip:dstport)=(10.0.0.1:8080) has higher priority 1 
   and (10.0.0.1:80) with lower priority 0,which means the traffic in flowspace (10.0.0.1:8080) 
   will pass through paths with high bandwidth.
    
    parameter list:
    1.dstip: the destination IP address, one element to make up flowspace.      
    2.dstport: the destination IP port, one element to make up flowspace. 
    3.priority: the priority of flowspace
    """

    p = optparse.OptionParser(description='Slicing the underlay network and assigning priority to different flowspace. \n For example we can divide flowspace (dstip:dstport)=(10.0.0.1:8080) has higher priority 1 and (10.0.0.1:80) with lower priority 2,which means the traffic in flowspace (10.0.0.1:8080) will pass through paths with high bandwidth.',
                                   prog='netSlicing',
                                   version='netSlicing 0.1',
                                   usage='%prog -d 10.0.0.1 -p 8080 -r 1')
    p.add_option('--dstip', '-d', default='0.0.0.0')
    p.add_option('--dstport', '-p', default='no')
    p.add_option('--priority', '-r', default='no')
    options, arguments = p.parse_args()
    dstip=options.dstip
    dstport=options.dstport
    priority=options.priority
    
#     dstip = '10.0.0.4'
#     dstport = '8080'
#     priority = '1' 

    if dstip == '0.0.0.0':
        print 'please set dstip. for example -d 10.0.0.1, -h for more help'
        sys.exit(1)
    if dstport == 'no':
        print 'please set dstport. for example -p 8080, -h for more help'
        sys.exit(2)
    if priority != '1' and priority != '0':
        print 'please set priority. for example -r 1 or -r 0, -h for more help'
        sys.exit(3)    
    print 'process start'
    start = time.clock()
    print 'dstip:',dstip,'dstport:',dstport,'priority:',priority
    process_flows(dstip,dstport,priority)
    end = time.clock()  
    print 'process end, time used: %f s'% (end - start)

def test():
    id='0'
    ip='10.0.0.2'
    port='8080'
    outputport='2'
    xmlbody= getBodyByXML('toflow.xml',id,ip,port,outputport)
    #url='http://10.1.0.242:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/'
    url='http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/'
#     print post_dict(url,xmlbody)
    print xmlbody
    print 'sssssssssss'

if __name__=="__main__":
#     clearflow()
    main()
#     test()
    
