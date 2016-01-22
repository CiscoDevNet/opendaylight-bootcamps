from basics.odl_http import odl_http_put, odl_http_get, odl_http_delete
import settings
import random
import thread
import time

def buildFlowMod(priority, ethType, ipv4Src, ipv4Dst, flowId, outPort):
    return '''  
{
  "flow": {
    "priority": "%s",
    "flow-name": "ODL_Team_5",
    "match": {
                "ethernet-match": {
                    "ethernet-type": {
                        "type": "%s"
                    }
                },
                "ipv4-source": "%s",
                "ipv4-destination": "%s"
    },
    "id": "%s",
    "table_id": "0",
    "instructions": {
      "instruction": {
        "order": "0",
        "apply-actions": {
          "action": {
            "order": "0",
            "output-action": {
              "output-node-connector": "%s",
              "max-length": "65535"
            }
          }
        }
      }
    }
  }
}
''' % (priority, ethType, ipv4Src, ipv4Dst, flowId, outPort)




def pushFlow(priority, ethType, ipv4Src, ipv4Dst, flowId, nodeId, outPort):
    return odl_http_put(
    url_suffix = "config/opendaylight-inventory:nodes/node/{nodeId}/table/0/flow/{flowId}",
    url_params = {"flowId" : flowId, "nodeId" : nodeId},
    contentType = "application/json",
    content = buildFlowMod(priority, ethType, ipv4Src, ipv4Dst, flowId, outPort),
    expected_status_code = 200
    )






class OdlNode():
    
    def __init__(self, myNodeId):
        
        self.nodeId = myNodeId
        self.neighbors = []
    
    def newMe(self):
        me = OdlNode(str(self.nodeId))
        me.neighbors = []
        
        for link in self.neighbors:
            me.neighbors.append([str(link[0]), str(link[1]), link[2], link[3]])
        
        return me
        
excludeDevice = {}
result = []
def getPaths(src, dst):
    
    excludeDevice.clear()
    while(len(result)>0):
        result.pop()
    
    current = []
    
    #current.append(src.nodeId)
    iterDevice(src, dst, current)
    #current.pop()
    
    return result
    
    
    
def iterDevice(iterNode, dstNode, current):
    
    if(excludeDevice.has_key(iterNode)):
        return
    
    if(iterNode == dstNode):
        putIn = []
        
        for a in current:
            putIn.append([str(a[0]), str(a[1]), a[2], a[3]])
            
        result.append(putIn)
        
        return
        
        #for a in current
        
    excludeDevice[iterNode] = None
    
    for link in iterNode.neighbors:
        
        current.append([str(link[0]), str(link[1]), link[2], link[3]])
        iterDevice(link[3], dstNode, current)
        current.pop()
        
    
    excludeDevice.pop(iterNode,None)
    



def addLink(src, dst, srcNode, dstNode):
    srcNode.neighbors.append([str(src), str(dst), srcNode, dstNode])
#     dstNode.neighbors.append([str(dst), str(src), dstNode, srcNode])
    
def selectPath_random(path_s):
    
    a = [[0] * len(path_s)]
    a = a[0]
    
    for i in range(0, len(path_s),1):
        a[i] = len(path_s[i])

    a.sort()
    
    holdPath = []
    shortest = a[0]
    for p in path_s:
        if(len(p)<=shortest+2):
            holdPath.append(p)     

    
    if(len(holdPath)>0):
        return holdPath[random.randint(0,len(holdPath)-1)]




switches = {}
def resolveDataFromJosn():
    data = odl_http_get(url_suffix='operational/network-topology:network-topology/topology/flow:1',accept='application/json')
    topo = data.json()["topology"][0]
    topo_id = topo["topology-id"]
    node = topo["node"]
    link = topo["link"]
    
    for nd in node:
        node_id = nd["node-id"]
        if(node_id.find("openflow") == -1):
            continue
        switches[node_id] = OdlNode(node_id)
    

    for lk in link:
        if(lk["source"]["source-node"].find("openflow") == -1 or
           lk["destination"]["dest-node"].find("openflow") == -1):
            continue
        srcNode = switches[lk["source"]["source-node"]]
        dstNode = switches[lk["destination"]["dest-node"]]
        src = lk["source"]["source-tp"]
        dst = lk["destination"]["dest-tp"]
        addLink(src,dst,srcNode,dstNode)


def deleteFlow():
    for i in range(1,9):
        print "openflow:"+str(i)
        odl_http_delete(
                        url_suffix = "config/opendaylight-inventory:nodes/node/openflow:%s/table/0/" % str(i),
                        expected_status_code=200
                        )


# ==========================

# switch = {"openflow:1":["openflow:1:1","openflow:1:2"],"openflow:2":["openflow:2:1","openflow:2:2"],"openflow:3":["openflow:3:1","openflow:3:2"]}
speeds = {}
sw_port = {}
def current_speed():
    for swId in switches:
        for ptId in switches[swId].neighbors:
            speed = list([0,0])
            if(ptId[0].find("openflow") == -1):
                continue
            speeds[ptId[0]] = speed
#     print(speeds)
#    try:
    thread.start_new_thread( thred_task ,(None,) )
#    except:
#        print "Error: unable to start thread"

def thred_task(foo):
    while True:
        for ptId in speeds:
            swId = str( ptId.split(":")[0] + ":" + ptId.split(":")[1] )
            port_stati(0.5,swId,ptId)
        
def port_stati( delay,switchId,portId):
    count = 0
