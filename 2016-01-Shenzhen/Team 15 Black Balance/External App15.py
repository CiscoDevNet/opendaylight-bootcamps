#coding:utf-8
import json
import httplib2

#Group Url Links
h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

#Get Url Links
def geturl(switch,tableid,id):
    urllist = ['http://172.23.22.75:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:',switch,'/table/',tableid,'/flow/',id]
    url = ''.join(urllist)
    return url

#Read FLows Tables and Flow entries Through REST API
def readflowfromhttp(switch,tableid,id):
    url = geturl(switch,tableid,id)
    resp1, content1 = h.request(
      uri = url,
      method = 'GET',
      headers={'Content-Type' : 'application/json'},
      )
    flow = json.loads(content1)
    return flow

#Read For Flow Template
def readflowfromfile(file):
    fp = open(file, 'r')
    flow = json.loads(fp.read().decode('utf-8'))
    fp.close()
    return flow

#Remodify flows and achieve load balance module
def modflowtable(switch,tableid):
    id = 0
    flag = 0
    url = geturl(switch,tableid,id.__str__())
    resp1, content1 = h.request(
      uri = url,
      method = 'GET',
      headers={'Content-Type' : 'application/json'},
      )
    status = resp1['status']
    flow = json.loads(content1)
    while(status == '200'):
        if flag == 1:
            flow['flow-node-inventory:flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector'] = 3
            resp1, content1 = h.request(
              uri = url,
              method = 'PUT',
              headers={'Content-Type' : 'application/json'},
              body=json.dumps(flow),
              )
            id = id + 1
            url = geturl(switch,tableid,id.__str__())
            resp1, content1 = h.request(
              uri = url,
              method = 'GET',
              headers={'Content-Type' : 'application/json'},
              )
            status = resp1['status']
            flow = json.loads(content1)
            flag = 0
        else:
            id = id + 1
            url = geturl(switch,tableid,id.__str__())
            resp1, content1 = h.request(
              uri = url,
              method = 'GET',
              headers={'Content-Type' : 'application/json'},
              )
            status = resp1['status']
            flow = json.loads(content1)
            flag = 1

#Publish flows to switches
def writeflow(switch,inport,outport,ipv4src,ipv4dst,tcpdst,id,tableid,priority,ethtype,name):
    url = geturl(switch,tableid,id)
    flow = readflowfromfile('E:\\flow template.json')
    flow['flow-node-inventory:flow'][0]['match']['in-port'] = inport
    flow['flow-node-inventory:flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector'] = outport
    flow['flow-node-inventory:flow'][0]['match']['ipv4-source'] = ipv4src
    flow['flow-node-inventory:flow'][0]['match']['ipv4-destination'] = ipv4dst
    flow['flow-node-inventory:flow'][0]['match']['tcp-destination-port'] = tcpdst
    flow['flow-node-inventory:flow'][0]['id'] = id
    flow['flow-node-inventory:flow'][0]['table_id'] = tableid
    flow['flow-node-inventory:flow'][0]['priority'] = priority
    flow['flow-node-inventory:flow'][0]['match']['ethernet-match']['ethernet-type']['type'] = ethtype
    flow['flow-node-inventory:flow'][0]['flow-name'] = name
    resp1, content1 = h.request(
      uri = url,
      method = 'PUT',
      headers={'Content-Type' : 'application/json'},
      body=json.dumps(flow),
      )

#Print flows 
def printflow(switch,tableid,id):
    flow = readflowfromhttp(switch,tableid,id)
    print 'inport',flow['flow-node-inventory:flow'][0]['match']['in-port']
    print 'outport',flow['flow-node-inventory:flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector']
    print 'ipv4src',flow['flow-node-inventory:flow'][0]['match']['ipv4-source']
    print 'ipv4dst',flow['flow-node-inventory:flow'][0]['match']['ipv4-destination']
    print 'tcpdst',flow['flow-node-inventory:flow'][0]['match']['tcp-destination-port']
    print 'id',flow['flow-node-inventory:flow'][0]['id']
    print 'tableid',flow['flow-node-inventory:flow'][0]['table_id']
    print 'priority',flow['flow-node-inventory:flow'][0]['priority']
    print 'ethtype',flow['flow-node-inventory:flow'][0]['match']['ethernet-match']['ethernet-type']['type']
    print 'name',flow['flow-node-inventory:flow'][0]['flow-name']

#Create unbalance data flows and disorder network data transfer circumstances
'''
writeflow('1',"1","2","172.23.22.168/32","172.23.22.167/32",8001,"0","0",7,2048,"0")
writeflow('1',"1","2","172.23.22.168/32","172.23.22.167/32",8002,"1","0",7,2048,"1")
writeflow('1',"1","2","172.23.22.168/32","172.23.22.167/32",8003,"2","0",7,2048,"2")
writeflow('1',"1","2","172.23.22.168/32","172.23.22.167/32",8004,"3","0",7,2048,"3")
writeflow('2',"2","1","172.23.22.168/32","172.23.22.167/32",8001,"0","0",7,2048,"0")
writeflow('2',"2","1","172.23.22.168/32","172.23.22.167/32",8002,"1","0",7,2048,"1")
writeflow('2',"2","1","172.23.22.168/32","172.23.22.167/32",8003,"2","0",7,2048,"2")
writeflow('2',"2","1","172.23.22.168/32","172.23.22.167/32",8004,"3","0",7,2048,"3")
writeflow('3',"2","1","172.23.22.168/32","172.23.22.167/32",8001,"0","0",7,2048,"0")
writeflow('3',"2","1","172.23.22.168/32","172.23.22.167/32",8002,"1","0",7,2048,"1")
writeflow('3',"2","1","172.23.22.168/32","172.23.22.167/32",8003,"2","0",7,2048,"2")
writeflow('3',"2","1","172.23.22.168/32","172.23.22.167/32",8004,"3","0",7,2048,"3")
writeflow('4',"3","1","172.23.22.168/32","172.23.22.167/32",8001,"0","0",7,2048,"0")
writeflow('4',"3","1","172.23.22.168/32","172.23.22.167/32",8002,"1","0",7,2048,"1")
writeflow('4',"3","1","172.23.22.168/32","172.23.22.167/32",8003,"2","0",7,2048,"2")
writeflow('4',"3","1","172.23.22.168/32","172.23.22.167/32",8004,"3","0",7,2048,"3")
writeflow('4',"2","1","172.23.22.168/32","172.23.22.167/32",8001,"4","0",7,2048,"4")
writeflow('4',"2","1","172.23.22.168/32","172.23.22.167/32",8002,"5","0",7,2048,"5")
writeflow('4',"2","1","172.23.22.168/32","172.23.22.167/32",8003,"6","0",7,2048,"6")
writeflow('4',"2","1","172.23.22.168/32","172.23.22.167/32",8004,"7","0",7,2048,"7")
'''

#修改流表
'''
modflowtable('1','0')
'''

#Print Flows to check
printflow('1',"0","0")
printflow('1',"0","1")
printflow('1',"0","2")
printflow('1',"0","3")
