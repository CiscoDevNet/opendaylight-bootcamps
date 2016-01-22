
import random

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
            putIn.append([str(a[0]), a[1]])
            
        result.append(putIn)
        
        return
        
        #for a in current
        
    excludeDevice[iterNode] = None
    
    for link in iterNode.neighbors:
        
        current.append([str(link[0]), link[2]])
        iterDevice(link[3], dstNode, current)
        current.pop()
        
    
    excludeDevice.pop(iterNode,None)
    



def addLink(src, dst, srcNode, dstNode):
    srcNode.neighbors.append([str(src), str(dst), srcNode, dstNode])
    dstNode.neighbors.append([str(dst), str(src), dstNode, srcNode])
    
def selectPath_random(path_s):
    if(path_s != None and len(path_s)>0):
        return path_s[random.randint(0,len(path_s)-1)]

def main():
    A = OdlNode("A")
    B = OdlNode("B")
    C = OdlNode("C")
    D = OdlNode("D")
    E = OdlNode("E")
    F = OdlNode("F")
    G = OdlNode("G")
    H = OdlNode("H")

    switches = [None,A,B,C,D,E,F,G,H]
    
    addLink(A.nodeId, B.nodeId, A, B)
    addLink(A.nodeId, C.nodeId, A, C)
    addLink(B.nodeId, C.nodeId, B, C)
    addLink(B.nodeId, D.nodeId, B, D)
    addLink(B.nodeId, E.nodeId, B, E)
    addLink(E.nodeId, C.nodeId, E, C)
    
    addLink(D.nodeId, E.nodeId, D, E)
    addLink(D.nodeId, F.nodeId, D, F)
    addLink(F.nodeId, E.nodeId, F, E)
    addLink(F.nodeId, H.nodeId, F, H)
    addLink(E.nodeId, G.nodeId, E, G)
    addLink(H.nodeId, G.nodeId, H, G)
    
#     print getPaths(A, B)
    
    while(True):
        try:
            src = input("input Source No. : ")
            if(False == (src != None and src>0 and src<9)):
                continue
         
            dst = input("input Destination No. : ")
            if(False == (dst != None and dst>0 and dst<9)):
                continue
            
        except:
            print("exit...")
            break
         
        path_s = getPaths(switches[src], switches[dst])
        
        path = selectPath_random(path_s)

        for r in path:
            print(r)
        
        




if __name__ == "__main__":
    main()