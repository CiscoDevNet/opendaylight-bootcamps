__author__ = 'cmcc'
from modelBase import  ModelBasev2, HasId
import sqlalchemy as sa

PIPE_SPLITOR = ":"
class SCTemplate(ModelBasev2, HasId):
    __tablename__ = "sctemplates"
    name = sa.Column(sa.String(255), nullable=False)
    pipe = sa.Column(sa.String(255), nullable=False)

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