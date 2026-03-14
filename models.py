from sqlalchemy import Column,Text,DateTime,text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    pass
class QueryLog(Base):
    __tablename__="query_logs"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    question=Column(Text,nullable=False)
    response=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)

class Users(Base):
    __tablename__="users"
    id=Column(UUID(as_uuid=True),primary_key=True,server_default=text("gen_random_uuid()"))
    email=Column(Text,unique=True, )
    username=Column(Text,nullable=False)
    password=Column(Text,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)