from service.models import OFNodeBase, OfLink,SCApp,SCInstance,SCTemplate
import django

import logging

LOG = logging.getLogger(__name__)


class DbServices():
    def __init__(self):
        self.ofnode_dict ={}
        self.oflink_dict = {}
        self.scapp_dict = {}
        self.scinst_dict = {}
        self.sctplt_dict = {}

    def add_ofnode(self, ofnode):
        ofnode.save()
        self.ofnode_dict.update({ofnode.nodeid:ofnode})

    def delete_ofnode(self, ofnode):
        ofnode = OFNodeBase.objects.get(nodeid=ofnode.nodeid)
        ofnode.delete()


    def add_oflink(self, oflink):
        oflink.save()
        self.oflink_dict.update({oflink.linkid:oflink})

    def delete_oflink(self, oflink):
        oflink = OfLink.objects.get(linkid=oflink.linkid)
        oflink.delete()

    def add_scapp(self, scApp):
        scApp.save()
        self.scapp_dict.update({scApp.appid: scApp})

    def delete_scapp(self, scApp):
        scApp= SCApp.objects.get(appid=scApp.appid)
        scApp.delete()

    def add_scinstance(self, scInst):
        scInst.save()
        self.scinst_dict.update({scInst.instid: scInst})

    def delete_scinstance(self, scInst):
        scInst = SCInstance.objects.get(instid=scInst.instid)
        scInst.delete()

    def add_sctplt(self, scTplt):
        scTplt.save()
        self.sctplt_dict.update({scTplt.tpltid:scTplt})

    def delete_sctplt(self, scTplt):
        sctplt = SCTemplate.objects.get(tpltid=scTplt.tpltid)
        sctplt.delete()

    def get_ofnode(self, nodeId):
        ofnode = self.ofnode_dict.get(nodeId,None)
        if ofnode:
            return ofnode
        return OFNodeBase.objects.get(nodeid=nodeId)

    def get_oflink(self, linkId):
        oflink = self.oflink_dict.get(linkId, None)
        if oflink:
            return oflink
        try:
            return OfLink.objects.get(linkid=linkId)
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get_scapp(self, scAppId):
        scapp = self.scapp_dict.get(scAppId, None)
        if scapp:
            return scapp
        return SCApp.objects.get(appid=scAppId)

    def get_scinstance(self, scInstId):
        scinst = self.scinst_dict.get(scInstId, None)
        if scinst:
            return scinst
        try:
            return SCInstance.objects.get(instid=scInstId)
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get_sctplt(self, scTpltId):
        sctplt = self.sctplt_dict.get(scTpltId, None)
        if sctplt:
            return sctplt
        try:
            return SCTemplate.objects.get(tpltid=scTpltId)
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get_ofnode_by_name(self, node_name):
        for value in self.ofnode_dict.values():
            if value.name == node_name:
                return value
        try:
            ofnode = OFNodeBase.objects.get(name=node_name)
            LOG.info("get ofnode %s by name %s"%(str(ofnode.nodeid), node_name))
            return ofnode
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get_ofnode_by_type(self, node_type):
        for value in self.ofnode_dict.values():
            if value.type == node_type:
                return value
        try:
            ofnode = OFNodeBase.objects.get(type=node_type)
            LOG.info("get ofnode %s by type %s"%(str(ofnode.nodeid), node_type))
            return ofnode
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get_ofnode_by_mac(self, mac):
        for value in self.ofnode_dict.values():
            if value.mac == mac:
                return value
        try:
            ofnode = OFNodeBase.objects.get(mac=mac)
            LOG.info("get ofnode %s by type %s"%(str(ofnode.nodeid), mac))
            return ofnode
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def get_oflink_by_srcdst(self,srcNode_id, dstNode_id):
        for oflink in self.oflink_dict.values():
            if oflink.snode == srcNode_id and oflink.dnode == dstNode_id:
                return oflink
        
        try:    
            oflink = OfLink.objects.filter(snode=srcNode_id, dnode=dstNode_id)
    
            LOG.info("get oflink %s by src_node %s dst_node %s"%(str(oflink.linkid), srcNode_id, dstNode_id))
            return oflink
        except django.core.exceptions.ObjectDoesNotExist:
            return None

    def list_ofnodes(self):
        return OFNodeBase.objects.all()

    def list_oflink(self):
        return OfLink.objects.all()

    def list_sctplt(self):
        return SCTemplate.objects.all()

    def list_scapp(self):
        return SCApp.objects.all()

    def list_scinstance(self):
        return SCInstance.objects.all()

    def mod_ofnode_type(self, ofnode_id, type):
        ofnode = OFNodeBase.objects.get(nodeid=ofnode_id)
        ofnode.type = type
        self.ofnode_dict.update({ofnode.nodeid:ofnode})
        OFNodeBase.objects.filter(nodeid=ofnode_id).update(type=type)
        return ofnode

    def get_tplt_by_name(self, name):
        for tplt in self.sctplt_dict.values():
            if tplt.name == name:
                return tplt
        try:
            return SCTemplate.objects.filter(name=name)
        except django.core.exceptions.ObjectDoesNotExist:
            return None