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

class User(Base):
    __tablename__ = "user"

    id = Column(UNSIGNED, primary_key=True)
    name = Column(VARCHAR)
    login = Column(VARCHAR)
    email = Column(VARCHAR)
    password = Column(VARCHAR)

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    user_id = Column(UNSIGNED, ForeignKey=True)
    gm = Column(TINYINT)
    systems = Column(VARCHAR)
    scenarios = Column(VARCHAR)
    desc = Column(VARCHAR)

class UserRelations(Base):
    __tablename__ = "user_relations"

    user_0 = Column(INTEGER, ForeignKey=True)
    user_1 = Column(INTEGER, ForeignKey=True)
    swipe_0 = Column(TINYINT)
    swipe_1 = Column(TINYINT)