#     print(portId)
   # portId = str("openflow:3:1")

    while (count < 2):
        response = odl_http_get(
            url_suffix = "operational/opendaylight-inventory:nodes/node/{switchId}/node-connector/{portId}/opendaylight-port-statistics:flow-capable-node-connector-statistics/bytes/",
            url_params={"switchId":switchId,"portId":portId},
            accept='application/json'
        )
        time.sleep(delay)
        count += 1
#         print count
        statistics = response.json()
        if count == 1:
            old_received = statistics["opendaylight-port-statistics:bytes"]["received"]
        else :
            new_received = statistics["opendaylight-port-statistics:bytes"]["received"]
        
    static = (new_received-old_received)*2.0
    speeds[portId][0] = new_received
    speeds[portId][1] = static

    if(static > 0):
        print(portId  + "    "+ str(speeds[portId][1]))

# ==========================


def main():
    
    print "Get Network Topology..."
    resolveDataFromJosn()
    
    print "Start Statistic Speed..."
    current_speed()
    
    print "Delete Global Flow Entries..."
    deleteFlow()

    ip_port = {
               "10.0.1.1/32":"1",
               "10.0.1.2/32":"2",
               "10.0.1.3/32":"3",
               "10.0.2.1/32":"1",
               "10.0.2.2/32":"2",
               "10.0.2.3/32":"3"
               }
    

    
    
    print "Start Management Platform..."
    countFlowId = 40110;
    while(True):
        
        srcHost = None
        dstHost = None
        src = None
        dst = None
        try:
            srcHost = raw_input("input Source Host IP : ")                          # 10.0.1.2/32
            if(False == (srcHost != None and srcHost != '' and True == isinstance(srcHost, str))):
                continue
            
            dstHost = raw_input("input Destination Host IP : ")                     # 10.0.1.2/32
            if(False == (dstHost != None and dstHost != '' and True == isinstance(dstHost, str))):
                continue
            
            src = raw_input("input Source Device ID : ")                                  # openflow:1
            if(False == (src != None and src != '' and True == isinstance(src, str))):
                continue
         
            dst = raw_input("input Destination Device ID : ")                             # openflow:2
            if(False == (dst != None and dst != ''and True == isinstance(dst, str))):
                continue
            
        except:
            print("exit...")
            break
         
        path_s = getPaths(switches[src], switches[dst])
        
        path = selectPath_random(path_s)
        
        ppp = []
        print (" ")
        print ("--- From ------------- To ---")
        for r in path:
            print(r[0]+"  ->  "+r[1])
            ppp.append(r[0].split(":")[1])
        print (" ")
        mmm = "Route: "
        for p_p in ppp:
            mmm = mmm + p_p + " -> "
        mmm = mmm + dst.split(":")[1]
        print(mmm)
        print (" ")
        print ("--------- length: "+ str(len(path)) + " ---------")

        for link in path:
            pushFlow(
                     priority = "40707",
                     ethType = str(2048),       # ipv4
                     ipv4Src = srcHost,
                     ipv4Dst = dstHost,
                     flowId = str(countFlowId), 
                     nodeId = link[2].nodeId,
                     outPort = link[0].split(":")[2])
            countFlowId = countFlowId + 1
            
            pushFlow(
                     priority = "40707",
                     ethType = str(2048),       # ipv4
                     ipv4Src = dstHost,
                     ipv4Dst = srcHost,
                     flowId = str(countFlowId), 
                     nodeId = link[3].nodeId,
                     outPort = link[1].split(":")[2])
            countFlowId = countFlowId + 1
            
            
            
            
            
            
            
            pushFlow(
                     priority = "40707",
                     ethType = str(2054),       # arp
                     ipv4Src = srcHost,
                     ipv4Dst = dstHost,
                     flowId = str(countFlowId), 
                     nodeId = link[2].nodeId,
                     outPort = link[0].split(":")[2])
            countFlowId = countFlowId + 1
            
            pushFlow(
                     priority = "40707",
                     ethType = str(2054),       # arp
                     ipv4Src = dstHost,
                     ipv4Dst = srcHost,
                     flowId = str(countFlowId), 
                     nodeId = link[3].nodeId,
                     outPort = link[1].split(":")[2])
            countFlowId = countFlowId + 1
            
            
        if(len(path) > 0):
            firstLink = path[0]
            
            pushFlow(
                     priority = "40707",
                     ethType = str(2048),       # ipv4
                     ipv4Src = dstHost,
                     ipv4Dst = srcHost,
                     flowId = str(countFlowId), 
                     nodeId = firstLink[2].nodeId,
                     outPort = ip_port[srcHost])
            countFlowId = countFlowId + 1
            
            pushFlow(
                     priority = "40707",
                     ethType = str(2054),       # arp
                     ipv4Src = dstHost,
                     ipv4Dst = srcHost,
                     flowId = str(countFlowId), 
                     nodeId = firstLink[2].nodeId,
                     outPort = ip_port[srcHost])
            countFlowId = countFlowId + 1    
                
                
                
                
            finalLink = path[-1]
            
            pushFlow(
                     priority = "40707",
                     ethType = str(2048),       # ipv4
                     ipv4Src = srcHost,
                     ipv4Dst = dstHost,
                     flowId = str(countFlowId), 
                     nodeId = finalLink[3].nodeId,
                     outPort = ip_port[dstHost])
            countFlowId = countFlowId + 1
            
            pushFlow(
                     priority = "40707",
                     ethType = str(2054),       # arp
                     ipv4Src = srcHost,
                     ipv4Dst = dstHost,
                     flowId = str(countFlowId), 
                     nodeId = finalLink[3].nodeId,
                     outPort = ip_port[dstHost])
            countFlowId = countFlowId + 1



if __name__ == "__main__":
    main()
