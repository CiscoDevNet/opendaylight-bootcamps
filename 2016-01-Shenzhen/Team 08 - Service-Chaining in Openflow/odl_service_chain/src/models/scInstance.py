__author__ = 'cmcc'
import sqlalchemy as sa
from sqlalchemy import orm
from modelBase import ModelBasev2, HasId
from scTemplate import SCTemplate
import utils.uuidutils as uuidutils


class SCInstance(ModelBasev2, HasId):
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
