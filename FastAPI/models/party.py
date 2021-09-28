from sqlalchemy import Column
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from ..database.database import Base
from sqlalchemy.dialects.mysql import (
    VARCHAR,
    INTEGER,
    UNSIGNED,
    TINYINT,
)

class Party(Base):
    __tablename__ = "party"

    party_id = Column(UNSIGNED, primary_key=True)
    name = Column(VARCHAR)
    desc = Column(VARCHAR)

class Party(Base):
    __tablename__ = "party"

    party_id = Column(UNSIGNED, ForeignKey=True)