from __future__ import unicode_literals

from django.db import models
from django.contrib import admin


class OfLink(models.Model):
    linkid = models.TextField()
    snode = models.TextField()
    dnode = models.TextField()
    srcPort = models.TextField()
    dstPort = models.TextField()

    def set_attributes(self, link_id, srcnode, dstnode, srcport, dstport):
        self.linkid = link_id
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

class OFNodeBase(models.Model):
    nodeid = models.TextField()
    name = models.TextField()
    type = models.TextField()
    profile = models.TextField(null=True)
    mac = models.TextField()

    def set_attributes(self, id, name, type, mac, profile=None):
        self.nodeid = id
        self.name = name
        self.type = type
        self.profile = profile
        self.mac = mac

    def make_dict(self):
        ofnode_dict = {
            "id": self.nodeid,
            "name": self.name,
            "type": self.type,
            "mac": self.mac
        }
        if self.profile:
            ofnode_dict.update({"profile":self.profile})

        return {"ofnode": ofnode_dict}
    
class SCApp(models.Model):
    appid = models.TextField()
    nodeId = models.TextField()
    scInstanceId = models.TextField()

    def set_attributes(self, nodeId, scInstID, appid):
        self.appid = appid
        self.nodeId = nodeId
        self.scInstanceId = scInstID

    def make_dict(self):
        sc_app = {
            "id": self.appid,
            "nodeId": self.nodeId,
            "scInstanceId": self.scInstanceId
        }
        return {"scapp": sc_app}
    
class SCInstance(models.Model):
    instid = models.TextField()
    proto = models.TextField()
    port = models.TextField()
    tpltID = models.TextField()

    def set_attributes(self, protocol, port, template, id):
        self.instid = id
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
class SCTemplate(models.Model):
    tpltid = models.TextField()
    name = models.TextField()
    pipe = models.TextField()

    def set_attributes(self, tpltName, tpltPipe, tpltId):
        self.tpltid = tpltId
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
    
# class NodesPostAdmin(admin.ModelAdmin):
#     list_display = ('NodeID', 'Name', 'Type', 'MacList')
# 
# class scTempPostAdmin(admin.ModelAdmin):
#     list_display = ('scTemID', 'Name', 'Pipe')
#     
# class scInsPostAdmin(admin.ModelAdmin):
#     list_display = ('scInsID', 'tmpID', 'Protocol', 'ProPort')
#     
# class scBindPostAdmin(admin.ModelAdmin):
#     list_display = ('NodeID', 'scID')
# 
# 
# 
# admin.site.register(NodeTable, NodesPostAdmin)
# admin.site.register(scTemplate, scTempPostAdmin)
# admin.site.register(scInstance, scInsPostAdmin)
# admin.site.register(scBinding, scBindPostAdmin)
# Create your models here.
