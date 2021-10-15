from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Time
from ..database.database import Base
from sqlalchemy.dialects.mysql import (
    VARCHAR,
    INTEGER,
    TINYINT,
    DATETIME
)

class Msg(Base):
    __tablename__ = "msg"

    msg_id = Column(INTEGER, primary_key=True)
    content = Column(VARCHAR)
    by = Column(INTEGER)
    recipient_type = Column(TINYINT)
    Time = Column(DATETIME)

class MsgTo(Base):
    __tablename__ = "msg_to"

    msg_id = Column(INTEGER, primary_key=True)
    to = Column(INTEGER, primary_key=True)