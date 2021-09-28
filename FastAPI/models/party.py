from sqlalchemy import Column
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from ..database.database import Base
from sqlalchemy.dialects.mysql import (
    VARCHAR,
    INTEGER,
    TINYINT,
)

class Party(Base):
    __tablename__ = "party"

    party_id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    desc = Column(VARCHAR)

class PartyUsers(Base):
    __tablename__ = "party_users"

    party_id = Column(INTEGER, ForeignKey=True)
    user_id = Column(INTEGER, ForeignKey=True)
    role = Column(TINYINT)