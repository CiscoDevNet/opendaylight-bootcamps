import sqlalchemy as sa
from sqlalchemy import orm
from ofnode import OFNodeBase
from scInstance import SCInstance
from modelBase import ModelBasev2, HasId


class SCApp(ModelBasev2, HasId):
    __tablename__ = "scapps"
    nodeId = sa.Column(sa.String(255), sa.ForeignKey("ofnodes.id"), nullable=False)
    scInstanceId = sa.Column(sa.String(255), sa.ForeignKey("scinstances.id"), nullable=False)

    def __init__(self, nodeId,scInstID):
        self.nodeId  = nodeId
        self.scInstanceId = scInstID

    def make_dict(self):
        sc_app = {
            "id": self.id,
            "nodeId": self.nodeId,
            "scInstanceId": self.scInstanceId
        }
        return {"scapp": sc_app}
