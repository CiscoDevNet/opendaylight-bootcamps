from django.db import models
from modelBase import ModelBasev2, HasId


class OfLink():
    id = models.TextField()
    snode = models.TextField()
    dnode = models.TextField()
    srcPort = models.TextField()
    dstPort = models.TextField()

    def __init__(self, link_id, srcnode, dstnode, srcport, dstport):
        self.id = link_id
        self.snode = srcnode
        self.dnode = dstnode
        self.srcPort = srcport
        self.dstPort = dstport

    def make_dict(self):
        oflink_dict = {"id": self.id,
                       "snode": self.snode,
                       "dnode": self.dnode,
                       "srcPort": self.srcPort,
                       "dstPort": self.dstPort
                       }
        return {"oflink": oflink_dict}

class OFNodeBase():
    id = models.TextField()
    name = models.TextField()
    type = models.TextField()
    profile = models.TextField()
    mac = models.TextField()

    def __init__(self, id, name, type, mac, profile=None):
        self.id = id
        self.name = name
        self.type = type
        self.profile = profile
        self.mac = mac

    def make_dict(self):
        ofnode_dict = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "mac": self.mac
        }
        if self.profile:
            ofnode_dict.update({"profile":self.profile})

        return {"ofnode": ofnode_dict}
    
class SCApp():
    id = models.TextField()
    nodeId = models.TextField()
    scInstanceId = models.TextField()

    def __init__(self, nodeId, scInstID):
        self.nodeId = nodeId
        self.scInstanceId = scInstID

    def make_dict(self):
        sc_app = {
            "id": self.id,
            "nodeId": self.nodeId,
            "scInstanceId": self.scInstanceId
        }
        return {"scapp": sc_app}
    
class SCInstance():
    id = models.TextField()
    proto = models.TextField()
    port = models.TextField()
    tpltID = models.TextField()

    def __init__(self, protocol, port, template, id=None):
        self.proto = protocol
        self.port = port
        self.tpltID = template

    def make_dict(self):
        sc_instance = {
            "id": self.id,
            "proto": self.proto,
            "tpltID": self.tpltID
        }
        return {"scinstance": sc_instance}
    
PIPE_SPLITOR = ":"
class SCTemplate():
    id = models.TextField()
    name = models.TextField()
    pipe = models.TextField()

    def __init__(self, tpltName, tpltPipe, tpltId=None):
        if tpltId:
            self.id = tpltId
        self.name = tpltName
        self.pipe = tpltPipe

    def getPipleLine(self):
        return self.pipe.split(PIPE_SPLITOR)

    def make_dict(self):
        sc_tplt = {
            "id": self.id,
            "name": self.name,
            "pipe": self.pipe
        }
        return {"sctemplate": sc_tplt}
    
