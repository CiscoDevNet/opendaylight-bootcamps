import sqlalchemy as sa
from modelBase import ModelBasev2,HasId


class OFNodeBase(ModelBasev2, HasId):
    __tablename__ = "ofnodes"
    name = sa.Column(sa.String(255))
    type = sa.Column(sa.String(255))
    profile = sa.Column(sa.String(255))
    mac = sa.Column(sa.String(255))

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
    
class SCInstance():
    __tablename__ = "scinstances"
    proto = sa.Column(sa.String(10), nullable=False )
    port = sa.Column(sa.INTEGER, default=0)
    tpltID = sa.Column(sa.String(255), sa.ForeignKey("sctemplates.id"), nullable=False)

    def __init__(self, protocol, port, template, id =None):
        self.proto = protocol
        self.port = port
        self.tpltID = template

    def make_dict(self):
        sc_instance ={
            "id": self.id,
            "proto": self.proto,
            "tpltID": self.tpltID
        }
        return {"scinstance": sc_instance}
