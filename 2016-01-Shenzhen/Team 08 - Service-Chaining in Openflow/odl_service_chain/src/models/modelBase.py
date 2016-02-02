from utils import uuidutils
import sqlalchemy as sa
from sqlalchemy.ext import declarative


class HasId(object):

    id = sa.Column(sa.String(36),
                   primary_key=True,
                   default=uuidutils.generate_uuid)


ModelBasev2 = declarative.declarative_base()