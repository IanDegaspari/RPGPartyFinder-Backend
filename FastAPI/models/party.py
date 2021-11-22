from sqlalchemy import Column
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from pydantic import BaseModel
from sqlalchemy.dialects.mysql import (
    VARCHAR,
    INTEGER,
    TINYINT,
)

class Party(BaseModel):
    __tablename__ = "party"

    party_id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    desc = Column(VARCHAR)

class PartyUsers(BaseModel):
    __tablename__ = "party_users"

    party_id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, primary_key=True)
    role = Column(TINYINT)